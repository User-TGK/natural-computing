import Data.List

f label test l = do
 test' <- readFile test
 label' <- readFile label
 return $ map snd $ filter (\x -> fst x == l) (zip (lines label') (lines test'))
 

writeToFile label test l dst = do
 result <- f label test l 
 writeFile dst (unlines result)


preprocessed fp n = do
 file <- readFile fp
 writeFile ("preprocessed"++fp) (unlines $ concatMap (substring n) $ lines file)

preprocessed' fp = do
 file <- readFile fp
 let n' = head $ sort (map length (lines file))
 writeFile ("preprocessed"++fp) (unlines $ concatMap (substring n') $ lines file)

substring n xs  = substr n 0 xs

substr n k xs | length (drop k xs) >= n = (take n (drop k xs)) : substr n (k + 1) (drop k xs)
         | otherwise = []
