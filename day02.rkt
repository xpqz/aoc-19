#lang racket

;; Advent of Code 2019
;;
;; Day 2: 1202 Program Alarm
;;
;; Stefan Kruger

(define data (stream->list (map string->number (string-split
                                                (first (file->lines "data/input02.data")) ","))))

(define (opcode! state i1 i2 out fn)
  (vector-set! state out (fn (vector-ref state i1) (vector-ref state i2))))

(define (run data noun verb)
  (define st (list->vector data))
  (vector-set! st 1 noun)
  (vector-set! st 2 verb)
  (for/or ([instr (in-slice 4 st)])
    (match instr
      [`(1 ,in1 ,in2 ,out) (opcode! st in1 in2 out +) #f]
      [`(2 ,in1 ,in2 ,out) (opcode! st in1 in2 out *) #f]
      [_ (vector-ref st 0)])))

(printf "Part1: ~a\n" (run data 12 2))
(printf "Part2: ~a\n"
        (for*/first ([noun (in-range 100)]
                     [verb (in-range 100)] #:when (= (run data noun verb) 19690720))
          (+ (* 100 noun) verb)))