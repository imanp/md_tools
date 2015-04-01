#note should be run from the directory where the pdbs are in


set contents [glob State*.pdb];


set output_file "[open [lindex $argv 0] w]";

foreach item $contents {
    mol load pdb $item;
    set sel [atomselect top "(same residue as water within 5 of resid 230 to 235) and  x<90 and x>69 and y <51 and y>30  and z>55 and z<90"]

    set a [lsort -unique [$sel get resid]];
    set numOH [llength $a]
    puts $output_file $numOH
}

exit