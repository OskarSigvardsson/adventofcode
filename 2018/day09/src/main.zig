const std = @import("std");

const Allocator = std.mem.Allocator;

const print = std.debug.print;

const Input = struct {
    players: usize,
    marbles: usize,
};

const test0 = Input { .players = 9,  .marbles = 25 };
const test1 = Input { .players = 10,  .marbles = 1618 };
const test2 = Input { .players = 13,  .marbles = 7999 };
const test3 = Input { .players = 17,  .marbles = 1104 };
const test4 = Input { .players = 21,  .marbles = 6111 };
const test5 = Input { .players = 30,  .marbles = 5807 };
const real1 = Input { .players = 458, .marbles = 72019 };
const real2 = Input { .players = 458, .marbles = 72019 * 100 };


const Link = struct {
    const Self = @This();
    
    marble: i64,
    next: *Self,
    prev: *Self,
};

pub fn main() !void {
    print("Part 1: {}\n", .{ try part1(std.heap.page_allocator, real1) });
    print("Part 2: {}\n", .{ try part1(std.heap.page_allocator, real2) });
}

fn debug(head: *Link, curr: *Link) void {
    var ptr = head;
    
    while (true) {
        if (ptr == curr) {
            print("({:>2})", .{ @intCast(usize, ptr.marble) });
        } else {
            print(" {:>2} ", .{ @intCast(usize, ptr.marble) });
        }

        ptr = ptr.next;

        if (ptr == head) break;
    }

    print("\n", .{});
}

fn part1(allocator: Allocator, params: Input) !i64 {
    var arena = std.heap.ArenaAllocator.init(allocator);
    defer arena.deinit();
    const alloc = arena.allocator();
    
    const head = try alloc.create(Link);
    var curr = head;

    curr.marble = 0;
    curr.next = curr;
    curr.prev = curr;

    var marble = @as(i64, 1);
    var player = @as(usize, 0);

    var scores = try alloc.alloc(i64, params.players);
    var maxScore = @as(i64, 0);

    for (scores) |*score| score.* = 0;
    
    while (marble <= params.marbles)  {
        defer marble += 1;
        defer player = (player + 1) % params.players;

        if (@intCast(usize, marble) % 23 == 0) {
            var link = curr.prev.prev.prev.prev.prev.prev.prev;
            
            link.prev.next = link.next;
            link.next.prev = link.prev;

            scores[player] += marble + link.marble;
            maxScore = @max(maxScore, scores[player]);

            curr = link.next;
        } else {
            var l1 = curr.next;
            var l2 = curr.next.next;

            var new = try alloc.create(Link);

            new.marble = marble;
            new.next = l2;
            new.prev = l1;
            l1.next = new;
            l2.prev = new;

            curr = new;
        }
        // print("[{:>2}] ", .{ player + 1});
        // debug(head, curr);
    }

    return maxScore;
}

const expectEqual = std.testing.expectEqual;

test "part1 test0" {
    try expectEqual(@as(i64, 32), try part1(std.testing.allocator, test0));
}
test "part1 test1" {
    try expectEqual(@as(i64, 8317), try part1(std.testing.allocator, test1));
}
test "part1 test2" {
    try expectEqual(@as(i64, 146373), try part1(std.testing.allocator, test2));
}
test "part1 test3" {
    try expectEqual(@as(i64, 2764), try part1(std.testing.allocator, test3));
}
test "part1 test4" {
    try expectEqual(@as(i64, 54718), try part1(std.testing.allocator, test4));
}
test "part1 test5" {
    try expectEqual(@as(i64, 37305), try part1(std.testing.allocator, test5));
}
