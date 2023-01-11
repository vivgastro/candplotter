import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons
import argparse
import pandas as pd

from Collection import MyCollection
from Axes import MainAxis, HistAxes

#HDR_keys = ['SNR', 'lpix', 'mpix', 'boxc_width', 'time', 'dm', 'iblk', 'rawsn', 'total_sample', 'obstime_sec', 'mjd', 'dm_pccm3', 'ra_deg', 'dec_deg']
#HDR_keys = ['SNR', 'lpix', 'mpix', 'boxc_width', 'time', 'dm', 'iblk', 'rawsn', 'total_sample', 'obstime_sec', 'mjd', 'dm_pccm3', 'ra_deg', 'dec_deg']
#HDR_keys = ['SNR',     'boxcar',  'DM',      'samp',    'ngroup']




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
    with open(args.candfile, 'r') as ff:
        while True:
            line = ff.readline()
            if line.strip() == "":
                continue
            print("Inferring Header keys from the first non-empty line - \n", line)
            HDR_keys = line.strip().strip('#').split()
            break
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
  
