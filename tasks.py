from invoke import task


@task
def lint(c):
    c.run("flake8 flake8_no_debug_vars.py tests --max-line-length 100")
    c.run("black flake8_no_debug_vars.py tests --check")
    c.run("isort flake8_no_debug_vars.py tests --profile black --check")


@task
def test(c):
    c.run("pytest --cov=.  --cov=tests --cov-report=xml --cov-report=html tests")
