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
    with open("/tmp/.dkube_job.ini", "w") as f:
        config.write(f)
    return config
    
def dkube_run():
    signal.signal(signal.SIGTERM, sigterm_handler)
    config = update_job_name()
    print ("**************************************************************************************")
    print ("DKube training dashboard: " + config['CUSTOM_JOB']["dkubeURL"] + "/#/ds/jobs/trainings")
    print ("**************************************************************************************")
    return os.system ("/project/dkubectl customjob start -c /tmp/.dkube_job.ini")