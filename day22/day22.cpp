#include <iostream>
#include <algorithm>
#include <cmath>
#include <assert.h>
#include <vector>

struct Quad
{
public:
	int64_t x0, y0, z0, x1, y1, z1;

	Quad(int64_t x0, int64_t y0, int64_t z0, int64_t x1, int64_t y1, int64_t z1);

	void subtract(const Quad &other, std::vector<Quad> &result) const;
	int64_t size() const;
	bool contains(const Quad &other) const;
};

class QuadCollection
{
private:
	std::vector<Quad> fQuads;

public:
	QuadCollection();
	QuadCollection(Quad quad);
	QuadCollection(std::vector<Quad> quads);

	QuadCollection& operator +=(const Quad &quad);
	QuadCollection& operator -=(const Quad &quad);

	int64_t size() const;
};


/**
 * A one-dimensional "range" with start/end values. Provides a
 * function which can subtract one range from another. You can use
 * this as a basis for higher-dimensional AABB booleans.
 */
struct range {
	enum range_t { RANGE_IN, RANGE_OUT } type;
	int64_t start;
	int64_t end;

	range() { }

	range(range_t type, int64_t start, int64_t end)
		: type(type)
		, start(std::min(start, end))
		, end(std::max(start, end))
	{
	}

	bool isNegative() const {
		return start > end;
	}
	
	int subtract(const range &other, range result[3]) const {
		if (isNegative()) return 0;

		if (other.isNegative()) {
			result[1] = range { RANGE_IN, start, end };
			return 1;
		}
		
		int cnt = 0;
		if (other.end < start || end < other.start)
		{
			// Ranges don't overlap:
			// other: |---|
			// this :       |----|
			// OR:
			// other:         |---|
			// this : |----|
			result[0] = range { RANGE_IN, start, end };
			cnt = 1;
		}
		else if (other.start <= start && end <= other.end)
		{
			// Other range fully contains this range
			// other: |-------------|
			// this :       |----|
			result[0] = range { RANGE_OUT, start, end };
			cnt = 1;
		}
		else if (other.start <= start && other.end <= end)
		{
			// Other range partially overlaps this range
			// other: |--------|
			// this :       |-----|
			result[0] = range { RANGE_OUT, start, other.end };
			result[1] = range { RANGE_IN, other.end + 1, end };
			cnt = 2;
		}
		else if (start <= other.start && other.end <= end)
		{
			// Other range is fully contained in this range
			// other:     |----|
			// this :  |----------|
			result[0] = range { RANGE_IN, start, other.start - 1};
			result[1] = range { RANGE_OUT, other.start, other.end };
			result[2] = range { RANGE_IN, other.end + 1, end };
			cnt = 3;
		}
		else if (start <= other.start && end <= other.end)
		{
			// Other range partially overlaps this range
			// other:     |---------|
			// this :  |----------|
			result[0] = range { RANGE_IN, start, other.start - 1};
			result[1] = range { RANGE_OUT, other.start, end };
			cnt = 2;
		} else {
			assert(false);
			return 0;
		}

		if (cnt > 0 && result[0].isNegative()) {
			std::swap(result[0], result[1]);
			std::swap(result[1], result[2]);

			cnt--;
		}

		if (cnt > 1 && result[1].isNegative()) {
			std::swap(result[1], result[2]);

			cnt--;
		}

		if (cnt > 2 && result[2].isNegative()) {
			cnt--;
		}
		
		return cnt;
	}
};

Quad::Quad(int64_t x0, int64_t y0, int64_t z0, int64_t x1, int64_t y1, int64_t z1)
	: x0(x0), y0(y0), z0(z0), x1(x1), y1(y1), z1(z1) { }

void Quad::subtract(const Quad &other, std::vector<Quad> &result) const
{
	range xRanges[3];
	range yRanges[3];
	range zRanges[3];

	const auto IN = range::range_t::RANGE_IN;
	const auto OUT = range::range_t::RANGE_OUT;
	
	range myX(IN, x0, x1);
	range myY(IN, y0, y1);
	range myZ(IN, z0, z1);

	range otherX(OUT, other.x0, other.x1);
	range otherY(OUT, other.y0, other.y1);
	range otherZ(OUT, other.z0, other.z1);

	int xCnt = myX.subtract(otherX, xRanges);
	int yCnt = myY.subtract(otherY, yRanges);
	int zCnt = myZ.subtract(otherZ, zRanges);

	for (int xi = 0; xi < xCnt; xi++)
	for (int yi = 0; yi < yCnt; yi++)
	for (int zi = 0; zi < zCnt; zi++)
	{
		if (xRanges[xi].type == IN || yRanges[yi].type == IN || zRanges[zi].type == IN)
		{
			result.emplace_back(
				xRanges[xi].start, yRanges[yi].start, zRanges[zi].start,
				xRanges[xi].end, yRanges[yi].end, zRanges[zi].end);
		}
	}
}

QuadCollection::QuadCollection() { }

QuadCollection::QuadCollection(std::vector<Quad> quads)
	: fQuads(quads) { }


/**
 * Add a single quad to this quad collection, without overlap.
 *
 * The idea is that we subtract all the already existing quads in the
 * collection from the quad, then add whatevers left into the
 * collection.
 */
QuadCollection& QuadCollection::operator +=(const Quad &quad)
{
	for (size_t i = 0; i < fQuads.size(); i++) {
		if (quad.contains(fQuads[i])) {
			fQuads.erase(fQuads.begin() + i);
			i--;
		}
	}
	
	std::vector<Quad> diff1;
	std::vector<Quad> diff2;

	diff1.emplace_back(quad);

	for (const auto &q1 : fQuads) {
		for (const auto &q2 : diff1) {
			q2.subtract(q1, diff2);
		}

		diff1.swap(diff2);
		diff2.clear();
	}

	fQuads.insert(fQuads.end(), diff1.begin(), diff1.end());

	std::cout << "Size: " << fQuads.size() << std::endl;
	return *this;
}

QuadCollection& QuadCollection::operator -=(const Quad &quad)
{
	std::vector<Quad> newQuads;

	for (const auto &q: fQuads) {
		q.subtract(quad, newQuads);
	}

	fQuads.swap(newQuads);

	return *this;
}

int64_t Quad::size() const
{
	int64_t dx = x1 - x0 + 1;
	int64_t dy = y1 - y0 + 1;
	int64_t dz = z1 - z0 + 1;

	return dx * dy * dz;
}

bool Quad::contains(const Quad& other) const
{
	return x0 <= other.x0
		&& y0 <= other.y0
		&& z0 <= other.z0
		&& x1 >= other.x1
		&& y1 >= other.y1
		&& z1 >= other.z1;
}

int64_t QuadCollection::size() const
{
	int64_t total = 0;
	
	for (const auto &q: fQuads) {
		total += q.size();
	}

	return total;
}


int main(int argc, char **argv) {
	/*
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10

on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
	*/

	QuadCollection coll{};
	
	#include "test2cpp.txt"
	
	std::cout << coll.size() << std::endl;
	return 0;
}
