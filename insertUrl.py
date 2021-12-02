# -*- coding: UTF-8 -*-
"""
Usage: 
Input a directory to work from, specify which filetype to search through,
type in the regex expression to match.
The script walks through all files within the top directory. 
Each line in each file is searched for the regex query. 
The url parameter gets grabbed from the directory path, reformatted and 
inserted in a new line after the matched query.
I still have to figure out what to do with files named 'index',
as the url is in part made up of the file name.
"""

import os    # Using os.chdir(), os.listdir(), os.path.isfile(), os.rename()
import re    # Using re.sub()
import fileinput

# grab working directory
startDir = input('Specify FULL PATH to local content directory: ')
# change current working directory
os.chdir(startDir)
# print new working directory
print('\nCurrent working directory: ', os.getcwd(), end='\n')

# The top argument for walk
topdir = '.'
# The extension to search through
#let's hardcode .md
exten = '.md'#input('\nPlease specify file extension to search: ')

#logname = 'findfiletype.log'
# What will be logged
#results = str()
# What are we searching for
#let's hardcode
start = 'title: ".*"'#input('\nPlease type in Regex to match:\n(hint: to match an entire title type in title: ".*") ')

for dirpath, dirnames, allfiles in os.walk(topdir):
    for name in allfiles:
        if name.lower().endswith(exten):
            print('File: ', os.path.join(dirpath, name))  # Print Filename
            os.altsep = '/'
            altPath = dirpath.replace(os.sep, os.altsep)
            # for toplevel directory
            with fileinput.input(os.path.join(dirpath, name), inplace=True, backup='', encoding="utf-8") as file:
                for line in file:
                    if re.match(start,line) != None:
                        matched = re.match(start,line)
                        # for toplevel directory
                        if dirpath == '.':
                            if name == 'index.md':
                                insert = matched.string + 'url: /' + '\n'
                            else:
                                insert = matched.string + 'url: /' + name[:-(len(exten))] + '\n'
                        # anything deeper
                        else:
                            if name == 'index.md':
                                insert = matched.string + 'url: /' + altPath[2:] + '\n'
                            else:
                                insert = matched.string + 'url: /' + altPath[2:] + '/' + name[:-(len(exten))] + '\n'
                        line = re.sub(r''+start,insert,line.rstrip())
                    print(line, end='')

            # Save to results string instead of printing
            #results += '%s\n' % os.path.join(dirpath, name)
 
# Write results to logfile
# with open(logname, 'w') as logfile:
#     logfile.write(results)




