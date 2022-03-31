

f label test l = do
 test' <- readFile test
 label' <- readFile label
 return $ map snd $ filter (\x -> fst x == l) (zip (lines label') (lines test'))
 

writeToFile label test l dst = do
 result <- f label test l 
 writeFile dst (unlines result)


substring n xs  = substr n 0 xs

substr n k xs | length (drop k xs) >= n = (take n (drop k xs)) : substr n (k + 1) (drop k xs)
         | otherwise = [take n (drop k xs)]
