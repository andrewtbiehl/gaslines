import sys
from collections import OrderedDict

import invoke


# Simple shell script that replaces empty standard output with a custom message
# Used as a wrapper for commands that print nothing upon success
REPLACE_EMPTY_STDOUT_SCRIPT = """\
output=$({command}); code=$?;
if [ $code -eq 0 ] && [ -z "$output" ]; then output="{message}"; fi
echo "$output" && exit $code
"""


ISORT_SUCCESS_MESSAGE = "No import order issues found!"


# A list of formatter tools to run
# The keys are the tool names and the values are the shell commands
FORMATTERS = OrderedDict(
    (
        ("black", "black ."),
        (
            "isort",
            REPLACE_EMPTY_STDOUT_SCRIPT.format(
                command="isort .", message=ISORT_SUCCESS_MESSAGE
            ),
        ),
    )
)


# A list of check tools to run
# The keys are the tool names and the values are the shell commands
CHECKS = OrderedDict(
    (
        ("black", "black . --check"),
        (
            "flake8",
            REPLACE_EMPTY_STDOUT_SCRIPT.format(
                command="flake8 .", message="No code quality issues found!"
            ),
        ),
        (
            "isort",
            REPLACE_EMPTY_STDOUT_SCRIPT.format(
                command="isort . --check-only", message=ISORT_SUCCESS_MESSAGE
            ),
        ),
    )
)


@invoke.task(name="format")
def format_(context):
    print("----FORMAT-----------------------")
    execute_sequentially(FORMATTERS)


@invoke.task
def check(context):
    print("----CHECK------------------------")
    execute_sequentially(CHECKS)


@invoke.task
def test(context, coverage=None):
    print("----TEST-------------------------")
    # Run tests
    print(" * pytest")
    print()
    failed = execute("coverage run -m pytest")
    # Print coverage report
    print()
    print(" * coverage")
    print()
    failed = execute("coverage report") or failed
    if coverage == "write":
        # Write coverage report to file, ignore threshold
        failed = execute("coverage html --fail-under=0") or failed
    elif coverage == "upload":
        # Upload coverage; fails if not run in GitHub Actions context
        print()
        failed = execute("coveralls") or failed
    failed = execute("rm .coverage") or failed
    sys.exit(failed)


def execute_sequentially(commands):
    """
    Helper function that runs a sequence of provided shell commands, prints their
    associated names simultaneously, and returns an error if any command failed.

    Args:
        commands (OrderedDict): Essentially a sequence of shell commands to execute.
            The values are the actual commands and the keys are their names.
    """
    failed = False
    for name, command in commands.items():
        print(f" * {name}")
        print()
        failed = execute(command) or failed
        print()
    sys.exit(failed)


def execute(command):
    """
    Helper function that runs a shell command and reports on whether it failed
    """
    return invoke.run(command, pty=True, warn=True).failed
