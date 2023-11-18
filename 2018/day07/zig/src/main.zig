const std = @import("std");

const PriorityQueue = std.PriorityQueue;
const Order = std.math.Order;

const testInput = @embedFile("test.txt");
const realInput = @embedFile("real.txt");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    var table: [26]u32 = undefined;
    var charset: [26]bool = undefined;
    
    try parse(testInput, &table, &charset);
    try std.testing.expectEqual(@as(i64, 15), try part2(allocator, table, charset, 1, 2));
}

fn match(str: *[]const u8, token: []const u8) !void {
    if (std.mem.startsWith(u8, str.*, token)) {
        str.* = str.*[token.len..];
    } else {
        return error.MatchError;
    }
}

fn getChr(str: *[]const u8) !u8 {
    if (str.len > 0) {
        const chr = str.*[0];
        str.* = str.*[1..];
        return chr;
    } else {
        return error.MatchError;
    }
}

fn ord(chr: u8) u8 {
    return chr - 'A';
}

fn parse(text: []const u8, table: *[26]u32, charset: *[26]bool) !void {
    var slice = text;

    table.* = [_]u32 {0} ** 26;
    charset.* = [_]bool {false} ** 26;
    
    while (slice.len > 0) {
        try match(&slice, "Step ");
        const from = try getChr(&slice);
        try match(&slice, " must be finished before step ");
        const to = try getChr(&slice);
        try match(&slice, " can begin.\n");

        table.*[ord(to)] |= @as(u32, 1) << @intCast(u5, ord(from));

        charset.*[ord(from)] = true;
        charset.*[ord(to)] = true;
    }
}

fn debug(table: [26]u32) void {
    var x: u5 = 0;
    var y: usize = 0;

    while (y < 26) : (y += 1) {
        x = 0;
        while (x < 26) : (x += 1) {
            std.debug.print("{}", .{ (table[y] >> x) & 1 });
        }
        std.debug.print("\n", .{});
    }
}

fn nextStep(table: [26]u32, done: [26]bool, charset: [26]bool) ?u8 {
    return for (table) |n,i| {
        if (n == 0 and !done[i] and charset[i]) break @intCast(u8, i);
    } else null;
}

fn clearCol(table: *[26]u32, col: u8) void {
    var row = @as(usize, 0);
    while (row < 26) : (row += 1) {
        table.*[row] &= @bitCast(u32, @as(i32, -1)) ^ (@as(u32, 1) << @intCast(u5, col));
    }
}

fn part1(inTable: [26]u32, charset: [26]bool) void {
    var table: [26]u32 = undefined;
    std.mem.copy(u32, &table, &inTable);
    
    var done = [_]bool{false} ** 26;

    // std.debug.print("Before loop:\n", .{});
    // debug(table);

    while (true) {
        var c = nextStep(table, done, charset) orelse break;

        std.debug.print("{c}", .{@intCast(u8, c + 'A')});

        done[c] = true;

        clearCol(&table, c);
    }
    std.debug.print("\n", .{});

    // std.debug.print("After loop :\n", .{});
    // debug(table);
}


fn part2(
    allocator: std.mem.Allocator,
    inTable: [26]u32,
    charset: [26]bool,
    comptime delay: i32,
    comptime workers: usize)
    !i64
{
    const print = std.debug.print;
    
    const Event = struct {
        time: i64,
        worker: usize,

        fn cmpFn(_: void, a: @This(), b: @This()) Order {
            return std.math.order(a.time, b.time);
        }
    };

    var assignments = [_]?u8 {null} ** workers;
    var events = PriorityQueue(Event, void, Event.cmpFn).init(allocator, {});
    defer events.deinit();

    var table: [26]u32 = undefined;
    std.mem.copy(u32, &table, &inTable);
    
    var done = [_]bool{false} ** 26;

    while (nextStep(table, done, charset)) |step| {
        const worker = for (assignments) |assignment, i| {
            if (assignment) |_| {} else break i;
        } else break;

        print("{}: Assigning worker {} to {}\n", .{0, worker, step});
        assignments[worker] = step;
        done[step] = true;

        try events.add(.{
            .time = delay + step,
            .worker = @intCast(u32, worker)
        });
    }

    var time = @as(i64, 0);
    
    while (events.removeOrNull()) |ev| {
        time = ev.time;
        print("{}: Worker {} finished\n", .{time, ev.worker});
        clearCol(&table, assignments[ev.worker].?);

        assignments[ev.worker] = null;

        while (nextStep(table, done, charset)) |step| {
            const worker = for (assignments) |assignment, i| {
                if (assignment) |_| {} else break i;
            } else break;
            print("{}: Assigning worker {} to {}\n", .{time, worker, step});

            assignments[worker] = step;
            done[step] = true;

            try events.add(.{
                .time = time + delay + step,
                .worker = worker
            });
        }
    }

    return time;
}

test "embed test file" {
    std.debug.print("\ntest input: \n{s}\n", .{ testInput });
}

// test "match" {
//     try std.testing.expectEqualSlices(u8, "def", try match("abcdef", "abc"));
//     try std.testing.expectEqualSlices(u8, "",    try match("abcdef", "abcdef"));
//     try std.testing.expectError(error.MatchError, match("abcdef", "abd"));
//     try std.testing.expectError(error.MatchError, match("abcdef", "abcdefg"));
// }

test "parse" {
    var table: [26]u32 = undefined;
    var charset: [26]bool = undefined;
    
    try parse(testInput, &table, &charset);
}

fn testFn(slice: *[10]i32) void {
    slice[5] = 16;
}

test "pass slice to function" {

    var slice1 = [_]i32 { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
    var slice2 = [_]i32 { 0, 1, 2, 3, 4, 16, 6, 7, 8, 9 };

    testFn(&slice1);

    try std.testing.expectEqualSlices(i32, &slice2, &slice1);
}

test "expression for" {
    const tbl = [_]i32 { 3, 4, 5, 6, 7 };

    var idx: ?usize = for (tbl) |n,i| {
        if (n == 5) break i;
    } else null;

    try std.testing.expectEqual(idx, 2);
}

test "part1 test" {
    var table: [26]u32 = undefined;
    var charset: [26]bool = undefined;
    
    try parse(testInput, &table, &charset);
    part1(table, charset);
}

test "part1 real" {
    var table: [26]u32 = undefined;
    var charset: [26]bool = undefined;
    
    try parse(realInput, &table, &charset);
    part1(table, charset);
}

test "part2 test" {
    var table: [26]u32 = undefined;
    var charset: [26]bool = undefined;
    
    try parse(testInput, &table, &charset);
    try std.testing.expectEqual(@as(i64, 15), try part2(std.testing.allocator, table, charset, 1, 2));
}

test "part2 real" {
    var table: [26]u32 = undefined;
    var charset: [26]bool = undefined;
    
    try parse(realInput, &table, &charset);
    std.debug.print("Answer: |{}| ", .{ try part2(std.testing.allocator, table, charset, 61, 5) });
}
