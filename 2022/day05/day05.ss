(library-directories '("../../scheme" "../../scheme/thunderchez"))

(import (advent)
        (srfi s115 regexp)
        (srfi s1 lists))

(define set-index
  (lambda (l i v)
    (map-index l i (lambda (_) v))))

(define map-index
  (lambda (l i f)
    (let loop ([i i] [l l] [acc '()])
      (if (= i 0) (append (reverse acc) `(,(f (car l))) (cdr l))
          (loop (- i 1) (cdr l) (cons (car l) acc))))))

(define parse-line
  (lambda (line)
    (let* ([re (rx "move " ($ (+ digit)) " from " ($ (+ digit)) " to " ($ (+ digit)))]
           [m (regexp-matches re line)]
           [l (cdr (regexp-match->list m))]
           [ds (map string->number l)])
      (values (car ds) (- (cadr ds) 1) (- (caddr ds) 1)))))

(define move-stacks
  (case-lambda
   [(stacks from to)
    (let* ([stack-from (list-ref stacks from)]
           [v (car stack-from)]
           [sr (set-index stacks from (cdr stack-from))]
           [sa (set-index sr to (cons v (list-ref sr to)))])
      sa)]
   [(stacks count from to)
    (fold (lambda (_ stacks)
            (move-stacks stacks from to))
          stacks
          (iota count))]))

(define move-stacks-p2
  (lambda (stacks count from to)
    (let* ([stack-from (list-ref stacks from)]
           [stack-to (list-ref stacks to)]
           [vs (take stack-from count)]
           [stack-from (drop stack-from count)]
           [stack-to (append vs stack-to)]
           [stacks (set-index stacks from stack-from)]
           [stacks (set-index stacks to stack-to)])
      stacks)))

(define run
  (lambda (lines move-stacks)
    (define push-stacks
      (lambda (stacks stack-count str)
        (let loop ([i 0] [stacks stacks])
          (if (= i stack-count) stacks
              (let ([c (string-ref str (+ 1 (* i 4)))])
                (if (char=? c #\ ) (loop (+ i 1) stacks)
                    (loop
                     (+ i 1)
                     (map-index stacks i (lambda (v) (cons c v))))))))))

    (let* ([si (list-index (lambda (line) (string=? "" line)) lines)]
           [p1 (reverse (take lines (- si 1)))]
           [p2 (drop lines (+ 1 si))]
           [stack-count (/ (+ 1 (string-length (car p1))) 4)]
           [stacks (map (lambda (_) '()) (iota stack-count))]
           [stacks
            (let loop ([in p1] [stacks stacks])
              (if (eq? in '()) stacks
                  (loop (cdr in) (push-stacks stacks stack-count (car in)))))]
           [stacks 
            (fold (lambda (line stacks)
                    (let-values ([(count from to) (parse-line line)])
                      (move-stacks stacks count from to)))
                  stacks p2)]
           [tops (map car stacks)])
      (list->string tops))))


(define test-input (file-lines "test.txt"))
(define real-input (file-lines "input.txt"))

(time (list
       (run test-input move-stacks)
       (run test-input move-stacks-p2)
       (run real-input move-stacks)
       (run real-input move-stacks-p2)))
