const std = @import("std");

const testInput = @embedFile("test.txt");
const realInput = @embedFile("input.txt");

fn manhattan(a: Point, b: Point) i32 {
    const abs = std.math.absInt;
    const dx = abs(a.x - b.x) catch unreachable;
    const dy = abs(a.y - b.y) catch unreachable;

    return dx + dy;
}
    
const Point = struct {
    x: i32,
    y: i32,
};

const Field = struct {
    xMin: i32,
    yMin: i32,
    xMax: i32,
    yMax: i32,

    field: []u8,


    fn init(allocator: std.mem.Allocator, points: []Point) !Field {
        var xMin: i32 = std.math.maxInt(i32);
        var yMin: i32 = std.math.maxInt(i32);
        var xMax: i32 = std.math.minInt(i32);
        var yMax: i32 = std.math.minInt(i32);

        for (points) |p| {
            xMin = @min(xMin, p.x);
            yMin = @min(yMin, p.y);
            xMax = @max(xMax, p.x);
            yMax = @max(yMax, p.y);
        }

        xMin -= 1;
        yMin -= 1;
        xMax += 1;
        yMax += 1;

        var width = @intCast(usize, xMax - xMin + 1);
        var height = @intCast(usize, yMax - yMin + 1);

        var this = Field {
            .xMin = xMin,
            .yMin = yMin,
            .xMax = xMax,
            .yMax = yMax,
            .field = try allocator.alloc(u8, width * height)
        };

        for (this.field) |*e| {
            e.* = 0;
        }

        return this;
    }

    fn assign(this: @This(), points: []Point) void {
        var p = Point { .x = this.xMin, .y = this.yMin };

        while (p.x <= this.xMax) : (p.x += 1) {
            p.y = this.xMin;

            while (p.y <= this.yMax) : (p.y += 1) {
                var dist: i32 = std.math.maxInt(i32);
                var closest: u8 = 255;
                var tie = false;

                for (points) |sp, i| {
                    const currDist = manhattan(p, sp);

                    if (currDist < dist) {
                        dist = currDist;
                        closest = @intCast(u8, i);
                        tie = false;
                    } else if (currDist == dist) {
                        tie = true;
                    }
                }

                if (tie) {
                    this.set(p, 0);
                } else {
                    this.set(p, 'A' + closest);
                }
            }
        }
    }

    fn part1(this: @This()) i32 {
        var excluded = [_]bool{false} ** 256;
        var counts = [_]i32{0} ** 256;
        var currBest: usize = 255;

        excluded[0] = true;
        
        var p = Point { .x = this.xMin, .y = this.yMin };

        while (p.y <= this.yMax) : (p.y += 1) {
            p.x = this.xMin;

            while (p.x <= this.xMax) : (p.x += 1) {
                var c = this.get(p);
                counts[c] += 1;

                if (p.x == this.xMin or p.x == this.xMax or p.y == this.yMin or p.y == this.yMax) {
                    excluded[c] = true;
                }

                if (!excluded[c] and (counts[c] > counts[currBest])) {
                    currBest = c;
                }
            }
        }

        return counts[currBest];
    }

    fn part2(this: @This(), allocator: std.mem.Allocator, points: []Point, limit: i64) !i64 {
        var stack = std.ArrayList(Point).init(allocator);
        defer stack.deinit();
        
        var included = std.AutoHashMap(Point, void).init(allocator);
        defer included.deinit();
        
        {
            var p = Point { .x = this.xMin, .y = this.yMin };

            while (p.y <= this.yMax) : (p.y += 1) {
                p.x = this.xMin;
                while (p.x <= this.xMax) : (p.x += 1) {
                    try stack.append(p);
                }
            }
        }

        while (stack.popOrNull()) |p| {
            if (included.contains(p)) continue;
            
            var dist: i64 = 0;

            for (points) |p2| {
                dist += manhattan(p, p2);
            }

            if (dist >= limit) continue;
            // std.debug.print("{},{}: {}\n", .{p.x,p.y,dist});
            
            try included.put(p, {});

            try stack.append(Point { .x = p.x + 0, .y = p.y + 1 });
            try stack.append(Point { .x = p.x + 0, .y = p.y - 1 });
            try stack.append(Point { .x = p.x + 1, .y = p.y + 0 });
            try stack.append(Point { .x = p.x - 1, .y = p.y + 0 });
        }

        return @intCast(i64, included.count());
    }
    
    fn deinit(this: @This(), allocator: std.mem.Allocator) void {
        allocator.free(this.field);
    }

    fn debug(this: @This()) void {
        var p = Point {.x = this.xMin, .y = this.yMin};

        while (p.y <= this.yMax) : (p.y += 1) {
            p.x = this.xMin;

            while (p.x <= this.xMax) : (p.x += 1) {
                const c = this.get(p);
                
                if (c == 0) {
                    std.debug.print(".", .{ });
                } else {
                    std.debug.print("{c}", .{ c });
                }
            }

            std.debug.print("\n", .{});
        }
    }

    fn pointToIndex(this: @This(), p: Point) usize {
        var width = @intCast(usize, this.xMax - this.xMin + 1);
        var xn = @intCast(usize, p.x - this.xMin);
        var yn = @intCast(usize, p.y - this.yMin);

        return yn * width + xn;
    }

    fn set(this: @This(), p: Point, val: u8) void {
        this.field[this.pointToIndex(p)] = val;
    }

    fn get(this: @This(), p: Point) u8 {
        return this.field[this.pointToIndex(p)];
    }
};
    
fn parse(allocator: std.mem.Allocator, txt: []const u8) ![]Point {
    const size = std.mem.count(u8, txt, ",");
    const points = try allocator.alloc(Point, size);

    var it = std.mem.tokenize(u8, txt, " ,\n");

    var i: usize = 0;
    
    while (it.next()) |xstr| {
        defer i += 1;

        const ystr = it.next().?;
        points[i] = Point {
            .x = try std.fmt.parseInt(i32, xstr, 10),
            .y = try std.fmt.parseInt(i32, ystr, 10),
        };
    }

    return points;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    
    var allocator = arena.allocator();

    const points = try parse(allocator, realInput);
    defer allocator.free(points);

    var field = try Field.init(allocator, points);
    defer field.deinit(allocator);

    field.assign(points);

    std.debug.print("Part 1: {}\n", .{field.part1()});
    std.debug.print("Part 2: {}\n", .{try field.part2(allocator, points, 10000)});
}

test "parse count" {
    const allocator = std.testing.allocator;
    const points = try parse(allocator, testInput);
    defer allocator.free(points);
    
    try std.testing.expectEqual(points.len, 6);
}

test "parse works" {
    const allocator = std.testing.allocator;
    const points = try parse(allocator, testInput);
    defer allocator.free(points);

    const ref = [_]Point {
        Point { .x = 1, .y = 1 },
        Point { .x = 1, .y = 6 },
        Point { .x = 8, .y = 3 },
        Point { .x = 3, .y = 4 },
        Point { .x = 5, .y = 5 },
        Point { .x = 8, .y = 9 },
    };

    for (points) |p, i| {
        try std.testing.expectEqual(p.x, ref[i].x);
        try std.testing.expectEqual(p.y, ref[i].y);
    }
}

test "test input" {
    const allocator = std.testing.allocator;
    const points = try parse(allocator, testInput);
    defer allocator.free(points);

    var xMin: i32 = std.math.maxInt(i32);
    var yMin: i32 = std.math.maxInt(i32);
    var xMax: i32 = std.math.minInt(i32);
    var yMax: i32 = std.math.minInt(i32);

    for (points) |p| {
        xMin = @min(xMin, p.x);
        yMin = @min(yMin, p.y);
        xMax = @max(xMax, p.x);
        yMax = @max(yMax, p.y);
    }

    try std.testing.expectEqual(xMin, 1);
    try std.testing.expectEqual(yMin, 1);
    try std.testing.expectEqual(xMax, 8);
    try std.testing.expectEqual(yMax, 9);
}

test "field debug" {
    const allocator = std.testing.allocator;
    const points = try parse(allocator, testInput);
    defer allocator.free(points);


    var field = try Field.init(allocator, points);
    defer field.deinit(allocator);

    std.debug.print("\n", .{});
    field.debug();
    std.debug.print("\n", .{});

    for (points) |p, i| {
        field.set(p, 'A' + @intCast(u8, i));
    }

    field.debug();
}

test "test input assign" {
    const allocator = std.testing.allocator;
    const points = try parse(allocator, testInput);
    defer allocator.free(points);


    var field = try Field.init(allocator, points);
    defer field.deinit(allocator);

    field.debug();
    field.assign(points);
    std.debug.print("\n", .{});
    field.debug();
}

test "test part1" {
    const allocator = std.testing.allocator;
    const points = try parse(allocator, testInput);
    defer allocator.free(points);


    var field = try Field.init(allocator, points);
    defer field.deinit(allocator);

    field.assign(points);
    var best = field.part1();
    std.debug.print("\nBest {}\n", .{best});
}

test "test part2" {
    const allocator = std.testing.allocator;
    const points = try parse(allocator, testInput);
    defer allocator.free(points);

    var field = try Field.init(allocator, points);
    defer field.deinit(allocator);

    try std.testing.expectEqual(try field.part2(allocator, points, 32), 16);
}
