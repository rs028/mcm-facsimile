# #################################################################### #
#                                                                      #
# FACSIMILE TRACK                                                      #
#                                                                      #
# Script to generate the FACSIMILE code to track the precursors of     #
# a list of selected species:                                          #
# - find all the reactions that produce the selected species           #
# - flag the species according to the reaction                         #
# - rewrite the destruction reactions for the flagged species          #
# - create proxies for the non-flagged species                         #
#                                                                      #
# The script uses the 'facmecha' function in the 'facsimile_funcs'     #
# module to extract the chemical equations from the mechanism          #
#                                                                      #
# IMPORTANT NOTE: THIS SCRIPT IS EXPERIMENTAL, AND HAS NOT BEEN        #
#                 PROPERLY TESTED OR DEBUGGED                          #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 0.9, may 2006                                                #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

import sys
import facsimile_funcs

# #################################################################### #

## This function extracts from a chemical mechanism all the
## reactions including a selected species. The mechanism is in the format
## of 'facmecha' function.
## The extracted mechanism is returned as a list with this format:
##                  [[list of production reactions],
##                   [list of destruction reactions]]
## All the products are ditched except when the product is the selected species
def findreactions(mecha,spec):

    # create a list for the extracted mechanism e two sublists
    # to contain the production and the destruction reactions
    newmecha = []; prodmecha = []; destrmecha = []
    # look into every equation in the mechanism and count
    # the occurence of the species in the equation
    for eq in mecha:
        neweq = []; reac = []; prod = []
        r = eq[1].count(spec)
        p = eq[2].count(spec)
        n = p - r

        # production reactions
        if n > 0:
            # rate coefficient
            neweq.append(eq[0])
            # reactants (excluding the selected species which
            # will be taken into account in the list of products)
            for i in eq[1]:
                if i != spec:
                    reac.append(i)
            neweq.append(reac)
            # products (only the selected species, taking into
            # account if the species is also a reactant)
            for j in range(0,n):
                prod.append(spec)
            neweq.append(prod)
            # append the production reaction to list
            prodmecha.append(neweq)

        # destruction reactions
        elif n < 0:
            # rate coefficient
            neweq.append(eq[0])
            # reactants which are not the selected species
            for i in eq[1]:
                if i != spec:
                    reac.append(i)
            # selected species (taking into account if it
            # is also a product)
            for j in range(0,abs(n)):
                reac.append(spec)
            neweq.append(reac)
            # append the destruction reaction to list
            destrmecha.append(neweq)

    # make list with the new mechanism and return it
    newmecha.append(prodmecha)
    newmecha.append(destrmecha)
    return newmecha

## This function modifies a chemical mechanism so that all
## the species which are not the selected species are substituted
## by a proxy (which is the species with the suffix 'p')
## The modified chemical mechanism is returned in this format:
##                  [[list of production reactions],
##                   [list of destruction reactions],
##                   [list of species changed]
##                   [list of proxies]]
def newreactions(mecha,spec):
    # list for the modified mechanism and for the old and the new
    # variables
    newmecha = [[],[]]
    specproxy = []; proxy = []
    # production (0) and destruction (1) reactions
    for i in range(0,2):
        # go through every equation in the lists of production and
        # destruction reactions
        for r in mecha[i]:
            # list for the modified equation and for the modified species
            neweq = []; newr = []
            # add the rate coefficients
            neweq.append(r[0])
            # add the reactants
            # change name if they are not the selected species
            # or if they are not in the list of parameters
            for sp in r[1]:
                # if species is selected species its name is not
                # modified
                if sp == spec:
                    newsp = sp
                # otherwise modify the name of the species which is not the
                # selected species
                else:
                    # look for the new variable name in the list of new
                    # variables and if it is already there use the modified
                    # name
                    if sp in specproxy:
                        n = specproxy.index(sp)
                        newsp = proxy[n]
                    # if the variable is not presente in the list of new
                    # variables create a new variable name and add it to
                    # the list of new variables
                    else:
                        specproxy.append(sp)
                        proxy.append("p"+sp)
                        newsp = "p"+sp
                # add the species to the list of new species
                newr.append(newsp)
            # add reactants
            neweq.append(newr)
            # add products only for the production reactions
            if i == 0:
                neweq.append(r[2])
            # append the new equation to the list containing the new
            # mechanism
            newmecha[i].append(neweq)

    # add the lists with the old and new variables and return the list
    newmecha.append(specproxy)
    newmecha.append(proxy)
    return newmecha

## This function takes a list of species as input and add a
## flag to a selected species if it is in the list
## All the species in the list are then joined in a string by
## a plus sign (" + ").
def markspecies(speclist,spec,flag):
    eq = ""
    for s in speclist:
        if s == spec:
            s = s + "_" + flag
        eq = eq + s + " + "
    return eq.strip(" + ")

## This function prints the new mechanism to the output file
## For each production reaction the selected species is marked
## with a number and all the destruction reactions are rewritten using the
## marked species
## The equations are written in FACSIMILE format
## The function returns a list containing the last number used to mark the
## reactant, the list of marked species and the corresponding list of production
## reactions
def writemechanism(mecha,spec,n,outputfile):
    reslist = []; news = []; newsr = []
    i = 1; j = 1
    # for each production reaction write to file the production reaction and
    # all the destruction reactions
    for p in mecha[0]:
        outputfile.write("% " + p[0] + " : " + " + ".join(p[1]) +  " = " \
                 + markspecies(p[2],spec,str(i)) + " ;\n")
        # add the marked species to a list
        news.append(markspecies(p[2],spec,str(i)).split(' + ')[0])
        newsr.append(" + ".join(p[1]) +  " = " + markspecies(p[2],spec,str(i)))
        for d in mecha[1]:
            outputfile.write("S" + str(n) + " % " + d[0] + " : " + \
                             markspecies(d[1],spec,str(i)) + " = ;\n")
            n = n + 1
            j = j + 1
        outputfile.write("* ;\n")
        i = i + 1

    # delete the prefix "p" from the list of production
    # reactions before appending it to the output list
    newsrt = []
    for j in newsr:
        s = ""
        for i in j:
            if i != "p":
                s = s + i
        newsrt.append(s)

    # append the reaction counter, the list of marked species and
    # the corrected list of production reactions to the output list
    reslist.append(n)
    reslist.append(news)
    reslist.append(newsrt)
    return reslist

# #################################################################### #

# opening message
print """
.......................................................
: FACSIMILE TRACK 0.9                                 :
:                                                     :
: generate the FACSIMILE code to track the precursors :
: of a list of selected species                       :
:                                                     :
:  !!! WARNING -- EXPERIMENTAL SCRIPT -- WARNING !!!  :
:.....................................................:
"""

# get list of species
listspecies = facsimile_funcs.openlist('facsimile_track.in')

# file with mechanism is provided as script argument
if sys.argv[1:]:
    fname = sys.argv[1]
# file with mechanism is entered manually
else:
    print "enter name of the file with the mechanism"
    fname = raw_input("filename: ")
fin = open(fname, "r")
fname = fname + ".track"
fout = open(fname+".out", "w")
foutl = open(fname+"_legend.out", "w")

# read the input file in string
facstring = fin.read()

# call 'facmecha' function
# the function returns a list of the reactions in the mechanism
mechanism = []
mechanism =  facsimile_funcs.facmecha(facstring)

# write the mechanism to track the species of interest
num = 1
newvar = []; oldvar = []; newspec = []; newsreac = []
fout.write("* *************************************************** * ;\n")
fout.write("* TRACKING EQUATIONS\n* ;\n")
for species in listspecies:
    outlist = []
    # use 'findreactions' function to extract the list of all production and
    # destruction reactions of the selected species in the mechanism
    # then input this list to 'newreactions' function to rewrite the mechanism
    # adding a suffix ('p') to all the species except the selected ones
    newmechanism = newreactions(findreactions(mechanism,species),species)
    fout.write("* tracking " + species + "\n")
    # create a list with the new variables and the new parameters
    for s in newmechanism[3]:
        if s not in newvar:
            newvar.append(s)
            oldvar.append(newmechanism[2][newmechanism[3].index(s)])
    fout.write("* ;\n")
    # write the new mechanism to the output file
    outlist = writemechanism(newmechanism,species,num,fout)
    num = outlist[0]
    newspec = newspec + outlist[1]
    newsreac = newsreac + outlist[2]
    num = num + 1

# output list of new species
fout.write("* *************************************************** * ;\n")
fout.write("* TRACKING SPECIES\n* ;\nVARIABLE\n")
facsimile_funcs.listblock(newspec,fout)
fout.write(" ;\n* ;\n")

# output list of new variables
fout.write("* *************************************************** * ;\n")
fout.write("* TRACKING VARIABLES\n* ;\nPARAMETER\n")
facsimile_funcs.listblock(newvar,fout)
fout.write(" ;\n* ;\n")

# output list of new species
fout.write("* *************************************************** * ;\n")
fout.write("* Reaction Rates Parameters\n* ;\nPARAMETER\n")
param = []
for p in range(1,num-1):
    param.append("S"+str(p))
facsimile_funcs.listblock(param,fout)
fout.write(" ;\n* ;\n")

# output new algebraic equations
fout.write("* *************************************************** * ;\n")
fout.write("* NEW EQUATIONS\n* ;\n")
for i in newvar:
    fout.write(i + " = " + oldvar[newvar.index(i)] + " ;\n")
fout.write("* ;\n")

# write the list of new variables and the corresponding
# production reactions to output files
foutl.write("reaction_code\treaction\n")
for i in range(0,len(newspec)):
    foutl.write(newspec[i]+"\t"+newsreac[i]+"\n")

# close files
fin.close()
fout.close()
foutl.close()
print "\n--- output written to", fname+".out", "---"
print "--- legend written to", fname+"_legend.out", "---\n"
