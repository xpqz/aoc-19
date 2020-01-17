/ Advent of Code, 2019, day 1
/ 
/ Explanation of solution: 1_*++/\+1_0|(-2+3/)\`i$0:"data/01"
/ 
/ From https://github.com/chrispsn/aoc2019/blob/master/01.k
/

/ Read a list of numbers as a string, and coerce to ints

d:`i$0:"data/01"

/ Scan over the list, applying max(0, div(x, 3) - 2) repeatedly
/ to each element, preserving all intermediate results -> list of lists.
/ Drop first element, as the start state

e:1_0|(-2+3/)\d

/ If we flip this matrix, each row represents the fuel requirements per
/ component - col 0 is fuel for the load, col 1 is fuel for the fuel for
/ the load etc. shakti-k transpose is monadic +:

m:+e

/ Part 1 is simply the sum of col 0: *+/m but for part 2 we need
/ the sum of all of those, so we need to keep the list around whilst 
/ preserving the result. we now apply the list sum as a scan over each 
/ element. +/\ applies +/ over and over until the result stops changing, 
/ but preserves a list of the intermediate results. 
/
/ Demonstrating the difference between +/ and +/\:
/
/  +/(1 2 3 4;5 6 7 8;9 10 11 12)   / column sums
/ 15 18 21 24
/ 
/  +/\(1 2 3 4;5 6 7 8;9 10 11 12)  / sum re-reduce
/ (1 2 3 4;5 6 7 8;9 10 11 12)      / original state
/ 15 18 21 24                       / reduce once - +/l which is column sums
/ 78                                / reduce again, sum of sums, giving an atom

s:+/\m

/ Our results could now be found as (s[1;0];s[2]) -- first element of second 
/ row and the (single) element of the last row. but we can simplify this a 
/ bit more. we have an irregular matrix - we transpose again and shakti's 
/ flip verb will pad out the shorter rows with atoms from the lower rows

t:+s

/ Our two solutions are now elements 1 and 2 of the first row. The monadic *
/ takes the head of a list

1_*t  / or could also have used 1_t@0

