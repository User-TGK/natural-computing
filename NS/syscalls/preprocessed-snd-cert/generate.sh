scores0=$(java -jar negsel2.jar -alphabet file://snd-cert.alpha -self snd-cert.train -n 7 -r $1 -c -k -l <preprocessedsnd-cert.3.normal.test)
scores1=$(java -jar negsel2.jar -alphabet file://snd-cert.alpha -self snd-cert.train -n 7 -r $1 -c -k -l <preprocessedsnd-cert.3.anomalous.test)

for score in $scores0; do
    echo "$score,0" >> tmp
done
for score in $scores1; do
    echo "$score,1" >> tmp
done

echo "predictions,labels" >> $2
sort -n tmp >> $2

rm tmp
