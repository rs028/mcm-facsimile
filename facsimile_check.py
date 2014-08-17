# #################################################################### #
#                                                                      #
# FACSIMILE CHECK                                                      #
#                                                                      #
# This program checks a FACSIMILE model for two common errors,         #
# which would cause FACSIMILE to crash:                                #
#                                                                      #
# 1. tabs instead of spaces in the file                                #
# 2. lines longer than 72 characters                                   #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 1.1, september 2005                                          #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

# opening message
print """
..................................................
: facsimile_check 1.0                            :
: checks a FACSIMILE model for two common errors :
: - tabs instead of spaces                       :
: - lines longer than 72 characters              :
:................................................:
"""

# open input and output files  and name and length
print "enter name of the file with the model"
filename = raw_input("filename: ")
fin = open(filename, "r")
filename = filename + ".check"
fout = open(filename, "w")
print "enter maximum line length"
limit = raw_input("[default=72]: ")

# check the line length against the default value
# 73 characters including the newline
if limit == "":
    limit = 73
else:
    limit = int(limit)

# initialize counter and lists
counter = 1
linelist = []
tablist = []

# read input file line by line
for line in fin.readlines():

    # add line number to list if line length is over the limit
    row = len(line)
    if row > limit:
        linelist.append(counter)

    # add line number to list if there is a tab in the line
    if "\t" in line:
        tablist.append(counter)

    # increment counter
    counter = counter + 1

# write list of lines over the limit to output file
fout.write("---------------------------\n")
fout.write("LINES LONGER THAN " + str(limit-1) + ":\n")
for i in linelist:
    fout.write(str(i))
fout.write("\n---------------------------\n")

# write list of lines with tabs to output file
fout.write("---------------------------\n")
fout.write("LINES WITH TABS:\n")
for i in tablist:
    fout.write(str(i))
fout.write("\n---------------------------\n")

# close files and end program
# output summary of results to console
fin.close()
fout.close()
print "\nn. of lines longer than", limit-1, ":", len(linelist)
print "n. of lines with tabs:", len(tablist)
print "\n--- output written to", filename, "---"
