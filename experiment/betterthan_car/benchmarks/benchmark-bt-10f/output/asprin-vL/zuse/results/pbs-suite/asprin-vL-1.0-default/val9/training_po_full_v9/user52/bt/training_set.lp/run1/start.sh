#!/bin/bash
# http://www.cril.univ-artois.fr/~roussel/runsolver/

CAT="../../../../../../../../../../../../programs/gcat.sh"

cd "$(dirname $0)"

#top -n 1 -b > top.txt

[[ -e .finished ]] || $CAT "../../../../../../../../../../../../benchmarks/clasp/val9/training_po_full_v9/user52/bt/training_set.lp" | "../../../../../../../../../../../../programs/runsolver-3.4.0" \
	-M 20000 \
	-w runsolver.watcher \
	-o runsolver.solver \
	-W 300 \
	"../../../../../../../../../../../../programs/asprin-vL-1.0" --stats=1 --print_output_instances --min_element -t4 --forbid_diff

touch .finished
