import qualified Data.List as L

op :: (Integer, Integer) -> String -> (Integer, Integer)
op (a, b) s =
  case ls of
    [True, True]  -> (a + 1, b + 1)
    [True, False] -> (a + 1, b)
    [False, True] -> (a, b + 1)
    _             -> (a, b)
  where
    has2s = any (\x -> length x == 2)
    has3s = any (\x -> length x == 3)
    ls = [has2s, has3s] <*> (pure . L.group . L.sort) s

countSame :: String -> String -> Int
countSame w1 w2 = length $ filter id $ zipWith (/=) w1 w2

main = do
  contents <- readFile "input.txt"
  let ls = lines contents
  let (c2, c3) = foldl op (0, 0) ls
  let p1 = c2 * c3
  print p1
  let (_, m1, m2) =
        minimum [(countSame w1 w2, w1, w2) | w1 <- ls, w2 <- ls, w1 /= w2]
  let p2 = map fst $ filter (uncurry (==)) $ zip m1 m2
  print p2
