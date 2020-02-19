⍝ Advent of Code 2019, day 3, Dyalog APL
⍝ https://adventofcode.com/2019/day/3

⎕IO←0
data ← 1(↑,∘⍎↓)¨ ⎕CSV'data/input03.data' ⍝ Convert each string a letter and a number.

o ← 4 2 ⍴ 0 1 0 ¯1 1 0 ¯1 0
dir ← 'U' 'D' 'R' 'L'

follow←{  ⍝ follow path ⍵, accumulate list of coordinate pairs visited
    0=≢⍵:⍺
    d s←⊃⍵
    seq←,⌿o[dir⍳d;]∘.×1+⍳s
    origin←(≢seq) ⍴ ⊂¯2↑∊⍺
    ⍺,∊(seq+origin)∇1↓⍵
}

intersects←{∪(↓(≢⍺) 2⍴⍺)∩↓(≢⍵) 2⍴⍵}
a←0 0 follow data[0;] ⋄ b←0 0 follow data[1;]

⍝ part 1 - find intersection with smallest manhattan distance
⍝ from origin
⌊/(+/|)¨1↓a intersects b 