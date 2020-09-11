import invoke


@invoke.task(name="format")
def format_(context):
    print("----FORMAT-----------------------")
    print(" * black")
    print()
    context.run("black .", pty=True)


@invoke.task
def check(context):
    print("----CHECK------------------------")
    print(" * black")
    print()
    context.run("black . --check", pty=True)


@invoke.task
def test(context):
    print("No tests yet!")
