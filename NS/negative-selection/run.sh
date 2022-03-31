echo "english.test"
java -jar negsel2.jar -self english.train -n 10 -r 4 -c -l < english.test | awk '{n+=$1}END{print n/NR}'
echo "tagalog.test"
java -jar negsel2.jar -self english.train -n 10 -r 4 -c -l < tagalog.test | awk '{n+=$1}END{print n/NR}'
echo "hiligaynon.txt"
java -jar negsel2.jar -self english.train -n 10 -r 4 -c -l < lang/hiligaynon.txt | awk '{n+=$1}END{print n/NR}'
echo "middle-english.txt"
java -jar negsel2.jar -self english.train -n 10 -r 4 -c -l < lang/middle-english.txt | awk '{n+=$1}END{print n/NR}'
echo "plautdietch.txt"
java -jar negsel2.jar -self english.train -n 10 -r 4 -c -l < lang/plautdietsch.txt | awk '{n+=$1}END{print n/NR}'
echo "xhosa.txt"
java -jar negsel2.jar -self english.train -n 10 -r 4 -c -l < lang/xhosa.txt | awk '{n+=$1}END{print n/NR}'
