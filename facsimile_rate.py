# #################################################################### #
#                                                                      #
# FACSIMILE REACTION RATES                                             #
#                                                                      #
# This program writes the FACSIMILE code for the calculation of the    #
# Rates of Production and Destruction of selected species in a         #
# chemical mechanism                                                   #
#                                                                      #
# The program uses the 'facmecha' function in the 'facsimile_funcs'    #
# module to extract the chemical equations from the mechanism          #
# to a list :                                                          #
#                                                                      #
# [ rate coefficients  [reactants list]  [products list] ]             #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 1.0, july 2005                                               #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

# import modules
import string
import facsimile_funcs

# opening message
print """
....................................................................
: facsimile_rate 1.0                                               :
: creates a new list of parameters and writes the FACSIMILE code   :
: to calculate the rates of production and destruction of selected :
: species                                                          :
:..................................................................:
"""

# open input and output files
print "enter name of the file with the chemical mechanism"
filename = raw_input("filename: ")
fin = open(filename, "r")
filename = filename + ".rate "
fout = open(filename, "w")

# read the input file in string
facstring = fin.read()

# call 'facmecha' function
# the function returns a list of the reactions in the mechanism
mechanism = []
mechanism =  facsimile_funcs.facmecha(facstring)

# input species
# correct input errors (upper case, no spaces) and make list
print "\nenter species of interest"
listspec = raw_input("comma separated list of species: ")
listspec = string.upper(listspec).replace(" ","").split(",")

# initialize list of new parameters and their definitions
paramlist = []; defparamlist = []

# write the header to the ouput file
fout.write("""* ;
* *************************************************** * ;
* *     Rate of Production/Destruction Analysis       * ;
* *************************************************** * ;\n""")

# write the code for the rate of production and destruction
# look in the mechanism list for each species selected
for spec in listspec:

    # initialize counters and lists
    i = 1; j =1; n = 0
    rodlist = []; roplist = []
    paramplist = []; paramdlist = []
    defparamplist = []; defparamdlist = []

    # counts the number of times the selected species is in the
    # reactants (eq[1]) and in the products (eq[2]) for each reaction
    # of the mechanism and take the difference (n)
    for eq in mechanism:
        n =  eq[2].count(spec) - eq[1].count(spec)

        # when n is positive the species is produced by the reaction
        # parameter name is: 'F_species_counter'
        # the definition of the parameter is: 'parameter_name : reaction'
        if n > 0:
            paramp = "F_" + string.lower(spec) + "_" + str(i)
            defparamp = paramp + " : "
            rop = paramp + " = " + str(n) + "*" + eq[0]
            for el in eq[1]:
                rop = rop + "*" + el
                defparamp = defparamp + el + "+"
            defparamp = defparamp[:-1] + "->"
            for el in eq[2]:
                defparamp = defparamp + el + "+"
            defparamp = defparamp[:-1] + "\n"
            rop = rop + " ;\n"
            roplist.append(rop)
            paramplist.append(paramp)
            defparamplist.append(defparamp)
            i = i + 1

        # when n is positive the species is destroyed by the reaction
        # parameter name is: 'D_species_counter'
        # the definition of the parameter is: 'parameter_name : reaction'
        elif n < 0:
            paramd = "D_" + string.lower(spec) + "_" + str(j)
            defparamd = paramd + " : "
            rod = paramd + " = " + str(n) + "*" + eq[0]
            for el in eq[1]:
                rod = rod + "*" + el
                defparamd = defparamd + el + "+"
            defparamd = defparamd[:-1] + "->"
            for el in eq[2]:
                defparamd = defparamd + el + "+"
            defparamd = defparamd[:-1] + "\n"
            rod = rod + " ;\n"
            rodlist.append(rod)
            paramdlist.append(paramd)
            defparamdlist.append(defparamd)
            j = j + 1

    # write to file the code to calculate the rates of production
    # and destruction of the selected species
    fout.write("* ;\n* " + spec + " production\n* ;\n")
    for el in roplist:
        fout.write(el)
    fout.write("* ;\n* " + spec + " destruction\n* ;\n")
    for el in rodlist:
        fout.write(el)

    # add parameters of production and destruction to list of parameters
    paramlist = paramlist + paramplist + paramdlist
    defparamlist = defparamlist + defparamplist + defparamdlist

# write list of new parameters and the definitions of the new parameters
# to the output file with headers
fout.write("""* ;
* *************************************************** * ;
* ;
PARAMETER\n""")
facsimile_funcs.listblock(paramlist,fout)
fout.write("""\n* ;
* *************************************************** * ;
* ;
DEFINITION OF THE PARAMETERS\n""")
for item in defparamlist:
    fout.write(item)

# close files and end program
fin.close()
fout.close()
print "\n--- output written to", filename, "---"
