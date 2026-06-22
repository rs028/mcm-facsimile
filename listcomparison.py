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
# #################################################################### #
#                                                                      #
# version 2.4, june 2026                                               #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

import sys
import facsimile_funcs

print("""
.......................................................
: LIST COMPARISON v2.4                                :
: - compare two lists of variables in two files       :
:.....................................................:
""")

# input files (script argument or enter manually)
if sys.argv[1:]:
    fnameA = sys.argv[1]
    fnameB = sys.argv[2]
else:
    print("-> name of file with list A:")
    fnameA = input("-> ")
    print("-> name of file with list B:")
    fnameB = input("-> ")

# output file
fout = open("listcomparison.out", "w")

# read files into lists of variables with the 'openlist' function
finA = facsimile_funcs.openlist(fnameA)
finB = facsimile_funcs.openlist(fnameB)

# compare the lists of variables with the 'complist' function
comparestr = facsimile_funcs.complist(finA,finB)

# write comparison results to output file
fout.write("------------------------------------------\n")
fout.write("list ' " + fnameA + " ' contains: " + str(comparestr[0]) + " variables\n")
fout.write("list ' " + fnameB + " ' contains: " + str(comparestr[1]) + " variables\n")
fout.write("------------------------------------------\n")

fout.write("\n\n===> these variables are in '" + fnameA + "' and in '" + fnameB + "' :\n\n")
facsimile_funcs.listblock(comparestr[2],fout)

fout.write("\n\n===> these variables are in '" + fnameA + "' but not in '" + fnameB + "' :\n\n")
facsimile_funcs.listblock(comparestr[3],fout)

fout.write("\n\n===> these variables are in '" + fnameB + "' but not in '" + fnameA + "' :\n\n")
facsimile_funcs.listblock(comparestr[5],fout)

# output summary of results to console
print("list '", fnameA, "' contains:", comparestr[0], "variables")
print("list '", fnameB, "' contains:", comparestr[1], "variables")
print("\n--- output written to listcomparison.out ---\n")

# close file
fout.close()
