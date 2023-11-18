(library-directories '("../../scheme/" "../../scheme/thunderchez/"))

(import (chezscheme)
        (advent)
        (srfi s1 lists)
        (srfi s115 regexp))

(define parse-line
  (lambda (line)
    (reverse
     (regexp-fold '(+ (or "-" num))
                  (lambda (i m str acc)
                    (cons (string->number (regexp-match-submatch m 0)) acc))
                  '()
                  line))))

(define markers
  (lambda (y sx sy bx by)
    (let* ([d (+ (abs (- sx bx)) (abs (- sy by)))]
           [dy (abs (- sy y))])
      d)))

(markers 0 8 7 2 10)

(parse-line (car (file-lines "test.txt")))

;; (define range-union
;;   (lambda (a b)
;;     (let ([mina (car a)]
;;           [maxa (cdr a)]
;;           [minb (car b)]
;;           [maxb (cdr b)])
;;       (if (or (< maxa minb)
;;               (< maxb mina))
;;           (list a b)
;;           (list (cons (min mina minb) (max maxa maxb)))))))

;; (define add-range
;;   (lambda (l r)
;;     (let loop ([l l]))))

;; (range-union '(1 . 2) '(3 . 4))
