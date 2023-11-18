const std = @import("std");

const Order = std.math.Order;
const print = std.debug.print;

pub fn main() !void {

    const start = [_]u8 { 2, 6, 4, 7, 9, 3 };
    const end   = [_]u8 { 8, 0, 3, 9, 3, 5 };

    var curr = start;
    
    var count: i64 = 0;

    while (std.mem.order(u8, &curr, &end) == .lt) {
        if (valid_part2(curr)) count += 1;
        nextPass(&curr);
    }

    print("Part 1: {}\n", .{ count });
}

fn nextPass(pass: *[6]u8) void {
    var i = pass.len - 1;
    pass.*[i] += 1;

    while (i >= 1) : (i -= 1) {
        if (pass.*[i] == 10) {
            pass.*[i] = 0;
            pass.*[i-1] += 1;
        }
    }
    // i = 0;
    
    // while (i < pass.len - 1) : (i += 1) {
    //     pass.*[i+1] = @max(pass.*[i], pass.*[i+1]);
    // }
}

fn valid_part1(pass: [6]u8) bool {
    var i: usize= 0;

    var hasRepeat: bool = false;

    while (i < pass.len - 1) : (i += 1) {
        if (pass[i] == pass[i+1]) {
            hasRepeat = true;
        }
        if (pass[i] > pass[i+1]) {
            return false;
        }
    }

    if (!hasRepeat) return false;

    return true;
}

fn valid_part2(pass: [6]u8) bool {
    var i: usize= 0;

    var hasDouble: bool = false;

    while (i < pass.len - 1) : (i += 1) {
        if (pass[i] > pass[i+1]) {
            return false;
        }

        if (pass[i] == pass[i+1]) {
            if (i != 0 and pass[i-1] == pass[i]) {
            } else if (i != pass.len - 2 and pass[i+1] == pass[i+2]) {
            } else {
                hasDouble = true;
            }
        }
    }

    if (!hasDouble) return false;

    return true;
}


const expectEqual = std.testing.expectEqual;

test "valid pass" {
    try expectEqual(true,  valid_part1(&[_]u8 { 1, 1, 1, 1, 1, 1}));
    try expectEqual(false, valid_part1(&[_]u8 { 2, 2, 3, 4, 5, 0}));
    try expectEqual(false, valid_part1(&[_]u8 { 1, 2, 3, 7, 8, 9}));
}
