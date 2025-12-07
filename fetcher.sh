#!/bin/bash


YEAR=$1
DAY=$2
DAY_PAD=$(printf "%02d" "$DAY")

mkdir -p "$YEAR/day$DAY_PAD/"
mkdir -p "$YEAR/inputs/"

curl "https://adventofcode.com/$YEAR/day/$DAY/input" -H "Cookie: session=$ADVENT_COOKIE" > "$YEAR/inputs/day$DAY_PAD-real.txt"

