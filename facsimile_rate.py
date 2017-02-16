# #################################################################### #
#                                                                      #
# FACSIMILE REACTION RATES                                             #
#                                                                      #
# This program creates a new list of parameters and writes the         #
# FACSIMILE code for the calculation of the rates of production and    #
# destruction of selected species in a chemical mechanism              #
# It also writes the definitions of the new parameters created that    #
# can be used to interpret the model output                            #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 2.5, july 2008                                               #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

# load module with facsimile functions
import textwrap
import facsimile_funcs

## This function writes the lists of parameters, the expressions to
## calculate the production and destruction rates and the definitions
## of the new parameters to an output file
def outputrates(r,fname,paramlist,totparamlist,expresslist,definlist):
    fout = open(fname, "w")

    # write list of parameters to output file
    fout.write("""* ;\nPARAMETER\n""")
    for p in paramlist:
        facsimile_funcs.listblock(p,fout)
        fout.write(" ")
    fout.write("\n")
    facsimile_funcs.listblock(totparamlist,fout)
    fout.write(" ;")

    # write the expressions to calculate the production/destruction
    # rates to output file
    if r == 'p':
        rstr = "production"
    elif r == 'd':
        rstr = "destruction"

    fout.write("""\n* ;
* ********************************************** * ;
* *    Rate of """ + rstr.capitalize() + """ Analysis
* ********************************************** * ;\n""")

    # write the expressions for each of the selected species
    i = 0
    for species in listspecies:
        fout.write("* ;\n* *** " + species + " " + rstr +"\n* ;\n")
        for el in expresslist[i]:
            # write the expression only if it contains a specified
            # reactant (default=all)
            if reactant in el:
                fout.write(el)
        # write expression for total
        # production/destruction rate 
        if reactant == '':
            fout.write("* ;\n")
            tot = totparamlist[i] + " = " + " + ".join(paramlist[i])
            fout.write(textwrap.fill(tot) + " ;\n")
        i = i + 1

    # write definition of parameters to output file
    fout.write("""* ;
* ********************************************** * ;
* ;\nDEFINITION OF THE PARAMETERS\n\n""")
    for dlist in definlist:
        for d in dlist:
            fout.write(d)

    # close file and print message
    fout.close()
    print "\n--- output written to", fname, "---\n"

# #################################################################### #
# opening message
print """
.......................................................
: facsimile_rate 2.5                                  :
: creates a new list of parameters and writes the     :
: FACSIMILE code to calculate the rates of production :
: and destruction of selected species                 :
:                                                     :
: >>> selected species in 'facsimile_rate.in' <<<     :
:.....................................................:
"""

# open input and output files
print "enter name of the file with the chemical mechanism"
filename = raw_input("filename: ")
fin = open(filename, "r")
fileoutP = filename + ".rateP.out"
fileoutD = filename + ".rateD.out" 

# read the input file in string
facstring = fin.read()

# call 'facmecha' function
# the function returns a list of the reactions in the mechanism
mechanism = []
mechanism =  facsimile_funcs.facmecha(facstring)

# input species of interest (all species in upper case)
finput = open("facsimile_rate.in", "r")
listspecies = facsimile_funcs.openlist("facsimile_rate.in")
for i in range(len(listspecies)):
    listspecies[i] = listspecies[i].upper()

# specify to output only the rates of reactions involving a specific
# reactant (reactant name in upper case)
print "\nwrite only the rates of reactions with a specific reactant?"
print "[default: write the rates of all reactions]"
reactant = raw_input("reactant name [press enter for default]: ")
if reactant != '':
    reactant = "*" + reactant.upper() + "*"

# call 'ropa' function
# the function returns a list with this output:
# [0 [list of production parameters]
#  1 [list of destruction parameters]
#  2 [list of production expressions]
#  3 [list of destruction expressions]
#  4 [list of number codes of production reactions]
#  5 [list of number codes of destruction reactions]
#  6 [list of definitions of production parameters]
#  7 [list of definitions of destruction parameters] ]
paramPlist = []; totparamPlist = []; expressPlist = []; definPlist = []
paramDlist = []; totparamDlist = []; expressDlist = []; definDlist = []
for species in listspecies:
    ratelist = []
    ratelist = facsimile_funcs.ropa(mechanism,species)

    paramPlist.append(ratelist[0])
    paramDlist.append(ratelist[1])
    totparamPlist.append("P_" + species.lower() + "_tot")
    totparamDlist.append("D_" + species.lower() + "_tot")
    expressPlist.append(ratelist[2])
    expressDlist.append(ratelist[3])
    definPlist.append(ratelist[6])
    definDlist.append(ratelist[7])

# write the output for the production and the destruction rates
outputrates('p',fileoutP,paramPlist,totparamPlist,expressPlist,definPlist)
outputrates('d',fileoutD,paramDlist,totparamDlist,expressDlist,definDlist)

# close files and end program
fin.close()
finput.close()
