from fabric.contrib.files import upload_template
from task import YmlParser

__author__ = 'Conan Dooley'

from fabric.api import *
import os.path

@task
def deploy_config(config_file=None):
    env.shell = ""
    if config_file is None:
        config_file = os.path.dirname(os.path.realpath(__file__)) + "/../config/config.yml"
    tasks = YmlParser().parse(config_file)
    for task in tasks:
        for config in task.configs:
            upload_template(config.source, config.destination, config.options)
        for command in task.commands:
            run(command, shell=False)