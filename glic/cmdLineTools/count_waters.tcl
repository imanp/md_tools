if { $argc  !=4 } {
 puts "USAGE: vmd -dispdev text -e count_waters.tcl my.gro my.xtc output.dat"
 exit

}
mol load gro "[lindex $argv 0]" xtc "[lindex $argv 1]";

set output_file "[open [lindex $argv 2] w]";
set nf [molinfo top get numframes];

set sel [atomselect top "(same residue as water within 5 of resid 230 to 233) and  x<90 and x>69 and y <51 and y>30  and z>55 and z<90"]


set avg 10
set index 0
set numOH 0


for {set frame 0} {$frame < $nf} {incr frame} {

        $sel frame $frame ;
        $sel update;
        set a [lsort -unique [$sel get resid]];

        #set numOH [expr {$numOH + [llength $a]}]
        set numOH [llength $a]
        incr index
        puts $output_file $numOH
        #averaging each 10th datapoint

}

exit

