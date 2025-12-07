const std = @import("std");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = try std.fs.cwd().openFile("../inputs/day01-test.txt", .{});

    var l1 = std.ArrayList(i32).init(allocator);
    var l2 = std.ArrayList(i32).init(allocator);

    var reader = input.reader();

    while (reader.readInt(i32)) |n1| {
        reader.skipBytes(3);
        const n2 = try reader.readInt(i32);
        l1.append(n1);
        l2.append(n2);
    }
}
