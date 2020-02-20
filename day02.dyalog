⍝ Advent of Code 2019, day 2, Dyalog APL
⍝ https://adventofcode.com/2019/day/2

⎕IO←0
DAY2 ← ⊢⌿⍎¨⎕CSV'data/input02.data'

Intcode←{
    ⍺←0                                               ⍝ Intcode interpreter. 
    (op p1 p2 p3) ← 4↑⍺↓⍵                             ⍝ Skip anything before ip (⍺) and take 4 cells
    op ∊ 1 2: (⍺+4)∇((op-1)⌷⍵[p1](+,×)⍵[p2])@p3 ⊢ ⍵   ⍝ Addition and multiplication
    op=99: ⍵[0]                                       ⍝ Exit
}

DAY2[1 2] ← 12 2
Intcode DAY2  ⍝ part 1: 10566835

Run←{19690720= Intcode ((⊃1↑⍵)@1 2) ⊢ ⍺: ⊃1↑⍵ ⋄ ⍺∇1↓⍵} ⍝ Set positions 1 and 2, and recurse over the list

(noun verb) ← DAY2 Run {,⍳⍵ ⍵} 100 
verb + 100 × noun ⍝ part 2: 2347