##############################################################
# PROC: change_dbu
# 
##############################################################

if { $argc != 2 } {
		puts "Usage:"
		puts "calibredrv tclChangeDBU.tcl input_gds new_dbu_nm"
} else {
		# Import input gds
		set Output [layout create [lindex $argv 0] -dt_expand -preservePaths -preserveProperties]
		set Dbu [expr [lindex $argv 1] ]
		$Output units database [ expr 1e-9*$Dbu ]
		
		$Output scale [expr 1.0/$Dbu]
		
		# Export file
		puts "***************** New filename ****************"
		
		set root [ file rootname [lindex $argv 0] ]
		append fileout0 $root _dbu_
		append fileout1 $fileout0 $Dbu
		append fileout2 $fileout1 nm.oas
		puts $fileout2
		
		puts "******************* New dbu *******************"
		
		append app1 $Dbu nm
		puts $app1
		
		puts "***********************************************"
		
		$Output oasisout $fileout2
}






