# ##################################################################### #
#                                                                       #
# FACSIMILE FUNCTIONS                                                   #
#                                                                       #
# Module of functions for the 'mcm-facsimile' scripts:                  #
#                                                                       #
# - facmecha  : extract the chemical equations from a mechanism         #
# - ropa      : find the chemical equations containing a given species  #
# - listblock : output formatted list of variables                      #
# - openlist  : read file of variables into a list                      #
# - complist  : compare two lists of variables                          #
# - listcount : find multiple variables in a list                       #
#                                                                       #
# ##################################################################### #
#                                                                       #
# version 1.4, july 2008                                                #
#                                                                       #
# author: R.S.                                                          #
#                                                                       #
# ##################################################################### #

import re
import textwrap

# ******************************************************************** #
# FACMECHA function
#
# This function parses a FACSIMILE code for chemical equations
# and extracts species and rate coefficients to a list
# Chemical equations in FACSIMILE have the following formats:
#
# % k1 : A + B = C + D ;
#
# or for equilibrium reactions:
#
# % k2 % k3 : E + F = G + H ;
#
# Some models also have a reaction rate parameter in front of '%'
# S1 % k1 : A + B = C + D ;
#
# The function returns a matrix with three columns:
#
# [ k1  [A, B]  [C, D] ]
# [ k2  [E, F]  [G ,H] ]
# [ k3  [G, H]  [E, F] ]

def facmecha(strfac):

    # regular expression to recognize the equations
    # in FACSIMILE format
    refac = r'''
                (^\w*\s*? | ^) % # reactions begin with '%'
                                 # (skip commented reactions)
                                 # the reaction rate ('S1') is optional
                (.*?)      # rate coefficient
                (%(.*?))?  # optional rate coefficient of the backward reaction
                :          # delimiter rate coefficient/species
                (.*?)      # reactants
                =          # delimiter reactants/products
                (.*?)      # products
                ;          # reactions end with ';'
                '''

    # compile regular expression
    regexpfac = re.compile(refac, re.VERBOSE | re.MULTILINE | re.DOTALL)

    # initialize lists of reactants and products
    # and the list to be returned by the function (mecha)
    react = []
    prod = []
    mecha =[]

    # apply regular expression to 'strfac' string which contains the
    # chemical mechanism and find all the chemical equations
    for ifac in regexpfac.finditer(strfac):

        # extracts the reaction rate (group 1), the rate coefficients
        # of the forward (group 2) and backward reactions (group 4),
        # the reactants (group 5) and the products (group 6)
        # and delete the withespaces
        rr =  re.sub(r"\s+", '', ifac.group(1))
        kf = re.sub(r"\s+", '', ifac.group(2))
        kb = ifac.group(4)
        r = re.sub(r"\s+", '', ifac.group(5))
        p = re.sub(r"\s+", '', ifac.group(6))

        # create list of reactants and products
        react = r.split('+')
        prod = p.split('+')

        # initialize lists for the forward and backward reactions
        forweq = []
        backeq = []

        # if there is a backward reaction
        # delete whitespaces from backward rate coefficient
        if kb:
            kb =  re.sub(r"\s+", '', kb)

            # add to list for the forward reaction the rate coefficient
            # and the lists of reactants and products
            forweq.append(kf)
            forweq.append(react)
            forweq.append(prod)

            # add to list for the backward reaction the rate coefficient
            # and the lists of products and reactants
            backeq.append(kb)
            backeq.append(prod)
            backeq.append(react)

            # add the forward and backward reactions to the 'mecha' list
            mecha.append(forweq)
            mecha.append(backeq)

        # if there is no backward reaction
        else:

            # add to list for the forward reaction the rate coefficient
            # and the lists of reactants and products
            forweq.append(kf)
            forweq.append(react)
            forweq.append(prod)

            # add the forward and backward reactions to the 'mecha' list
            mecha.append(forweq)

    # return the list of the reactions extracted
    return mecha

# ******************************************************************** #
# ROPA function
#
# This function extracts all the reactions containing a selected
# species in a chemical mechanism and assemble the expressions to
# calculate the reaction rates in FACSIMILE format.
# The chemical mechanism is a list extracted with the FACMECHA
# function with the format:
#
# [ rate coefficients  [reactants list]  [products list] ]
#
# The function returns a list containing the lists of the parameters,
# the lists of the expressions to calculate the reaction rates in
# FACSIMILE format, two lists with the number code of the reactions
# involved and and a list with the definition of the parameters:
#
# [ [list of production parameters]
#   [list of destruction parameters]
#   [list of production expressions]
#   [list of destruction expressions]
#   [list of number codes of production reactions]
#   [list of number codes of destruction reactions]
#   [list of definitions of production parameters]
#   [list of definitions of destruction parameters] ]

def ropa(mecha,spec):

    # initialize a list for the parameters, a list for the definitions
    # of the parameters and a list for the result
    paramlist = []; defparamlist = []; resultlist = []

    # initialize counters
    i = 1; j =1; n = 0
    # lists of expressions to calculate the reaction rates
    rodlist = []; roplist = []
    # lists of parameters and definitions of parameters
    paramplist = []; paramdlist = []
    defparamplist = []; defparamdlist = []
    # lists of number codes of the reactions
    codeplist = []; codedlist = []

    # counts the number of times the selected species is in the
    # reactants (eq[1]) and in the products (eq[2]) for each reaction
    # of the mechanism and take the difference (n)
    for eq in mecha:
        n =  eq[2].count(spec) - eq[1].count(spec)

        # when n is positive the species is produced by the reaction
        # parameter name is: 'P_species_counter'
        # expression is 'parameter_name = n*rate coeff*species'
        # code number is the number of the reaction
        # definition of the parameter is: 'parameter_name : reaction'
        if n > 0:
            paramp = "P_" + spec.lower() + "_" + str(i)
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
            codeplist.append(mecha.index(eq)+1)
            i = i + 1

        # when n is positive the species is destroyed by the reaction
        # parameter name is: 'D_species_counter'
        # expression is 'parameter_name = n*rate coeff*species'
        # code number is the number of the reaction
        # the definition of the parameter is: 'parameter_name : reaction'
        elif n < 0:
            paramd = "D_" + spec.lower() + "_" + str(j)
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
            codedlist.append(mecha.index(eq)+1)
            j = j + 1

#     # create a list of parameters and a list of defintions of the parameters
#     paramlist = paramlist + paramplist + paramdlist
#     defparamlist = defparamlist + defparamplist + defparamdlist

    # create and return the list with the results
    resultlist.append(paramplist)
    resultlist.append(paramdlist)
    resultlist.append(roplist)
    resultlist.append(rodlist)
    resultlist.append(codeplist)
    resultlist.append(codedlist)
    resultlist.append(defparamplist)
    resultlist.append(defparamdlist)
    return resultlist

# ******************************************************************** #
# LISTBLOCK function
#
# This function output to a file a list of variables
# with 70 characters on each line

def listblock(varlist,outputfile):
    outstr = textwrap.fill(" ".join(varlist))
    outputfile.write(outstr)

# ******************************************************************** #
# OPENLIST function
#
# This function opens a file containing a list of variables
# and returns a list of the variables

def openlist(listname):

    # initialize list
    retlist = []

    # open file and read content into a string
    fin = open(listname,"r")
    retstr = fin.read()

    # split the string into a list
    retlist = retstr.split()

    # close the file and return list of variables
    fin.close()
    return retlist

# ******************************************************************** #
# COMPLIST function
#
# This function compares two lists of variables (list A and list B)
# and return a list with this format:
#
# [length A,
#  length B,
#  [elements in A and in B],
#  [elements in A not in B],
#  [elements in B and in A],
#  [elements in B not in A]]

def complist(listA,listB):

    # initialize lists
    AinB = []
    AnotB = []
    BinA = []
    BnotA = []
    resultlist = []

    # calculates length of the two lists
    nA = len(listA)
    nB = len(listB)

    # check elements in list A
    # elements which are also in list B --> AinB
    # elements which are not in list B --> AnotB
    for el in listA:
        el = el.upper()
        if el in listB:
            AinB.append(el)
        else:
            AnotB.append(el)

    # check elements in list B
    # elements which are also in list A --> BinA
    # elements which are not in list A --> BnotA
    for el in listB:
        el = el.upper()
        if el in listA:
            BinA.append(el)
        else:
            BnotA.append(el)

    # create list with results
    resultlist.append(nA)    # [0] n. elements in list A
    resultlist.append(nB)    # [1] n. elements in list B
    resultlist.append(AinB)  # [2] elements in list A which are also in list B
    resultlist.append(AnotB) # [3] elements in list A which are not in list B
    resultlist.append(BinA)  # [4] elements in list B which are also in list A
    resultlist.append(BnotA) # [5] elements in list B which are not in list A

    # return list of results
    return resultlist

# ******************************************************************** #
# LISTCOUNT function
#
# This function finds variables that are present more than once in a list
# and return a list with this format:
#
# [[variable, times in list], [variable, times in list], ...]

def listcount(flist):

    # initialize lists
    duplicatelist = []

    # count how many times each variable is present in the list
    for el in flist:
        n = flist.count(el)

        # add variables that are present more than once to the
        # list of results if not already there
        if n > 1:
            if [el,n] not in duplicatelist:
                duplicatelist.append([el,n])

    # return list with the multiple variables
    return duplicatelist
