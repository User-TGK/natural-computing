scores0=$(java -jar negsel2.jar -alphabet file://english.train -self english.train -n 10 -r $1 -c -l <english.test)
scores1=$(java -jar negsel2.jar -alphabet file://english.train -self english.train -n 10 -r $1 -c -l <tagalog.test)

for score in $scores0; do
    echo "$score,0" >> tmp
done
for score in $scores1; do
    echo "$score,1" >> tmp
done

echo "predictions,labels" >> $2
sort -n tmp >> $2

rm tmp
