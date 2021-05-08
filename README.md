mcm-facsimile
=============

Python (https://www.python.org/) programs for the manipulation of
chemical mechanisms in FACSIMILE format (https://www.mcpa-software.com/).

Developed for use with the Master Chemical Mechanism (MCM,
http://mcm.leeds.ac.uk/MCM/).


DESCRIPTION
-----------

1) facsimile_check.py:  
   check a FACSIMILE model for common errors which cause FACSIMILE
   to crash.

2) facsimile_expcorr.py:  
   fix the exponent issue in FACSIMILE output files.

3) facsimile_funcs.py:  
   module of functions used by the `mcm-facsimile` scripts.

4) facsimile_rate.py:  
   generate the FACSIMILE code to calculate the rates of production
   and destruction of selected species.

5) facsimile_timecode.py:  
   generate the FACSIMILE code for the time control of a model.

6) facsimile_track.py **[EXPERIMENTAL SCRIPT]**:  
   generate the FACSIMILE code to track the precursors of selected
   species.

7) facsimile_var.py:  
   create the list of species in a chemical mechanism and
   calculate the number of species and of reactions.

8) listcomparison.py:  
   compare two lists of variables.


REQUIREMENTS & INSTALLATION
---------------------------

A basic installation of Python (version 2.7.x) is needed to run the
scripts. Note that the scripts do not work with Python 3.x, although
they can be easily converted, if needed, as explained here:
https://docs.python.org/3/library/2to3.html

Download the `mcm-facsimile` archive file
(https://github.com/rs028/mcm-facsimile/archive/refs/heads/master.zip)
and unzip it in a directory of choice.

**IMPORTANT:** the module file `facsimile_funcs.py` must always be
kept in the same directory as the `mcm-facsimile` scripts.


USAGE
-----

Open a console (DOS Prompt or Command Prompt under Windows, Terminal
under Linux/Unix/macOS), move into the directory containing the
`mcm-facsimile` scripts and type:

    python2 <scriptname>.py

where <scriptname> is `facsimile_check`, `facsimile_var`, etc...

Some scripts have arguments and some require input files. Check the
script header for details.
