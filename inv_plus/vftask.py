from invoke import Task
from invoke.context import Context
import ctx_mod

class VFTask(Task):
    def __init__(self, *args, **kw):
        super(VFTask, self).__init__(*args,**kw)
        self.contextualized = True

    def __call__(self, *args, **kw):
        #print "CALLING VFTASK"
        do_push = False
        if len(args) and isinstance(args[0], Context):
            do_push = True
            newargs = args[1:]
        else:
            newargs = args

        if do_push:
            ctx_mod.push_ctx(args[0])
        result = self.body(*newargs, **kw)
        self.times_called += 1
        if do_push:
            ctx_mod.pop_ctx()
        return result

    def get_arguments(self):
        self.contextualized = False
        res = super(VFTask, self).get_arguments()
        self.contextualized = True
        return res

# OPERATE THE SAME as invoke.task, but use VFTask instead of Task
def vftask(*args, **kw):
    # @task -- no options were (probably) given.
    # Also handles ctask's use case when given as @ctask, equivalent to
    # @task(obj, contextualized=True).
    if len(args) == 1 and callable(args[0]) and not isinstance(args[0], Task):
        return VFTask(args[0], **kw)
    # @task(pre, tasks, here)
    if args:
        if 'pre' in kw:
            raise TypeError("May not give *args and 'pre' kwarg simultaneously!")
        kw['pre'] = args
    # @task(options)
    # TODO: pull in centrally defined defaults here (see Task)
    name = kw.pop('name', None)
    contextualized = kw.pop('contextualized', False)
    aliases = kw.pop('aliases', ())
    positional = kw.pop('positional', None)
    optional = tuple(kw.pop('optional', ()))
    default = kw.pop('default', False)
    auto_shortflags = kw.pop('auto_shortflags', True)
    help = kw.pop('help', {})
    pre = kw.pop('pre', [])
    post = kw.pop('post', [])
    autoprint = kw.pop('autoprint', False)
    # Handle unknown kw
    if kw:
        kwarg = (" unknown kw %r" % (kw,)) if kw else ""
        raise TypeError("@task was called with" + kwarg)
    def inner(obj):
        obj = VFTask(
            obj,
            name=name,
            contextualized=contextualized,
            aliases=aliases,
            positional=positional,
            optional=optional,
            default=default,
            auto_shortflags=auto_shortflags,
            help=help,
            pre=pre,
            post=post,
            autoprint=autoprint,
        )
        return obj
    return inner

