# #################################################################### #
#                                                                      #
# FACSIMILE VARIABLES                                                  #
#                                                                      #
# This program extracts all the species of a chemical mechanism        #
# in FACSIMILE format and calculates the number of species and the     #
# number of reactions of the mechanism                                 #
#                                                                      #
# The program uses the 'facmecha' function in the 'facsimile_funcs'    #
# module to extract the chemical equations from the mechanism          #
# to a list:                                                           #
#                                                                      #
# [ rate coefficients  [reactants list]  [products list] ]             #
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
: facsimile_var 1.0                                   :
: extracts a list of all the species in the mechanism :
: and calculates the number of species and reactions  :
: in the mechanism (FACSIMILE format)                 :
:.....................................................:
"""

# open input and output files
## file with mechanism is provided as script argument
if sys.argv[1:]:
    fname = sys.argv[1]
## enter name of file with mechanism manually
else:
    print "enter name of the file with the model"
    fname = raw_input("filename: ")
fin = open(fname, "r")
## output file
fname = fname + ".var.out"
fout = open(fname, "w")

# read the input file in string
facstring = fin.read()

# call 'facmecha' function
# the function returns a list of the reactions in the mechanism
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

# calculates number of variables and reactions
nvar = str(len(varlist))
nreac = str(len(mechanism))

# write the number of variables and reactions to the output file
# write the list of variables to the output file
fout.write("---------------------------\n")
fout.write("n. variables: " + nvar + "\n")
fout.write("n. reactions: " + nreac + "\n")
fout.write("---------------------------\n")
facsimile_funcs.listblock(varlist,fout)

# close files and end program
# output to console the number of variables and reactions
fin.close()
fout.close()
print "\nn. variables:", nvar
print "n. reactions:", nreac
print "\n--- output written to", fname, "---\n"
