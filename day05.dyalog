⎕IO←0
DAY5 ← ⊢⌿⍎¨⎕CSV'data/input05.data'

Intcode←{
    ⍝ intcode interpreter. Call as: 0 intcode code
    state ←⍵
    ev ← {⍺=0: state[⍵] ⋄ ⍵}               ⍝ Position or immediate mode
    op p1 p2 p3 ← 4↑⍺↓⍵                    ⍝ Skip anything before and take 4 cells
    params ← 4 4 2 2 3 3 4 4 1             ⍝ Number of parameters by opcode
    ops ← (1+⍳8), 99                       ⍝ Valid opcodes
    m3 m2 m1 o2 o1 ← (5⍴10) ⊤ op           ⍝ Unpack the param modes
    op ← 10 ⊥ o2 o1                        ⍝ Repack the opcode, to go from (say) 1001 to 1
    count ← params[ops⍳op]                 ⍝ Number of params
    parmod ← m1 m2 m3 ,⍪ p1 p2 p3          ⍝ Table combining modes and params
    d1 d2 d3 ← 3↑ev/(¯1+count)↑parmod      ⍝ Pick relevant number of params, and apply modes
    ip ← ⍺+count                           ⍝ Advance ip by the width of current instr
    op ∊ 1 2: ip∇((op-1)⌷d1(+,×)d2)@p3 ⊢ ⍵ ⍝ Addition and multiplicatin
    op=3: ip∇input@p1⊢⍵                    ⍝ Input
    op=4: d1,ip∇⍵                          ⍝ Output
    op∊5 6: ⍵∇⍨ip d2⌷⍨(op-5)⌷d1(≠,=)0      ⍝ Jumps 
    op∊7 8: ip∇((op-7)⌷d1(<,=)d2)@p3 ⊢ ⍵   ⍝ Comparison < or =
    op=99: ⍬                               ⍝ Exit
}

input←1 ⋄ ¯1↑0 Intcode DAY5 ⍝ part 1
input ← 5 ⋄ 0 Intcode DAY5 ⍝ part 2