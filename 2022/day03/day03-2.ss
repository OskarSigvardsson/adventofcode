(library-directories '("../../scheme/" "../../scheme/thunderchez/"))
(import (advent)
		(srfi s1 lists)
		(srfi s113 sets)
		(srfi s128 comparators))

(define test-lines (file-lines "test.txt"))
(define input-lines (file-lines "input.txt"))

(define between?
  (lambda (min x max)
	(and (<= min x) (<= x max))))

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

(define comp (make-default-comparator))
(define make-set
  (lambda (l)
	(list->set comp l)))

(define part1
  (lambda (line)
	(let* ([len (string-length line)]
		   [half (/ len 2)])
	  (char-priority
	   (car (set->list
			 (set-intersection
			  (make-set (string->list (substring line 0 half)))
			  (make-set (string->list (substring line half len))))))))))

(define part2
  (lambda (lines)
	(let loop ([l lines] [acc '()])
	  (if (eq? l '()) (reverse acc)
		  (loop
		   (cdddr l)
		   (cons
			(car (set->list
				  (set-intersection
				   (make-set (map char-priority (string->list (car l))))
				   (make-set (map char-priority (string->list (cadr l))))
				   (make-set (map char-priority (string->list (caddr l)))))))
			acc))))))

(apply + (map part1 input-lines))
(apply + (part2 input-lines))

