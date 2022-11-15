import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons
import argparse
import pandas as pd

if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument('candfile', type=str, help="Path to the file containing candidates")

    args = a.parse_args()
    
HDR_keys = ['SNR', 'lpix', 'mpix', 'boxc_width', 'time', 'dm', 'iblk', 'rawsn', 'total_sample', 'obstime_sec', 'mjd', 'dm_pccm3', 'ra_deg', 'dec_deg']

f = pd.read_csv(args.candfile, skiprows=1, skipfooter=1, sep="\s+", header = 0, names = HDR_keys)

ncols = len(f.keys())

fig = plt.figure(figsize=(16.5, 5))

ax_main = plt.subplot2grid(shape=(6, 8), loc=(0, 2), rowspan=5, colspan=5)
ax_main.grid(True)
ax_y = plt.subplot2grid(shape=(6, 8), loc=(0, 7), rowspan=5, colspan=1, sharey=ax_main)
ax_x = plt.subplot2grid(shape=(6, 8), loc=(5, 2), rowspan=1, colspan=5, sharex=ax_main)

button_box_facecolor = "lightgoldenrodyellow"
ax1_radio_buttons = plt.subplot2grid(shape=(6, 8), loc=(1, 0), rowspan=4, colspan=1, facecolor=button_box_facecolor)
ax2_radio_buttons = plt.subplot2grid(shape=(6, 8), loc=(1, 1), rowspan=4, colspan=1, facecolor=button_box_facecolor)
ax_plot_button = plt.subplot2grid(shape=(6, 8), loc=(5, 0), rowspan=1, colspan=1, facecolor='green')

ax1_radio_buttons.set_title("X-axis")
ax2_radio_buttons.set_title("Y-axis")

button_labels = list(f.keys())
button_active_color = 'red'

xstart_val_idx = 0
ystart_val_idx = 4

x_radio_buttons = RadioButtons(ax1_radio_buttons, labels=button_labels, active=xstart_val_idx, activecolor=button_active_color)
y_radio_buttons = RadioButtons(ax2_radio_buttons, labels=button_labels, active=ystart_val_idx, activecolor=button_active_color)

plot_button = Button(ax_plot_button, "Plot", color="green")

plt.subplots_adjust(left=0.01, right=0.99, wspace=0.25)

x_axis_plot = f.keys()[xstart_val_idx]
y_axis_plot = f.keys()[ystart_val_idx]

def clear_axes():
    ax_main.cla()
    ax_x.cla()
    ax_y.cla()
    ax_main.grid(True)

def sel_x_axis(label):
    global x_axis_plot
    x_axis_plot = label
    plt.draw()

def sel_y_axis(label):
    global y_axis_plot
    y_axis_plot = label
    plt.draw()

def redraw_plot(x):
    clear_axes()
    ax_main.plot(f[x_axis_plot], f[y_axis_plot], '.')
    ax_x.set_xlabel(x_axis_plot)
    ax_main.set_ylabel(y_axis_plot)
    ax_x.hist(f[x_axis_plot]);
    ax_y.hist(f[y_axis_plot]);
    plt.draw()

x_radio_buttons.on_clicked(sel_x_axis)
y_radio_buttons.on_clicked(sel_y_axis)
plot_button.on_clicked(redraw_plot)

plt.show()