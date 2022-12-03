(library-directories '("../../scheme/" "../../scheme/thunderchez/"))
(import (advent) (srfi s1 lists))

(define test-lines (file-lines "test.txt"))
(define input-lines (file-lines "input.txt"))

;; helper, is number between two other numbers
(define between?
  (lambda (min x max)
	(and (<= min x) (<= x max))))

;; char to priority 
(define char-priority
  (lambda (c)
	(let ([i (char->integer c)]
		  [A (char->integer #\A)]
		  [Z (char->integer #\Z)]
		  [a (char->integer #\a)]
		  [z (char->integer #\z)])
	  (cond
	   [(between? A i Z) (+ 27 (- i A))]
	   [(between? a i z) (+ 1 (- i a))]))))

;; splits a line into two compartments and returns a list of prios
(define compartment-split
  (lambda (s)
	(let* ([len (string-length s)]
		   [half (/ len 2)])
	  (list
	   (map char-priority (string->list (substring s 0 half)))
	   (map char-priority (string->list (substring s half len)))))))

;; remove duplicates from a list
(define remove-dupes
  (lambda (l)
	(let loop ([l (sort < l)] [acc '()])
	  (cond
	   [(eq? l '()) acc]
	   [(eq? (cdr l) '()) (cons (car l) acc)]
	   [(= (car l) (cadr l)) (loop (cdr l) acc)]
	   [else (loop (cdr l) (cons (car l) acc))]))))

;; loop through the lines, split into compartments, remove duplicates from the
;; compartments, then find the intersection of the two sets
(define prios-part1
  (lambda (lines)
	(map (lambda (s)
		   (car (lset-intersection =
								   (remove-dupes (car s))
								   (remove-dupes (cadr s)))))
		 (map compartment-split lines))))

;; print answer to test and input
(apply + (prios-part1 test-lines))
(apply + (prios-part1 input-lines))

;; map the lines to priorities
(define prio-lines
  (lambda (lines)
	(map (lambda (line) (map char-priority (string->list line))) lines)))

;; in chunks of three, remove the duplicates from each line and find intersection
(define prios-part2
  (lambda (lines)
	(let loop ([l (prio-lines lines)] [acc '()])
	  (if (eq? l '())
		  (reverse acc)
		  (let ([l1 (remove-dupes (car l))]
				[l2 (remove-dupes (cadr l))]
				[l3 (remove-dupes (caddr l))])
			(loop
			 (cdddr l)
			 (cons (car (lset-intersection = l1 l2 l3))
				   acc)))))))

;; print answer to test and input for part 2
(apply + (prios-part2 test-lines))
(apply + (prios-part2 input-lines))
