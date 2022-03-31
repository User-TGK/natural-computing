

f label test l = do
 test' <- readFile test
 label' <- readFile label
 return $ map snd $ filter (\x -> fst x == l) (zip (lines label') (lines test'))
 

writeToFile label test l dst = do
 result <- f label test l 
 writeFile dst (unlines result)
