import invoke
import sys


@invoke.task(name="format")
def format_(context):
    print("----FORMAT-----------------------")
    print(" * black")
    print()
    failed = execute("black .")
    sys.exit(failed)


@invoke.task
def check(context):
    print("----CHECK------------------------")
    print(" * black")
    print()
    failed = execute("black . --check")
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
