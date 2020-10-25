"""
AUTHOR: IPvZero
Date: 25th Oct 2020
Purpose: This script references my Youtube video on Desired State
"""

from nornir import InitNornir
from nornir_scrapli.tasks import netconf_edit_config
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file

nr = InitNornir(config_file="config.yaml")


def load_vars(task):
    """
    Load host variables and bind them to a per-host dict key called "facts"
    """

    data = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yaml")
    task.host["facts"] = data.result
    config_eigrp(task)


def config_eigrp(task):
    """
    Build EIGRP template based on IOS-XE YANG Model
    Push configuration over NETCONF
    """

    eigrp_template = task.run(
        task=template_file,
        name="Buildling EIGRP Configuration",
        template="eigrp.j2",
        path="./templates",
    )
    eigrp_output = eigrp_template.result
    task.run(task=netconf_edit_config, target="running", config=eigrp_output)


result = nr.run(task=load_vars)
print_result(result)
