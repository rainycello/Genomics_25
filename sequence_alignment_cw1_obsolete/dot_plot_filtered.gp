set terminal png tiny size 800,800
set output "dot_plot_filtered.png"
set xtics rotate ( \
 "0" 1.0, \
 "1" 100000.0, \
 "" 200000 \
)
set ytics ( \
 "0" 1.0, \
 "1" 204655.0, \
 "" 376625 \
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
set xrange [1:200000]
set yrange [1:376625]
set style line 1  lt 1 lw 3 pt 6 ps 1
set style line 2  lt 3 lw 3 pt 6 ps 1
set style line 3  lt 2 lw 3 pt 6 ps 1
plot \
 "dot_plot_filtered.fplot" title "FWD" w lp ls 1, \
 "dot_plot_filtered.rplot" title "REV" w lp ls 2
