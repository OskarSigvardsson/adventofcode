const std = @import("std");

const testInput = @embedFile("test.txt");
const realInput = @embedFile("real.txt");

const print = std.debug.print;
const Allocator = std.mem.Allocator;
const List = std.ArrayListUnmanaged;
const parseInt = std.fmt.parseInt;

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const slice = try parse(allocator, realInput);

    print("Part 1: {}\n", .{ part1(slice, 0).sum });
    print("Part 2: {}\n", .{ (try part2(allocator, slice, 0)).sum });
}

fn parse(allocator: Allocator, str: []const u8) ![]i64 {
    var list = try List(i64).initCapacity(allocator, 16);

    var head = @as(usize, 0);
    var tail = @as(usize, 0);

    while (head < str.len) {
        while (str[tail] != ' ' and str[tail] != '\n') {
            tail += 1;
        }
        try list.append(allocator, try parseInt(i64, str[head..tail], 10));

        tail += 1;
        head = tail;
    }

    return list.toOwnedSlice(allocator);
}

fn part1(tree: []i64, start: usize) struct { sum: i64, end: usize } {
    //print("part1({}) starts\n", .{start});

    if (start >= tree.len) return .{ .sum = 0, .end = start };
    
    const children = tree[start];
    const metadatas = @intCast(usize, tree[start + 1]);

    var nextChildIndex = @as(usize, start + 2);
    var child = @as(usize, 0);
    var sum = @as(i64, 0);

    while (child < children) : (child += 1) {
        const ret = part1(tree, nextChildIndex);
        sum += ret.sum;
        nextChildIndex = ret.end + 1;
    }

    var metaIndex = @as(usize, 0);

    while (metaIndex < metadatas) : (metaIndex += 1) {
        sum += tree[nextChildIndex + metaIndex];
    }

    //print("part1({}) = {}, {} \n", .{start, sum, nextChildIndex + metadatas});
    return .{ .sum = sum, .end = nextChildIndex + metadatas - 1};
}

fn part2(allocator: Allocator, tree: []i64, start: usize) !struct { sum: i64, end: usize } {
    //print("part2({}) starts\n", .{start});

    if (start >= tree.len) return .{ .sum = 0, .end = start };
    
    var childvals = try List(i64).initCapacity(allocator, 0);
    defer childvals.deinit(allocator);

    const children = tree[start];
    const metadatas = @intCast(usize, tree[start + 1]);

    var nextChildIndex = @as(usize, start + 2);
    var child = @as(usize, 0);
    var sum = @as(i64, 0);

    while (child < children) : (child += 1) {
        const ret = try part2(allocator, tree, nextChildIndex);
        try childvals.append(allocator, ret.sum);
        nextChildIndex = ret.end + 1;
    }

    var metaIndex = @as(usize, 0);

    while (metaIndex < metadatas) : (metaIndex += 1) {
        var idx = tree[nextChildIndex + metaIndex];

        if (children == 0) {
            sum += tree[nextChildIndex + metaIndex];
        } else if (idx != 0 and (idx - 1) < childvals.items.len) {
            sum += childvals.items[@intCast(usize, idx) - 1];
        }
    }

    //print("part1({}) = {}, {} \n", .{start, sum, nextChildIndex + metadatas});
    return .{ .sum = sum, .end = nextChildIndex + metadatas - 1};
}

const alloc = std.testing.allocator;
const expectEqual = std.testing.expectEqual;
const expectEqualSlices = std.testing.expectEqualSlices;

test "parse" {
    const slice = try parse(alloc, "1 2 3 4 5\n");
    defer alloc.free(slice);

    try expectEqualSlices(i64, &[_]i64 {1, 2, 3, 4, 5}, slice);
}

fn testMultiReturn() struct { a: i64, b: i64 } {
    return .{ .a = 14, .b = 54 };
}

test "multireturn" {
    const ret = testMultiReturn();

    try expectEqual(@as(i64, 14), ret.a);
    try expectEqual(@as(i64, 54), ret.b);
}

test "part1 test" {
    const slice = try parse(alloc, testInput);
    defer alloc.free(slice);

    try expectEqual(@as(i64, 138), part1(slice, 0).sum);
    // print("\n", .{});
    // print("Answer: {} ", .{ part1(slice, 0).sum });
}



test "part2 test" {
    const slice = try parse(alloc, testInput);
    defer alloc.free(slice);

    try expectEqual(@as(i64, 66), (try part2(alloc, slice, 0)).sum);
    // print("\n", .{});
    // print("Answer: {} ", .{ part1(slice, 0).sum });
}
