;; (library-directories '("../../scheme/" "../../scheme/thunderchez/"))
(import (chezscheme)
        (advent)
        (srfi s115 regexp))

(define input
  (lambda (file)
    (map 
     (lambda (line)
       (let* ([match (regexp-matches
                      (rx bos ($ (+ digit)) "-" ($ (+ digit)) "," ($ (+ digit)) "-" ($ (+ digit)) eos)
                      line)])
         (define d
           (lambda (i)
             (string->number (regexp-match-submatch match i))))
         `( (,(d 1) . ,(d 2)) (,(d 3) . ,(d 4)))))
     (file-lines file))))

;; (input "test.txt")
;; (input "input.txt")

(define test-input (input "test.txt"))
(define real-input (input "input.txt"))

(define contained
  (lambda (ranges)
    (let ([r1 (car ranges)]
          [r2 (cadr ranges)])
      (or (and (between? (car r1) (car r2) (cdr r1))
               (between? (car r1) (cdr r2) (cdr r1)))
          (and (between? (car r2) (car r1) (cdr r2))
               (between? (car r2) (cdr r1) (cdr r2)))))))

(define overlap
  (lambda (ranges)
    (let ([r1 (car ranges)]
          [r2 (cadr ranges)])
      (not
       (or (< (cdr r1) (car r2))
           (< (cdr r2) (car r1)))))))

(define count
  (lambda (list)
    (fold-left (lambda (x y) (if y (+ x 1) x)) 0 list)))

(time (begin
        (display (count (map contained test-input))) (newline) 
        (display (count (map contained real-input))) (newline)
        (display (count (map overlap test-input))) (newline)
        (display (count (map overlap real-input))) (newline)))

