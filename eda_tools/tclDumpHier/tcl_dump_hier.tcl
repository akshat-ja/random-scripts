##############################################################
# PROC: dump_hier
# L = layout object name
# F = file to dump hierarchy to
# C = cell to start dumping from, "" means use topcell
# Indent = string used to format the hierarchy
##############################################################

##############################################################
puts -nonewline "Please enter your DATA.gds : "
flush stdout
set argv [split [gets stdin] { }]
##############################################################

set DATA  [ lindex $argv 0 ]

proc dump_hier { T L F {C ""} {Indent ""} } {
	if {$C == ""} {
		set C [$L topcell]
	}

#	old way with bbox
#	set B [$L bbox $C]
#	puts $F "$Indent-> $C $B"

#	new way with iterator
	set details [$L iterator ref $T range 0 0 -depth 0 20 -filterCell $C]
	puts $F "$Indent--> $details"

	append Indent "\t"
	foreach child [$L children $C] {
		dump_hier $T $L $F $child $Indent
	}
}

##############################################################
# Run everything
##############################################################

set fileID [open dump_hier.txt w]
#
# Step 1: open the layout
#
set layout [layout create $DATA]
set topcell [$layout topcell]
#
# Step 2: write the hierarchy to the file
#
dump_hier $topcell $layout $fileID
#
# Step 3: Close (and save the file)
#
close $fileID
