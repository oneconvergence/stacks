from __future__ import print_function
import ptvsd
import argparse
import tensorflow as tf
import os, sys

if __name__ == "__main__":
    run_in_dkube = os.environ("RUN_IN_DKUBE", "false")

    if run_in_dkube == "true":
        exit_code = os.system ("dkubectl customjob start -c .dkube_job.ini")
        sys.exit (exit_code)
        
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()

    if args.debug:
        ptvsd.enable_attach(redirect_output=True)
        print ("Debugger: waiting...")
        ptvsd.wait_for_attach()
        

    # Simple hello world using TensorFlow

    # Create a Constant op
    # The op is added as a node to the default graph.
    #
    # The value returned by the constructor represents the output
    # of the Constant op.
    hello = tf.constant('Hello, TensorFlow!')

    # Start tf session
    sess = tf.Session()

    # Run the op
    print(sess.run(hello))