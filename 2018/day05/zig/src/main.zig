const std = @import("std");
const abs = std.math.absCast;

fn println(comptime fmt: []const u8, args: anytype) void {
    std.debug.print(fmt ++ "\n", args);
}

fn print(comptime fmt: []const u8, args: anytype) void {
    std.debug.print(fmt, args);
}

fn caseConv(c1: u8) u8 {
    if (c1 < 'a') return c1 + ('a' - 'A');

    return c1 - ('a' - 'A');
}

fn caseCmp(c1: u8, c2: u8) bool {
    return c1 == caseConv(c2);
}

const Polymer = struct {
    const Self = @This();

    allocator: std.mem.Allocator,
    chars: []u8,
    erased: []bool,
    len: usize,

    fn init(alloc: std.mem.Allocator, str: []const u8) !Self {
        var ret = Self{
            .allocator = alloc,
            .chars = try alloc.alloc(u8, str.len),
            .erased = try alloc.alloc(bool, str.len),
            .len = str.len
        };

        std.mem.copy(u8, ret.chars, str);
        ret.restore();

        return ret;
    }

    fn deinit(this: Self) void {
        this.allocator.free(this.chars);
        this.allocator.free(this.erased);
    }

    fn debug(this: Self) void {
        for (this.chars) |c, i| {
            if (!this.erased[i]) print("{c}", .{c});
        }
        print("\n", .{});
    }

    fn reduce(this: *Polymer) void {
        var i: usize = 0;
        var j: usize = 1;

        while (j < this.chars.len) {
            if (this.erased[j]) {
                j += 1;
                continue;
            }
            if (this.erased[i]) {
                i = j;
                j = i + 1;
                continue;
            }


            if (caseCmp(this.chars[i], this.chars[j])) {
                this.erased[i] = true;
                this.erased[j] = true;

                if (i != 0) i -= 1;
                while (i != 0 and this.erased[i]) i -= 1;

                j += 1;

                this.len -= 2;
            } else {
                i = j;
                j = i + 1;
            }
        }
    }

    fn erase(this: *Self, char: u8) void {
        for (this.chars) |c, i| {
            if (c == char or c == caseConv(char)) {
                this.erased[i] = true;
                this.len -= 1;
            }
        }
    }

    fn string(this: Self, alloc: std.mem.Allocator) ![]u8 {
        var str = try alloc.alloc(u8, this.len);

        var from: usize = 0;
        var to: usize = 0;

        while (from < this.chars.len) {
            if (this.erased[from]) {
                from += 1;
            } else {
                str[to] = this.chars[from];
                from += 1;
                to += 1;
            }
        }

        return str;
    }

    fn restore(this: *Polymer) void {
        this.len = this.chars.len;

        for (this.erased) |*e| {
            e.* = false;
        }
    }
};

const expect = std.testing.expect;
const expectEqual= std.testing.expectEqual;
const expectEqualStrings = std.testing.expectEqualStrings;

const testInput = @embedFile("test.txt");
const realInput = @embedFile("input.txt");

fn findBestReduction(polymer: *Polymer) usize {
    var best: usize = std.math.maxInt(usize);

    for ("abcdefghijklmnopqrstuvwxyz") |c| {
        polymer.erase(c);
        polymer.reduce();
        best = @min(best, polymer.len);
        polymer.restore();
    }

    return best;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();

    var allocator = arena.allocator();

    var polymer = try Polymer.init(allocator, realInput);
    defer polymer.deinit();
    
    polymer.reduce();
    println("Part 1: {}", .{ polymer.len });
    polymer.restore();

    var best = findBestReduction(&polymer);
    println("Part 2: {}", .{ best });
}


test "pointer for loop" {
    var arr = [_]u8{ 1, 2, 3, 4 };
    var ref = [_]u8{ 14, 14, 14, 14 };

    for (&arr) |*v| {
        v.* = 14;
    }

    try std.testing.expectEqualSlices(u8, &arr, &ref);
}

test "caseCmp" {
    try expect(caseCmp('A', 'a'));
    try expect(caseCmp('a', 'A'));
    try expect(!caseCmp('b', 'A'));
    try expect(!caseCmp('A', 'b'));
}

test "alloc/free" {
    var alloc = std.testing.allocator;
    var v = try alloc.alloc(u8, 100);
    defer alloc.free(v);
}

test "polymer string" {
    var alloc = std.testing.allocator;
    var polymer = try Polymer.init(alloc, "aAbBcC");
    defer polymer.deinit();
    var str = try polymer.string(alloc);
    defer alloc.free(str);

    try expectEqualStrings(str, "aAbBcC");
}

test "polymer reduce" {
    var alloc = std.testing.allocator;
    var polymer = try Polymer.init(alloc, testInput);
    defer polymer.deinit();

    polymer.reduce();
    var str = try polymer.string(alloc);
    defer alloc.free(str);

    try expectEqualStrings("dabCBAcaDA", str);
}
    

test "polymer erase/restore" {
    var alloc = std.testing.allocator;
    var polymer = try Polymer.init(alloc, testInput);
    defer polymer.deinit();

    var str1 = try polymer.string(alloc);
    defer alloc.free(str1);

    polymer.erase('a');
    var str2 = try polymer.string(alloc);
    defer alloc.free(str2);

    polymer.reduce();
    var str3 = try polymer.string(alloc);
    defer alloc.free(str3);

    polymer.restore();
    var str4 = try polymer.string(alloc);
    defer alloc.free(str4);

    try expectEqualStrings(testInput, str1);
    try expectEqualStrings("dbcCCBcCcD", str2);
    try expectEqualStrings("dbCBcD", str3);
    try expectEqualStrings(testInput, str4);
    
}
    
test "best reduce" {
    var alloc = std.testing.allocator;
    var polymer = try Polymer.init(alloc, testInput);
    defer polymer.deinit();

    var best = findBestReduction(&polymer);
                
    try expect(best == 4);
}
