import numpy as np

class MainAxis:

    def __init__(self, collection, ax, fig):
        self.collection = collection
        self.ax = ax
        self.fig = fig
        self.clear()

    def plot(self):
        self.clear()
        self.ax.plot(self.collection.df[self.collection.X_label], self.collection.df[self.collection.Y_label], '.')
        self.ax.set_xlabel(self.collection.X_label)
        self.ax.set_ylabel(self.collection.Y_label)

    def clear(self):
        self.ax.cla()
        self.ax.grid(True)

    def draw(self):
        self.fig.canvas.draw_idle()

class HistAxes:

    def __init__(self, collection, label, ax, fig, nbin):
        self.collection = collection
        self.ax = ax
        self.fig = fig
        if label in ['X_label', 'Y_label']:
            self._label = label
        else:
            raise ValueError(f"Unknown label provided: {label}")
        self.nbin = nbin

    @property
    def orientation(self):
        if self._label == 'X_label':
            return 'vertical'
        else:
            return 'horizontal'

    @property
    def axis(self):
        return self.collection.__getattribute__(self._label)

    def plot(self, nbin=None):
        self.clear()
        if nbin is None:
            nbin = self.nbin
        _, bins, _ = self.ax.hist(self.collection.df[self.axis], bins=nbin, orientation = self.orientation)
        self.nbin = len(bins) -1
        self.draw()

    def increase_nbins(self, x):
        nbin = int(np.ceil(1.25 * self.nbin))
        self.plot(nbin=nbin)

    def decrease_nbins(self, x):
        nbin = max( [ int(np.floor(0.75 * self.nbin)), 1 ] )
        self.plot(nbin = nbin)

    def clear(self):
        self.ax.cla()

    def draw(self):
        self.fig.canvas.draw_idle()


