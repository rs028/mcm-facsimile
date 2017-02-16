# #################################################################### #
#                                                                      #
# FACSIMILE CHECK                                                      #
#                                                                      #
# This program checks a FACSIMILE model for three common errors        #
# which would cause FACSIMILE to crash:                                #
#                                                                      #
# 1. tabs instead of spaces in the file                                #
# 2. lines longer than 72 characters                                   #
# 3. variables names longer than 10 characters                         #
#                                                                      #
# The program uses the 'facmecha' function in the 'facsimile_funcs'    #
# module to extract the chemical equations from the mechanism          #
# to a list:                                                           #
#                                                                      #
# [ rate coefficients  [reactants list]  [products list] ]             #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 1.2, december 2007                                           #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

# load modules
import sys
import facsimile_funcs

# opening message
print """
.......................................................
: facsimile_check 1.0                                 :
: checks a FACSIMILE model for three common errors    :
: - tabs instead of spaces                            :
: - lines longer than 72 characters                   :
: - variables names longer than 10 characters         :
:.....................................................:
"""

# open input and output files
## file with mechanism is provided as script argument
if sys.argv[1:]:
    fname = sys.argv[1]
## enter name of file with mechanism manually
else:
    print "enter name of the file with the chemical mechanism"
    fname = raw_input("filename: ")
fin = open(fname, "r")
facstring = fin.read()
## output file
fname = fname + ".check.out"
fout = open(fname, "w")

# enter maximum line length
print "\nenter maximum number of characters per line"
limit = raw_input("[default=72]: ")

# check the line length against the default value
# 73 characters (includes the newline)
if limit == "":
    limit = 73
else:
    limit = int(limit)

# initialize lists 
linelist = []; tablist = []; varlist = []
mechanism = []

# read input file line by line
i = 1
for line in facstring:
    
    # add line number to list if line length is over the limit
    row = len(line)
    if row > limit:
        linelist.append(i)

    # add line number to list if there is a tab in the line 
    if "\t" in line:
        tablist.append(i)

    # increment counter
    i = i + 1

# extract mechanism and go through the lists of reactants (eq[1])
# and of products (eq[2]) in the 'mechanism' list
mechanism = facsimile_funcs.facmecha(facstring)
for eq in mechanism:
    # add variable to list if name is too long if not there
    for var in eq[1]:
        if len(var) > 10 and var not in varlist:
            varlist.append(var)
    for var in eq[2]:
        if len(var) > 10 and var not in varlist:
            varlist.append(var)

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

# write list of variables with long names to output file
fout.write("---------------------------\n")
fout.write("VARIABLE NAMES TOO LONG:\n")
for i in tablist:
    fout.write(str(i))
fout.write("\n---------------------------\n")


# close files and end program
# output summary of results to console
fin.close()
fout.close()
print "\nn. of lines longer than", limit-1, ":", len(linelist)
print "n. of lines with tabs:", len(tablist)
print "n. of variables with long names:", len(varlist)
print "\n--- output written to", fname, "---\n"
