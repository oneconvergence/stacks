from __future__ import print_function
import os, sys
import ptvsd
import argparse
from dkube_job import dkube_run
import train

if __name__ == "__main__":
    run_in_dkube = os.environ.get("RUN_IN_DKUBE", "false")

    if run_in_dkube == "true":
        exit_code = dkube_run()
        sys.exit (exit_code)
        
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()

    if args.debug:
        ptvsd.enable_attach(redirect_output=True)
        print ("Debugger: waiting...")
        ptvsd.wait_for_attach()

    train.main()
