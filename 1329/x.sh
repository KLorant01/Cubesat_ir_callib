#!/bin/bash

for u in 0 1; do

xxd -g 1 ir2$((2*u))x.b | \
awk -v n=0 -v u=$u -v l=0 \
'BEGIN \
 {	if ( u==1 )
	 {	printf("\n\n");
	 }
 } \
 {	for ( i=0; i<16; i++ )
	 {	if ( 8<=n && n<392 ) 		printf("%s ",$(2+i));
		else if ( 488<=n && n<872 ) 	printf("%s ",$(2+i));
		n++;
		if ( n==392 || n==872 )
		 {	printf("\n");
			l++;
			if ( l==2 )
			 {	l=0;
				printf("\n\n");
			 }
		 }
		if ( n==968 )
			n=0;
	 }
}' | tee raw_block_$((2*u))$((2*u+1)).txt

done

paste raw_block_01.txt raw_block_23.txt > raw_block.txt
