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
# version 1.0, march 2005                                              #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

# load module with facsimile functions
import facsimile_funcs

# opening message
print """
.................................................................
: facsimile_var 1.0                                             :
: extracts a list of all the species in the mechanism and       :
: calculates the number of species and reactions in the         :
: mechanism (FACSIMILE format)                                  :
:...............................................................:
"""

# open input and output files
print "enter name of the file with the chemical mechanism"
filename = raw_input("filename: ")
fin = open(filename, "r")
filename = filename + ".var"
fout = open(filename, "w")

# read the input file in string
facstring = fin.read()

# call 'facmecha' function
# the function returns a list of the reactions in the mechanism
mechanism = []
mechanism = facsimile_funcs.facmecha(facstring)

# initialize list of species
speclist = []

# look into the lists of reactants (eq[1]) and of products (eq[2])
# of each reaction (eq) in the 'mechanism' list
for eq in mechanism:

    # add reactants to list of species if not there
    for spec in eq[1]:
        if spec not in speclist and spec != "":
            speclist.append(spec)

    # add products to list of species if not there
    for spec in eq[2]:
        if spec not in speclist and spec != "":
            speclist.append(spec)

# calculates number of species and reactions
nspec = str(len(speclist))
nreac = str(len(mechanism))

# write the number of species and reactions to the output file
# write the list of species to the output file
fout.write("---------------------------\n")
fout.write("n. species: " + nspec + "\n")
fout.write("n. reactions: " + nreac + "\n")
fout.write("---------------------------\n")
facsimile_funcs.listblock(speclist,fout)

# close files and end program
# output to console the number of species and reactions
fin.close()
fout.close()
print "\nn. species:", nspec
print "n. reactions:", nreac
print "\n--- output written to", filename, "---"
