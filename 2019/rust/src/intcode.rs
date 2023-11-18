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
    ip: usize,
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
        IntCode::new(
            str.trim()
                .split(",")
                .map(|s| s.trim())
                .filter(|s| !s.is_empty())
                .map(|s| s.parse::<i64>().unwrap())
                .collect::<Vec<_>>(),
        )
    }

    #[allow(non_snake_case)]
    pub fn new(initial: Vec<i64>) -> IntCode {
        let (inTx, inRx) = channel();
        let (outTx, outRx) = channel();
        let (threadTx, threadRx) = channel::<ThreadMessage>();
        let exec = Arc::new(Mutex::new(ExecutionState {
            memory: initial.clone(),
            ip: 0,
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
            initial,
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
        self.execution.lock().unwrap().load(i, ParamMode::Position)
    }

    pub fn store(&mut self, i: i64, val: i64) {
        self.execution.lock().unwrap().store(i, val)
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
}

#[derive(Debug)]
enum ParamMode {
    Position,
    Immediate,
}

impl ParamMode {
    fn from(i: i64) -> ParamMode {
        match i {
            0 => ParamMode::Position,
            1 => ParamMode::Immediate,
            _ => panic!("unknown param mode"),
        }
    }
}

impl ExecutionState {
    pub fn reset(&mut self, initial: &Vec<i64>) {
        self.memory.clone_from(initial);
        self.ip = 0;

        for _ in self.input.try_iter() {}
    }

    pub fn next(&mut self) -> i64 {
        let val = self.memory[self.ip];

        if self.debug {
            println!("inst[{}] = {}", self.ip, val);
        }

        self.ip += 1;
        val
    }

    pub fn load(&self, i: i64, pmode: ParamMode) -> i64 {
        match pmode {
            ParamMode::Position => {
                let val = self.memory[i as usize];
                if self.debug {
                    println!("LOAD ({}) -> {}", i, val);
                }
                val
            }
            ParamMode::Immediate => {
                if self.debug {
                    println!("LOAD (const) -> {}", i);
                }
                i
            }
        }
    }

    pub fn store(&mut self, i: i64, val: i64) {
        if self.debug {
            println!("STORE {} -> ({})", val, i);
        }
        self.memory[i as usize] = val;
    }

    pub fn jump(&mut self, dest: i64) {
        if self.debug {
            println!("JUMP {}", dest);
        }
        self.ip = dest as usize;
    }

    pub fn run(&mut self) {
        let dbg = self.debug;

        if dbg {
            println!("STARTING INTERPRETER");
        }

        loop {
            if dbg {
                println!("--------------")
            }
            let inst = self.next();

            let opcode = inst % 100;
            let pm1 = ParamMode::from((inst / 100) % 10);
            let pm2 = ParamMode::from((inst / 1000) % 10);
            #[allow(unused_variables)]
            let pm3 = ParamMode::from((inst / 10000) % 10);

            if dbg {
                println!("    OPCODE {}", opcode)
            }
            if dbg {
                println!("    PMs {:?} {:?} {:?}", pm1, pm2, pm3)
            }

            match opcode {
                1 => {
                    let (a, b, dest) = (self.next(), self.next(), self.next());

                    if dbg {
                        println!("ADD");
                    }

                    self.store(dest, self.load(a, pm1) + self.load(b, pm2));
                }

                2 => {
                    let (a, b, dest) = (self.next(), self.next(), self.next());

                    if dbg {
                        println!("MUL");
                    }

                    self.store(dest, self.load(a, pm1) * self.load(b, pm2));
                }

                3 => {
                    let addr = self.next();
                    let input = match self.input.recv().unwrap() {
						InputMessage::Stop => return,
						InputMessage::Value(v) => v,
					};
						

                    if dbg {
                        println!("INPUT {}", input);
                    }

                    self.store(addr, input);
                }

                4 => {
                    let addr = self.next();

                    if dbg {
                        println!("OUTPUT");
                    }

                    self.output
                        .send(OutputMessage::Value(self.load(addr, pm1)))
                        .unwrap();
                }

                5 => {
                    let (test, dest) = (self.next(), self.next());

                    if dbg {
                        println!("JMP-IF-TRUE")
                    }

                    if self.load(test, pm1) != 0 {
                        self.jump(self.load(dest, pm2))
                    }
                }

                6 => {
                    let (test, dest) = (self.next(), self.next());

                    if dbg {
                        println!("JMP-IF-FALSE")
                    }

                    if self.load(test, pm1) == 0 {
                        self.jump(self.load(dest, pm2))
                    }
                }

                7 => {
                    let (a, b, dest) = (self.next(), self.next(), self.next());

                    if dbg {
                        println!("LESS-THAN")
                    }

                    let result = if self.load(a, pm1) < self.load(b, pm2) {
                        1
                    } else {
                        0
                    };
                    self.store(dest, result);
                }

                8 => {
                    let (a, b, dest) = (self.next(), self.next(), self.next());

                    if dbg {
                        println!("EQUALS")
                    }

                    let result = if self.load(a, pm1) == self.load(b, pm2) {
                        1
                    } else {
                        0
                    };
                    self.store(dest, result);
                }

                99 => {
                    if dbg {
                        println!("HALT");
                    }
                    self.output.send(OutputMessage::Halt).unwrap();
                    break;
                }

                _ => panic!("unrecognized opcode"),
            }
        }

        if dbg {
            println!("ENDING INTERPRETER");
        }
    }
}
