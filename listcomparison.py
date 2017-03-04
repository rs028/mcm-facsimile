# #################################################################### #
#                                                                      #
# LIST COMPARISON                                                      #
#                                                                      #
# This program compares two lists of variables from two files          #
# => the files must be whitespace separated and without header         #
#                                                                      #
# The program uses the 'complist' function in the 'facsimile_funcs'    #
# module to obtain the differences between the two lists.              #
# The information is in a list :                                       #
#                                                                      #
# [length A,length B,                                                  #
#  [elements in A and in B],                                           #
#  [elements in A not in B],                                           #
#  [elements in B and in A],                                           #
#  [elements in B not in A]]                                           #
#                                                                      #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 1.1, december 2007                                           #
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
: listcomparison 1.1                                  :
: compares two lists of variables in two files        :
:.....................................................:
"""

# open input and output files
## list of files is provided as script argument
if sys.argv[1:]:
    fnameA = sys.argv[1]
    fnameB = sys.argv[2]
## list of files is manual input
else:
    print "enter name of the file containing the first list"
    fnameA = raw_input("filename: ")
    print "enter name of the file containing the second list"
    fnameB = raw_input("filename: ")
## output file
fout = open("listcomparison.out", "w")

# read files into lists of variables with the 'openlist' function
finA = facsimile_funcs.openlist(fnameA)
finB = facsimile_funcs.openlist(fnameB)

# compare the two lists of variables with the 'complist' function
comparestr = facsimile_funcs.complist(finA,finB)

# write results of the comparison to the output file
fout.write("\n'" + fnameA + "' contains " + str(comparestr[0]) + " variables\n")
fout.write("\n'" + fnameB + "' contains " + str(comparestr[1]) + " variables\n")
fout.write("\n\n\tthese variables of '" + fnameA + "' are also in '" + fnameB + "' :\n")
facsimile_funcs.listblock(comparestr[2],fout)
fout.write("\n\n\tthese variables are in '" + fnameA + "' but not in '" + fnameB + "' :\n")
facsimile_funcs.listblock(comparestr[3],fout)
fout.write("\n\n\tthese variables of '" + fnameB + "' are also in '" + fnameA + "' :\n")
facsimile_funcs.listblock(comparestr[4],fout)
fout.write("\n\n\tthese variables are in '" + fnameB + "' but not in '" + fnameA + "' :\n")
facsimile_funcs.listblock(comparestr[5],fout)

# close output file
print "\n--- output written to listcomparison.out ---\n"
fout.close()
