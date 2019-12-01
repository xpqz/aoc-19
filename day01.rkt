#lang racket

;; Advent of Code 2019
;;
;; Day 1: The Tyranny of the Rocket Equation
;;
;; Stefan Kruger

(define data (map string->number (file->lines "data/input01.data")))

(define (fuel mass)
  (- (truncate (/ mass 3)) 2))

(define (total-fuel mass)
  (let loop ([m mass] [fuel-sum 0])
    (define f (fuel m))
    (cond [(<= f 0) fuel-sum]
          [else (loop f (+ fuel-sum f))])))

(printf "Part1: ~a\n" (apply + (map fuel data)))
(printf "Part2: ~a\n" (apply + (map total-fuel data)))
