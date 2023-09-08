"""
Here's an example of EIC pad-coordnates files. I don’t have one for the PIC yet, but the syntax / format is going to be the same. For now, imagine you’ll have two such files as we talked about. One file for eic and the other file for pic.
./ic-chipBumps.padcoord.txt

 1.  Please write the parser for this file. Once I generate the pic pad-coords, things will become more realistic. Please note the following:
     -  For each eic bump, there will be two pic bumps
     -  Names will have different prefixes N_<eicName> and S_<eicName>
     -  Y-offset will be different for the N_ and S_ bump
     -  X-offset will be exactly the same.
 2.  The job of d2dlvs script is to compare the two files and create a list of bumps that don’t match either the name or the x,y location.

-----

   1. read pic-chip pad-coords
   2. foreach pic-chip pad
       - store xy and name
       - calc eicx =(x-xoffset), eicy=(y-North_yoffset)
       - at (eicx, eicy), bumpname should be N_<eicName> or S_<eicName> ie the <eicName>
       - repeat for South_yoffset

"""

#!/usr/bin/env python3

from ast import Delete
import sys
import argparse
import re
import copy

# Global variables
coord_margin = 0.5
# Offset between ic-chip and pic-chip (centered N/S): ic-chip centered
die_offset_x = 500
die_offset_y = 330
# Placement difference of +/- um between N/S
# Use as is for N, *-1 for S!
die_placement_x = 4690 # Mirroring on the y axis will move it to the left of the y axis
die_placement_y = 8370 - die_offset_y # Adding both values, so it needs a difference between the two
# Used IBUS/N_IBUS/S_IBUS for reference:
#    ic-chip  : 4240, 815
#    ULU_N: 950,  9185
#    ULU_S: 950,  1145

class Coordinate:
    def __init__(self, name, x, y, match=False):
        # super().__init__()
        self.name = str(name)
        self.x = float(x)
        self.y = float(y)
        self.match = match
        # self.coord = (name, x, y)
    
    def get(self):
        # return self.coord
        return [self.name, self.x, self.y]
    
    def check_name(self, check_name):
        return True if self.name == check_name else False
    
    def check_x(self, check_x):
        if check_x in range(self.x - coord_margin, self.x + coord_margin):
            return True
        return False
    
    def check_y(self, check_y):
        if check_y in range(self.y - coord_margin, self.y + coord_margin):
            return True
        return False
    
    def check_xy(self, check__x, check__y):
        if self.check_x(check__x) and self.check_y(check__y):
            return True
        return False
    
    def check_prefix(self):
        if self.name.startswith('N_'):
            return 'N'
        elif self.name.startswith('S_'):
            return 'S'
        else:
            return False
    
    def add_prefix(self, prefix):
        self.name = prefix + self.name
        return self
    
    def x_mirror(self):
        self.y *= -1
        return self
    
    def y_mirror(self):
        self.x *= -1
        return self
    
    def offset(self, offset_x, offset_y):
        self.x += offset_x
        self.y += offset_y
        return self
    
    def print(self):
        print(self.name, '\t', self.x, '\t', self.y, '\t', self.match)


class Coordinates:
    def __init__(self):
        self.coordinates = set()
    
    def get(self):
        return self.coordinates
    
    def add(self, input):
        self.coordinates.add(input)
    
    def discard(self, input):
        self.coordinates.discard(input)
    
    def print_all(self):
        for item in self.coordinates:
            print(item.get())
    
    def x_mirror_coordinates(self):
        for c in self.coordinates:
            c.x *= -1
    
    def y_mirror_coordinates(self):
        for c in self.coordinates:
            c.y *= -1


def regex_parse_coordinates(string):
    # Regular expression pattern matching
    # Chevrons/angle brackets? <[^>]+> or <(.*?)> or <([^<>]*)>
    # All chic-chipcters and spaces except: ^(?=[a-zA-Z0-9~@#$^*()_+=[\]{}|\\,.?: -]*$)(?!.*[<>'"/;`%])
    # ^(?=[a-zA-Z0-9<>()[\]{})(?!.* [~@#$^*_+='"/;`%]) ???
    # [a-zA-Z0-9~@#\^\$&\*\(\)-_\+=\[\]\{\}\|\\,\.\?\s]* worked
    return re.search(r'([a-zA-Z0-9~@#\^\$&\*\(\)-_\+=\[\]\{\}\|\\,\.\?]*)\s+(\d+(\.\d*)?|\.\d+)\s+(\d+(\.\d*)?|\.\d+)', string)

def offset_coordinates(coordinates, x_offset, y_offset):
    for c in coordinates:
        c.x += x_offset
        c.y += y_offset

def compare_coordinates(coord_1, coord_2):
    if coord_1 >= coord_2 - coord_margin <= coord_2 + coord_margin:
        return True
    return False

def print_usage(str):
    print(f"{str}\nCorrect usage is:\n\t{sys.argv[0]} input_file_1 input_file2\n\t{sys.argv[0]} ic-chip_coordinates pic-chip_coordinates")

def main():
    # Arguments
    args = sys.argv[1:]

    # TODO Verbose output
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-v', '--verbose', action='count', default=0)

    # for c in ['', '-v', '-v -v', '-vv', '-vv -v', '-v -v --verbose -vvvv']:
    #     print(parser.parse_args(c.split()))
    
    # Throw exceptions if something isn't right
    try:
        inputfile_1 = args[0]
        inputfile_2 = args[1]
    except Exception as e:
        print(e)
        print_usage('Expecting 2 arguments.')
        return -1
    
    try:
        with open (inputfile_1, "r") as input_1:
            lines_1 = input_1.readlines()
        with open (inputfile_2, "r") as input_2:
            lines_2 = input_2.readlines()
    except IOError as e:
        print(e)
        print_usage('Files not found.')
        return -1
    
    # TODO Output file
    output_file = open(r"./output_py.txt", "w")
    
    # --------------------------------------------- #
    # ic-chip coordiniates added to N and S lists
    # --------------------------------------------- #
    print("\nic-chip COORDINATES\n")
    # --------------------------------------------- #
    
    # Read in list
    coordinates_1 = Coordinates()
    # N & S instance lists
    coordinates_N = Coordinates()
    coordinates_S = Coordinates()
    
    # Pad Opening Name check here
    # Running a for loop until "Pad Opening Name" is found
    # Save start point to start_count
    start_count = 0
    for line in lines_1:
        start_count += 1
        if line.find("Pad Opening Name") >= 0:
            start_count += 1
            break
    
    for n in range(start_count, len(lines_1)):
        re_line = regex_parse_coordinates(lines_1[n])
        
        if re_line:
            # re_full = re_line.group(0)
            re_padname = re_line.group(1)
            re_x = float(re_line.group(2))
            re_y = float(re_line.group(4))
            coordinate_1 = Coordinate(re_padname, re_x, re_y)
            ### coordinate_1.print()
            coordinates_1.add(coordinate_1)
            
            # Populate N & S lists to crosscheck
            # Offset and placement shifts applied
            coordinate_N = copy.deepcopy(coordinate_1).add_prefix("N_").y_mirror().offset(die_offset_x + die_placement_x, die_offset_y + die_placement_y)
            coordinate_S = copy.deepcopy(coordinate_1).add_prefix("S_").y_mirror().offset(die_offset_x + die_placement_x, die_offset_y) # No die_placement_y here
            coordinates_N.add(coordinate_N)
            coordinates_S.add(coordinate_S)
            
            ### coordinate_N.print()
            ### coordinate_S.print()
            
    
    # --------------------------------------------- #
    # pic-chip coordiniates added to one list
    # --------------------------------------------- #
    print("\npic-chip COORDINATES\n")
    # --------------------------------------------- #
    
    coordinates_2 = Coordinates()
    
    # Pad Opening Name check here
    # Running a for loop until "Pad Opening Name" is found
    # Save start point to start_count
    start_count = 0
    for line in lines_2:
        start_count += 1
        if line.find("Pad Opening Name") >= 0:
            start_count += 1
            break
    
    for n in range(start_count, len(lines_2)):
        re_line = regex_parse_coordinates(lines_2[n])
        
        if re_line:
            # re_full = re_line.group(0)
            re_padname = re_line.group(1)
            re_x = float(re_line.group(2))
            re_y = float(re_line.group(4))
            coordinate_2 = Coordinate(re_padname, re_x, re_y)
            ### coordinate_2.print()
            coordinates_2.add(coordinate_2)
    
    # --------------------------------------------- #
    # Checking stage
    # --------------------------------------------- #
    print("\nd2dlvs Check\n")
    # --------------------------------------------- #
    
    for coord in coordinates_2.coordinates:
        for coord_N in coordinates_N.coordinates:
            if coord_N.name == coord.name:
                ### print(coord.name)
                if compare_coordinates(coord.x, coord_N.x) and compare_coordinates(coord.y, coord_N.y):
                    coord.match, coord_N.match = True, True
                
        for coord_S in coordinates_S.coordinates:
            if coord_S.name == coord.name:
                ### print(coord.name)
                if compare_coordinates(coord.x, coord_S.x) and compare_coordinates(coord.y, coord_S.y):
                    coord.match, coord_S.match = True, True
    
    
    for c in coordinates_N.coordinates:
        #print(c.name, ' ', c.match)
        if not c.match:
            c.print()
    
    for c in coordinates_S.coordinates:
        #print(c.name, ' ', c.match)
        if not c.match:
            c.print()
    
    for c in coordinates_2.coordinates:
        #print(c.name, ' ', c.match)
        if not c.match:
            c.print()
    
    
    # padnames_ic-chip = []
    # for e in coordinates_1.coordinates:
    #     padnames_ic-chip.append(e.name)
    # padnames_N = []
    # for e in coordinates_N.coordinates:
    #     if not e.name in padnames_ic-chip:
    #         padnames_N.append(e.name)
    # padnames_S = []
    # for e in coordinates_S.coordinates:
    #     if not e.name in padnames_ic-chip:
    #         padnames_S.append(e.name)
    
    # Debug
    # print(", ".join(padnames_ic-chip))
    # print(", ".join(padnames_N))
    # print(", ".join(padnames_S))
    

if __name__ == "__main__":
    main()
