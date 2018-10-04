import os.path
from collections import Iterable
import xml.etree.ElementTree as ET

import robot

TEST_FOLDER = "tests"
TEMP_FOLDER = ".robot-test-balancer"

PARAMETER_DRY_RUN = "--dryrun"
PARAMETER_DISABLE_LOG = ["-l", "NONE"]
PARAMETER_DISABLE_HTML = ["-r", "NONE"]
PARAMETER_ENABLE_OUTPUT = ["-o", "output.xml"]
PARAMETER_OUTPUT_DIR_TEMP = ["-d", TEMP_FOLDER]

def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x


def get_test_data_from_suite(root):
    for suite in root.iter("suite"):

        print(suite.attrib["id"])

        for test in suite.iter("test"):
            name = test.attrib["name"]

            for tag in test.find("tags").iter("tag"):
                print(tag.text)

            duration_in_ms = 0


def get_test_data_from_output_file():
    tree = ET.parse(os.path.join(TEMP_FOLDER, "output.xml"))
    root = tree.getroot()

    test_data = get_test_data_from_suite(root.find("suite"))

def dry_run():
    robot.run_cli(
        flatten(
            [
                PARAMETER_DRY_RUN,
                PARAMETER_DISABLE_LOG,
                PARAMETER_DISABLE_HTML,
                PARAMETER_ENABLE_OUTPUT,
                PARAMETER_OUTPUT_DIR_TEMP,
                TEST_FOLDER
            ]
        ),
        exit=False
    )

def wet_run():
    robot.run_cli(
        flatten(
            [
                PARAMETER_DISABLE_LOG,
                PARAMETER_DISABLE_HTML,
                PARAMETER_ENABLE_OUTPUT,
                PARAMETER_OUTPUT_DIR_TEMP,
                TEST_FOLDER
            ]
        ),
        exit=False
    )

if __name__ == "__main__":




    #if os.path.isfile(os.path.join(TEMP_FOLDER, "output.xml")):

    dry_run()
    get_test_data_from_output_file()
