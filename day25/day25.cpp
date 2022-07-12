#include <vector>
#include <fstream>
#include <iostream>
#include <array>

using field = std::vector<std::vector<uint8_t>>; 

enum {
	EMPTY = 0, RIGHT = 1, DOWN = 2
};

bool step(field &f)
{
	static field f1;
	static field f2;

	if (f1.size() != f.size()) {
		f1 = f;
		f2 = f;
	}

	auto width = f[0].size();
	auto height = f.size();

	for (auto y = 0; y < height; y++)
	for (auto x = 0; x < width; x++)
	{
		f1[y][x] = EMPTY;
		f2[y][x] = EMPTY;
	}

	auto wrap = [](auto size) {
		return [size](auto c) -> int {
			if (c == size) return 0;
			if (c == -1) return size - 1;
			return c;
		};
	};

	auto xw = wrap(width);
	auto yw = wrap(height);


	auto changed = false;

	for (int y = 0; y < height; y++)
	for (int x = 0; x < width; x++)
	{
		switch (f[y][x]) {
		case RIGHT:
			if (f[y][xw(x+1)] == EMPTY) {
				f2[y][xw(x+1)] = RIGHT;
				changed = true;
			} else {
				f2[y][x] = RIGHT;
			}
			break;

		default:
			break;
		}
	}

	for (int y = 0; y < height; y++)
	for (int x = 0; x < width; x++)
	{
		switch (f[y][x]) {
		case DOWN:
			if (f[yw(y+1)][x] != DOWN && f2[yw(y+1)][x] == EMPTY) {
				f2[yw(y+1)][x] = DOWN;
				changed = true;
			} else {
				f2[y][x] = DOWN;
			}
			break;

		default:
			break;
		}
	}

	std::swap(f2, f);

	return changed;
}

int main(int argc, char **argv) {
	std::ifstream stream { "input.txt" };

	field f;
	auto row = &f.emplace_back();

	char c;
	while (stream.get(c)) {
		switch (c) {
		case '.': row->push_back(EMPTY); break;
		case '>': row->push_back(RIGHT); break;
		case 'v': row->push_back(DOWN);  break;

		case '\n':
			row = &f.emplace_back();
			break;

		default:
			assert(false);
		}
	}

	if (f.back().size() == 0) f.resize(f.size() - 1);

	int steps = 0;
	do { 
		steps++;
		// char cs[] = { '.', '>', 'v' };

		// std::cout << "Step " << steps++ << std::endl;

		// for (auto &row: f) {
		// 	for (auto &c: row) {
		// 		std::cout << cs[c];
		// 	}
		// 	std::cout << std::endl;
		// }

		// std::cout << std::endl;
	} while (step(f));

	std::cout << steps << std::endl;
}
