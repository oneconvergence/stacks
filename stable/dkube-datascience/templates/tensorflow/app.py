from __future__ import print_function
import ptvsd
import argparse
import tensorflow as tf
import os, sys
import signal
import configparser, yaml, time

def sigterm_handler(_signo, _stack_frame):
    print("sigterm_handler executed, %s, %s" % (_signo, _stack_frame))
    sys.exit(0)

def update_job_name():
    #generage uniq job name
    y = yaml.safe_load(open(".appsody-config.yaml"))
    config = configparser.ConfigParser()
    config.read('.dkube_job.ini')
    config['CUSTOM_JOB']["name"] = '"{}"'.format(y["project-name"] + "-" + time.strftime("%Y%m%d-%H%M%S"))
    with open(".dkube_job.ini", "w") as f:
        config.write(f)

if __name__ == "__main__":
    run_in_dkube = os.environ.get("RUN_IN_DKUBE", "false")

    if run_in_dkube == "true":
        signal.signal(signal.SIGTERM, sigterm_handler)
        update_job_name()
        exit_code = os.system ("/project/dkubectl customjob start -c .dkube_job.ini")
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