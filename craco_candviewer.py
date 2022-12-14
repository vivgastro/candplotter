import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons
import argparse
import pandas as pd

HDR_keys = ['SNR', 'lpix', 'mpix', 'boxc_width', 'time', 'dm', 'iblk', 'rawsn', 'total_sample', 'obstime_sec', 'mjd', 'dm_pccm3', 'ra_deg', 'dec_deg']

class MyCollection(object):

    def __init__(self, df):
        self.df = df
        self.selections = []
        self.deletions = []
        #self.mask = ~(self.df == np.nan)
        self.keys = list(self.df.keys())
        self._X_label = self.keys[0]
        self._Y_label = self.keys[0]

    @property
    def X_label(self):
        return self._X_label

    def set_X_label(self, new_label):
        if new_label not in self.keys:
            raise ValueError(f"New X label {new_label} not in self.keys: {self.keys}")
        self._X_label = new_label
        print(f"Setting new X label as {self.X_label}")

    @property
    def Y_label(self):
        return self._Y_label

    def set_Y_label(self, new_label):
        if new_label not in self.keys:
            raise ValueError(f"New Y label {new_label} not in self.keys: {self.keys}")
        self._Y_label = new_label
        print(f"Setting new Y label as {self.Y_label}")


class MainAxis:

    def __init__(self, collection, ax, fig):
        self.collection = collection
        self.ax = ax
        self.fig = fig

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
        #_, bins, _ = self.ax.hist(self.collection.df[self.axis], bins = nbin, orientation=self.orientation)
        #self.nbin = len(bins) -1
        #self.draw()

    def decrease_nbins(self, x):
        nbin = max( [ int(np.floor(0.75 * self.nbin)), 1 ] )
        self.plot(nbin = nbin)
        #_, bins, _ = self.ax.hist(self.collection.df[self.axis], bins = nbin, orientation = self.orientation)
        #self.nbin = len(bins) -1
        #self.draw()

    def clear(self):
        self.ax.cla()

    def draw(self):
        self.fig.canvas.draw_idle()


def make_main_axes(fig):
    ax_main = plt.subplot2grid(shape=(6, 8), loc=(0, 2), rowspan=5, colspan=5, fig=fig)
    ax_y = plt.subplot2grid(shape=(6, 8), loc=(0, 7), rowspan=5, colspan=1, sharey=ax_main, fig=fig)
    ax_x = plt.subplot2grid(shape=(6, 8), loc=(5, 2), rowspan=1, colspan=5, sharex=ax_main, fig=fig)

    return ax_main, ax_x, ax_y

def make_label_selector_axes(fig, button_box_facecolor):
    ax1_radio_axis = plt.subplot2grid(shape=(6, 8), loc=(1, 0), rowspan=4, colspan=1, facecolor=button_box_facecolor, fig=fig)
    ax2_radio_axis = plt.subplot2grid(shape=(60, 80), loc=(10, 9), rowspan=40, colspan=8, facecolor=button_box_facecolor, fig=fig)
    return ax1_radio_axis, ax2_radio_axis

def make_zoom_buttons(fig):
    ax_zoom_histx_plus_button = plt.subplot2grid(shape=(60, 80), loc=(51, 70), rowspan=4, colspan=1, facecolor='lightgrey', fig=fig)
    zoom_histx_plus_button = Button(ax=ax_zoom_histx_plus_button, label="+", color='lightgrey')

    ax_zoom_histx_minus_button = plt.subplot2grid(shape=(60, 80), loc=(56, 70), rowspan=4, colspan=1, facecolor='lightgrey', fig = fig)
    zoom_histx_minus_button = Button(ax=ax_zoom_histx_minus_button, label="-", color='lightgrey')

    ax_zoom_histy_plus_button = plt.subplot2grid(shape=(60, 80), loc=(54, 78), rowspan=4, colspan=1, facecolor='lightgrey', fig = fig)
    zoom_histy_plus_button = Button(ax=ax_zoom_histy_plus_button, label="+", color='lightgrey')

    ax_zoom_histy_minus_button = plt.subplot2grid(shape=(60, 80), loc=(54, 79), rowspan=4, colspan=1, facecolor='lightgrey', fig = fig)
    zoom_histy_minus_button = Button(ax=ax_zoom_histy_minus_button, label="-", color='lightgrey')

    return zoom_histx_minus_button, zoom_histx_plus_button, zoom_histy_minus_button, zoom_histy_plus_button


def main(args):
    f = pd.read_csv(args.candfile, skiprows=1, skipfooter=1, sep="\s+", header = 0, names = HDR_keys)
    fig = plt.figure(figsize=(16.5, 5))
    data = MyCollection(f)
    
    button_box_facecolor = "lightgoldenrodyellow"
    axis_selector_button_active_color = "red"

    ax_main, ax_x, ax_y = make_main_axes(fig)
    main_ax = MainAxis(data, ax_main, fig)
    hist_x = HistAxes(data, 'X_label', ax_x, fig, 20)
    hist_y = HistAxes(data, 'Y_label', ax_y, fig, 20)

    ax1_radio_axis, ax2_radio_axis = make_label_selector_axes(fig, button_box_facecolor)
    ax1_radio_axis.set_title("Y-axis")
    ax2_radio_axis.set_title("X-axis")
    x_radio_buttons = RadioButtons(ax2_radio_axis, labels=data.keys, active=0, activecolor=axis_selector_button_active_color)
    y_radio_buttons = RadioButtons(ax1_radio_axis, labels=data.keys, active=0, activecolor=axis_selector_button_active_color)

    zoom_histx_minus_button, zoom_histx_plus_button, zoom_histy_minus_button, zoom_histy_plus_button = make_zoom_buttons(fig)

    ax_plot_button = plt.subplot2grid(shape=(6, 8), loc=(5, 0), rowspan=1, colspan=1, facecolor='green', fig=fig)
    plot_button = Button(ax_plot_button, "Plot", color="green")

    plt.subplots_adjust(left=0.01, right=0.99, wspace=0.25)

    def plot_button_action(x):
        main_ax.plot()
        hist_x.plot()
        hist_y.plot()

    x_radio_buttons.on_clicked(data.set_X_label)
    y_radio_buttons.on_clicked(data.set_Y_label)
    plot_button.on_clicked(plot_button_action)
    zoom_histx_plus_button.on_clicked(hist_x.increase_nbins)
    zoom_histy_plus_button.on_clicked(hist_y.increase_nbins)
    zoom_histx_minus_button.on_clicked(hist_x.decrease_nbins)
    zoom_histy_minus_button.on_clicked(hist_y.decrease_nbins)   

    plt.show()




if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('candfile', type=str, help="Path to the file containing candidates")

    args = a.parse_args()
    main(args)
  