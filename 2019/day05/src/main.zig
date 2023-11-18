const std = @import("std");
const IntCode = @import("intcode").IntCode;

const Allocator = std.mem.Allocator;
const assert = std.debug.assert;
const print = std.debug.print;

const day2input = @embedFile("day2.txt");
const day5input = @embedFile("day5.txt");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();

    const allocator = arena.allocator();

    try day2(allocator);
    try day5(allocator);
}


fn day5(allocator: Allocator) !void {
    var computer = try IntCode.initFromString(allocator, day5input);
    defer computer.deinit(allocator);

    computer.input = 1;
    // computer.debug = true;

    while (true) {
        switch (computer.resumeRun()) {
            .halt => break,
            .input => unreachable,
            .output => {
                assert(0 == computer.readOutput().?);
            },
        }
    }
    print("Day 5 part 1: {}\n", .{ computer.readOutput().? });

    computer.input = 5;
    var rc = computer.run();
    assert(rc == .halt);

    print("Day 5 part 2: {}\n", .{ computer.readOutput().? });
}

fn day2(allocator: Allocator) !void {
    var computer = try IntCode.initFromString(allocator, day2input);
    defer computer.deinit(allocator);
    {
        computer.code[1] = 12;
        computer.code[2] = 2;

        var rc = computer.run();
        assert(rc == .halt);

        print("Day 2 part 1: {}\n", .{computer.memory[0]});
    }

    var i = @as(i64, 0);

    outer: while (i < 100) : (i += 1) {
        var j = @as(i64, 0);
        while (j < 100) : (j += 1) {
            computer.code[1] = i;
            computer.code[2] = j;
            var rc = computer.run();
            assert(rc == .halt);

            if (computer.memory[0] == 19690720) {
                const v = i * 100 + j;
                print("Day 2 part 2: {}\n", .{v});
                break :outer;
            }
        }

    }

}
