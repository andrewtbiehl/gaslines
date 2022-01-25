"""
Tasks module used by the Invoke task execution tool. Run `invoke --list` from the
command line for more information on which tasks are available to run.
"""


import collections
import functools
import inspect
import sys

import invoke


# Simple shell script that replaces empty standard output with a custom message
# Used as a wrapper for commands that print nothing upon success
REPLACE_EMPTY_STDOUT_SCRIPT = """\
output=$({command}); code=$?;
if [ $code -eq 0 ] && [ -z "$output" ]; then output="{message}"; fi
echo "$output" && exit $code
"""


PROSELINT_IGNORED_PATHS = (
    r"\./\.git/",
    r"\./\.pytest_cache/",
)


PROSELINT_IGNORED_PATHS_REGEX = f"^({'|'.join(PROSELINT_IGNORED_PATHS)})"


PROSELINT_IGNORED_ERRORS = (
    r"typography\.symbols\.copyright",
    r"typography\.symbols\.curly_quotes",
    r"\./\.yamllint\.yaml:18:14: garner\.phrasal_adjectives\.ly",
)


PROSELINT_IGNORED_ERRORS_REGEX = f"({'|'.join(PROSELINT_IGNORED_ERRORS)})"


# Shell script that runs proselint on a filtered list of files and then filters out
# false positive errors
PROSELINT_CHECK_SCRIPT = f"""\
checked_files=$(find . -type f | grep --extended-regexp --invert-match \
"{PROSELINT_IGNORED_PATHS_REGEX}");
raw_output=$(echo "$checked_files" | xargs proselint);
output=$(echo "$raw_output" | grep --extended-regexp --invert-match \
"{PROSELINT_IGNORED_ERRORS_REGEX}");
code=$(expr 1 - $?);
if [ $code -eq 0 ]; then output="No prose issues found!"; fi
echo "$output" && exit $code;
"""


# Shell script pipes output from a command to ydiff to enable prettier diff printing
# The command must support the `--in-place` flag for modifying files
# Intended for use by the format task
FORMAT_AND_PRETTY_PRINT_DIFF_SCRIPT = """\
success="All files left unchanged!"
error="The following changes were made:"
disclaimer="Disclaimer: this tool is imperfect; further changes may be required."
output=$({base_command} | ydiff --pager=cat --color=always);
if [ -z "$output" ]; then
  echo "$success";
else
  {base_command} --in-place;
  echo "$error\n\n$output\n\n$disclaimer";
fi
"""


# Shell script pipes output from a command to ydiff to enable prettier diff printing
# Intended for use by the check task
CHECK_AND_PRETTY_PRINT_DIFF_SCRIPT = """\
success="{message}"
error="The following changes would be made:"
output=$({command}); code=1 && [ -z "$output" ] && code=0;
if [ $code -eq 0 ]; then
  output="$success"
else
  output=$(echo "$output" | ydiff --pager=cat --color=always);
  output="$error\n\n$output";
fi
echo "$output" && exit $code
"""


ERADICATE_CHECK_COMMAND = "eradicate . --recursive --aggressive"


AUTOFLAKE_CHECK_COMMAND = " ".join(
    (
        "autoflake",
        ".",
        "--expand-star-imports",
        "--remove-all-unused-imports",
        "--remove-duplicate-keys",
        "--remove-unused-variables",
        "--recursive",
    ),
)


PYBETTER_FORMAT_COMMAND = "pybetter . --exclude B004"


ERADICATE_SUCCESS_MESSAGE = "No commented-out code found!"


AUTOFLAKE_SUCCESS_MESSAGE = "No unused code found!"


ISORT_SUCCESS_MESSAGE = "No import order issues found!"


LINTER_SUCCESS_MESSAGE = "No code quality issues found!"


TOOL_LIST_HEADER = "Currently, this includes:" + "\n"


PARAGRAPH_SEPARATOR = "\n" * 2


# A list of formatter tools to run
# The keys are the tool names and the values are the shell commands
FORMATTERS = collections.OrderedDict(
    (
        (
            "eradicate",
            FORMAT_AND_PRETTY_PRINT_DIFF_SCRIPT.format(
                base_command=ERADICATE_CHECK_COMMAND,
            ),
        ),
        (
            "autoflake",
            FORMAT_AND_PRETTY_PRINT_DIFF_SCRIPT.format(
                base_command=AUTOFLAKE_CHECK_COMMAND,
            ),
        ),
        (
            "pybetter",
            PYBETTER_FORMAT_COMMAND,
        ),
        ("black", "black ."),
        (
            "isort",
            REPLACE_EMPTY_STDOUT_SCRIPT.format(
                command="isort .",
                message=ISORT_SUCCESS_MESSAGE,
            ),
        ),
    ),
)


# A list of check tools to run
# The keys are the tool names and the values are the shell commands
CHECKS = collections.OrderedDict(
    (
        (
            "validate python",
            REPLACE_EMPTY_STDOUT_SCRIPT.format(
                command="find . -type f -name '*.py' | xargs check-ast",
                message="No python syntax issues found!",
            ),
        ),
        ("black", "black . --check"),
        (
            "flake8",
            REPLACE_EMPTY_STDOUT_SCRIPT.format(
                command="flake8 .",
                message=LINTER_SUCCESS_MESSAGE,
            ),
        ),
        (
            "isort",
            REPLACE_EMPTY_STDOUT_SCRIPT.format(
                command="isort . --check-only",
                message=ISORT_SUCCESS_MESSAGE,
            ),
        ),
        (
            "pylint",
            REPLACE_EMPTY_STDOUT_SCRIPT.format(
                command="pylint tasks.py gaslines tests",
                message=LINTER_SUCCESS_MESSAGE,
            ),
        ),
        (
            "yamllint",
            REPLACE_EMPTY_STDOUT_SCRIPT.format(
                command="yamllint --format=colored .",
                message=LINTER_SUCCESS_MESSAGE,
            ),
        ),
        (
            "vulture",
            REPLACE_EMPTY_STDOUT_SCRIPT.format(
                command="vulture",
                message=LINTER_SUCCESS_MESSAGE,
            ),
        ),
        (
            "eradicate",
            CHECK_AND_PRETTY_PRINT_DIFF_SCRIPT.format(
                command=ERADICATE_CHECK_COMMAND,
                message=ERADICATE_SUCCESS_MESSAGE,
            ),
        ),
        (
            "proselint",
            PROSELINT_CHECK_SCRIPT,
        ),
        (
            "autoflake",
            CHECK_AND_PRETTY_PRINT_DIFF_SCRIPT.format(
                command=AUTOFLAKE_CHECK_COMMAND,
                message=AUTOFLAKE_SUCCESS_MESSAGE,
            ),
        ),
        (
            "pybetter",
            " ".join((PYBETTER_FORMAT_COMMAND, "--noop --exit-code 1")),
        ),
    ),
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
    task_function.__signature__ = prepend_context_parameter(signature)  # noqa: V101


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
    def task_function(context, *args, **kwargs):  # noqa: V107
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


def create_bulleted_list(items, bullet="-"):
    """
    Returns a text-based bulleted list of the given items.

    Args:
        items (iterable): The items to add to the text-based list.
        bullet (str): The choice of bullet to use. Defaults to "-".

    Returns:
        str: A bulleted, newline delimited list of the given items.
    """
    return "\n".join(f"{bullet} {item}" for item in items)


def append_to_docstring(content):
    """
    Appends the given content to the docstring of the decorated function.

    Args:
        content (str): The text to append to the decorated function's docstring.

    Returns:
        function: A standard function decorator.
    """

    def wrapper(function):
        function.__doc__ += content  # noqa: V101
        return function

    return wrapper


def create_bulleted_tool_list(tools):
    """
    Helper function that returns a text-based bulleted list of the given tools.

    Args:
        tools (OrderedDict): The tools whose names (the keys) will be added to the
            text-based list.

    Returns:
        str: A bulleted list of tool names.
    """
    return TOOL_LIST_HEADER + create_bulleted_list(tools.keys())


def append_tool_list_to_docstring(tools):
    """
    Helper function that appends a list of the given tools to the docstring of the
    annotated task function.

    Args:
        tools (OrderedDict): The tools to add as a bulleted list to the docstring.

    Returns:
        function: A standard function decorator.
    """
    return append_to_docstring(PARAGRAPH_SEPARATOR + create_bulleted_tool_list(tools))


@task(use_context=False, name="format")
@append_tool_list_to_docstring(FORMATTERS)
def format_():
    """Runs all formatting tools configured for use with this project."""
    print("----FORMAT-----------------------")
    execute_sequentially(FORMATTERS)


@task(use_context=False)
@append_tool_list_to_docstring(CHECKS)
def check():
    """Runs all code checks configured for use with this project."""
    print("----CHECK------------------------")
    execute_sequentially(CHECKS)


@task(use_context=False)
def test(coverage=None):
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
    """Helper function that runs a shell command and reports on whether it failed"""
    return invoke.run(command, pty=True, warn=True).failed
