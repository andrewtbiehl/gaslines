import invoke, sys


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
def test(context):
    print("----TEST-------------------------")
    print(" * pytest")
    print()
    failed = execute("pytest")
    sys.exit(failed)


def execute(command):
    """
    Helper function that runs a shell command and reports on whether it failed
    """
    return invoke.run(command, pty=True, warn=True).failed
