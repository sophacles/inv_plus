import ctx_mod
from ctx_mod import ctx

def clean_dict(d):
    return {k:v for k,v in d.iteritems() if v is not None}

class UpdateContext(object):
    def __init__(self, *args):
        self.newargs = args

    def __enter__(self):
        new_ctx = ctx.clone()
        for updates in self.newargs:
            new_ctx.update(updates)
        ctx_mod.push_ctx(new_ctx)

    def __exit__(self, *args):
        ctx_mod.pop_ctx()
        return False

def run_ctx(format_string, **kw):
    command = format_string.format(**ctx.config['general'])
    ctx.run(command, **kw)

def start_or_restart(svcname, force_restart=False):
    x = ctx.run("sudo status {svcname}".format(**vars()), hide=True)
    status = x.stdout.split(',')[0].split(' ')[1]
    if 'running' in status:
        if force_restart:
            ctx.run("sudo stop {svcname}".format(**vars()))
            ctx.run("sudo start {svcname}".format(**vars()))
        else:
            ctx.run("sudo restart {svcname}".format(**vars()))
    else:
        ctx.run("sudo start {svcname}".format(**vars()))


