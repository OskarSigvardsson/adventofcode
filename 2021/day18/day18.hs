-- import System.IO
import Data.List

data Node = Value Int | Tree Node Node

showNode :: Node -> String
showNode (Value x) = show x
showNode (Tree n1 n2) = "[" ++ showNode n1 ++ "," ++ showNode n2 ++ "]"

instance Show Node where
  show = showNode

-- test :: String -> Maybe Int
-- test "one" = Just 1
-- test "two" = Just 2
-- test _ = Nothing

-- test2 :: [String] -> [Maybe Int]
-- test2 :: [String] -> Maybe Int
-- test2 list = fmap (map test list)


-- test4 :: [String] -> Maybe Int
-- test4 [s1, s2, "+"] = do
--   v1 <- test s1
--   v2 <- test s2
--   Just (v1 + v2)
-- test4 _ = Nothing
  
  
-- main = do
--   line <- getLine
--   print $ test line

readChar :: Char -> String -> Maybe String
readChar c1 [] = Nothing
readChar c1 (c2 : rest) = if c1 == c2 then Just rest else Nothing


readDigit :: String -> Maybe Int
readDigit (x:xs) = elemIndex x "0123456789"


parse :: String -> Maybe (String, Node)
parse ('0' : xs1) = Just (xs1, Value 0)
parse ('[' : xs1) = do
  (xs2, n1) <- parse xs1
  xs3       <- readChar ',' xs2
  (xs4, n2) <- parse xs3
  xs5       <- readChar ']' xs4
  Just (xs5, Tree n1 n2)


parse _ = Nothing

-- main :: IO ()
-- main = do
--   file <- openFile "input.txt" ReadMode
--   contents <- hGetContents file
--   putStr contents

