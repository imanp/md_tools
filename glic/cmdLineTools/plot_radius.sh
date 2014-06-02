

#set term pdf enhanced color
#set output "./plot.pdf"

#set term postscript enhanced color
#set output "./plot.eps"

set term pdfcairo enhanced color
set output outfile

#set term pngcairo transparent font "Arial,24" size 1920,1080
#set output outfile

#set term canvas
#set output "./plot.html"

#set term svg
#set output "./plot.svg"

#set terminal aqua


set zrange [0:11]
set cbrange [1:11]
set cbtic 1,1,11
#set xrange [-70:30]
#set yrange [-70:30]
#number of frames
set xrange [0:1000]
set yrange [-55:55]
#set yrange [0:45]


set encoding  iso_8859_1
set title title
set xlabel "Time (ns)"
#set ylabel "z (\305)" offset -5,8.5
set ylabel "z (\305)"
set cblabel "Radius (\305)"
#set zlabel "Diameter (\305)"


set pm3d  map
set palette define (1 "gray", 1.5 "black", 2 "red", 2.5 "yellow", 3 "green",  3.5 "cyan", 4 "blue", 7 "white", 11 "purple")
#set palette define (1 "#000000", 1.5 "#9e9e9e", 2 "#568F84", 2.5 "#9BDEC7", 3 "#7C9B5F",  3.5 "#B8D197", 4 "#E3FFF3", 7 "white", 11 "purple")
#set palette define (1 "#878787", 1.5 "#000000", 2 "#2E4D46", 2.5 "#45736A", 3 "#66A397",  3.5 "#73ABA0", 4 "#73ABA0", 7 "white", 11 "purple")
unset colorbox
#set colorbox

#set multiplot

set tmargin 0
set bmargin 0
set rmargin 0
set lmargin 0

#set size 1,0.715
#set origin 0.0,0.0
set colorbox vertical user origin 0.9,0.125 size 0.02,0.71

splot infile matrix using ($1*0.5):($2-63):3 notitle
#splot "./output.dat" nonuniform matrix notitle
#splot "./output.dat"  matrix notitle
