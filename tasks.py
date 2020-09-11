import invoke


@invoke.task(name="format")
def format_(context):
    print("No formatting yet!")


@invoke.task
def check(context):
    print("No checks yet!")


@invoke.task
def test(context):
    print("No tests yet!")
