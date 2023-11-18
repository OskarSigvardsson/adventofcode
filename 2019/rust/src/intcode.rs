use std::sync::mpsc::{channel, Receiver, Sender};
use std::sync::{Arc, Mutex};
use std::thread;
use std::thread::JoinHandle;
use std::vec::Vec;

pub struct IntCode {
    initial: Vec<i64>,
    execution: Arc<Mutex<ExecutionState>>,
    input: Sender<InputMessage>,
    output: Receiver<OutputMessage>,
    thread_handle: Option<JoinHandle<()>>,
    thread_messages: Sender<ThreadMessage>,
}

struct ExecutionState {
    memory: Vec<i64>,
    input: Receiver<InputMessage>,
    output: Sender<OutputMessage>,
    debug: bool,
}

#[derive(Debug)]
pub enum InputMessage {
    Stop,
    Value(i64),
}

#[derive(PartialEq, Debug)]
pub enum OutputMessage {
    Halt,
    Value(i64),
}

pub enum ThreadMessage {
    Run,
    Stop,
}

impl Drop for IntCode {
    fn drop(&mut self) {
        self.thread_messages.send(ThreadMessage::Stop).unwrap();
        self.input.send(InputMessage::Stop).unwrap();

        for _ in self.output.try_iter() {}

        self.thread_handle.take().unwrap().join().unwrap();
    }
}

impl IntCode {
    pub fn new_from_str(str: &str) -> IntCode {
        let vec = str
            .trim()
            .split(",")
            .map(|s| s.trim())
            .filter(|s| !s.is_empty())
            .map(|s| s.parse::<i64>().unwrap())
            .collect::<Vec<_>>();

        IntCode::new(vec)
    }

    #[allow(non_snake_case)]
    pub fn new(initial: Vec<i64>) -> IntCode {
        let (inTx, inRx) = channel();
        let (outTx, outRx) = channel();
        let (threadTx, threadRx) = channel::<ThreadMessage>();
        let exec = Arc::new(Mutex::new(ExecutionState {
            memory: initial.clone(),
            input: inRx,
            output: outTx,
            debug: false,
        }));
        let execThread = exec.clone();

        let thread = thread::spawn(move || loop {
            match threadRx.recv().unwrap() {
                ThreadMessage::Stop => break,
                ThreadMessage::Run => execThread.lock().unwrap().run(),
            }
        });

        IntCode {
            initial: initial,
            execution: exec,
            input: inTx,
            output: outRx,
            thread_handle: Some(thread),
            thread_messages: threadTx,
        }
    }

    pub fn debug(&mut self, debug: bool) {
        self.execution.lock().unwrap().debug = debug;
    }

    pub fn input(&self, val: i64) {
        self.input.send(InputMessage::Value(val)).unwrap();
    }

    pub fn output(&self) -> OutputMessage {
        self.output.recv().unwrap()
    }

    pub fn output_value(&self) -> i64 {
        match self.output.recv().unwrap() {
            OutputMessage::Value(v) => v,
            OutputMessage::Halt => panic!("unexpected halt"),
        }
    }

    pub fn output_halt(&self) {
        match self.output.recv().unwrap() {
            OutputMessage::Value(_) => panic!("unexpected value"),
            OutputMessage::Halt => (),
        }
    }

    pub fn reset(&mut self) {
        let mut exec = self.execution.lock().unwrap();

        exec.reset(&self.initial);

        for _ in self.output.try_iter() {}
    }

    pub fn load(&self, i: i64) -> i64 {
        self.execution.lock().unwrap().memory[i as usize]
    }

    pub fn store(&mut self, i: i64, val: i64) {
        self.execution.lock().unwrap().memory[i as usize] = val;
    }

    pub fn run(&mut self) {
        self.thread_messages.send(ThreadMessage::Run).unwrap();
    }

    pub fn run_to_halt(&mut self) {
        self.run();
        loop {
            match self.output() {
                OutputMessage::Value(_) => continue,
                OutputMessage::Halt => break,
            }
        }
    }

    pub fn collect_output(&mut self) -> Vec<i64> {
        let mut output = Vec::new();

        loop {
            match self.output() {
                OutputMessage::Value(v) => {
                    output.push(v);
                }
                OutputMessage::Halt => return output,
            }
        }
    }
}

#[derive(Debug)]
enum ParamMode {
    Position,
    Immediate,
    Relative,
}

impl ParamMode {
    fn from(i: i64) -> ParamMode {
        match i {
            0 => ParamMode::Position,
            1 => ParamMode::Immediate,
            2 => ParamMode::Relative,
            _ => panic!("unknown param mode"),
        }
    }
}

impl ExecutionState {
    pub fn reset(&mut self, initial: &Vec<i64>) {
        self.memory.clone_from(initial);

        for _ in self.input.try_iter() {}
    }

    fn ensure_mem_size(&mut self, i: i64) {
        if i as usize >= self.memory.len() {
            if self.debug {
                println!("memory resize {} -> {}", self.memory.len(), i);
            }

            self.memory.resize(i as usize + 1, 0);
        }
    }

    pub fn run(&mut self) {
        let mut ip: i64 = 0;
        let mut rb: i64 = 0;

        let dbg = self.debug;

        macro_rules! trace {
			($($tts:tt)*) => {
				if dbg {
					println!($($tts)*)
				}
			}
		}

        macro_rules! next {
            () => {{
                assert!(ip >= 0);
                let val = self.memory[ip as usize];

                trace!("inst[{}] = {}", ip, val);

                ip += 1;
                val
            }};
        }

        macro_rules! jump {
            ($dest:expr) => {{
                let d = $dest;

                trace!("JUMP {}", d);

                ip = d as i64;
            }};
        }

        macro_rules! store {
            ($arg:expr, $mode:expr, $val:expr) => {{
                let arg = $arg;
                let val = $val;

                match $mode {
                    ParamMode::Position => {
                        trace!("STORE {} -> ({})", val, arg);

                        self.ensure_mem_size(arg);
                        self.memory[arg as usize] = val;
                    }

                    ParamMode::Immediate => {
                        panic!("Can't store with immediate param mode");
                    }

                    ParamMode::Relative => {
                        self.ensure_mem_size(rb + arg);

                        trace!("STORE {} -> ({} + {})", val, rb, arg);
                        self.memory[(rb + arg) as usize] = val;
                    }
                }
            }};
        }

        macro_rules! load {
            ($arg:expr, $mode:expr) => {{
                let arg = $arg;

                match $mode {
                    ParamMode::Position => {
                        self.ensure_mem_size(arg);

                        let val = self.memory[arg as usize];

                        trace!("LOAD ({}) -> {}", arg, val);

                        val
                    }

                    ParamMode::Immediate => {
                        trace!("CONST {}", arg);

                        arg
                    }

                    ParamMode::Relative => {
                        self.ensure_mem_size(rb + arg);

                        let val = self.memory[(rb + arg) as usize];

                        trace!("LOAD ({} + {}) -> {}", rb, arg, val);

                        val
                    }
                }
            }};
        }

        trace!("STARTING INTERPRETER");

        loop {
            trace!("--------------");
            let inst = next!();

            let opcode = inst % 100;
            let pm1 = ParamMode::from((inst / 100) % 10);
            let pm2 = ParamMode::from((inst / 1000) % 10);
            #[allow(unused_variables)]
            let pm3 = ParamMode::from((inst / 10000) % 10);

            trace!("    OPCODE {}", opcode);
            trace!("    PMs {:?} {:?} {:?}", pm1, pm2, pm3);

            match opcode {
                1 => {
                    let (a, b, dest) = (next!(), next!(), next!());

                    trace!("ADD");

                    store!(dest, pm3, load!(a, pm1) + load!(b, pm2));
                }

                2 => {
                    let (a, b, dest) = (next!(), next!(), next!());

                    trace!("MUL");

                    store!(dest, pm3, load!(a, pm1) * load!(b, pm2));
                }

                3 => {
                    let addr = next!();
                    let input = match self.input.recv().unwrap() {
                        InputMessage::Stop => return,
                        InputMessage::Value(v) => v,
                    };

                    trace!("INPUT {}", input);

                    store!(addr, pm1, input);
                }

                4 => {
                    let addr = next!();
                    let val = load!(addr, pm1);

                    trace!("OUTPUT {val}");

                    self.output.send(OutputMessage::Value(val)).unwrap();
                }

                5 => {
                    let (test, dest) = (next!(), next!());

                    trace!("JMP-IF-TRUE");

                    if load!(test, pm1) != 0 {
                        jump!(load!(dest, pm2))
                    }
                }

                6 => {
                    let (test, dest) = (next!(), next!());

                    trace!("JMP-IF-FALSE");

                    if load!(test, pm1) == 0 {
                        jump!(load!(dest, pm2))
                    }
                }

                7 => {
                    let (a, b, dest) = (next!(), next!(), next!());

                    trace!("LESS-THAN");

                    let result = if load!(a, pm1) < load!(b, pm2) { 1 } else { 0 };
                    store!(dest, pm3, result);
                }

                8 => {
                    let (a, b, dest) = (next!(), next!(), next!());

                    trace!("EQUALS");

                    let result = if load!(a, pm1) == load!(b, pm2) { 1 } else { 0 };
                    store!(dest, pm3, result);
                }

                9 => {
                    let p = next!();
                    let adj = load!(p, pm1);

                    trace!("ADJUST-RB {} + {} -> {}", rb, adj, rb + adj);

                    rb += adj;
                }

                99 => {
                    trace!("HALT");
                    self.output.send(OutputMessage::Halt).unwrap();
                    break;
                }

                _ => panic!("unrecognized opcode"),
            }
        }

        trace!("ENDING INTERPRETER");
    }
}
