set terminal png tiny size 800,800
set output "final_short.png"
set xtics rotate ( \
 "0" 1, \
 "1" 229266, \
 "" 414184 \
)
set ytics ( \
 "NODE_1_length_99993_cov_9.395322" 1, \
 "NODE_2_length_99979_cov_9.515585" 99993, \
 "" 199972 \
)
set size 1,1
set grid
unset key
set border 0
set tics scale 0
set xlabel "REF"
set ylabel "QRY"
set format "%.0f"
set mouse format "%.0f"
set mouse mouseformat "[%.0f, %.0f]"
set mouse clipboardformat "[%.0f, %.0f]"
set xrange [1:414184]
set yrange [1:199972]
set style line 1  lt 1 lw 3 pt 6 ps 1
set style line 2  lt 3 lw 3 pt 6 ps 1
set style line 3  lt 2 lw 3 pt 6 ps 1
plot \
 "final_short.fplot" title "FWD" w lp ls 1, \
 "final_short.rplot" title "REV" w lp ls 2
