# #################################################################### #
#                                                                      #
# FACSIMILE EXPCORRECT                                                 #
#                                                                      #
# Script to fix a formatting issue in some FACSIMILE output files:     #
# if the exponent of number in scientific format has 3 digits or more, #
# the 'e' or 'E' is sometimes omitted:                                 #
# e.g.:                                                                #
#       1.234-100 instead of 1.234e-100                                #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 1.3, may 2020                                                #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

import sys
import re

# #################################################################### #

def expcorr(fname):

    # open I/O files
    fin = open(fname, "r")
    fname = fname+".out"
    fout = open(fname, "w")

    # read file into string
    finstr = fin.read()

    # use regular expression to replace all occurences of the wrong
    # exponential format (e.g.: 1.234-100) with the correct one
    newfinstr = re.sub(r'\B(\d)(-)(\d\d\d)\b',r'\1e\2\3',finstr)

    # save processed file
    fout.write(newfinstr)
    fin.close()
    fout.close()
    print "\n--- output written to", fname, "---\n"


# #################################################################### #

print """
.......................................................
: FACSIMILE EXPCORRECT v1.3                           :
:                                                     :
: fix the exponential format issue (e.g., 1.234-100)  :
: in FACSIMILE output files                           :
:.....................................................:
"""

## FACSIMILE output files to process (script argument)
if sys.argv[1:]:
    for f in sys.argv[1:]:
        expcorr(f)
