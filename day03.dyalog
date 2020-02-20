⍝ Advent of Code 2019, day 3, Dyalog APL
⍝ https://adventofcode.com/2019/day/3

⎕IO←0
DAY3 ← 1(↑,∘⍎↓)¨ ⎕CSV'data/input03.data' ⍝ Convert each string to a letter and a number.
OFFSETS ← 4 2 ⍴ 0 1 0 ¯1 1 0 ¯1 0
DIRS ← 'U' 'D' 'R' 'L'

Pairs←{↓(2÷⍨≢⍵) 2⍴⍵} 

Follow←{                                 ⍝ Follow path ⍵, accumulate list of coord pairs visited
    0=≢⍵: ⍺                              ⍝ Quit if ⍵ is empty, and return accumulator ⍺
    (dir steps)←⊃⍵                       ⍝ Dir of travel, and number of steps, e.g. 'R' 200
    seq←,⌿OFFSETS[DIRS⍳dir;]∘.×1+⍳steps  ⍝ Expand out the steps into a vector
    origin←(≢seq) ⍴ ⊂¯2↑∊⍺               ⍝ Vector as long as seq; elem is the last pos we got to 
    ⍺,∊(seq+origin)∇1↓⍵                  ⍝ Sum the two vectors and append, then recurse on tail
}

path1←Pairs 0 0 Follow DAY3[0;] ⋄ path2←Pairs 0 0 Follow DAY3[1;]

crossings←1↓path1 {∪⍺∩⍵} path2           ⍝ Find intersections; drop the start point which is shared.
⌊/ (+/|) ¨ crossings                     ⍝ Part 1. Minimise Manhattan distance = sum of absolute values
⌊/+/(path1⍳crossings),⍪path2⍳crossings   ⍝ Part 2: Find intersect with smallest sum steps 
