(library-directories '("../../scheme/" "../../scheme/thunderchez/"))

(import (chezscheme)
        (advent)
        (srfi s1 lists)
        (srfi s115 regexp))

(define enumerate (lambda (list)
      (let loop ([l list] [i 0] [acc '()])
        (if (null? l) (reverse acc)
            (loop (cdr l) (+ i 1) (cons (cons i (car l)) acc))))))

(define parse-line
  (lambda (line)
    (read (open-string-input-port
           (regexp-replace-all "," line " ")))))

(define 3<
  (lambda (a b)
    (cond
     [(= a b) 'equal]
     [(< a b) 'ordered]
     [else 'unordered])))

(define cmp
  (lambda (a b)
    (cond
     [(and (number? a) (number? b)) (3< a b)]
     [(number? a) (cmp (list a) b)]
     [(number? b) (cmp a (list b))]
     [(and (null? a) (null? b)) 'equal]
     [(null? a) 'ordered]
     [(null? b) 'unordered]
     [else
      (case (cmp (car a) (car b))
        ['equal (cmp (cdr a) (cdr b))]
        ['ordered 'ordered]
        ['unordered 'unordered])])))

(define cmp<
  (lambda (a b)
    (case (cmp a b)
      ['ordered #t]
      [else #f])))

(define part1
  (lambda (file)
    (let* ([lines (file-lines file)]
           [lines (map parse-line lines)]
           [chunks (split-delim (eof-object) lines)]
           [processed (map (lambda (p) (cmp (car p) (cadr p))) chunks)]
           [filtered (filter (lambda (p) (eq? (cdr p) 'ordered)) (enumerate processed))]
           [indexes (map (lambda (i) (+ 1 (car i))) filtered)])
      (fold-left + 0 indexes))))

(define part2
  (lambda (file)
    (let* ([lines (file-lines file)]
           [lines (filter (lambda (line) (not (string=? "" line))) lines)]
           [lines (cons "[[2]]" lines)]
           [lines (cons "[[6]]" lines)]
           [lines (map parse-line lines)]
           [sorted (sort cmp< lines)]
           [i2 (list-index (lambda (v) (equal? v '((2)))) sorted)]
           [i6 (list-index (lambda (v) (equal? v '((6)))) sorted)])
      (* (+ 1 i2) (+ 1 i6)))))

(part1 "test.txt")
(part1 "input.txt")
(part2 "test.txt")
(part2 "input.txt")
