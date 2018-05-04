# #################################################################### #
#                                                                      #
# FACSIMILE CHECK                                                      #
#                                                                      #
# Script to check a FACSIMILE model for three common errors which may  #
# cause FACSIMILE to crash at runtime:                                 #
# 1. tabs instead of spaces                                            #
# 2. lines longer than 72 characters                                   #
# 3. variables longer than 10 characters                               #
#                                                                      #
# The script uses the 'facmecha' function in the 'facsimile_funcs'     #
# module to extract the chemical equations from the mechanism          #
#                                                                      #
# OUTPUT :                                                             #
#                                                                      #
# [ rate coefficients  [reactants list]  [products list] ]             #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 1.4, april 2018                                              #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

import sys
import facsimile_funcs

print """
.......................................................
: FACSIMILE CHECK v1.3                                :
:                                                     :
: - tabs instead of spaces                            :
: - lines longer than 72 characters                   :
: - variables longer than 10 characters               :
:.....................................................:
"""

# input file (script argument or enter manually)
if sys.argv[1:]:
    fname = sys.argv[1]
else:
    print "-> name of mechanism file:"
    fname = raw_input("-> ")
fin = open(fname, "r")

# set maximum length of lines
print "\n-> maximum number of characters per line [default=72]:"
llimit = raw_input("-> ")
if llimit == "":
    llimit = 73
else:
    llimit = int(llimit)

# output file
fout = open("facsimile_check.out", "w")

# read input file into string
facstring = fin.read()

# initialize lists
linelist = []
tablist = []
varlist = []

# find long lines and lines with tabs
i = 1
for line in facstring:

    # add line number to list if line length is over the limit
    row = len(line)
    if row > llimit:
        linelist.append(i)

    # add line number to list if there is a tab in the line
    if "\t" in line:
        tablist.append(i)

    # increment line counter
    i = i + 1

# make list of reactions in the mechanism
mechanism = []
mechanism = facsimile_funcs.facmecha(facstring)

# parse the lists of reactants (eq[1]) and of products (eq[2]) of each
# reaction (eq) in the 'mechanism' list
for eq in mechanism:

    # add reactant with long name to list of variables if not there
    for var in eq[1]:
        if len(var) > 10 and var not in varlist:
            varlist.append(var)

    # add product with long name to list of variables if not there
    for var in eq[2]:
        if len(var) > 10 and var not in varlist:
            varlist.append(var)

# write list of long lines to output file
fout.write("---------------------------\n")
fout.write("LINES LONGER THAN " + str(llimit-1) + ":\n")
for i in linelist:
    fout.write(str(i) + "\n")
fout.write("\n---------------------------\n")

# write list of lines with tabs to output file
fout.write("---------------------------\n")
fout.write("LINES WITH TABS:\n")
for i in tablist:
    fout.write(str(i) + "\n")
fout.write("\n---------------------------\n")

# write list of variables with long name to output file
fout.write("---------------------------\n")
fout.write("VARIABLES WITH LONG NAME:\n")
for i in varlist:
    fout.write(str(i) + "\n")
fout.write("\n---------------------------\n")

# output summary of results to console
print "\nn. of lines longer than", llimit-1, ":", len(linelist)
print "n. of lines with tabs:", len(tablist)
print "n. of variables with long names:", len(varlist)
print "\n--- output written to facsimile_check.out ---\n"

# close files
fin.close()
fout.close()
