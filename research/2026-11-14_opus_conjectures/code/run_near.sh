#!/bin/bash
# usage: bash run_near.sh OUTFILE "models" "sizes" count roots seed maxd
out=$1; models=$2; sizes=$3; count=$4; roots=$5; seed=$6; maxd=$7
for m in $models; do for V in $sizes; do
  python gen.py $m $V $count $seed > _g_$seed.txt
  echo "== model=$m V=$V graphs=$count roots_per_graph=$roots seed=$seed" >> $out
  ./bar2.exe -t -N $maxd -r $roots -s $seed -d ../data/near_flags_${m}_${V}_${seed}.txt < _g_$seed.txt | grep -E "SUMMARY|NEAR" >> $out
done; done
rm -f _g_$seed.txt
