set terminal png tiny size 800,800
set output "dot_plot_BS_natto_168.png"
set size 1,1
set grid
unset key
set border 15
set tics scale 0
set xlabel "ENA|AP011541|AP011541.2"
set ylabel "NC_000964.3"
set format "%.0f"
set mouse format "%.0f"
set mouse mouseformat "[%.0f, %.0f]"
set mouse clipboardformat "[%.0f, %.0f]"
set xrange [1:4105380]
set yrange [1:4215606]
set style line 1  lt 1 lw 3 pt 6 ps 1
set style line 2  lt 3 lw 3 pt 6 ps 1
set style line 3  lt 2 lw 3 pt 6 ps 1
plot \
 "dot_plot_BS_natto_168.fplot" title "FWD" w lp ls 1, \
 "dot_plot_BS_natto_168.rplot" title "REV" w lp ls 2
