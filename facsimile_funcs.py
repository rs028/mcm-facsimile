# #################################################################### #
#                                                                      #
# FACSIMILE functions                                                  #
#                                                                      #
# This module contains functions to be used by the FACSIMILE tools:    #
# facsimile_var.py                                                     #
# facsimile_rate.py                                                    #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 1.0, december 2004                                           #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

# FACSIMILE MECHANISM function
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
# The function returns a matrix with three columns:
#
# [ k1  [A, B]  [C, D] ]
# [ k2  [E, F]  [G ,H] ]
# [ k3  [G, H]  [E, F] ]

def facmecha(strfac):

    # import modules
    import re, string

    # regular expression to recognize the equations
    # in FACSIMILE format
    refac = r'''
                ^%         # reactions begin with '%' (skip commented reactions)
                (.*?)      # rate coefficient
                (%(.*?))?  # optional rate coefficient of the backward reaction
                :          # delimiter rate coefficient/species
                (.*?)      # reactants
                =          # delimiter reactants/products
                (.*?)      # products
                ;          # reactions end with ';'
                '''

    # compile regular expression
    regexpfac = re.compile(refac, re.VERBOSE| re.MULTILINE | re.DOTALL)

    # initialize lists of reactants and products
    # and the list to be returned by the function (mecha)
    react = []
    prod = []
    mecha =[]
    
    # apply regular expression to 'strfac' string which contains the
    # chemical mechanism and find all the chemical equations
    for ifac in regexpfac.finditer(strfac):
        
        # extracts the rate coefficients of the forward (group 1) and
        # backward reactions (group 3), the reactants (group 4) and
        # the products (group 5) and delete the withespaces
        kf = re.sub(r"\s+", '', ifac.group(1))
        kb = ifac.group(3)
        r = re.sub(r"\s+", '', ifac.group(4))
        p = re.sub(r"\s+", '', ifac.group(5))

        # create list of reactants and products
        react = string.split(r,'+')
        prod = string.split(p, '+')

        # empty lists for the forward and backward reactions
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

            # add to list for the backward  reaction the rate coefficient
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

# LISTBLOCK function
#
# This function output to a file a list of variables
# writing 5 variables per line

def listblock(varlist,outputfile):
    i = 1
    for el in varlist:
        outputfile.write(el)
        if i == 5:
            outputfile.write("\n")
            i = 0
        else:
            outputfile.write(" ")
        i = i + 1
