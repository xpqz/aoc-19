day1 ← ⍎¨ ⊃ ⎕NGET 'data/input01.data' 1
fuel ← {0⌈¯2+⌊⍵÷3}
+/ fuel day1 ⍝ Day 1, part 1
+/ {⍵=0:0 ⋄ (fuel ⍵) + ∇ fuel ⍵} ¨ day1 ⍝ Day1, part 2
