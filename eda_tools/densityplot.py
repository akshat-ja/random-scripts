#####################################################################################
#
#     Density plot script
#     Akshat Jangam
#     07/09/2015
#
#####################################################################################

import csv
import sys, getopt
import commands

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------

print '   argv [', len(sys.argv), '] : ', str(sys.argv)

def main(argv):

   printhelp = 'densityplot.py -l <layernum> -d <datatype> -w <window> -s <step> -i <inputfile.gds/csv> -o <outputfile.csv>\nOptional : -t <topcell>'

   inputfile = ''
   outputfile = ''
   topcell = ''

   layernum_str = ''
   layernum = 0
   datatype_str = ''
   datatype = 0

   window_str = ''
   window = 0.0
   step_str = ''
   step = 0.0

   input_ok = False
   output_ok = False
   topcell_ok = False
   l_ok = False
   d_ok = False
   w_ok = False
   s_ok = False

   try:
      opts, args = getopt.getopt(argv,"hi:o:l:d:t:w:s:",["ifile=","ofile=","layernum=","datatype=","topcell=","window=","step="])
   except getopt.GetoptError:
      print "Exception!\nUse : ", printhelp
      sys.exit(2)

   for opt, arg in opts:
      if opt in ("-h","--help"):
         print printhelp
         sys.exit()

      # Check input file
      elif opt in ("-i", "--ifile"):
         inputfile = arg
         input_ok = True
         print 'Input file is ', inputfile
      # Check output file
      elif opt in ("-o", "--ofile"):
         outputfile = arg
         output_ok = True
         print 'Output file is ', outputfile

      # Check layer number
      elif opt in ("-l", "--layernum", "--layernumber"):
         layernum_str = arg
         layernum = int(layernum_str)
         l_ok = True
         print 'Layer number is ', layernum
      # Check datatype
      elif opt in ("-d", "--datatype"):
         datatype_str = arg
         datatype = int(datatype_str)
         d_ok = True
         print 'Datatype is ', datatype
         
      # Check window
      elif opt in ("-w", "--window"):
         window_str = arg
         window = float(window_str)
         w_ok = True
         print 'Window is ', window
      # Check step
      elif opt in ("-s", "--step"):
         step_str = arg
         step = float(step_str)
         s_ok = True
         print 'Step is ', step

      # Check topcell
      elif opt in ("-t", "-tc", "--topcell"):
         topcell = arg
         topcell_ok = True
         print 'Topcell is ', topcell

   # Topcell extraction, if required
   if topcell_ok == False :
      runProcess_in = "calibredrv -a puts [layout peek " + inputfile + " -topcell]"
      topcell = commands.getstatusoutput(runProcess_in)[1]
      topcell_ok = True
      print 'Topcell is ', topcell

   if input_ok == False or output_ok == False or l_ok == False or d_ok == False or w_ok == False or s_ok == False :
      print "Incorrect input!\nUse : ", printhelp
      sys.exit()

   runProcess_in = "calibredrv -a puts [layout peek " + inputfile + " -bbox " + topcell + "]"
   bbox = commands.getstatusoutput(runProcess_in)[1]
   bbox = bbox[len(topcell)+3:len(bbox)-2]
   bbox = bbox.split(' ', 4)
   x_orig = bbox[0]
   y_orig = bbox[1]
   x_size = bbox[2]
   y_size = bbox[3]
   print bbox


if __name__ == "__main__":
   main(sys.argv[1:])