"""
Tasks module used by the Invoke task execution tool. Run `invoke --list` from the
command line for more information on which tasks are available to run.
"""


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
LINTER_SUCCESS_MESSAGE = "No code quality issues found!"


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
                command="flake8 .", message=LINTER_SUCCESS_MESSAGE
            ),
        ),
        (
            "isort",
            REPLACE_EMPTY_STDOUT_SCRIPT.format(
                command="isort . --check-only", message=ISORT_SUCCESS_MESSAGE
            ),
        ),
        (
            "pylint",
            REPLACE_EMPTY_STDOUT_SCRIPT.format(
                command="pylint tasks.py gaslines tests", message=LINTER_SUCCESS_MESSAGE
            ),
        ),
    )
)


def compose(outer_function, inner_function):
    """
    Utility function that returns the composition of two functions.

    Args:
        outer_function (function): A function that can take as input the output of
            `inner_function`.
        inner_function (function): Any function.

    Returns:
        function: The composition of `outer_function` with `inner_function`.
    """
    return lambda *args, **kwargs: outer_function(inner_function(*args, **kwargs))


@invoke.task(name="format")
def format_(context):  # pylint: disable=W0613
    """
    Runs all formatting tools configured for use with this project.

    Currently, this includes:
    - black
    - isort
    """
    print("----FORMAT-----------------------")
    execute_sequentially(FORMATTERS)


@invoke.task
def check(context):  # pylint: disable=W0613
    """
    Runs all code checks configured for use with this project.

    Currently, this includes:
    - black
    - flake8
    - isort
    """
    print("----CHECK------------------------")
    execute_sequentially(CHECKS)


@invoke.task
def test(context, coverage=None):  # pylint: disable=W0613
    """
    Runs tests and reports on the current the code coverage.

    Args:
        coverage (String): Optional argument for specifying what to do with the
            coverage report. If "write", writes out the report in html form. If
            "upload", uploads the report to coveralls. Otherwise, does nothing.
    """
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
