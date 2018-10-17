import logging
import os.path
import subprocess
import sys
import threading
import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import timedelta

import robot
import yaml
from sortedcontainers import SortedDict

from robotb.framework_consts import ROBOT_FRAMEWORK_DATETIME_FORMAT, PARAMETER_DRY_RUN, PARAMETER_DISABLE_LOG, \
    PARAMETER_DISABLE_HTML, PARAMETER_ENABLE_OUTPUT_TO_DEFAULT, PARAMETER_OUTPUT_DIR_TEMP
from robotb.helper import flatten
from robotb.test import Test

TEMP_FOLDER = ".robot-test-balancer"


def load_config():
    stream = open('config.yaml', 'r')
    return yaml.load(stream)


def get_test_data_from_output_file(file):
    root = ET.parse(file).getroot()
    suite = root.find("suite")
    tests = []

    for test in suite.iter("test"):
        name = test.attrib["name"]
        tags = [tag.text for tag in test.find("tags").iter("tag")]

        status = test.find("status")
        start_time = datetime.strptime(status.attrib["starttime"], ROBOT_FRAMEWORK_DATETIME_FORMAT)
        end_time = datetime.strptime(status.attrib["endtime"], ROBOT_FRAMEWORK_DATETIME_FORMAT)
        duration = end_time - start_time

        tests.append(Test(name=name, tags=tags, duration=duration))

    return sorted(
        tests,
        key=lambda x: x.duration,
        reverse=True
    )


def run_tests_dry(arguments):
    robot.run_cli(
        flatten(
            [
                PARAMETER_DRY_RUN,
                PARAMETER_DISABLE_LOG,
                PARAMETER_DISABLE_HTML,
                PARAMETER_ENABLE_OUTPUT_TO_DEFAULT,
                PARAMETER_OUTPUT_DIR_TEMP,
                arguments
            ]
        ),
        exit=False
    )


def run_tests(id, tests, variables, arguments):
    params = list(flatten([
        PARAMETER_OUTPUT_DIR_TEMP,
        [["-v", name + ":" + value] for name, value in variables.items()],
        [["-t", test.name.replace(" ", "_")] for test in tests],
        ["-o", id + "_output.xml"],
        ["-r", id + "_output.html"],
        ["-b", id + "_debug.txt"],
        arguments
    ]))

    logging.info("calling robot with following arguments: " + " ".join(params))

    try:
        pid = subprocess.Popen(["python", "-m", "robot"] + params)
        status = pid.wait()
    except:
        logging.exception("ups")


def balance_tests_on_maschines(maschines, loads):
    for name, maschine in maschines.items():
        maschine["estimated_run_time"] = timedelta(0)
        maschine["tests"] = []

    sorted_maschines = SortedDict(lambda x: maschines[x]["estimated_run_time"], maschines)

    for load in loads:

        load_assigned = False

        for name, maschine in sorted_maschines.items():

            if not set(load.tags) & set(maschine["blacklist-tags"]):
                maschine["tests"].append(load)
                maschine["estimated_run_time"] += load.duration
                load_assigned = True
                sorted_maschines.update({name: maschine})
                break

        if not load_assigned:
            logging.warning(f"unabled to assign testcase [{load.name}] to any maschine.")

    return maschines


def run(arguments):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    config = load_config()

    # get test data
    run_tests_dry(arguments)

    balanced_tests = balance_tests_on_maschines(
        config["maschines"],
        get_test_data_from_output_file(os.path.join(TEMP_FOLDER, "output.xml"))
    )

    threads = []

    for name, maschine in balanced_tests.items():
        logging.info(
            f"maschine [{name}] will run following tests: [{[test.name for test in maschine['tests']]}] "
            f"with a total estimted running time of [{maschine['estimated_run_time']}]."
        )

        threads.append(threading.Thread(target=run_tests, args=(name, maschine['tests'], maschine['variables'], arguments)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()



if __name__ == '__main__':
    run(sys.argv[1:])
