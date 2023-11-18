const std = @import("std");

const Allocator = std.mem.Allocator;
const List = std.ArrayListUnmanaged;
const parseInt = std.fmt.parseInt;
const assert = std.debug.assert;
const print = std.debug.print;

pub const IntCode = struct {
    const Self = @This();

    pub const Op = enum {
        add,
        mul,
        halt,
        input,
        output,
        jmpt,
        jmpf,
        lt,
        eq,

        fn getOp(opcode: usize) @This() {
            return switch (opcode) {
                1 => .add,
                2 => .mul,
                3 => .input,
                4 => .output,
                5 => .jmpt,
                6 => .jmpf,
                7 => .lt,
                8 => .eq,
                99 => .halt,
                else => unreachable
            };
        }
    };

    pub const ParamMode = enum {
        position,
        immediate,

        fn getParamMode(v: usize) @This() {
            return switch (v) {
                0 => .position,
                1 => .immediate,
                else => unreachable
            };
        }
    };

    pub const RunResult = enum {
        halt,
        input,
        output,
    };

    
    code: []i64,
    memory: []i64,
    isp: usize,
    base: i64,
    input: ?i64,
    output: ?i64,
    debug: bool,

    pub fn init(allocator: Allocator, code: []const i64) !Self {
        return Self {
            .code = try allocator.dupe(i64, code),
            .memory = try allocator.dupe(i64, code),
            .isp = 0,
            .base = 0,
            .input = null,
            .output = null,
            .debug = false,
        };
    }

    pub fn initFromString(allocator: Allocator, str: []const u8) !Self {
        var arr = try List(i64).initCapacity(allocator, 16);

        var head: usize = 0;
        var tail: usize = 0;

        while (head < str.len) {
            assert(head == tail);

            while (str[tail] != ',' and str[tail] != '\n') {
                tail += 1;
                assert(tail < str.len);
            }

            try arr.append(allocator, try parseInt(i64, str[head..tail], 10));

            tail += 1;
            head = tail;
        }

        const slice: []i64 = arr.toOwnedSlice(allocator);

        return Self {
            .code = slice,
            .memory = try allocator.dupe(i64, slice),
            .isp = 0,
            .base = 0,
            .input = null,
            .output = null,
            .debug = false,
        };
    }
                      
    pub fn deinit(this: Self, allocator: Allocator) void {
        allocator.free(this.code);
        allocator.free(this.memory);
    }

    fn read(this: *Self) i64 {
        const v = this.memory[this.isp];
        //print("read: {}\n", .{v});
        this.isp += 1;
        return v;
    }


    fn readOp(this: *Self)
        struct {
            op: Self.Op,
            a1: Self.ParamMode,
            a2: Self.ParamMode,
            a3: Self.ParamMode,
        }
    {
        const v = @intCast(usize, this.read());

        return .{
            .op = Self.Op.getOp(v % 100),
            .a1 = Self.ParamMode.getParamMode((v / 100) % 10),
            .a2 = Self.ParamMode.getParamMode((v / 1000) % 10),
            .a3 = Self.ParamMode.getParamMode((v / 10000) % 10),
        };
    }

    pub fn readOutput(this: *Self) ?i64 {
        const v = this.output;
        this.output = null;
        return v;
    }

    pub fn reset(this: *Self) void {
        this.isp = 0;
        this.base = 0;
        this.output = null;
        std.mem.copy(i64, this.memory, this.code);
    }

    fn load(this: *Self, mode: Self.ParamMode) i64 {
        switch (mode) {
            .position => {
                const v = this.read();
                const m = this.memory[@intCast(usize, v)];

                if (this.debug) print("[{}]->{} ", .{ v, m });
                return m;
            },
            .immediate => {
                const v = this.read();
                if (this.debug) print("{} ", .{ v });
                return v;
            }
        }
    }
    
    pub fn run(this: *Self) Self.RunResult {
        this.reset();
        return this.resumeRun();
    }
    
    pub fn resumeRun(this: *Self) Self.RunResult {
        while (true) {
            const op = this.readOp();

            if (this.debug) print("{}: .{s}: ", .{ this.isp - 1, @tagName(op.op) });
            
            switch (op.op) {
                .add => {
                    const a1 = this.load(op.a1);
                    const a2 = this.load(op.a2);
                    const a3 = this.read();

                    if (this.debug) print("[{}]", .{a3});
                    this.memory[@intCast(usize, a3)] = a1 + a2;
                },
                .mul => {
                    const a1 = this.load(op.a1);
                    const a2 = this.load(op.a2);
                    const a3 = this.read();

                    if (this.debug) print("[{}]", .{a3});
                    this.memory[@intCast(usize, a3)] = a1 * a2;
                },
                .input => {
                    if (this.input) |i| {
                        const v = this.read();
                        if (this.debug) print("({})->{}", .{ i, v });

                        this.memory[@intCast(usize, v)] = i;
                        this.input = null;
                    } else {
                        if (this.debug) print("<suspend>\n", .{});

                        this.isp -= 1;
                        return .input;
                    }
                },
                .output => {
                    if (this.output) |_| {
                        if (this.debug) print("<suspend>\n", .{});

                        this.isp -= 1;
                        return .output;
                    } else {
                        this.output = this.load(op.a1);
                    }
                },
                .jmpt => {
                    const a1 = this.load(op.a1);
                    const a2 = this.load(op.a2);

                    if (a1 != 0) this.isp = @intCast(usize, a2);
                },
                .jmpf => {
                    const a1 = this.load(op.a1);
                    const a2 = this.load(op.a2);

                    if (a1 == 0) this.isp = @intCast(usize, a2);
                },
                .lt => {
                    const a1 = this.load(op.a1);
                    const a2 = this.load(op.a2);
                    const a3 = this.read();

                    this.memory[@intCast(usize, a3)] = if (a1 < a2) 1 else 0;
                },
                .eq => {
                    const a1 = this.load(op.a1);
                    const a2 = this.load(op.a2);
                    const a3 = this.read();

                    this.memory[@intCast(usize, a3)] = if (a1 == a2) 1 else 0;
                },
                .halt => {
                    return .halt;
                },
            }

            if (this.debug) print("\n", .{});
        }
    }
};

const expectEqual = std.testing.expectEqual;
const expectEqualSlices = std.testing.expectEqualSlices;

test "parse" {
    const str = "123,456,789\n";
    const computer = try IntCode.initFromString(std.testing.allocator, str);
    defer computer.deinit(std.testing.allocator);

    try expectEqualSlices(i64, &[_]i64 { 123, 456, 789 }, computer.code);
}

test "test1" {
    const str = "1,9,10,3,2,3,11,0,99,30,40,50\n";
    var computer = try IntCode.initFromString(std.testing.allocator, str);
    defer computer.deinit(std.testing.allocator);

    var rc = computer.run();
    try expectEqual(IntCode.RunResult.halt, rc);

    try expectEqualSlices(i64, &[_]i64 { 3500,9,10,70,2,3,11,0,99,30,40,50}, computer.memory);

    rc = computer.run();
    try expectEqual(IntCode.RunResult.halt, rc);

    try expectEqualSlices(i64, &[_]i64 { 3500,9,10,70,2,3,11,0,99,30,40,50}, computer.memory);
}

test "test2" {
    const str = "1,0,0,0,99\n";
    var computer = try IntCode.initFromString(std.testing.allocator, str);
    defer computer.deinit(std.testing.allocator);

    var rc = computer.run();
    try expectEqual(IntCode.RunResult.halt, rc);

    try expectEqualSlices(i64, &[_]i64 { 2,0,0,0,99 }, computer.memory);
}

test "test3" {
    const str = "2,3,0,3,99\n";
    var computer = try IntCode.initFromString(std.testing.allocator, str);
    defer computer.deinit(std.testing.allocator);

    var rc = computer.run();
    try expectEqual(IntCode.RunResult.halt, rc);

    try expectEqualSlices(i64, &[_]i64 {2,3,0,6,99}, computer.memory);
}

test "test4" {
    const str = "2,4,4,5,99,0\n";
    var computer = try IntCode.initFromString(std.testing.allocator, str);
    defer computer.deinit(std.testing.allocator);

    var rc = computer.run();
    try expectEqual(IntCode.RunResult.halt, rc);

    try expectEqualSlices(i64, &[_]i64 {2,4,4,5,99,9801}, computer.memory);
}

test "test5" {
    const str = "1,1,1,4,99,5,6,0,99\n";
    var computer = try IntCode.initFromString(std.testing.allocator, str);
    defer computer.deinit(std.testing.allocator);

    var rc = computer.run();
    try expectEqual(IntCode.RunResult.halt, rc);

    try expectEqualSlices(i64, &[_]i64 {30,1,1,4,2,5,6,0,99}, computer.memory);
}

test "test6" {
    const str = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99\n";
    var computer = try IntCode.initFromString(std.testing.allocator, str);
    defer computer.deinit(std.testing.allocator);

    computer.input = 7;
    var rc = computer.resumeRun();
    try expectEqual(IntCode.RunResult.halt, rc);
    try expectEqual(@as(i64, 999), computer.readOutput().?);

    computer.input = 8;
    rc = computer.run();
    try expectEqual(IntCode.RunResult.halt, rc);
    try expectEqual(@as(i64, 1000), computer.readOutput().?);

    computer.input = 9;
    rc = computer.run();
    try expectEqual(IntCode.RunResult.halt, rc);
    try expectEqual(@as(i64, 1001), computer.readOutput().?);
}
