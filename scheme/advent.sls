#!r6rs

(library (advent)
  (export file-lines split-delim between?)
  (import (chezscheme))

  (define split-delim
	(lambda (delim list)
	  (let loop ([l list] [curr '()] [chunks '()])
		(cond
		 [(eq? l '()) (reverse (cons (reverse curr) chunks))]
		 [(equal? delim (car l))
		  (loop (cdr l) '() (cons (reverse curr) chunks))]
		 [else
		  (loop (cdr l) (cons (car l) curr) chunks)]))))

  (define file-lines
	(lambda (file)
	  (with-input-from-file file
		(lambda ()
		  (let loop ([acc '()])
			(let ([line (get-line (current-input-port))])
			  (if (eof-object? line) (reverse acc)
				  (loop (cons line acc)))))))))

  

  (define between?
	(lambda (min x max)
      (and (<= min x) (<= x max)))))

