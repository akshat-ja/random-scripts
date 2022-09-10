#####################################################################################
#
#     Generate 2D Barcode
#     Akshat Jangam
#     18/02/2016
#
#     Generate text file datamatrixout.txt based 2D barcode (Data matrix)
#     
#     Run script : python 2d_barcode.py <BARCODE_TEXT>
#
#####################################################################################

import os
import sys
import getopt
import commands

# -----------------------------------------------------------------------------------
# Usage help function
# Input  : -
# Output : print help
# -----------------------------------------------------------------------------------
def usage() :
    print 'usage : py_2d_barcode <BARCODE_TEXT>'

# -----------------------------------------------------------------------------------
# Main function
# Input  : 
# Output : 
# -----------------------------------------------------------------------------------
def main(argv):
    
    try :
        opts, args = getopt.getopt(argv,"h:")
    except getopt.GetoptError :
        usage()
        sys.exit(2)
    
    if len(sys.argv) != 2 :
        print "Pass only one argument for the barcode text."
        usage()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help") :
            usage()
            sys.exit(0)
    
    # Extract text output
    commands.getstatusoutput("./iec16022 -s 32x32 -c " + argv[0] + " -o temp.txt -f Text -e AAAAAAAAAAAAAAAAAAAAAAAA")
     
    outfile = open("temp.txt", "r")
    contents = outfile.read()
    replaced_contents = contents.replace('*', '1').replace(' ', '0')
    outfile.close()

    os.remove("temp.txt")

    outfile = open("datamatrixout.txt", "wt")
    outfile.write(replaced_contents)
    outfile.close()

    cdrv_tcl_script = open('./run_temp1.tcl', 'w')
    cdrv_tcl_script.write("set L1 [layout create -dt_expand]\n")
    cdrv_tcl_script.write("$L1 create cell 2D_BC_GEN\n\n")
    cdrv_tcl_script.write("$L1 gdsout 2d_bc_out.gds 2D_BC_GEN\n\n")
    cdrv_tcl_script.write("set L1 [layout create 2d_bc_out.gds -dt_expand]\n")

    
    cdrv_tcl_script.write("set L2 [layout create ./euv_bc_dot.gds -dt_expand]\n")
    cdrv_tcl_script.write("$L1 import layout $L2 FALSE overwrite\n")

    x_pos = 0
    y_pos = 0
    increment = 0

    print replaced_contents

    for row in replaced_contents :
        #print row
        row = row.strip()
        for char_it in row :
            x_pos = divmod(increment, 32)[1]
            y_pos = divmod(increment, 32)[0]
                
            #print char_it + " " + str(x_pos) + " " + str(y_pos)
            if char_it == "1" :
                cdrv_tcl_script.write("$L1 create ref 2D_BC_GEN euv_bc_dot " + str(x_pos*50000) + " " + str(-y_pos*50000) + " 0 0 1\n")

            increment += 1

    cdrv_tcl_script.write("$L1 gdsout 2d_bc_out.gds 2D_BC_GEN\n\n")

    file.close(cdrv_tcl_script)
    os.system("calibredrv ./run_temp1.tcl")

    os.remove("./datamatrixout.txt")
    os.remove("./run_temp1.tcl")

# -----------------------------------------------------------------------------------
# Run main function
# -----------------------------------------------------------------------------------
if __name__ == "__main__" :
    main(sys.argv[1:])

      





















