#!/usr/bin/python
# Submit Spinach Job.py
# 2014/07/30 Kevin Claytor
#            kec30@duke.edu
import os, pwd, sys, argparse
from subprocess import call

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

def get_base_filename(inputfile):
    path, filename = os.path.split(inputfile)
    basename = os.path.splitext(filename)[0]
    return basename

def make_submission_script(args, mscript):
    basename = get_base_filename(args.input)
    newfile = 'sspy_%s.q' % basename
    out = open(newfile, 'w')
    # Assemble the script
    # Header
    out.write('#!/bin/tcsh\n')
    out.write('#\n')
    out.write('#$ -S /bin/tcsh -cwd\n')
    # write the output
    if True:
        outputline = '#$ -o %s.log\n' % (basename)
        out.write(outputline)
    # Direct the error
    if True:
        errorline = '#$ -e %s_errors.log\n' % (basename)
        out.write(errorline)
    # If we want to run a highprio job specify the node
    if not args.lowprio:
        out.write('#$ -l highprio\n')
        nodeline = '#$ -q *@%s\n' % (args.highprio)
        out.write(nodeline)
    # Email the user
    # TODO: debug with the -u option
    if args.email:
        emailline = '#$ -M %s%s -m e\n' % (args.user, args.domain)
        out.write(emailline)
    # Finally the matlab script to run
    out.write('\n')
    mainline = '%s -nodisplay -r "%s"\n' % (args.matlab, mscript)
    out.write(mainline)
    out.close()
    return newfile

def make_matlab_script(args):
    basename = get_base_filename(args.input)
    # New way, return a string of commands
    help_header = r"fprintf('Starting...\n'); "
    # Make sure to specify the full path, not relative path
    spinachadd = "addpath_recurse(fullfile(pwd, '%s')); " % (args.spinach)
    # We don't want the .m in the matlab script call
    path, filename = os.path.split(args.input)
    changedir = "cd '%s'; " % (path)
    runscript = "%s; " % (basename)
    # spmd is throwing erross, found this to be helpful;
    # http://www.mathworks.com/matlabcentral/newsreader/view_thread/300734
    #disablespmd = "distcomp.feature('LocalUseMpiexec',false); "
    #disablespmd_par = "mypool = parpool('SpmdEnabled', false); "
    start_custom_pool = "newPool = parpool('local'); myPool = parcluster('local'); "
    kill_old_parjobs = "delete(myPool.Jobs); "
    help_footer = r"fprintf('Done.\n'); "
    help_quit = r"quit;"
    matlabfile = help_header + spinachadd + changedir + start_custom_pool + kill_old_parjobs + runscript + help_footer + help_quit
    return matlabfile

def parse_args():
    # Some useful constants
    matlabpath = '/opt/apps/matlabR2014a/bin/matlab'
    spinachpath = 'spinach_1.4.2114'
    prionode = 'warren-n09'
    username = get_username()
    domain = '@duke.edu'
    # Begin parsing the input arguments
    description_string = 'SPINACH submission script for SGE Queuing system. 2014-07-30 Kevin Claytor kec30@duke.edu.'
    parser = argparse.ArgumentParser(description=description_string)

    parser.add_argument('-i', '--input', help='Full path to file you want to run', required=True)

    # Set the priority
    priogroup = parser.add_mutually_exclusive_group()
    highprio_help_string = 'Request priority node. Default: %s' % (prionode)
    priogroup.add_argument('-l','--lowprio', help='Low Priority (no node request)', required=False, action='store_true')
    priogroup.add_argument('-p','--highprio', help=highprio_help_string, required=False, default=prionode)

    # Email the user options
    emailgroup = parser.add_mutually_exclusive_group()
    emailgroup.add_argument('-e','--email', help='Email when script finsishes (automatic if -u is used)', action='store_true')
    user_help_string = 'NetID to e-mail to if other than username (%s)' % (username)
    emailgroup.add_argument('-u','--user', help=user_help_string, required=False, default=username)
    user_domain_string = 'Domain to e-mail to if other than default (%s)' % (domain)
    parser.add_argument('-d','--domain', help=user_domain_string, required=False, default=domain)

    # Matlab path options
    matlab_help_string = 'Full path to version of Matlab you want to use. Default: %s)' % (matlabpath)
    parser.add_argument('-m','--matlab', help=matlab_help_string, required=False, default=matlabpath)
    spinach_help_string = 'Full path to version of SPINACH you want to use. Default: %s)' % (spinachpath)
    parser.add_argument('-s','--spinach', help=spinach_help_string, required=False, default=spinachpath)

    # Do the heavy lifitng
    args = parser.parse_args()
    # For debugging
    verbalize_input_parser(args)
    return args

def submit_job(scriptfile):
    call(['qsub', scriptfile])
    return True

def verbalize_input_parser(args):
    # Help function that spits out all the input file files
    print 'Preparing the script located at %s' % (args.input)
    if args.lowprio:
        print 'Running low priority'
    else:
        print 'Running high priority on node: %s' % (args.highprio)
    if args.email:
        print 'Emailing the user at: %s%s' % (args.user, args.domain)
    print 'Using matlab located at: %s' % (args.matlab)
    print 'Using spinach located at: %s' % (args.spinach)
    return True

if __name__ == "__main__":
    args = parse_args()
    # Make the matlab file to submit
    mfile = make_matlab_script(args)
    # Make the submission script
    scriptfile = make_submission_script(args, mfile)
    # Now submit the job
    submit_job(scriptfile)
