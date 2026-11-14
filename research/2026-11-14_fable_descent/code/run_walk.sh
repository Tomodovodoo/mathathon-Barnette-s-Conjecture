#!/bin/bash
# Sampling campaign on random instances. Run from this folder in Git Bash.
# Usage: bash run_walk.sh OUT "MODELS" "SIZES" COUNT SEED STEPS BIAS [extra walk flags]
# Instances come from the generator of the conjectures folder (read only).
G=../../2026-11-14_opus_conjectures/code/gen.py
OUT=$1; MODELS=$2; SIZES=$3; COUNT=$4; SEED=$5; STEPS=$6; BIAS=$7; shift 7
for m in $MODELS; do for v in $SIZES; do
  echo "== $m V=$v graphs=$COUNT seed=$SEED steps=$STEPS bias=$BIAS $*" >> $OUT
  python $G $m $v $COUNT $SEED | ./walk.exe -R 2 -steps $STEPS -gap 3 -bias $BIAS -seed $SEED "$@" | cut -c1-12000 >> $OUT
done; done
