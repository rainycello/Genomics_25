set terminal png small
set output "compare_genomes.png"
set xtics rotate ( \
 "0" 1.0, \
 "1" 194656.0, \
 "" 373964 \
)
set ytics ( \
 "0" 1.0, \
 "1" 265243.0, \
 "" 512639 \
)
set size 1,1
set grid
set nokey
set border 0
set tics scale 0
set xlabel "REF"
set ylabel "QRY"
set format "%.0f"
set xrange [1:373964]
set yrange [1:512639]
set linestyle 1  lt 1 lw 3 pt 6 ps 1
set linestyle 2  lt 3 lw 3 pt 6 ps 1
set linestyle 3  lt 2 lw 3 pt 6 ps 1
plot \
 "compare_genomes.fplot" title "FWD" w lp ls 1, \
 "compare_genomes.rplot" title "REV" w lp ls 2
