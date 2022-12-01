#include <queue>
#include <vector>
#include <absl/container/flat_hash_map.h>
#include <absl/container/flat_hash_set.h>
#include <absl/container/btree_set.h>
#include <absl/container/btree_map.h>

template<typename K, typename V>
using multimap = absl::btree_multimap<K,V>;

template<typename T>
using vec = std::vector<T>;

template<typename T>
using set = absl::flat_hash_set<T>;

template<typename K, typename V>
using map = absl::flat_hash_map<K,V>;

template<typename T, typename Compare>
using priority_queue = std::priority_queue<T, std::vector<T>, Compare>;

static constexpr int APHIDS = 16;

struct coord
{
	//uint8_t c;
	int x,y;

	template <typename H>
	friend H AbslHashValue(H h, const coord& c) {
		auto [x,y] = c.unpack();
		return H::combine(std::move(h), x, y);
	}

	// coord() : c { 0 } { } 
	// coord(int x, int y)
	// 	: c { (uint8_t)((x << 4) | y) }
	// {}
	
	//std::tuple<int,int> unpack() const { return { c >> 4, c & 0xF }; }
	std::tuple<char,char> unpack() const { return { x, y }; }
	
	// char x() const { return c >> 4;  }
	// char y() const { return c & 0xF; }

	auto operator<=>(const coord&) const = default;
};

int dist(coord c1, coord c2) {
	auto [x1,y1] = c1.unpack();
	auto [x2,y2] = c2.unpack();

	return std::abs(x1 - x2) + std::abs(y1 - y2);
}

multimap<coord, vec<coord>> build_paths()
{
	multimap<coord, vec<coord>> paths;

	for (int xs = 3; xs <= 9; xs+=2) {
		for (int ys = 2; ys <= 5; ys++) {
			//for (int ys = 2; ys <= 3; ys++) {
			for (int xe = 1; xe <= 11; xe++) {
				if (xe == 3 || xe == 5 || xe == 7 || xe == 9) continue;

				vec<coord> path;

				int x = xs;
				int y = ys;

				while (y > 1) {
					path.push_back({x, --y});
				}

				//path.push_back({x, y});

				assert(xs != xe);

				int d = xs > xe ? -1 : 1;

				while (x != xe) {
					path.push_back({x+=d, y});
				}

				//path.push_back({xe,y});

				paths.emplace(coord {xs, ys}, std::move(path));
			}
		}
	}

	for (int xs = 1; xs <= 11; xs++) {
		if (xs == 3 || xs == 5 || xs == 7 || xs == 9) continue;

		for (int xe = 3; xe <= 9; xe+=2) {
			for (int ye = 2; ye <= 5; ye++) {
			//for (int ye = 2; ye <= 3; ye++) {
				vec<coord> path;

				int d = xs > xe ? -1 : 1;

				int x = xs;
				int y = 1;
				
				while (x != xe) {
					path.push_back({x+=d, y});
				}

				while (y != ye) {
					path.push_back({x, ++y});
				}

				paths.emplace(coord {xs, 1}, std::move(path));
			}
		}
	}

	return paths;
}

const auto paths = build_paths();

struct state {
	
	int32_t energy;
	int32_t heuristic;

	std::array<coord, APHIDS> aphids;
	std::array<int, APHIDS> movecnt;
	
	void debug() {
		std::string_view templ =
			"#############\n"
			"#...........#\n"
			"###.#.#.#.###\n"
			"  #.#.#.#.#  \n"
			"  #.#.#.#.#  \n"
			"  #.#.#.#.#  \n"
			"  #########  \n\n";

		int x = 0;
		int y = 0;

		std::cout << "energy: " << energy << '\n';
		std::cout << "heuristic: " << heuristic << '\n';
		
		for (auto &c: templ) {
			switch (c) {
			case ' ':
			case '#': {
				std::cout << c;
				x++;
				break;
			}
			
			case '\n': {
				std::cout << '\n';
				y++;
				x = 0;
				break;
			}

			case '.': {
				bool found = false;

				for (int aphid = 0; aphid < APHIDS; aphid++) {
					auto [ax,ay] = aphids[aphid].unpack();

					if (x == ax && y == ay) {
						found = true;
						std::cout << (char)('A' + (aphid >> 2));
						break;
					}
				}

				if (!found) std::cout << ".";

				x++;
				break;
			}

			default:
				assert(false);
			}
		}
	}

	template <typename H>
	friend H AbslHashValue(H h, const state& c) {

		for (int i = 0; i < 4; i++) {
			h = H::combine(
				std::move(h),
				absl::Hash<coord>{}(c.aphids[4*i+0]) ^
				absl::Hash<coord>{}(c.aphids[4*i+1]) ^
				absl::Hash<coord>{}(c.aphids[4*i+2]) ^
				absl::Hash<coord>{}(c.aphids[4*i+3]));
		}

		return h;
	}

	bool operator==(const state &other) const {
		for (int i = 0; i < 4; i++) {
			std::array<coord, 4> mine {
				aphids[4*i+0],
				aphids[4*i+1],
				aphids[4*i+2],
				aphids[4*i+3],
			};

			std::array<coord, 4> theirs {
				other.aphids[4*i+0],
				other.aphids[4*i+1],
				other.aphids[4*i+2],
				other.aphids[4*i+3],
			};

			std::sort(std::begin(mine), std::end(mine));
			std::sort(std::begin(theirs), std::end(theirs));

			if (mine != theirs) return false;
		}

		return true;
	}

	void calc_heuristic() {
		heuristic = 0;
		
		for (int aphid = 0; aphid < APHIDS; aphid++) {
			auto a = aphids[aphid];
			auto [x,y] = a.unpack();

			int kind = aphid >> 2;
			int col = 3 + 2*kind;


			if (x != col) {
				heuristic += std::pow(10, kind) * dist(a, {col, 1});
				a = {col, 1};
			}

			coord t1 { 3 + kind*2, 2 };
			coord t2 { 3 + kind*2, 3 };
			coord t3 { 3 + kind*2, 4 };
			coord t4 { 3 + kind*2, 5 };

			heuristic += std::pow(10, kind) *
				std::min({
					dist(a, t1),
					dist(a, t2),
					dist(a, t3),
					dist(a, t4)
				});
		}
	}

	bool is_home(int aphid) const
	{
		auto kind = aphid >> 2;
		auto col = 3 + 2 * kind;
		auto [x,y] = aphids[aphid].unpack();

		if (y < 2 || y > 5) return false;
		if (x != col) return false;

		for (int yc = y+1; yc <= 5; yc++) {
			if (kind != occupied_by({x, yc})) return false;
		}

		return true;
	}

	bool is_occupied(coord c) const {
		for (int i = 0; i < APHIDS; i++) {
			if (c == aphids[i]) return true;
		}
		return false;
	}

	bool is_floor(coord c) const {
		auto [x,y] = c.unpack();

		if (y == 1) return x >= 1 && x <= 11;
		if (y == 2) return x == 3 || x == 5 || x == 7 || x == 9;
		if (y == 3) return x == 3 || x == 5 || x == 7 || x == 9;
		if (y == 4) return x == 3 || x == 5 || x == 7 || x == 9;
		if (y == 5) return x == 3 || x == 5 || x == 7 || x == 9;

		return false;
	}

	bool is_free(coord c) const {
		return is_floor(c) && !is_occupied(c);
	}

	int occupied_by(coord c) const {
		for (int i = 0; i < APHIDS; i++) {
			if (aphids[i] == c) return i >> 2;
		}

		return -1;
	}

	void push_new_states(auto &collection, bool debug) {
		for (int aphid = 0; aphid < APHIDS; aphid++) {
			if (is_home(aphid)) continue;
			if (movecnt[aphid] == 2) continue;

			auto a = aphids[aphid];
			
			auto [pb, pe] = paths.equal_range(a);
			
			for (auto &it = pb; it != pe; it++) {
				const auto &path = it->second;
				coord fin = path[path.size() - 1];

				auto [fx, fy] = fin.unpack();

				auto kind = aphid >> 2;
				auto col = 3 + 2 * kind;

				if (fy != 1 && fx != col) continue;

				bool valid = true;

				for (auto c: path) {
					if (is_occupied(c)) {
						valid = false;
						break;
					}

					fin = c;
				}

				

				if (!valid) continue;

				state newState = *this;
				
				newState.energy = energy + path.size() * std::pow(10, aphid >> 2); 
				newState.aphids[aphid] = fin;
				newState.movecnt[aphid]++;
				newState.calc_heuristic();
				
				if (debug) {
					newState.debug();
				}

				collection.push_back(newState);
			}
		}
	}
};
	
state make_state(std::string_view pattern) {
	int idxs[4] { 0, 4, 8, 12 };
	char x = 0;
	char y = 0;

	state s;
	
	s.energy = 0;
	for (auto c: pattern) {
		if (c == '\n') {
			x = 0;
			y++;
			continue;
		}
		
		auto t = c - 'A';
		
		if (t >= 0 && t < 4) {
			s.aphids[idxs[t]++] = coord { x, y };
		}

		x++;
	}

	for (int i = 0; i < APHIDS; i++) {
		s.movecnt[i] = 0;
	}

	s.calc_heuristic();
	return s;
}

void print_paths(coord start) {
	auto [x,y] = start.unpack();
	
	auto [pb, pe] = paths.equal_range(start);
			
	std::cout << "(" << (int)x << "," << (int)y << "):\n";
	for (auto &it = pb; it != pe; it++) {
		const auto &path = it->second;

		for (auto c: path) {
			auto [x,y] = c.unpack();
			std::cout << "(" << (int)x << "," << (int)y << ") ";
		}

		std::cout << "\n";
	}

	std::cout << '\n';
}

int main() {
	print_paths({5, 4});
	print_paths({3, 2});
	
	// std::string input =
	// 	"#############\n"
	// 	"#...........#\n"
	// 	"###B#C#B#D###\n"
	// 	"  #D#C#B#A#  \n"
    //     "  #D#B#A#C#  \n"
	// 	"  #A#D#C#A#  \n"
	// 	"  #########  \n";
	
	std::string input =
		"#############\n"
		"#...........#\n"
		"###B#A#B#C###\n"
		"  #D#C#B#A#  \n"
        "  #D#B#A#C#  \n"
		"  #D#A#D#C#  \n"
		"  #########  \n";

	std::string look_for =
		"#############\n"
		"#...B.......#\n"
		"###.#C#B#D###\n"
		"  #D#C#B#A#  \n"
        "  #D#B#A#C#  \n"
		"  #A#D#C#A#  \n"
		"  #########  \n";

	std::string fin_pat =
		"#############\n"
		"#...........#\n"
		"###A#B#C#D###\n"
		"  #A#B#C#D#  \n"
        "  #A#B#C#D#  \n"
		"  #A#B#C#D#  \n"
		"  #########  \n";

	auto init = make_state(input);
	auto check = make_state(look_for);
	auto fin = make_state(fin_pat);


	init.debug();
	check.debug();
	fin.debug();

	struct comparer {
		bool operator()(const state &s1, const state &s2) {
			return s1.energy + s1.heuristic > s2.energy + s2.heuristic;
		}
	};

	vec<state> next;
	set<state> closed;
	
	priority_queue<state, comparer> queue;

	queue.push(init);

	int64_t i = 0;
	
	while (!queue.empty()) {
		next.clear();
		
		auto s = queue.top();
		queue.pop();

		if (closed.find(s) != closed.end()) {
			continue;
		}

		if (i++ % 1000 == 0) {
			std::cout << s.energy + s.heuristic << " " << queue.size() << "          \r" << std::flush;
		}

		// if (s.energy == 40) {
		// 	s.debug();
		// }

		if (s == check) {
			std::cout << "Check!\n";
			s.debug();
		}

		if (s == fin) {
			s.debug();
			break;
		}
		
		closed.insert(s);

		s.push_new_states(next, s == check);

		for (auto &s: next) {
			if (closed.find(s) == closed.end()) {
				queue.push(s);
			}
		}
	}
}

