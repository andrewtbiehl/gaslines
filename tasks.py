import sys

import invoke


# Simple shell script that replaces empty standard output with a custom message
# Used as a wrapper for commands that print nothing upon success
REPLACE_EMPTY_STDOUT_SCRIPT = """\
output=$({command}); code=$?;
if [ $code -eq 0 ] && [ -z "$output" ]; then output="{message}"; fi
echo "$output" && exit $code
"""


ISORT_SUCCESS_MESSAGE = "No import order issues found!"


@invoke.task(name="format")
def format_(context):
    print("----FORMAT-----------------------")
    print(" * black")
    print()
    failed = execute("black .")
    print()
    print(" * isort")
    print()
    # Upon isort success, print a message because isort doesn't do so on its own
    isort_command = REPLACE_EMPTY_STDOUT_SCRIPT.format(
        command="isort .", message=ISORT_SUCCESS_MESSAGE
    )
    failed = execute(isort_command) or failed
    sys.exit(failed)


@invoke.task
def check(context):
    print("----CHECK------------------------")
    print(" * black")
    print()
    failed = execute("black . --check")
    print()
    print(" * flake8")
    print()
    # Upon flake8 success, print a message because flake8 doesn't do so on its own
    flake8_command = REPLACE_EMPTY_STDOUT_SCRIPT.format(
        command="flake8 .", message="No code quality issues found!"
    )
    failed = execute(flake8_command) or failed
    print()
    print(" * isort")
    print()
    # Upon isort success, print a message because isort doesn't do so on its own
    isort_command = REPLACE_EMPTY_STDOUT_SCRIPT.format(
        command="isort . --check-only", message=ISORT_SUCCESS_MESSAGE
    )
    failed = execute(isort_command) or failed
    sys.exit(failed)


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


def execute(command):
    """
    Helper function that runs a shell command and reports on whether it failed
    """
    return invoke.run(command, pty=True, warn=True).failed
