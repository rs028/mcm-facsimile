# #################################################################### #
#                                                                      #
# FACSIMILE TIMECODE                                                   #
#                                                                      #
# Script to generate the FACSIMILE code for the time control of a      #
# FACSIMILE model and calculate the correct input/output times         #
#                                                                      #
# If the timesteps are irregular, they must be listed in an input      #
# file called: 'timecode.in'                                           #
#                                                                      #
# #################################################################### #
#                                                                      #
# version 1.4, may 2021                                                #
#                                                                      #
# author: R.S.                                                         #
#                                                                      #
# #################################################################### #

import textwrap
import facsimile_funcs

# #################################################################### #

# function for regular timesteps
def regular_time():

    # model time information
    gmt = raw_input('enter timezone [+4]: ')
    t_delay = raw_input('enter minutes of delay [02:30]: ')
    start_time = raw_input('enter start hour [00:00]: ')
    stop_time = raw_input('enter stop hour [24:00]: ')
    n_days = raw_input('enter number of days [2]: ')
    time_step = raw_input('enter time step [30]: ')
    n_iter = raw_input('enter number of iterations [2]: ')

    # check initial values and set defaults
    if gmt == '':
        gmt = +4
    else:
        gmt = int(gmt)

    if t_delay == '':
        t_delay = '02:30'

    if start_time == '':
        start_time = '00:00'

    if stop_time == '':
        stop_time = '24:00'

    if n_days == '':
        n_days = 2
    else:
        n_days = int(n_days)

    if time_step == '':
        time_step = 30
    else:
        time_step = int(time_step)

    if n_iter == '':
        n_iter = 2
    else:
        n_iter = int(n_iter)

    # convert to seconds
    t_delay = t_delay.split(':')
    t_delay = int(t_delay[0])*60 + int(t_delay[1])

    gmt = gmt*3600

    start_time = start_time.split(':')
    start_time = int(start_time[0])*3600 + int(start_time[1])*60

    stop_time = stop_time.split(':')
    stop_time = (n_days-1)*86400 + int(stop_time[0])*3600 + int(stop_time[1])*60

    time_step = time_step*60

    # total time of the model run
    run_time = (stop_time-start_time) - time_step
    total_time = (stop_time-start_time)*(n_iter-1) + run_time

    # time constant due to minutes of delay and timezone
    time_lag = t_delay + gmt

    # time of the first input and output
    first_output = run_time*(n_iter-1) + time_step*(n_iter-1) + time_lag
    n_output = run_time/time_step

    # number of inputs and outputs
    first_input = start_time + time_step + time_lag
    n_input = (total_time-time_step)/time_step

    # number of times to rewind the input file
    rewind_time = run_time + time_step + time_lag
    n_rewind = n_iter - 2

    # print FACSIMILE code
    print "\n----------"
    print "FACSIMILE code:"
    print "----------"
    print "* ;\nWHENEVER"
    print "TIME =", first_output, "+", time_step, "*", n_output, " % CALL OUTP ;"
    print "TIME =", first_input, "+", time_step, "*", n_input, " CALL INP RESTART ;"
    if n_iter == 2:
        print "TIME =", rewind_time, " CALL REWP RESTART ;"
    if n_iter > 2:
        print "TIME =", rewind_time, "+", rewind_time, "*", n_rewind, " CALL REWP RESTART ;"
    print "* ;\n** ;"
    print "----------"

# function for irregular timesteps
def irregular_time():

    # open file 'timecode.in' containing the irregular time steps
    time_points = facsimile_funcs.openlist("timecode.in")

    # add time steps to FACSIMILE code
    time_series_out = " ".join(time_points)
    time_series_in = " ".join(time_points[1:])

    time_code_out = "TIME = " + time_series_out + " % CALL OUTP ;"
    time_code_in = "TIME = " + time_series_in + " CALL INP RESTART ;"

    # print FACSIMILE code
    print "\n----------"
    print "FACSIMILE code:"
    print "----------"
    print "* ;\nWHEN"
    print textwrap.fill(time_code_out)
    print textwrap.fill(time_code_in)
    print "* ;\n** ;"
    print "----------"

# #################################################################### #

print """
.......................................................
: FACSIMILE TIMECODE v1.4                             :
:                                                     :
: generate the FACSIMILE code for the time control    :
: of a model                                          :
:.....................................................:
"""

print "[1]\t regular timesteps"
print "[2]\t irregular timesteps"
op = raw_input("? ")

if op == "1":
    regular_time()
elif op == "2":
    irregular_time()
else:
    print "----- input error -----"
