#lang racket

;; Advent of Code 2019
;;
;; Day 4: Secure Container
;;
;; https://adventofcode.com/2019/day/4
;;
;; By Stefan Kruger

(define data '(236491 713787))

(define (monotonic? ns)
  (let loop ([digits ns])
    (cond [(or (null? digits) (= 1 (length digits))) #t]
          [(char>? (first digits) (second digits)) #f]
          [else (loop (cdr digits))])))

(define (repeats? str allow-multiples)
  (define r (regexp-match* #px"(.)\\1+" str))
  (cond [(zero? (length r)) #f]
        [(for/or ([m (in-list r)]) (= 2 (string-length m)))]
        [else allow-multiples]))
  
(define (valid? num allow-multiples)
  (define number-string (number->string num))
  (cond [(not (monotonic? (string->list number-string))) #f]
        [else (repeats? number-string allow-multiples)]))

(define (count-valid data [allow-multiples #t])
  (for/sum ([i (in-range (first data) (second data))] #:when (valid? i allow-multiples)) 1))

(define (main)
  (printf "Part1: ~a\n" (count-valid data))
  (printf "Part2: ~a\n" (count-valid data #f)))

(main)