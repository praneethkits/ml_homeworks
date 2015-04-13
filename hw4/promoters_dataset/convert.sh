set -x

if [ $# -ne 1 ]; then
    echo "USAGE: $0 <input file>"
    exit 2
fi

i=56
while [ $i -ge 0 ]
do
    k=$(($i+1))
    sed -i "s/ $i:/ $k:/g" $1
    i=$(($i-1))
done
