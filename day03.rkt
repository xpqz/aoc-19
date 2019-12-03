#lang racket

;; Advent of Code 2019
;;
;; Day 3: Crossed Wires
;;
;; Stefan Kruger

(define routes (map (curryr string-split ",") (file->lines "data/input03.data")))

(define (vector->set vect)
  (list->set (vector->list vect)))

(define (vector-last vect)
  (vector-ref vect (sub1 (vector-length vect))))

(define (cab-dist p)
  (+ (abs (car p)) (abs (cdr p))))

(define (visited-points x y point)
  (define dist (string->number (substring point 1)))
  (match (string-ref point 0)
    [#\U (for/vector ([d (in-range 1 (add1 dist))]) (cons x (+ y d)))]
    [#\D (for/vector ([d (in-range 1 (add1 dist))]) (cons x (- y d)))]
    [#\R (for/vector ([d (in-range 1 (add1 dist))]) (cons (+ x d) y))]
    [_   (for/vector ([d (in-range 1 (add1 dist))]) (cons (- x d) y))]))

(define (trace route)
  (for/fold ([points '#()] [x 0] [y 0] #:result points)
            ([point (in-list route)])
    (define new-points (visited-points x y point))
    (define end (vector-last new-points))
    (values (vector-append points new-points) (car end) (cdr end))))

(define (count-steps route point)
  (add1 (vector-member point (trace route))))  ;; Unnecessarily slow, but fast enough

(define (closest routes intersects)
  (for/fold ([mdist +inf.0])
            ([point (in-set intersects)])
    (define total (+ (count-steps (first routes) point) (count-steps (second routes) point)))
    (if (< total mdist) total mdist)))

(define (main)
  (define r1 (vector->set (trace (first routes))))
  (define r2 (vector->set (trace (second routes))))
  (printf "Part1: ~a\n" (cab-dist (argmin cab-dist (set->list (set-intersect r1 r2)))))
  (printf "Part2: ~a\n" (closest routes (set-intersect r1 r2))))

(main)