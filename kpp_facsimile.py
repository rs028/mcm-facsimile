# #################################################################### #
#                                                                      #
# KPP FACSIMILE                                                        #
#                                                                      #
# Script to convert a chemical mechanism to/from FACSIMLE/KPP formats  #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 0.9, october 2022                                            #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

import sys
import re

# #################################################################### #

## function to convert KPP to FAC
def kpp2fac(reaclist):
    varlist = []
    for reac in reaclist:
        xx = re.split(r"[}:;]", reac)
        kk = re.sub(r'J\((\d+)\)', r'J<\1>', xx[2])
        kk = kk.replace('**', '@')
        yy = "%" + kk + ":" + xx[1] + ";\n"
        varlist.append(yy)
    return varlist

## function to convert FAC to KPP
def fac2kpp(reaclist):
    varlist = []
    i = 1
    for reac in reaclist:
        xx = re.split(r"[%:;]", reac)
        kk = re.sub(r'J<(\d+)>', r'J(\1)', xx[1])
        kk = kk.replace('@', '**')
        yy = "{" + str(i) + ".}" + xx[2] + ":" + kk + ";\n"
        i = i + 1
        varlist.append(yy)
    return varlist

# #################################################################### #

print """
.......................................................
: KPP FACSIMILE  v0.9                                 :
:                                                     :
: convert FAC to KPP/ KPP to FAC                      :
:.....................................................:
"""

# input file (script argument or enter manually)
if sys.argv[1:]:
    fname = sys.argv[1]
else:
    print "-> name of mechanism file:"
    fname = raw_input("-> ")
fin = open(fname, "r")
fname = fname+".out"
fout = open(fname, "w")

# read mechanism file into list
finlist = fin.readlines()

# get mechanism file extension
fext = fname.split(".")[1]

# convert to kpp format
if fext == "fac":
    mechlist = fac2kpp(finlist)
# convert to fac format
elif fext == "kpp":
    mechlist = kpp2fac(finlist)
else:
    print "file not recognized"

# save
for r in mechlist:
    fout.write(r)

# close files
fin.close()
fout.close()
print "\n--- output written to", fname, "---\n"
