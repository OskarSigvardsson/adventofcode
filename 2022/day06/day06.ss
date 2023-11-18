(library-directories '("../../scheme" "../../scheme/thunderchez"))

(import (advent)
        (srfi s1 lists))

(define test-input (car (file-lines "test.txt")))
(define real-input (car (file-lines "input.txt")))

(define all-distinct
  (lambda (l < =)
    (let ([sorted (sort < l)])
      (every (lambda (x) (not (= (car x) (cadr x))))
             (zip sorted (cdr sorted))))))

(define find-distinct
  (lambda (str c)
    (let loop ([i 0])
      (if (all-distinct (string->list (substring str i (+ i c))) char<? char=?)
          (+ i c)
          (loop (+ i 1))))))

(time (list
       (find-distinct test-input 4)
       (find-distinct real-input 4)
       (find-distinct test-input 14)
       (find-distinct real-input 14)))

(let ([x 3]
      [y 4])
  (+ x y))

(let loop ([i 0])
  (if (= i 10) 10
      (+ i (loop (+ i 1)))))


