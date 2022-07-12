#include <queue>
#include <vector>
#include <absl/container/flat_hash_set.h>
#include <absl/container/btree_set.h>
#include <absl/container/btree_map.h>

template<typename K, typename V>
using multimap = absl::btree_multimap<K,V>;

template<typename T>
using vec = std::vector<T>;

template<typename T>
using set = absl::flat_hash_set<T>;

template<typename T, typename Compare>
using priority_queue = std::priority_queue<T, std::vector<T>, Compare>;

struct coord
{
	uint8_t c;

	template <typename H>
	friend H AbslHashValue(H h, const coord& c) {
		auto [x,y] = c.unpack();
		return H::combine(std::move(h), x, y);
	}

	coord() : c { 0 } { } 
	coord(int x, int y)
		: c { (uint8_t)((x << 4) | y) }
	{}
	
	std::tuple<int,int> unpack() const { return { c >> 4, c & 0xF }; }
	//std::tuple<char,char> unpack() const { return { x, y }; }
	
	// char x() const { return c >> 4;  }
	// char y() const { return c & 0xF; }

	auto operator<=>(const coord&) const = default;
};

multimap<coord, vec<coord>> build_paths()
{
	multimap<coord, vec<coord>> paths;
	
	for (int xs = 3; xs <= 9; xs+=2) {
		for (int ys = 2; ys <= 3; ys++) {
			for (int xe = 1; xe <= 11; xe++) {
				vec<coord> path;

				if (ys == 3) path.push_back({xs, 2});
			
				if (xe == 3 || xe == 5 || xe == 7 || xe == 9) continue;

				assert(xs != xe);

				int d = xs > xe ? -1 : 1;

				for (int xc = xs; xc != xe; xc+=d) {
					path.push_back({xc, 1});
				}

				path.push_back({xe,1});

				paths.emplace(coord {xs, ys}, std::move(path));
			}
		}
	}

	for (int xs = 1; xs <= 11; xs++) {
		for (int xe = 3; xe <= 9; xe+=2) {
			for (int ye = 2; ye <= 3; ye++) {
				vec<coord> path;

				int d = xs > xe ? -1 : 1;
				for (int xc = xs; xc != xe; xc+=d) {
					if (xc == xs) continue;
					path.push_back({xc, 1});
				}

				path.push_back({xe, 1});
				path.push_back({xe, 2});

				if (ye == 3) path.push_back({xe, 3});

				paths.emplace(coord {xs, 1}, std::move(path));
			}
		}
	}

	return paths;
}

const auto paths = build_paths();

struct state {
	int32_t energy;

	std::array<coord, 8> aphids;
	std::array<int, 8> movecnt;
	
	void debug() {
		std::string_view templ =
			"#############\n"
			"#...........#\n"
			"###.#.#.#.###\n"
			"  #.#.#.#.#  \n"
			"  #########  \n\n";

		int x = 0;
		int y = 0;

		std::cout << "energy: " << energy << '\n';
		
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

				for (int aphid = 0; aphid < 8; aphid++) {
					auto [ax,ay] = aphids[aphid].unpack();

					if (x == ax && y == ay) {
						found = true;
						std::cout << (char)('A' + (aphid>>1));
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
		return H::combine(
			std::move(h),
			absl::Hash<coord>{}(c.aphids[0]) ^ absl::Hash<coord>{}(c.aphids[1]),
			absl::Hash<coord>{}(c.aphids[2]) ^ absl::Hash<coord>{}(c.aphids[3]),
			absl::Hash<coord>{}(c.aphids[4]) ^ absl::Hash<coord>{}(c.aphids[5]),
			absl::Hash<coord>{}(c.aphids[6]) ^ absl::Hash<coord>{}(c.aphids[7]));
	}

	bool operator==(const state &other) const {
		for (int i = 0; i < 4; i++) {
			auto a1 = aphids[2*i];
			auto a2 = aphids[2*i+1];
			auto b1 = other.aphids[2*i];
			auto b2 = other.aphids[2*i+1];

			if (((a1 != b1) || (a2 != b2)) && ((a1 != b2) || (a2 != b1))) return false;
		}

		return true;
	}

	bool is_home(int aphid) const
	{
		auto [x,y] = aphids[aphid].unpack();
		auto [ox,oy] = aphids[aphid + ((aphid % 2) == 1 ? -1 : 1)].unpack();
		
		auto i = aphid/2;
		auto xt = 3 + 2*i;

		return (y == 3 && x == xt) || (y == 2 && x == xt && oy == 3 && ox == xt);
	}

	bool is_occupied(coord c) {
		for (int i = 0; i < 8; i++) {
			if (c == aphids[i]) return true;
		}
		return false;
	}

	void push_new_states(auto &collection, bool debug) {
		for (int aphid = 0; aphid < 8; aphid++) {
			if (is_home(aphid)) continue;
			if (movecnt[aphid] == 2) continue;

			auto a = aphids[aphid];
			
			auto [pb, pe] = paths.equal_range(a);
			
			for (auto &it = pb; it != pe; it++) {
				const auto &path = it->second;
				coord fin {0,0};

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
				
				newState.energy = energy + path.size() * std::pow(10, aphid >> 1); 
				newState.aphids[aphid] = fin;
				newState.movecnt[aphid]++;
				
				if (debug) {
					newState.debug();
				}

				collection.push_back(newState);
			}
		}
	}
};
	
state make_state(std::string_view pattern) {
	int idxs[4] { 0, 2, 4, 6 };
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

	for (int i = 0; i < 8; i++) {
		s.movecnt[i] = 0;
	}

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
	print_paths({5, 3});
	
	// std::string input =
	// 	"#############\n"
	// 	"#...........#\n"
	// 	"###B#C#B#D###\n"
	// 	"  #A#D#C#A#  \n"
	// 	"  #########  \n";
	
	std::string input =
		"#############\n"
		"#...........#\n"
		"###B#A#B#C###\n"
		"  #D#A#D#C#  \n"
		"  #########  \n";

	std::string look_for =
		"#############\n"
		"#...B.......#\n"
		"###B#.#C#D###\n"
		"  #A#D#C#A#  \n"
		"  #########  \n";

	std::string fin_pat =
		"#############\n"
		"#...........#\n"
		"###A#B#C#D###\n"
		"  #A#B#C#D#  \n"
		"  #########  \n";

	auto init = make_state(input);
	auto check = make_state(look_for);
	auto fin = make_state(fin_pat);

	init.debug();

	struct comparer {
		bool operator()(const state &s1, const state &s2) {
			return s1.energy > s2.energy;
		}
	};

	vec<state> next;
	set<state> visited;
	priority_queue<state, comparer> queue;

	queue.push(init);

	int64_t i = 0;
	
	while (!queue.empty()) {
		next.clear();
		
		auto s = queue.top();
		queue.pop();

		if (visited.find(s) != visited.end()) {
			continue;
		}

		if (i++ % 1000 == 0) {
			std::cout << s.energy << '\r' << std::flush;
		}

		// if (s.energy == 40) {
		// 	s.debug();
		// }

		// if (s == check) {
		// 	std::cout << "Check!\n";
		// 	s.debug();
		// }

		if (s == fin) {
			s.debug();
			break;
		}
		
		visited.insert(s);

		s.push_new_states(next, false);

		for (auto &s: next) {
			if (visited.find(s) == visited.end()) {
				queue.push(s);
			}
		}
	}
}

