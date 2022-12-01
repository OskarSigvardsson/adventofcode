(define elves
  (lambda (file)
	(with-input-from-file file
	  (lambda ()
		(let loop ([curr 0] [elves '()])
		  (let ([line (get-line (current-input-port))])
			(cond
			 [(eof-object? line) (cons curr elves)]
			 [(string=? "" line) (loop 0 (cons curr elves))]
			 [else (loop (+ curr (string->number line)) elves)])))))))

;; part 1
(apply max (elves "test.txt"))
(apply max (elves "input.txt"))

;; part 2
(let ([sorted (sort > (elves "test.txt"))])
  (+ (car sorted) (cadr sorted) (caddr sorted)))

(let ([sorted (sort > (elves "input.txt"))])
  (+ (car sorted) (cadr sorted) (caddr sorted)))
