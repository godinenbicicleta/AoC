import qualified Data.Set as Set

parse :: String -> Integer
parse x = y * s
  where
    y = read (tail x) :: Integer
    s =
      if head x == '-'
        then -1
        else 1

findDup :: [Integer] -> Integer
findDup nums = findDup' nums Set.empty

findDup' :: [Integer] -> Set.Set Integer -> Integer
findDup' (x:xs) acc
  | x `Set.member` acc = x
  | otherwise = findDup' xs (Set.insert x acc)

main :: IO ()
main = do
  contents <- readFile "input.txt"
  let nums = (map parse . lines) contents
  let p1 = sum nums
  let p2 = (findDup . scanl1 (+) . concat . repeat) nums
  print p1
  print p2
