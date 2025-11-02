set terminal png tiny size 800,800
set output "dot_plot_reps_2.png"
set xtics rotate ( \
 "0" 1, \
 "1" 208024, \
 "" 404031 \
)
set ytics ( \
 "0" 1, \
 "1" 208024, \
 "" 404031 \
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
set xrange [1:404031]
set yrange [1:404031]
set style line 1  lt 1 lw 3 pt 6 ps 1
set style line 2  lt 3 lw 3 pt 6 ps 1
set style line 3  lt 2 lw 3 pt 6 ps 1
plot \
 "dot_plot_reps_2.fplot" title "FWD" w lp ls 1, \
 "dot_plot_reps_2.rplot" title "REV" w lp ls 2
