"""
The python progressbar library is useful but nonstandard. This
wraps it, providing a progressbar if possible, and a more basic
progress reading if not.
"""


try:
    from progressbar import ProgressBar, Percentage, Bar, ETA
    got_progressbar = True
except ImportError:
    got_progressbar = False


class Progress(object):

    def __init__(self, maxval, name=None, visible=True,
                 use_progressbar=got_progressbar):

        self.visible = visible
        self.use_progressbar = use_progressbar

        if not self.visible:
            pass

        elif self.use_progressbar:
            widgets = [Percentage(), Bar(), ETA()]
            if name is not None:
                widgets = [name] + widgets
            self.pbar = ProgressBar(widgets=widgets, maxval=maxval)

        else:
             self.maxval = maxval
             self.name = name

    def __enter__(self):
        if not self.visible:
            pass
        elif self.use_progressbar:
            self.pbar.start()
        else:
            if self.name is not None:
                print self.name
        return self

    def update(self, i):
        if not self.visible:
            pass
        elif self.use_progressbar:
            self.pbar.update(i)
        else:
            print "  %d/%d (%.2f%%)"%(i, self.maxval, 100.0*i/self.maxval)

    def __exit__(self, t, v, b):
        if not self.visible:
            pass
        elif self.use_progressbar:
            self.pbar.finish()



def progressrange(n, name=None, use_progressbar=got_progressbar, visible=True):

    with Progress(n, name=name, use_progressbar=use_progressbar, visible=visible) as p:
        for i in xrange(n):
            yield i
            p.update(i+1)
