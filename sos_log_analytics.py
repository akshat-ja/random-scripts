#!/usr/bin/env python
"""

This script generates analytics from an SOS generated log files.
It will output a comma separated value file sos_log_analytics_*.csv.

The output CSV table consists of the 4 columns:
    Command
    Number of times the command was run
    Sum of time taken to run each command, in seconds
    Average of time taken to run each command, in seconds

Usage syntax:
    ./sos_log_analytics.py [logfile(s)]
Examples:
    ./sos_log_analytics.py log1
    ./sos_log_analytics.py log*
    ./sos_log_analytics.py log1 log2 log3

"""

__author__ = "Akshat Jangam"
__version__ = "0.1.0"

# A preliminary version made over 2 evenings. There is still room for lots of improvement.
# I hope that this will be a point of conversation later on.
#
# My debug statements are commented with two #s

import sys # For argument parsing with sys.argv(), etc.
import os # For checking existing files for renaming
import re # For regular expression search pattern
import glob # For returning all the pathnames matching a specified pattern (Unix style)
import time # For time formatting
import datetime # For datetime formatting, conversion to/from string, etc.

def usage(type):
    '''
    A Usage/Help function that can be called with usage('') or usage('help').
    Contents are identical to the script header.
    '''
    if type == 'help':
        # When a detailed set of instructions is needed.
        print(
            'This script generates analytics from an SOS generated log files.\n' \
            'It will output a comma separated value file sos_log_analytics_*.csv.\n' \
            'The output CSV table consists of the 4 columns:\n' \
            '\tCommand\n' \
            '\tNumber of times the command was run\n' \
            '\tSum of time taken to run each command, in seconds\n' \
            '\tAverage of time taken to run each command, in seconds\n\n' \
            'Usage syntax:\n' \
            '\t./sos_log_analytics.py [logfile(s)]\n' \
            'Examples:\n' \
            '\t./sos_log_analytics.py log1\n' \
            '\t./sos_log_analytics.py log*\n' \
            '\t./sos_log_analytics.py log1 log2 log3\n'
        )
    else:
        # When a short set of instructions is needed.
        print(
            'Usage syntax:\n\t./sos_log_analytics.py [logfile(s)]\n' \
            'For detailed help:\n\t./sos_log_analytics.py help' \
            )

# I have put everything under the main function
def main():
    '''
    Main function of the script, called from the 
    '''
    
    # Defining argument list separately.
    args = sys.argv[1:]
    
    try:
        if len(args) == 0:
            # If no input file names are provided.
            print('No input files provided.')
            usage('')
            return 1
        elif args[0].lower() in ['h', 'help', '-h', '--help']:
            # If the detailed usage function is called.
            usage('help')
            return 1
        else:
            pass
    except:
        # Short usage function called.
        usage('')
        return 1
    
    # After this point, the program can begin properly!
    
    # Defining input file name list.
    input_filenames = []
    
    # Defining outputs.
    # I kept these three separate for better readability.
    command_list = set()
    command_freq = dict()
    command_time = dict()
    
    # Open an output file.
    # To avoid overwriting an existing output file, the following setup is used:
    csv_n = 0
    csv_filename = 'sos_log_analytics_'
    while os.path.exists(f"{csv_filename}{csv_n}.csv"):
        csv_n += 1
    csv_output = open(f"{csv_filename}{csv_n}.csv", 'w')
    # If overwriting is not an issue the following command can be used:
    # csv_output = open("sos_log_analytics.csv", "w")
    
    # Start with a timestamp
    currenttime_str = time.ctime()
    csv_output.write('Started at ' + currenttime_str + '.\n\n')
    
    # Add all relevant file names to the list input_filenames
    # Collect the pathnames matching a specified pattern (Unix style)
    # If wildcards expressions (*, **, ?, []) are used.
    for arg in args:
        input_filenames += glob.glob(arg)
    
    # Counters for command begin and end statements.
    count_begin = 0
    count_end = 0
    # Counter to verify begin-end statement pairs.
    count_bit = 0
    # Empty command string.
    cmd_now = ''
    # Empty print string
    print_this = ''
    
    if len(input_filenames) > 0:
        # If the list of files are greater than zero, list them.
        ## print('The following log files were analyzed:')
        ## print('\n'.join(input_filenames), '\n')
        csv_output.write('The following log files were analyzed:\n')
        csv_output.write('\n'.join(input_filenames) + '\n')
    else:
        # This else statement is required, if arguments provided returned no valid file names.
        # Only valid for full pathnames, wildcard expressions will not fall here.
        print('No such input files found.', ', '.join(args))
        usage('')
        return 1
    
    csv_output.write('\n')
    
    for file in input_filenames:
        # Open all the files with glob parsed pathnames.
        with open(file) as openfile:
            # Read one line at a time and find RegEx matches.
            for line in openfile.readlines():
                # Check for expressions matching with 'Begin cmd [command]'.
                # Capture date and time stamp, command name.
                #          ___________________                ________
                # Example: 2010/11/02 14:38:08 ** # Begin cmd populate
                re_cmd = re.search(r'(\d+/\d+/\d+ \d+:\d+:\d+) \*\* # Begin \w+ (\w+)', line)
                
                # Check for expressions matching with 'End cmd'.
                # Capture date and time stamp.
                #          ___________________
                # Example: 2010/11/02 14:48:31 ** # End cmd
                re_out = re.search(r'(\d+/\d+/\d+ \d+:\d+:\d+) \*\* # End cmd', line)
                
                # I am making an asumption here that a Begin command, and its End command
                # follow one another sequentially, so that I can parse for one at a time and
                # be certain that it will not interfere with other Begin/End commands.
                # Otherwise, I would have to introduce a stack or two.
                
                if re_cmd:
                    # Begin command counter
                    count_begin += 1
                    # Capture command name
                    cmd_now = re_cmd.group(2)
                    # Date+time in time.struct_time object format
                    dt_in_unix = datetime.datetime.strptime(re_cmd.group(1), "%Y/%m/%d %H:%M:%S")
                    # Date+time converted to a tuple containing 9 elements and then to seconds
                    dt_in_fl = time.mktime(dt_in_unix.timetuple())
                    ## print_this = re_cmd.group(0)
                    ## print(print_this)
                    # Begin counting
                    command_list.add(cmd_now)
                    
                    # I put a [0, 1] count_bit flip in place to check for Begin/End cmd pairs.
                    count_bit += 1
                    if count_bit > 1:
                        # If count goes out of bounds, over 1, flag it and set it back to 1.
                        count_bit = 1
                        print_this = re_out.group(0)
                        ## print('Extra statement ignored: ' + print_this)
                        csv_output.write('Extra statement in ' + file + ' ignored: ' + print_this + '\n')
                    else:
                        if not (cmd_now in command_freq):
                            # If new command, add it to the command_freq dictionary.
                            command_freq[cmd_now] = 0
                        # Command frequency counter +1.
                        command_freq[cmd_now] += 1
                
                if re_out:
                    # End command counter
                    count_end += 1
                    # Date+time in time.struct_time object format
                    dt_out_unix = datetime.datetime.strptime(re_out.group(1), "%Y/%m/%d %H:%M:%S")
                    # Date+time converted to a tuple containing 9 elements and then to seconds
                    dt_out_fl = time.mktime(dt_out_unix.timetuple())
                    ## print_this = re_out.group(0)
                    ## print(print_this)
                    # End counting
                    count_bit -= 1
                    
                    # I put a [0, 1] count_bit flip in place to check for Begin/End cmd pairs.
                    # This is where I caught the exception that I asked you about in my email on Sept 21st 2022.
                    if count_bit < 0:
                        # If count goes out of bounds, below 0, flag it and set it back to 0.
                        count_bit = 0
                        print_this = re_out.group(0)
                        ## print('Extra statement ignored: ' + print_this)
                        csv_output.write('Extra statement in ' + file + ' ignored: ' + print_this + '\n')
                    else:
                        if not (cmd_now in command_time):
                            # If new command, add it to the command_time dictionary.
                            command_time[cmd_now] = 0
                        if dt_in_fl == dt_out_fl:
                            # If command begin time == command end time, set it to 0.5.
                            # Add it to the command_time dictionary.
                            command_time[cmd_now] += 0.5
                        else:
                            # If difference is non-zero, and add it to the command_time dictionary.
                            dt_diff = dt_out_fl - dt_in_fl
                            command_time[cmd_now] += dt_diff
                
    # Flag the case when begin count != end count, make a note of the two numbers.
    if count_begin != count_end:
        ## print(f'NOTE: Begin statement counts {count_begin} and end statement counts {count_end} do not match.')
        csv_output.write(f'NOTE: Begin statement counts {count_begin} and end statement counts {count_end} do not match.' + '\n')
    
    # Output the csv table.
    # First three column are available: commmand, # times ran, sum of times ran
    ## print('\nCommand, Number of times ran, Sum of all runs, Average run time')
    csv_output.write('\nCommand, Number of times run, Sum of all runs, Average run time\n')
    for cmd in command_list:
        # Fourth column is calculated into command_avg, rounded to one decimal point.
        command_avg = round(command_time[cmd]/command_freq[cmd], 2)
        ## print(cmd, ',', command_freq[cmd], ',', command_time[cmd], ',', command_avg)
        csv_output.write(cmd + ', ' + str(command_freq[cmd]) + ', ' + str(command_time[cmd]) + ', ' + str(command_avg) + '\n')
    
    # End with a timestamp
    currenttime_str = time.ctime()
    csv_output.write('\nEnded at ' + currenttime_str + '.\n')
    
    # Close the output csv file.
    csv_output.close()

# Facilitate the top level code to run from CLI.
if __name__ == "__main__":
    """
    This is executed when run from the command line.
    The Python interpreter will call this automatically.
    """
    main()