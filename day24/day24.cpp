#include <iterator>
#include <variant>
#include <regex>
#include <fstream>
#include <iostream>
#include <sstream>
#include <unordered_map>

#define COEFS 16

using std::endl;

struct Num;
struct Var;
struct Add;
struct Mul;
struct Div;
struct Mod;
struct Eql;
struct Neq;
struct Lin;

using Expr = std::variant<Num, Var, Add, Mul, Div, Mod, Eql, Neq, Lin>;

using i64 = int64_t;
using u8 = uint8_t;

struct Num {
	i64 val;
};

struct Var {
	u8 var;
};

struct Add {
	std::shared_ptr<Expr> left;
	std::shared_ptr<Expr> right;
};

struct Mul {
	std::shared_ptr<Expr> left;
	std::shared_ptr<Expr> right;
};

struct Div {
	std::shared_ptr<Expr> left;
	std::shared_ptr<Expr> right;
};

struct Mod {
	std::shared_ptr<Expr> left;
	std::shared_ptr<Expr> right;
};

struct Eql {
	std::shared_ptr<Expr> left;
	std::shared_ptr<Expr> right;
};

struct Neq {
	std::shared_ptr<Expr> left;
	std::shared_ptr<Expr> right;
};

struct Lin {
	std::array<i64, COEFS> cs{};

	Lin() {
	}
	Lin(const Var& v) {
		cs[v.var] = 1;
	}

	Lin(const Num& n) {
		cs[0] = n.val;
	}

	bool constant() const
	{
		for (int i = 1; i < COEFS; i++) {
			if (cs[i] != 0) return false;
		}
		return true;
	}

	bool zero() const
	{
		return cs[0] == 0 && constant();
	}

	bool one() const
	{
		return cs[0] == 1 && constant();
	}

	Lin operator+(const Lin &right) const {
		Lin res;

		for (int i = 0; i < COEFS; i++) {
			res.cs[i] = cs[i] + right.cs[i];
		}

		return res;
	}

	bool operator==(const Lin &right) const {
		for (int i = 0; i < COEFS; i++) {
			if (cs[i] != right.cs[i]) return false;
		}

		return true;
	}
};

bool is_zero(const Expr &e) {
	const Num *n;
	const Lin *l;
	
	if ((n = std::get_if<Num>(&e))) {
		return n->val == 0;
	} else if ((l = std::get_if<Lin>(&e))) {
		return l->zero();
	} else {
		return false;
	}
}

bool is_one(const Expr &e) {
	const Num *n;
	const Lin *l;
	
	if ((n = std::get_if<Num>(&e))) {
		return n->val == 1;
	} else if ((l = std::get_if<Lin>(&e))) {
		return l->one();
	} else {
		return false;
	}
}

bool is_zero(const std::shared_ptr<Expr> &e) {
	return is_zero(*e);
}

bool is_one(const std::shared_ptr<Expr> &e) {
	return is_one(*e);
}

std::shared_ptr<Expr> optimize(std::shared_ptr<Expr> input);

auto expr(auto &&expr) {
	return optimize(std::make_shared<Expr>(expr));
}

auto zero = expr(Num{0});

std::ostream& operator<<(std::ostream& os, Expr &expr);
std::ostream& operator<<(std::ostream& os, std::shared_ptr<Expr> &expr);

struct Stream {
	std::ostream &os;
	
	std::ostream& operator()(Num &v) {
		os << v.val;
		return os;
	}

	std::ostream& operator()(Var &v) {
		os << "v" << std::to_string(v.var);
		return os;
	}

	std::ostream& operator()(Add &v) {
		os << "add(" << v.left << ", " << v.right << ")";
		return os;
	}

	std::ostream& operator()(Mul &v) {
		os << "mul(" << v.left << ", " << v.right << ")";
		return os;
	}

	std::ostream& operator()(Div &v) {
		os << "div(" << v.left << ", " << v.right << ")";
		return os;
	}

	std::ostream& operator()(Mod &v) {
		os << "mod(" << v.left << ", " << v.right << ")";
		return os;
	}

	std::ostream& operator()(Eql &v) {
		os << "eql(" << v.left << ", " << v.right << ")";
		return os;
	}

	std::ostream& operator()(Neq &v) {
		os << "neq(" << v.left << ", " << v.right << ")";
		return os;
	}

	std::ostream& operator()(Lin &v) {
		bool any = false;
		for (int i = 0; i < COEFS; i++) {
			auto c = v.cs[i];

			if (c != 0) {
				if (any) {
					os << " + ";
				}
				if (i == 0) {
					os << c;
				} else if (c == 1) {
					os << "v" << i;
				} else {
					os << c << "v" << i;
				}
				any = true;
			}
		}

		if (!any) os << 0;

		return os;
	}
};

i64 eval(const std::vector<i64> &vars, std::shared_ptr<Expr> expr);

struct Eval {
	const std::vector<i64> &vars;
	
	i64 operator()(Num &v) {
		return v.val;
	}

	i64 operator()(Var &v) {
		return vars[v.var];
	}

	i64 operator()(Add &v) {
		return eval(vars, v.left) + eval(vars, v.right);
	}

	i64 operator()(Mul &v) {
		return eval(vars, v.left) * eval(vars, v.right);
	}

	i64 operator()(Div &v) {
		return eval(vars, v.left) / eval(vars, v.right);
	}

	i64 operator()(Mod &v) {
		return eval(vars, v.left) % eval(vars, v.right);
	}

	i64 operator()(Eql &v) {
		return eval(vars, v.left) == eval(vars, v.right);
	}

	i64 operator()(Neq &v) {
		return eval(vars, v.left) != eval(vars, v.right);
	}

	i64 operator()(Lin &v) {
		i64 sum = 0;
		
		for (int i = 0; i < COEFS; i++) {
			sum += v.cs[i] * vars[i];
		}
		
		return sum;
	}
};


struct Optimize {
	std::shared_ptr<Expr> &curr;
	
	std::shared_ptr<Expr> operator()(Num &v) {
		return expr(Lin {v});
	}

	std::shared_ptr<Expr> operator()(Var &v) {
		return expr(Lin {v});
	}

	std::shared_ptr<Expr> operator()(Add &v) {
		auto left = v.left;
		auto right = v.right;

		auto n1 = std::get_if<Lin>(left.get());
		auto n2 = std::get_if<Lin>(right.get());

		if (n1 && n2) {
			return expr(*n1 + *n2);
		} else if (is_zero(left)) {
			return right;
		} else if (is_zero(right)) {
			return left;
		} else {
			return curr;
		}
	}

	std::shared_ptr<Expr> operator()(Mul &v) {
		auto left = v.left;
		auto right = v.right;

		auto n1 = std::get_if<Lin>(left.get());
		auto n2 = std::get_if<Lin>(right.get());

		if (n1 && n2 && n1->constant() && n2->constant()) {
			return expr(Lin { Num {n1->cs[0] * n2->cs[0]} } );
		} else if (is_zero(left)) {
			return zero;
		} else if (is_zero(right)) {
			return zero;
		} else if (is_one(left)) {
			return right;
		} else if (is_one(right)) {
			return left;
		} else {
			return curr;
			return expr(Mul{left, right});
		}
	}

	std::shared_ptr<Expr> operator()(Div &v) {
		auto left = v.left;
		auto right = v.right;

		auto n1 = std::get_if<Lin>(left.get());
		auto n2 = std::get_if<Lin>(right.get());

		if (n1 && n2 && n1->constant() && n2->constant()) {
			return expr(Lin { Num { n1->cs[0] / n2->cs[0]} });
		} else if (is_one(right)) {
			return left;
		} else {
			return curr;
			return expr(Div{left,right});
		}
	}

	std::shared_ptr<Expr> operator()(Mod &v) {
		auto left = v.left;
		auto right = v.right;

		auto n1 = std::get_if<Lin>(left.get());
		auto n2 = std::get_if<Lin>(right.get());

		if (n1 && n2 && n1->constant() && n2->constant()) {
			return expr(Lin { Num { n1->cs[0] % n2->cs[1] }});
		} else {
			return curr;
			return expr(Mod{left,right});
		}
	}

	std::shared_ptr<Expr> operator()(Eql &v) {
		auto left = v.left;
		auto right = v.right;

		auto n1 = std::get_if<Lin>(left.get());
		auto n2 = std::get_if<Lin>(right.get());

		auto e1 = std::get_if<Eql>(left.get());

		if (n1 && n2 && n1->constant() && n2->constant()) {
			return expr(Lin { Num { *n1 == *n2 } });
		} else if (e1 && n2 && n2->constant()) {
			if (n2->cs[0] == 0) {
				return expr(Neq { e1->left, e1->right });
			} else if (n2->cs[1] == 1) {
				return left;
			} else {
				return zero;
			}
		} else {
			return curr;
			return expr(Eql{left,right});
		}
	}

	std::shared_ptr<Expr> operator()(Neq &v) {
		auto left = v.left;
		auto right = v.right;

		auto n1 = std::get_if<Lin>(left.get());
		auto n2 = std::get_if<Lin>(right.get());

		if (n1 && n2 && n1->constant() && n2->constant()) {
			return expr(Lin {Num { n1->cs[0] != n2->cs[0] }});
		} else {
			return curr;
			return expr(Eql{left,right});
		}
	}

	std::shared_ptr<Expr> operator()(Lin &v) {
		return curr;
	}
};

std::shared_ptr<Expr> optimize(std::shared_ptr<Expr> input)
{
	return std::visit(Optimize { input }, *input);
}

i64 eval(const std::vector<i64> &vars, std::shared_ptr<Expr> expr)
{
	return std::visit(Eval{vars}, *expr);
}

std::ostream& operator<<(std::ostream& os, Expr &expr)
{
	return std::visit(Stream{os}, expr);
}

std::ostream& operator<<(std::ostream& os, std::shared_ptr<Expr> &expr)
{
	return os << *expr;
}
	


const auto split(auto &m) {
	return std::make_tuple(m.str(1), m.str(2), m.str(3));
}

int main()
{
	std::string file;
	
	{
		std::ifstream stream { "input.txt" };
		std::stringstream buf;
		buf << stream.rdbuf();

		file = buf.str();
	}
	
	auto ins_begin = std::sregex_iterator(file.begin(), file.end(), instruction);
	auto ins_end = std::sregex_iterator();

	std::unordered_map<char, std::shared_ptr<Expr>> regs {
		{ 'x', zero },
		{ 'y', zero },
		{ 'z', zero },
		{ 'w', zero },
	};
	std::vector<Expr> instructions;
	
	u8 varCtr = 0;

	auto parse_arg = [&](auto &str) {
		switch (str[0]) {
		case 'x':
		case 'y':
		case 'z':
		case 'w':
			return regs[str[0]];
		default:
			return expr(Num { std::stoi(str) });
		}
	};

	
	for (auto it = ins_begin; it != ins_end; it++) {
		auto &[ins, arg1, arg2] = split(*it);
		auto reg = arg1[0];

		std::cout << ins << " " << arg1 << " " << arg2 << std::endl;
		if (ins == "inp") {
			regs[reg] = expr(Var { ++varCtr });
		} else if (ins == "add") {
			regs[reg] = expr(Add { regs[reg], parse_arg(arg2) });
		} else if (ins == "mul") {
			regs[reg] = expr(Mul { regs[reg], parse_arg(arg2) });
		} else if (ins == "div") {
			regs[reg] = expr(Div { regs[reg], parse_arg(arg2) });
		} else if (ins == "mod") {
			regs[reg] = expr(Mod { regs[reg], parse_arg(arg2) });
		} else if (ins == "eql") {
			regs[reg] = expr(Eql { regs[reg], parse_arg(arg2) });
		} else {
			assert(false);
		}

		for (auto &c: std::string("xyzw")) {
			regs[c] = optimize(regs[c]);
			std::cout << c << ": " << regs[c] << std::endl;
		}
		getchar();
	}

	std::vector<i64> vars { 11 };
	
	// std::cout << "Before optimization:" << std::endl;
	// for (auto &c: std::string("xyzw")) {
	// 	std::cout << c << ": " << regs[c] << std::endl;
	// }

	// for (auto &c: std::string("xyzw")) {
	// 	std::cout << c
	// 			  << " evals to "
	// 			  << eval(vars, regs[c])
	// 			  << std::endl;
	// }

	std::cout << std::endl << "After optimization:" << std::endl;
	for (auto &c: std::string("xyzw")) {
		regs[c] = optimize(regs[c]);
		std::cout << c << ": " << regs[c] << std::endl;
	}
	
	// for (auto &c: std::string("xyzw")) {
	// 	std::cout << c
	// 			  << " evals to "
	// 			  << eval(vars, regs[c])
	// 			  << std::endl;
	// }

	return 0;
}
