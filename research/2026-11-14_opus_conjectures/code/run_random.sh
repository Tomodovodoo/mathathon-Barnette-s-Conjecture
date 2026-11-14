#!/bin/bash
# usage: bash run_random.sh OUTFILE "models" "sizes" count roots seed
out=$1; models=$2; sizes=$3; count=$4; roots=$5; seed=$6
for m in $models; do for V in $sizes; do
  python gen.py $m $V $count $seed > _g.txt
  echo "== model=$m V=$V graphs=$count roots_per_graph=$roots seed=$seed" >> $out
  ./bar2.exe -t -m full -S -r $roots -cap 200000 -s $seed -d ../data/rand_flags_${m}_${V}_${seed}.txt < _g.txt | grep -E "SUMMARY|C1 |STRUCT|TM by" >> $out
done; done
rm -f _g.txt
