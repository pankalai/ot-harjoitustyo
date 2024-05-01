from invoke import task

 
@task
def test(ctx):
    ctx.run("pytest src")

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest")
    
@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")
    
@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src")
    
@task(format)
def lint(ctx):
    ctx.run("pylint src")
    
@task
def build(ctx):
    ctx.run("python3 src/build.py")
  
@task
def start(ctx):
    ctx.run("python src/index.py")