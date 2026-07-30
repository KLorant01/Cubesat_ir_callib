#!/bin/bash

base=raw_block
s=20
n=0

TMP=/dev/shm

cat ${base}.txt | \
while read line; do
	A=($line)
	x=0
	y=0
	w=`printf "%.3d" $n`
	for ((p=0;p<192;p++)); do
		value=0x${A[2*p+0]}${A[2*p+1]}
		value=$((0x8000<=value ? value-65536 : value))
		echo $x $y $value
		x=$((x+1))
		if [ $x == 16 ]; then
			x=0
			y=$((y+1))
		fi
	done | \
	firandom -s 16,12 --input-sky - --col-pixel 1,2 --col-value 3 -o ${base}-n${w}-${s}.fits
	s=$((20+(s+1)%4))
	if [ $s == 20 ]; then

		convert -size 1x256 xc:grey ${TMP}/00.png

		fiinfo ${base}-n${w}-20.fits --pgm linear,min=-2000,max=1000 --output-pgm - | \
		pnmscale 16 | \
		pamflip -r270 > $TMP/20.pgm

		fiinfo ${base}-n${w}-21.fits --pgm linear,min=-2000,max=1000 --output-pgm - | \
		pnmscale 16 | \
		pamflip -r180 > $TMP/21.pgm

		fiinfo ${base}-n${w}-23.fits --pgm linear,min=-2000,max=1000 --output-pgm - | \
		pnmscale 16 | \
		pamflip -r270 > $TMP/23.pgm

		fiinfo ${base}-n${w}-22.fits --pgm linear,min=-2000,max=1000 --output-pgm - | \
		pnmscale 16 | \
		pamflip -r180 > $TMP/22.pgm

		montage ${TMP}/00.png ${TMP}/22.pgm ${TMP}/23.pgm ${TMP}/21.pgm ${TMP}/20.pgm ${TMP}/00.png -tile 6x1 -geometry +8+8 -background grey -limit thread 1 ${base}-n${w}.png

		n=$((n+1))

	fi

done
