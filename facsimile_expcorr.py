# #################################################################### #
#                                                                      #
# EXPCORRECT                                                           #
#                                                                      #
# Program to fix a formatting issue in some FACSIMILE output files: in   #
# exponential format, 'e' or 'E' can be omitted when a negative        #
# exponent has more than 3 digits.                                     #
# e.g.:                                                                #
#       1.234-100 instead of 1.234e-100                                #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 1.2, november 2010                                           #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

# load modules
import re, sys

## Function to fix the exponential format in FACSIMILE output files
def expcorr(fname):

    # open I/O files
    fin = open(fname, "r")
    fname = fname+".1"
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
# opening message
print """
.......................................................
: expcorrect 1.2                                      :
:                                                     :
: fix the exponential format issue (e.g., 1.234-100)  :
: in FACSIMILE output files                             :
:.....................................................:"""

## list of files is provided as script argument
if sys.argv[1:]:
    for f in sys.argv[1:]:
        expcorr(f)

## list of files is manual input (comma separated list)
else:
    print "\nenter name of FACSIMILE output file(s) to process"
    print ">> separate multiple files with commas <<"
    filename = raw_input("name of file(s): ")
    for f in filename.split(','):
        expcorr(f)
