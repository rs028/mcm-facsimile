mcm-facsimile
=============

Python (http//www.python.org/) programs for the manipulation of a
chemical mechanisms in FACSIMILE format
(http://www.mcpa-software.com/). Developed for use with the Master
Chemical Mechanism (http://mcm.leeds.ac.uk/MCM/).


DESCRIPTION
-----------

1) facsimile_funcs.py:
   contains functions used by the other scripts.

2) facsimile_var.py:
   extracts the list of species in a chemical mechanism and calculates
   the number of species and the number of reactions in a chemical
   mechanism.

3) facsimile_rate.py:
   finds all the reactions in a chemical mechanism that produce and
   consume a list of species, then creates a new group of parameters
   and writes the FACSIMILE code that can be inserted in the model to
   calculate the rates of production and destruction of the selected
   species.

4) facsimile_check.py:
   checks a model for two common errors which cause FACSIMILE to crash
   (lines longer than 72 characters and tabs instead of spaces).

5) facsimile_expcorr.py:
   fixes a formatting issue with exponential numbers in some FACSIMILE
   output files.


REQUIREMENTS & INSTALLATION
---------------------------

All you need to run the scripts is to have Python (version < 2.7) on
your system. If it is not already installed, you can download it at
http://www.python.org/. Note that these scripts will not work with
Python 3.0 or later. Download the files in a directory of your
choice.


USAGE
-----

Put the file with the model or the mechanism in the same directory of
the scripts. Open a console (DOS Prompt or Command Prompt under
Windows, shell under Linux/Unix), move into the directory and type:

    python <scriptname>.py

where <scriptname> is 'facsimile_var', 'facsimile_rate',
'facsimile_check', 'facsimile_expcorr'. Then follow the
instructions.

IMPORTANT: facsimile_funcs.py must always be in the same directory as
the other script files otherwise they will not work.
