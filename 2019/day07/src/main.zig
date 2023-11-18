const std = @import("std");
const IntCode = @import("intcode").IntCode;

const Allocator = std.mem.Allocator;

const assert = std.debug.assert;
const print = std.debug.print;

const testInput1 = @embedFile("test1.txt");
const testInput2 = @embedFile("test2.txt");
const testInput3 = @embedFile("test2.txt");
const realInput = @embedFile("real.txt");

pub fn main() !void {
}

const Amps = struct {
    const Self = @This();
    
    a: IntCode,
    b: IntCode,
    c: IntCode,
    d: IntCode,
    e: IntCode,

    fn init(allocator: Allocator, str: []const u8) !Self {
        return Self {
            .a = try IntCode.initFromString(allocator, str),
            .b = try IntCode.initFromString(allocator, str),
            .c = try IntCode.initFromString(allocator, str),
            .d = try IntCode.initFromString(allocator, str),
            .e = try IntCode.initFromString(allocator, str),
        };
    }

    fn deinit(self: *Self, allocator: Allocator) void {
        self.e.deinit(allocator);
        self.d.deinit(allocator);
        self.c.deinit(allocator);
        self.b.deinit(allocator);
        self.a.deinit(allocator);
    }

    fn configure(self: *Self, setting: [5]i64) void {
        self.a.reset();
        self.b.reset();
        self.c.reset();
        self.d.reset();
        self.e.reset();

        self.a.input = setting[0];
        self.b.input = setting[1];
        self.c.input = setting[2];
        self.d.input = setting[3];
        self.e.input = setting[4];

        var arc = self.a.resumeRun();
        var brc = self.b.resumeRun();
        var crc = self.c.resumeRun();
        var drc = self.d.resumeRun();
        var erc = self.e.resumeRun();

        assert(arc == .input);
        assert(brc == .input);
        assert(crc == .input);
        assert(drc == .input);
        assert(erc == .input);
    }

    fn feed(self: *Self, val: i64) i64 {
        self.a.input = val;
        _ = self.a.resumeRun();

        self.b.input = self.a.readOutput().?;
        _ = self.b.resumeRun();

        self.c.input = self.b.readOutput().?;
        _ = self.c.resumeRun();

        self.d.input = self.c.readOutput().?;
        _ = self.d.resumeRun();

        self.e.input = self.d.readOutput().?;
        _ = self.e.resumeRun();

        return self.e.readOutput().?;
    }
};

fn part1(allocator: Allocator, str: []const u8) !i64 {
    var amps = try Amps.init(allocator, str);
    defer amps.deinit(allocator);
    
    var i = @as(i64, 0);
    var max = @as(i64, 0);
    var maxSetting: [5]i64 = undefined;
    
    while (i < 5*5*5*5*5) : (i += 1) {
        const a: i64 = @mod(@divTrunc(i, 5*5*5*5), 5);
        const b: i64 = @mod(@divTrunc(i, 5*5*5), 5);
        const c: i64 = @mod(@divTrunc(i, 5*5), 5);
        const d: i64 = @mod(@divTrunc(i, 5), 5);
        const e: i64 = @mod(i, 5);

        const setting = [_]i64 { a, b, c, d, e };
        if (!all_distinct(setting)) continue;

        amps.configure(setting);
        const value = amps.feed(0);

        //print("{any} {}\n", .{ [_]i64 { a, b, c, d, e }, curr });
        if (value > max) {
            maxSetting = [_]i64 { a, b, c, d, e };
            max = value;
        }
    }

    //print("{any}\n", .{ maxSetting });
    return max;
}

fn part1(allocator: Allocator, str: []const u8) !i64 {
    var amps = try Amps.init(allocator, str);
    defer amps.deinit(allocator);
    
    var i = @as(i64, 0);
    var max = @as(i64, 0);
    var maxSetting: [5]i64 = undefined;
    
    while (i < 5*5*5*5*5) : (i += 1) {
        const a: i64 = 5 + @mod(@divTrunc(i, 5*5*5*5), 5);
        const b: i64 = 5 + @mod(@divTrunc(i, 5*5*5), 5);
        const c: i64 = 5 + @mod(@divTrunc(i, 5*5), 5);
        const d: i64 = 5 + @mod(@divTrunc(i, 5), 5);
        const e: i64 = 5 + @mod(i, 5);

        const setting = [_]i64 { a, b, c, d, e };
        if (!all_distinct(setting)) continue;

        amps.configure(setting);
        const value = amps.feed(0);

        //print("{any} {}\n", .{ [_]i64 { a, b, c, d, e }, curr });
        if (value > max) {
            maxSetting = [_]i64 { a, b, c, d, e };
            max = value;
        }
    }

    //print("{any}\n", .{ maxSetting });
    return max;
}

fn all_distinct(vals: [5]i64) bool {
    var i = @as(usize, 0);
    while (i < 4) : (i += 1) {
        var j = @as(usize, i + 1);
        while (j < 5) : (j += 1) {
            if (vals[i] == vals[j]) return false;
        }
    }

    return true;
}

const expectEqual = std.testing.expectEqual;

test "part1 test1" {
    try expectEqual(@as(i64, 43210), try part1(std.testing.allocator, testInput1));
}
test "part1 test2" {
    try expectEqual(@as(i64, 54321), try part1(std.testing.allocator, testInput2));
}
// test "part1 test3" {
//     try expectEqual(@as(i64, 65210), try part1(std.testing.allocator, testInput3));
// }

test "part1 real" {
    print("{}\n", .{ try part1(std.testing.allocator, realInput) });
}
