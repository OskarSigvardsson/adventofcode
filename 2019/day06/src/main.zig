const std = @import("std");

const testInput = @embedFile("test.txt");
const testInput2 = @embedFile("test2.txt");
const realInput = @embedFile("real.txt");


const Orbit = struct {
    a: [3]u8,
    b: [3]u8,
};


pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    
    var testOrbits = try parse(allocator, testInput);
    var testOrbits2 = try parse(allocator, testInput2);
    var realOrbits = try parse(allocator, realInput);

    std.debug.print("Part 1 (test): {d}\n", .{ try countOrbits(allocator, testOrbits) });
    std.debug.print("Part 1 (real): {d}\n", .{ try countOrbits(allocator, realOrbits) });

    std.debug.print("Part 2 (test): {d}\n", .{ try santaTransfer(allocator, testOrbits2) });
    std.debug.print("Part 2 (real): {d}\n", .{ try santaTransfer(allocator, realOrbits) });
                        
}

fn parse(allocator: std.mem.Allocator, text: []const u8) ![]Orbit {
    var orbits = std.ArrayList(Orbit).init(allocator);
    
    var lines = std.mem.split(u8, text, "\n");
    
    while (lines.next()) |line| {
        var planets = std.mem.split(u8, line, ")");

        var p1 = planets.next() orelse break;
        var p2 = planets.next() orelse break;
        
        try orbits.append(Orbit {
            .a = p1[0..3].*,
            .b = p2[0..3].*,
        });
    }

    return orbits.toOwnedSlice();
}

fn countOrbits(allocator: std.mem.Allocator, orbits: []Orbit) !i64 {
    var map = std.AutoHashMap([3]u8, [3]u8).init(allocator);
    defer map.deinit();

    for (orbits) |orbit| {
        std.debug.assert(!map.contains(orbit.b));
        try map.put(orbit.b, orbit.a);
    }

    var keys = map.keyIterator();

    var count: i64 = 0;
    
    while (keys.next()) |planet| {
        var curr = planet.*;
        while (map.contains(curr)) {
            count += 1;
            curr = map.get(curr) orelse unreachable;
        }
    }

    return count;
}

fn santaTransfer(allocator: std.mem.Allocator, orbits: []Orbit) !i64 {
    var orbitMap = std.AutoHashMap([3]u8, [3]u8).init(allocator);
    defer orbitMap.deinit();

    for (orbits) |orbit| {
        std.debug.assert(!orbitMap.contains(orbit.b));
        try orbitMap.put(orbit.b, orbit.a);
    }

    var transferCount = std.AutoHashMap([3]u8, i64).init(allocator);
    defer transferCount.deinit();
    var curr: [3]u8 = "YOU".*;
    var depth: i64 = 0;
        
    while (orbitMap.get(curr)) |around| {
        try transferCount.put(around, depth);
        depth += 1;
        curr = around;
    }

    curr = "SAN".*;
    depth = 0;

    while (orbitMap.get(curr)) |around| {
        if (transferCount.get(around)) |d| {
            return d + depth;
        }
        depth += 1;
        curr = around;
    }

    return error.NoPath;
}

test "parse" {
    var allocator = std.testing.allocator;
    var orbits = try parse(allocator, testInput);
    defer allocator.free(orbits);

    try std.testing.expectEqualStrings("COM", &orbits[0].a);
    try std.testing.expectEqualStrings("BBB", &orbits[0].b);
    try std.testing.expectEqualStrings("KKK", &orbits[10].a);
    try std.testing.expectEqualStrings("LLL", &orbits[10].b);
}

test "count" {
    var allocator = std.testing.allocator;
    var orbits = try parse(allocator, testInput);
    defer allocator.free(orbits);
    try std.testing.expectEqual(@as(i64, 42), try countOrbits(allocator, orbits));
}

test "transferCount" {
    var allocator = std.testing.allocator;
    var orbits = try parse(allocator, testInput2);
    defer allocator.free(orbits);
    try std.testing.expectEqual(@as(i64, 4), try santaTransfer(allocator, orbits));
}

test "slice copy" {
    const T = struct { a: [3]i32 };
    
    const slice = [_]i32 { 1, 2, 3 };
    var other = slice;
    var other2 = T { .a = slice };
    var other3: [1]i32 = slice[1..2].*;

    other[1] = 5;
    
    try std.testing.expectEqualSlices(i32, &[_]i32 { 1, 2, 3 }, &slice);
    try std.testing.expectEqualSlices(i32, &[_]i32 { 1, 5, 3 }, &other);
    try std.testing.expectEqualSlices(i32, &[_]i32 { 1, 2, 3 }, &other2.a);
    try std.testing.expectEqualSlices(i32, &[_]i32 { 2 }, &other3);
}

test "simple test" {
    var list = std.ArrayList(i32).init(std.testing.allocator);
    defer list.deinit(); // try commenting this out and see if zig detects the memory leak!
    try list.append(42);
    try std.testing.expectEqual(@as(i32, 42), list.pop());
}
