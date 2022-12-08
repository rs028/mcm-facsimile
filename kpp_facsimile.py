# #################################################################### #
#                                                                      #
# KPP FACSIMILE                                                        #
#                                                                      #
# Script to convert a chemical mechanism between the FACSIMLE and KPP  #
# formats.                                                             #
#                                                                      #
# Example of FACSIMILE format:                                         #
#   % 1.4D-12*EXP(-1310/TEMP) : NO + O3 = NO2 ;                        #
#   % J<4> : NO2 = NO + O ;                                            #
#                                                                      #
# Example of KPP format:                                               #
#   {7.} NO + O3 = NO2 : 1.4D-12*EXP(-1310/TEMP) ;                     #
#   {41.} NO2 = NO + O : J(4) ;                                        #
#                                                                      #
# N.B.: Only the chemical reactions are converted. Complex rate        #
# coefficients, declarations of variables, and comments are ignored.   #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 1.0, december 2022                                           #
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
        if re.match(r'{\d+\.}', reac):
            # KPP reaction
            reac1 = re.split(r'[}:;]', reac)
            # convert rate coefficient
            kk1 = re.sub(r'J\((\d+)\)', r'J<\1>', reac1[2])
            kk2 = kk1.replace('**', '@')
            # FAC reaction
            reac2 = "%" + kk2 + ":" + reac1[1] + ";\n"
            varlist.append(reac2)
    return varlist

## function to convert FAC to KPP
def fac2kpp(reaclist):
    varlist = []
    i = 1  # reaction counter
    for reac in reaclist:
        if re.match(r'%', reac):
            # FAC reaction
            reac1 = re.split(r'[%:;]', reac)
            # convert rate coefficient
            kk1 = re.sub(r'J<(\d+)>', r'J(\1)', reac1[1])
            kk2 = kk1.replace('@', '**')
            # KPP reaction
            reac2 = "{" + str(i) + ".}" + reac1[2] + ":" + kk2 + ";\n"
            i = i + 1
            varlist.append(reac2)
    return varlist

# #################################################################### #

print """
...................................................
: KPP FACSIMILE  v1.0                             :
:                                                 :
: convert a chemical mechanism from FAC to KPP or :
: from KPP to FAC                                 :
:.................................................:
"""

# input file (script argument or enter manually)
if sys.argv[1:]:
    fname = sys.argv[1]
else:
    print "-> name of mechanism file:"
    fname = raw_input("-> ")

# open I/O files
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
    print "\n--- mechanism format not recognized ---\n"

# save mechanism in new format
for reac in mechlist:
    fout.write(reac)
print "\n--- mechanism saved to", fname, "---\n"

# close files
fin.close()
fout.close()
