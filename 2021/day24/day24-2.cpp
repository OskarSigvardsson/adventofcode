#include <iostream>
#include <fstream>
#include <sstream>
#include <regex>

auto plus = [](auto a, auto b) { return a + b; };
auto mult = [](auto a, auto b) { return a * b; };
auto divi = [](auto a, auto b) { return a / b; };
auto modu = [](auto a, auto b) { return a % b; };
auto equl = [](auto a, auto b) { return a == b; };

using i64 = int64_t;

struct Range;
struct Domain;

Domain& combine(auto &&op, Domain &d1, const Domain &d2);


template<typename T>
T min(T a, T b) {
	return a < b ? a : b;
}

auto min(auto a, auto b)
{
	return a < b ? a : b;
}

auto x = min(123, 142.5);

struct Range {
	i64 min;
	i64 max;

	Range(i64 min, i64 max) : min { min }, max { max } { }
	
	struct iterator {
		i64 val;

		bool operator==(const iterator &other) const = default;
		int operator*() { return val; };
		iterator& operator++() { val++; return *this; }
	};

	iterator begin() const { return { min }; }
	iterator end() const { return { max + 1 }; }
};


struct Domain
{
	std::vector<Range> ranges;

	Domain() {}
	Domain(i64 val) : ranges { { val, val } } { }
	Domain(i64 val1, i64 val2) : ranges { { val1, val2 } } { }

	bool contains(i64 val) const
	{
		for (const auto &r1: ranges) {
			if (r1.min <= val && val <= r1.max) return true;
			if (val < r1.min) return false;
		}

		return false;
	}
};


static std::vector<i64> vals;

Domain& combine(auto &&op, Domain &d1, const Domain &d2)
{
	vals.clear();
	
	for (const auto &r1: d1.ranges)
	for (const auto &r2: d2.ranges)
	{
		for (const auto &n1: r1)
		for (const auto &n2: r2)
		{
			vals.push_back(op(n1, n2));
		}
	}

	std::sort(vals.begin(), vals.end());
	d1.ranges.clear();

	auto sz = vals.size();
	for (int i = 0; i < sz; i++) {
		auto min = vals[i];
		auto curr = min;

		while (i + 1 < sz && vals[i+1] <= curr + 1) {
			curr = vals[++i];
		}

		auto max = curr;
		d1.ranges.emplace_back(min, max);
	}

	return d1;
}

enum OpCode {
	INP, ADD, MUL, DIV, MOD, EQL
};

struct Val {
	bool reg;
	int val;
	Domain dom;
};

struct Instruction {
	OpCode op;
	Val arg1;
	Val arg2;
};


bool check_prefix(const std::vector<Instruction> inst, std::vector<char> &prefix, int length)
{
	static Domain regs[4]{};
	static std::vector<Domain> input;

	input.clear();

	for (auto &i: prefix) {
		input.emplace_back(i);
	}

	while (input.size() < length) {
		input.emplace_back(1, 9);
	}

	regs[0].ranges.assign({{0, 0}});
	regs[1].ranges.assign({{0, 0}});
	regs[2].ranges.assign({{0, 0}});
	regs[3].ranges.assign({{0, 0}});

	int ictr = 0;
	
	if (prefix.size() <= 5) {
		std::cout << "Prefix: ";

		for (int c: prefix) {
			std::cout << c;
		}
		std::cout << "... " << std::endl;
	}
	
	for (auto &[op, arg1, arg2]: inst) {
		switch (op) {
		case INP:
			regs[arg1.val] = input[ictr++];
			break;
		case ADD:
			combine(plus, regs[arg1.val], arg2.reg ? regs[arg2.val] : arg2.dom);
			break;
		case MUL:
			combine(mult, regs[arg1.val], arg2.reg ? regs[arg2.val] : arg2.dom);
			break;
		case DIV:
			combine(divi, regs[arg1.val], arg2.reg ? regs[arg2.val] : arg2.dom);
			break;
		case MOD:
			combine(modu, regs[arg1.val], arg2.reg ? regs[arg2.val] : arg2.dom);
			break;
		case EQL:
			combine(equl, regs[arg1.val], arg2.reg ? regs[arg2.val] : arg2.dom);
			break;
		}
	}

	auto hit = regs[2].contains(0);
	
	if (hit && prefix.size() == length) {
		std::cout << "Found!" << std::endl;

		for (int c: prefix) {
			std::cout << c;
		}

		std::cout << std::endl;
		return true;
	}

	if (hit && prefix.size() < length) {
		prefix.push_back(0);

		for (char c = 9; c >= 1; c--) {
			prefix.back() = c;

			if (check_prefix(inst, prefix, length)) {
				return true;
			}
		}

	    prefix.erase(prefix.end() - 1);
	}

	return false;
}

int main()
{
	std::regex instruction (R"REGEX((...) *(x|y|z|w) *(-?[\d]+|x|y|z|w)?)REGEX");

	std::string file;
	
	{
		std::ifstream stream { "input.txt" };
		std::stringstream buf;
		buf << stream.rdbuf();

		file = buf.str();
	}
	
	auto ins_begin = std::sregex_iterator(file.begin(), file.end(), instruction);
	auto ins_end = std::sregex_iterator();

	auto parse_arg = [&](auto &str) -> Val {
		switch (str[0]) {
		case 'x': return { true, 0 };
		case 'y': return { true, 1 };
		case 'z': return { true, 2 };
		case 'w': return { true, 3 };
		default:
			return { false, 0, Domain { std::stoi(str) } };
		}
	};

	auto split = [](auto &m) {
		return std::make_tuple(m.str(1), m.str(2), m.str(3));
	};
	
	int inputs = 0;
	
	std::vector<Instruction> inst;
	
	for (auto it = ins_begin; it != ins_end; it++) {
		const auto &[ins, arg1, arg2] = split(*it);

		if (ins == "inp") {
			inputs++;
			inst.push_back({INP, parse_arg(arg1), Val { false, 0 }});
		} else if (ins == "add") {
			inst.push_back({ADD, parse_arg(arg1), parse_arg(arg2)});
		} else if (ins == "mul") {
			inst.push_back({MUL, parse_arg(arg1), parse_arg(arg2)});
		} else if (ins == "div") {
			inst.push_back({DIV, parse_arg(arg1), parse_arg(arg2)});
		} else if (ins == "mod") {
			inst.push_back({MOD, parse_arg(arg1), parse_arg(arg2)});
		} else if (ins == "eql") {
			inst.push_back({EQL, parse_arg(arg1), parse_arg(arg2)});
		} else {
			assert(false);
		}
	}

	std::vector<char> prefix(1);

	for (char c = 9; c >= 1; c--) {
		prefix[0] = c;
		check_prefix(inst, prefix, inputs);
	}
}
