# #################################################################### #
#                                                                      #
# FACSIMILE VARIABLES                                                  #
#                                                                      #
# Script to create a list of the chemical variables in a chemical      #
# mechanism (in FACSIMILE format) and count the number of species      #
# and reactions in the mechanism                                       #
#                                                                      #
# The script uses the 'facmecha' function in the 'facsimile_funcs'     #
# module to extract the chemical equations from the mechanism          #
# to a list:                                                           #
#                                                                      #
# [ rate coefficients  [reactants list]  [products list] ]             #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 1.2, july 2017                                               #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

import sys
import facsimile_funcs

print """
.......................................................
: FACSIMILE VARIABLES  v1.2                           :
:                                                     :
: - list chemical variables in mechanism              :
: - count number of species and reactions             :
:.....................................................:
"""

# input file is function argument
if sys.argv[1:]:
    fname = sys.argv[1]
# input file entered manually
else:
    print "-> name of the mechanism file:"
    fname = raw_input("-> ")
    print("")
fin = open(fname, "r")

# output file
fout = open("facsimile_var.out", "w")

# read input file into string
facstring = fin.read()

# make list of reactions in the mechanism
mechanism = []
mechanism = facsimile_funcs.facmecha(facstring)

# initialize list of variables
varlist = []

# look into the lists of reactants (eq[1]) and of products (eq[2])
# of each reaction (eq) in the 'mechanism' list
for eq in mechanism:

    # add reactants to list of variables if not there
    for var in eq[1]:
        if var not in varlist and var != "":
            varlist.append(var)

    # add products to list of variables if not there
    for var in eq[2]:
        if var not in varlist and var != "":
            varlist.append(var)

# count number of variables and reactions
nvar = str(len(varlist))
nreac = str(len(mechanism))

# write number of variables and reactions and list of variables to
# output file
fout.write("---------------------------\n")
fout.write("n. variables: " + nvar + "\n")
fout.write("n. reactions: " + nreac + "\n")
fout.write("---------------------------\n\n")
facsimile_funcs.listblock(varlist,fout)

# output summary of results to console
print "n. variables:", nvar
print "n. reactions:", nreac
print "\n--- output written to facsimile_var.out ---\n"

# close files
fin.close()
fout.close()
