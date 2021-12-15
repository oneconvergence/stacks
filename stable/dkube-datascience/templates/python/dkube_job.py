import os, sys
import signal
import configparser, yaml, time
from dkube.sdk import *

def sigterm_handler(_signo, _stack_frame):
    print("sigterm_handler executed, %s, %s" % (_signo, _stack_frame))
    sys.exit(0)
    
def dkube_run():
    signal.signal(signal.SIGTERM, sigterm_handler)
    y = yaml.safe_load(open(".appsody-config.yaml"))
    config = configparser.ConfigParser()
    config.read('.dkube_job.ini')

    c = config["JOB"]
    tags = c["tags"].split(",")
    api = DkubeApi(URL=c["dkubeURL"],token=c["token"], common_tags=tags)
    info = api.validate_token()
    username = info["username"]
    training_name = generate(c["name"])
    training = DkubeTraining(username, name=training_name)
    training.update_container(framework="tensorflow_2.6.0", image_url=c["image"])

    datasets = c["datasets"].split(",") if c["datasets"] else []
    models = c["models"].split(",") if c["models"] else []
    tags = c["tags"].split(",") if c["tags"] else []
    envs = c["envs"].split(",") if c["envs"] else []

    for dataset in datasets:
        training.add_input_dataset(dataset, "/mnt/datasets/"+dataset)
    for model in models:
        training.add_output_model(model, "/mnt/models/"+model)
    
    vars = {}
    for env in envs:
        parts = env.split(":")
        vars[parts[0]] = parts[1]
    training.add_envvars(vars=vars)

    api.create_training_run(training)