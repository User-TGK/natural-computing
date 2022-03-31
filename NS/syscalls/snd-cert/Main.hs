import System.Environment

f label test l = do
 test' <- readFile test
 label' <- readFile label
 return $ map snd $ filter (\x -> fst x == l) (zip (lines label') (lines test'))

writeToFile label test l dst = do
 result <- f label test l 
 writeFile dst (unlines result)

main = do
 args <- getArgs
 case args of
   (label:test:l:dst:[]) -> writeToFile label test l dst
   _ -> putStrLn "Expecting [Filepath] [Filepath] [\"1\" | \"0\"] [Filepath]"
