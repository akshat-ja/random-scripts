##############################################################
# Filename: tcl_db_info.tcl
# Description: Display layer and cell information about a database.
# This script accepts two optional arguments:
# arg 0 --> layout filename
# arg 1 --> output filename
# Default filename argument values.
##############################################################

set layoutfilename "mylayout.gds"
set outputfilename "myoutput.txt"

# Print out the children of a given cell.
proc proc_cell_tree { L F {C ""} {Indent ""} } {
	if {$C == ""} {
		set C [$L topcell]
	}
	set B [$L bbox $C]
	if { [ check_cell_empty $L $C ] } {
		puts $F "$Indent--> $C\t$B -- Empty cell"
	} else {
		puts $F "$Indent--> $C\t$B"
	}
	append Indent "\t"
	foreach child [$L children $C] {
		proc_cell_tree $L $F $child $Indent
	}
}

# Check for empty cells.
proc check_cell_empty { L cell_name } {
	if { [ $L exists cell $cell_name ] } {
	# Check if cell contains at least one polygon, wire, or text.
	foreach layer [ $L layers ] {
		if { [ $L iterator count poly $cell_name $layer ] != 0 || \
			[ $L iterator count wire $cell_name $layer ] != 0 || \
			[ $L iterator count text $cell_name $layer ] != 0 } {
				return 0
		}
	}
	# If cell only contains a reference, check if reference is empty.
	if { [ $L iterator count ref $cell_name ] != 0 } {
		set ref_list [ $L iterator ref $cell_name range 0 end ]
		foreach ref $ref_list {
			set refname [ lindex [ split $ref ] 0 ]
			if { ![ check_cell_empty $L $refname ] } {
				return 0
				}
			}
		}
		return 1
	}
}

# Argument processing.
if {$argc == 0} {
	puts "$argv0: Default layout filename: $layoutfilename"
	puts "$argv0: Default output filename: $outputfilename"
} elseif {$argc == 1} {
	set layoutfilename [lindex $argv 0]
	puts "$argv0: Default output filename: $outputfilename"
} elseif {$argc == 2} {
	set layoutfilename [lindex $argv 0]
	set outputfilename [lindex $argv 1]
} else {
	puts "$argv0: Wrong number of arguments, $argc."
	puts "Usage: $argv0 [layout filename] [output filename]"
	puts "$argv0: Default layout filename: $layoutfilename"
	puts "$argv0: Default output filename: $outputfilename"
	exit
}
if { ![ file exists $layoutfilename] } {
	puts "$argv0: Database $layoutfilename does not exist"
	exit
}

# Open data file for writing.
set fileID [open $outputfilename w]

# Capture layout handle.
set mylayout [layout create $layoutfilename]

# Output layer and cell information to data file.
puts $fileID "This file displays layer and cell information about the [$mylayout file] database."
puts $fileID "\nLayers:"
foreach lay [lsort -integer [$mylayout layers]] {
	set layname [$mylayout layernames $lay]
	puts $fileID "--> $lay : $layname"
}
puts $fileID "\nCells:"

# Write out results to data file.
proc_cell_tree $mylayout $fileID

close $fileID
set fileID [open $outputfilename r]
read $fileID
close $fileID








