# #################################################################### #
#                                                                      #
# LIST COMPARISON                                                      #
#                                                                      #
# Script to compare two lists of variables contained in two separate   #
# files (whitespace separated, no header)                              #
#                                                                      #
# The script uses the 'complist' function in the 'facsimile_funcs'     #
# module to find the differences between the lists                     #
#                                                                      #
# OUTPUT :                                                             #
#                                                                      #
# [length of list A, length of list B,                                 #
#  [elements in list A and in list B],                                 #
#  [elements in list A not in list B],                                 #
#  [elements in list B not in list A]]                                 #
#                                                                      #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 1.3, july 2017                                               #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

import sys
import facsimile_funcs

print """
.......................................................
: LIST COMPARISON v1.3                                :
: - compare two lists of variables in two files       :
:.....................................................:
"""

# input files (script argument or enter manually)
if sys.argv[1:]:
    fnameA = sys.argv[1]
    fnameB = sys.argv[2]
else:
    print "-> name of file with list A:"
    fnameA = raw_input("-> ")
    print "-> name of file with list B:"
    fnameB = raw_input("-> ")

# output file
fout = open("listcomparison.out", "w")

# read files into lists of variables with the 'openlist' function
finA = facsimile_funcs.openlist(fnameA)
finB = facsimile_funcs.openlist(fnameB)

# compare the lists of variables with the 'complist' function
comparestr = facsimile_funcs.complist(finA,finB)

# write comparison results to output file
fout.write("---------------------------\n")
fout.write("'" + fnameA + "' contains " + str(comparestr[0]) + " variables\n")
fout.write("'" + fnameB + "' contains " + str(comparestr[1]) + " variables\n")
fout.write("---------------------------\n")

fout.write("\n\n===> these variables of '" + fnameA + "' are also in '" + fnameB + "' :\n\n")
facsimile_funcs.listblock(comparestr[2],fout)

fout.write("\n\n===> these variables are in '" + fnameA + "' but not in '" + fnameB + "' :\n\n")
facsimile_funcs.listblock(comparestr[3],fout)

fout.write("\n\n===> these variables are in '" + fnameB + "' but not in '" + fnameA + "' :\n\n")
facsimile_funcs.listblock(comparestr[5],fout)

# output summary of results to console
print "\n'" + fnameA + "' contains " + str(comparestr[0]) + " variables"
print "'" + fnameB + "' contains " + str(comparestr[1]) + " variables"
print "\n--- output written to listcomparison.out ---\n"

# close file
fout.close()
