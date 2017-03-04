# #################################################################### #
#                                                                      #
# FACSIMILE MODIFIER                                                   #
#                                                                      #
# This program performs a number of operations necessary to assemble   #
# an MCM model in FACSIMILE format:                                    #
#                                                                      #
# 1. check that all parameters are present only once                   #
# 2. separates list of constraints from list of variables              #
# 3. check that all RO2 and PANs are included in their summation terms #
# 4. extracts list of dry deposition terms                             #
# 5. exc
#                                                                      #
# Reference files (from MCMv3.1 box model) are :                       #
# ro2.mcm      -> RO2 in MCM                                           #
# pan.mcm      -> PANs in MCM                                          #
# depterm.mcm  -> dry deposition terms in MCM                          #
#                                                                      #
# Subset files are :                                                   #
# var.subset    -> variables in subset                                 #
# const.subset  -> constraints in subset                               #
# ro2.subset    -> RO2 in subset                                       #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 0.9, january 2008                                            #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

# load modules
import facsimile_funcs

## This function checks that there are no doubles in the lists of  parameters
## (RO2, PANs, Deposition Terms) in the MCM and in the lists of parameters
## (variables, RO2) in the subset
def var_decl():

    # load the list of parameters 
    ro2_mcm = facsimile_funcs.openlist("ro2.mcm")
    pan_mcm = facsimile_funcs.openlist("pan.mcm")
    depterm_mcm = facsimile_funcs.openlist("depterm.mcm")
    var_sub = facsimile_funcs.openlist("var.subset")
    ro2_sub = facsimile_funcs.openlist("ro2.subset")
    
    # finds parameters that are present more than once in a the lists
    n_ro2_mcm = facsimile_funcs.listcount(ro2_mcm)
    n_pan_mcm = facsimile_funcs.listcount(pan_mcm)
    n_depterm_mcm = facsimile_funcs.listcount(depterm_mcm)
    n_var_sub = facsimile_funcs.listcount(var_sub)
    n_ro2_sub = facsimile_funcs.listcount(ro2_sub)

    # check that all parameters in the MCM lists are present only once
    if len(n_ro2_mcm) != 0:
        print "!!! warning !!! there are multiple variables in ro2.mcm" 
        print n_ro2_mcm
    if len(n_pan_mcm) != 0:
        print "!!! warning !!! there are multiple variables in pan.mcm" 
        print n_pan_mcm
    if len(n_depterm_mcm) != 0:
        print "!!! warning !!! there are multiple variables in depterm.mcm" 
        print n_depterm_mcm

    # check that all parameters in the subset are present only once
    if len(n_var_sub) != 0:
        print "!!! warning !!! there are multiple variables in var.subset" 
        print n_var_sub
    if len(n_ro2_sub) != 0:
        print "!!! warning !!! there are multiple variables in ro2.subset" 
        print n_ro2_sub
 

## This function checks that all the constraints of the subset are
## declared then removes them from the list of variables and creates
## a FACSIMILE input routine
def constr_var(fname):
    
    # load list of variables and of constraints in the subset
    var_sub = facsimile_funcs.openlist("var.subset")
    constr_sub = facsimile_funcs.openlist("constr.subset")

    # check that all the constraints are in the list of variables
    constrlist = facsimile_funcs.complist(var_sub,constr_sub)[5]    
    if len(constrlist) != 0:
        print "!!! warning !!! some constraints have not been declared"
        print constrlist

    # take all variables not included in the constraints list
    new_varlist = facsimile_funcs.complist(var_sub,constr_sub)[3]

    # write to output file the list of variables without the constraints
    fname.write("* ;\n* *** Variables *** ;\n* ;\nVARIABLE\n")
    facsimile_funcs.listblock(new_varlist,fname)
    fname.write(" ;")

    # write to file list of constraints
    fname.write("\n* ;\n* *** Constrained Parameters *** ;\n* ;\nPARAMETER\n")
    facsimile_funcs.listblock(constr_sub,fname)
    fname.write(" ;")

    # create and write to file the FACSIMILE input instructions
    fname.write("\n* ;\n* *** Input Routine *** ;\n* ;\nCOMPILE INP ;\n* ;\n")
    for c in constr_sub:
        fname.write("READ 4 " + c + " ;\n")
    fname.write("* ;\n** ;\n* ;")

## This function checks that all RO2 and PANs are included in their
## summation terms
def sum_terms(fname):

    # load the list of RO2 in MCM and lists of variables and RO2 in subset
    ro2_mcm = facsimile_funcs.openlist("ro2.mcm")
    pan_mcm = facsimile_funcs.openlist("pan.mcm")
    var_sub = facsimile_funcs.openlist("var.subset")
    ro2_sub = facsimile_funcs.openlist("ro2.subset")

    # compare the list of RO2 and PANs in the MCM with variables in subset
    ro2_comp = facsimile_funcs.complist(ro2_mcm,var_sub)
    pan_comp =  facsimile_funcs.complist(pan_mcm,var_sub)

    # compare the list of RO2 in subset with list derived by
    # comparison with variables in subset
    ro2_final = facsimile_funcs.complist(ro2_sub,ro2_comp[2])
    
    # write the list of RO2 and PANs in the subset to file
    fname.write("\n*** list of RO2 in subset ***\n\n")
    facsimile_funcs.listblock(ro2_comp[2],fname)
    fname.write("\n\n*** list of PANs in subset ***\n\n")
    facsimile_funcs.listblock(pan_comp[2],fname)

    # write an error message if the list of RO2 in subset is different
    # from the list derived by comparison with variables in subset
    if ro2_final[3] != '' or ro2_final[5] !='':
        fname.write("\n\n***** ERRORS *****\n")
        fname.write("\n\tRO2 in the subset but not in the MCM list:\n")
        facsimile_funcs.listblock(ro2_final[3],fname)
        fname.write("\n\n\tRO2 in the MCM list but not in the subset:\n")
        facsimile_funcs.listblock(ro2_final[5],fname)

## This function extracts the list of dry deposition terms from the variables of
## of the subset
def dep_terms(fname):

    # load the list of variables in subset and file with the dry deposition
    # terms in the MCM
    var_sub = facsimile_funcs.openlist("var.subset")
    fin_dep = open("depterm.mcm","r")

    # write header to output file
    fname.write("\n*** list of Dry Deposition Terms in subset ***\n\n")
    for line in fin_dep.readlines():
        
        # split the dry deposition term in rate coefficient (line[0])
        # and equation (line[1])
        line = line.split(':')
        
        # extracts the name of the species from the equation
        eq = line[1].split('=')
        species = eq[0].replace(' ','')
        
        # reassemble the dry deposition term for the species
        # present in the subset and write to output file 
        if species in var_sub:
            fname.write(line[0] + " : " + line[1])

# #################################################################### #
# opening message
print """
.......................................................
: facsimile_mod 0.9                                   :
:   :
:.....................................................:
"""

# menu
# 1. check that all parameters are present only once                   #
# 2. separates list of constraints from list of variables              #
# 3. check that all RO2 and PANs are included in their summation terms #
# 4. extracts list of dry deposition terms                             #

#
print "choose operation:\n"
print "[1]\t check variables"
print "[2]\t check constraints"
print "[3]\t check sum terms"
print "[4]\t find dry deposition terms"
op = raw_input("? ")

#
if op == '1':
    var_decl()

# 
elif op == "2":
    fout = open("facsimile_mod.out","w")
    constr_var(fout)
    fout.close()
    print "\n--- output written to facsimile_mod.out ---\n"

#
elif op == '3':
    fout = open("facsimile_mod.out","w")
    sum_terms(fout)
    fout.close()
    print "\n--- output written to facsimile_mod.out ---\n"

#
elif op == '4':
    fout = open("facsimile_mod.out","w")
    dep_terms(fout)
    fout.close()
    print "\n--- output written to facsimile_mod.out ---\n"

#
else:
    print "input error"
