from invhelpers import run_ctx

# TODO: make __call__ kwargs turn in to named options...
# e.g.:
# cp("/tmp/a", "/tmp/b", r=None) => cp -r /tmp/a /tmp/b
# foo("arg1", "arg2", s=None, long="val") => foo -s --long=val arg1 arg2
class Command(object):
    def __init__(self, name, fmt, nargs):
        self.fmt = fmt
        self.nargs = nargs
    def __call__(self, *args, **kw):
        if len(callargs) != self.nargs:
            raise Exception("Not enough arguments to command" + self.__name__)
        wrap = kw.get('wrap', None)
        if wrap is not None:

            command = wrap.format(self.fmt)
        else:
            command = self.fmt

        command = command.format(*callargs)
        return run_ctx(command)

class Sudo(Command):
    def __init__(self):
        self.fmt = "sudo {}"
        self.nargs = 1

    def __call__(self, what, *args, **kw):
        if isinstance(what, Command):
            return what(wrap=self.fmt, *args, **kw)
        else:
            super(Sudo, self).__call__(what,*args, **kw)

cp = Command("cp", "cp {} {}", 2)
sudo = Sudo()
