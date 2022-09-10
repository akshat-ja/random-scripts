##############################################################
# PROC: label_extract
# 
##############################################################

if { $argc != 1 } {
	puts "Usage:"
	puts "calibredrv tclLabelExtract.tcl input_gds"
} else {
	set N [lindex $argv 0]
	set Lin [layout create $N -dt_expand -preservePaths -preserveProperties]
	
	set root [ file rootname [lindex $argv 0] ]
	append Loutf $root _labels_only.gds
	
	#set Lout [layout create $Loutf -dt_expand -preservePaths -preserveProperties]
	set Ltop [$Lin topcell]
	
	$Lin flatten cell $Ltop -withDelete
	
	puts "***************** Output file *****************"
	puts $Loutf
	puts "***********************************************"
	
	$Lin gdsout $Loutf -noEmptyCells noRefs -map 10151.0 10151 0
}
