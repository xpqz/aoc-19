⍝ Read the file, and for each line, find all words (i.e split on paranthesis)
⍝ We then transpose the matrix and destructure into two separate vectors, 
⍝ holding parents and direct descendants respectively

⎕IO←0
(a b) ← ↓⍉↑ '\w+' ⎕S '&' ¨ ⊃⎕NGET'data/input06.data'1 ⍝ The '&' means return the matching string

parents ← b ⍳ a                                       ⍝ parents gives the index into a of each item's parent.
path ← {3::⍵ ⋄ ⍵,∇⍵⊃parents}                          ⍝ 3::⍵ returns the arg in case of an INDEX ERROR

≢ ∊ path ¨ parents                                    ⍝ Part 1 - apply path to each of the parent array, enlist and count
{¯2+≢⍺(∪~∩)⍵}/path¨b⍳'YOU' 'SAN'                      ⍝ Part 2 - tally of union minus intersection, minus 2 (want edges, not nodes)