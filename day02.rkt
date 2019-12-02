#lang racket

;; Advent of Code 2019
;;
;; Day 2: 1202 Program Alarm
;;
;; Stefan Kruger

(define data (stream->list (map string->number (string-split
                                                (first (file->lines "data/input02.data")) ","))))

(define (opcode state i1 i2 out fn)
  (vector-set! state out (fn (vector-ref state i1) (vector-ref state i2)))
  state)

(define (instr ip state)
  (cond [(>= ip (- (vector-length state) 4)) (vector->list state)]
        [else (list (vector-ref state ip) (vector-ref state (+ ip 1))
                    (vector-ref state (+ ip 2)) (vector-ref state (+ ip 3)))]))

(define (run data target noun verb)
  (define st (list->vector data))
  (vector-set! st 1 noun)
  (vector-set! st 2 verb)
  (let loop ([ip 0] [state st])
    (cond [(and (> target 0) (> (vector-ref state 0) target)) (vector-ref state 0)]
          [else
           (match (instr ip state)
             [(list 1 in1 in2 out) (loop (+ ip 4) (opcode state in1 in2 out +))]
             [(list 2 in1 in2 out) (loop (+ ip 4) (opcode state in1 in2 out *))]
             [_ (vector-ref state 0)])])))
             

(printf "Part1: ~a\n" (run data -1 12 2))
(printf "Part2: ~a\n"
        (for*/first ([noun (in-range 100)]
                     [verb (in-range 100)] #:when (= (run data 19690720 noun verb) 19690720))
          (+ (* 100 noun) verb)))

