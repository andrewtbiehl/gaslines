"""
Tasks module used by the Invoke task execution tool. Run `invoke --list` from the
command line for more information on which tasks are available to run.
"""


import functools
import inspect
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


CONTEXT_PARAMETER = inspect.Parameter("context", inspect.Parameter.POSITIONAL_ONLY)


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


def prepend_context_parameter(signature):
    """
    Helper function that returns a Signature identical to the one given, with the one
    exception of having an additional initial positional parameter named 'context'.

    Args:
        signature (Signature): Any function signature.

    Returns:
        Signature: A new signature with a new initial 'context' parameter.
    """
    parameters = signature.parameters.values()
    parameters_with_context = (CONTEXT_PARAMETER, *parameters)
    return signature.replace(parameters=parameters_with_context)


def prepend_context_parameter_to_signature(task_function):
    """
    Helper function that patches the signature of a given Invoke task function under
    the assumption that it is erroneously missing the function's initial context
    parameter.

    The new context parameter is (unsurprisingly) named 'context'.

    Args:
        task_function (function): A function to be used as an Invoke task that happens
            to have an erroneous signature.
    """
    # Implementation details inspired by the examples provided in recipe 9.11 of
    # "Python Cookbook" (2013) by Brian Jones and David Beazley
    signature = inspect.signature(task_function)
    task_function.__signature__ = prepend_context_parameter(signature)


def create_task_function(function):
    """
    Helper function that returns a function identical to the one given, with the only
    difference being that the returned function has an initial dummy context parameter
    and therefore can be used to create an Invoke task.

     The new context parameter is (unsurprisingly) named 'context'.

    Args:
        function (function): A function to be used as an Invoke task despite missing
            an initial context parameter.

    Returns:
        function: A function with an initial dummy context parameter.
    """

    @functools.wraps(function)
    def task_function(context, *args, **kwargs):
        # The `context` variable is just a dummy and may be immediately removed
        del context
        return function(*args, **kwargs)

    prepend_context_parameter_to_signature(task_function)
    return task_function


def task(_function=None, *args, use_context=True, **kwargs):  # pylint: disable=W1113
    """
    Replacement Invoke task decorator that enables the decorating of task functions
    that don't have an initial context parameter. In all other ways this decorator is
    identical to Invoke's own `task` decorator.

    The Invoke execution tool requires that all task functions include an initial
    context parameter, even if that parameter is not referenced anywhere in the
    function body. If, on the other hand, the `use_context` parameter is set to False
    in this decorator, then the decorated function does not need (and should not have)
    a context parameter.

     The new context parameter is (unsurprisingly) named 'context'.

    Args:
        _function (function, optional): The task function to decorate. This parameter
            need not be set explicitly. Defaults to None.
        use_context (bool): Whether the function has an initial Invoke context
            parameter. Defaults to True. If not set to False then this decorator
            behaves identically to the Invoke equivalent.
        *args: Argument list passed directly to the Invoke task decorator.
        **kwargs: Keyword argument list passed directly to the Invoke task decorator.

    Returns:
        function, Task: A decorator to apply to a task function if the function was
            not yet supplied. Otherwise, returns the Invoke Task object resulting from
            the decorator having been already applied to the task function.
    """
    task_decorator = invoke.task(*args, **kwargs)
    # Add a dummy context parameter to the function if it doesn't have one already
    if not use_context:
        task_decorator = compose(task_decorator, create_task_function)
    # Enable usage of the decorator both with and without parentheses
    return task_decorator if _function is None else task_decorator(_function)


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
