from invoke import Collection
from inv_plus import *

@vftask
def bar():
    print "enter bar"
    run_ctx("echo bar arg1={arg1} arg2={arg2}")
    print "exiting bar"

@vftask
def foo(arg1=None, arg2=None):
    print "enter foo"
    print "entering update"
    with UpdateContext(clean_dict(vars())):
        run_ctx("echo arg1={arg1} arg2={arg2}")
        bar()
    print "exited update"
    bar()
    print "exiting foo"

ns = Collection(foo, bar)
ns.configure({"arg1":"default", 'arg2':'default'})
