import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, RectangleSelector
import argparse
import pandas as pd

from candplotter.Collection import MyCollection
from candplotter.Axes import MainAxis, HistAxes
import candplotter.default_buttons as D

#HDR_keys = ['SNR', 'lpix', 'mpix', 'boxc_width', 'time', 'dm', 'iblk', 'rawsn', 'total_sample', 'obstime_sec', 'mjd', 'dm_pccm3', 'ra_deg', 'dec_deg']
#HDR_keys = ['SNR', 'lpix', 'mpix', 'boxc_width', 'time', 'dm', 'iblk', 'rawsn', 'total_sample', 'obstime_sec', 'mjd', 'dm_pccm3', 'ra_deg', 'dec_deg']
#HDR_keys = ['SNR',     'boxcar',  'DM',      'samp',    'ngroup']




def make_main_axes(fig):
    ax_main = plt.subplot2grid(shape=(60, 80), loc=(0, 30), rowspan=50, colspan=40, fig=fig)
    ax_y = plt.subplot2grid(shape=(60, 80), loc=(0, 72), rowspan=50, colspan=10, sharey=ax_main, fig=fig)
    ax_x = plt.subplot2grid(shape=(60, 80), loc=(50, 30), rowspan=10, colspan=40, sharex=ax_main, fig=fig)

    return ax_main, ax_x, ax_y

def make_label_selector_axes(fig, button_box_facecolor):
    ax1_radio_axis = plt.subplot2grid(shape=(60, 80), loc=(10, 0), rowspan=40, colspan=6, facecolor=button_box_facecolor, fig=fig)
    ax2_radio_axis = plt.subplot2grid(shape=(60, 80), loc=(10, 7), rowspan=40, colspan=6, facecolor=button_box_facecolor, fig=fig)
    ax3_radio_axis = plt.subplot2grid(shape=(60, 80), loc=(10, 14), rowspan=40, colspan=6, facecolor=button_box_facecolor, fig=fig)
    ax4_radio_axis = plt.subplot2grid(shape=(60, 80), loc=(10,21), rowspan=40, colspan=6, facecolor=button_box_facecolor, fig=fig)
    return ax1_radio_axis, ax2_radio_axis, ax3_radio_axis, ax4_radio_axis

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

def make_select_button_axes(fig):
    ax_plot_button = plt.subplot2grid(shape=(60, 80), loc=(51, 0), rowspan=9, colspan=8, facecolor='green', fig=fig)
    plot_button = Button(ax_plot_button, "Plot", color="green")
    plot_button.drawon = False
    ax_select_button = plt.subplot2grid(shape=(60, 80), loc=(51, 9), rowspan=9, colspan=4, facecolor='cyan', fig=fig)
    select_button = Button(ax = ax_select_button, label='Select', color='cyan')
    select_button.drawon = False    #This disables triggering of fig.canvas.draw_idle() when you hover over the button -- which if left True will make the rectangular selections disappear upon hovering
    ax_delete_button = plt.subplot2grid(shape=(60, 80), loc=(51, 14), rowspan=9, colspan=4, facecolor='orange', fig=fig)
    delete_button = Button(ax = ax_delete_button, label='Delete', color='orange')
    delete_button.drawon = False
    ax_reset_button = plt.subplot2grid(shape=(60, 80), loc=(51, 19), rowspan=9, colspan=4, facecolor='lightgrey', fig=fig)
    reset_button = Button(ax = ax_reset_button, label='Reset', color='lightgrey')
    reset_button.drawon = False
    ax_export_button = plt.subplot2grid(shape=(60, 80), loc=(51, 24), rowspan=9, colspan=3, facecolor='white', fig=fig)
    export_button = Button(ax = ax_export_button, label='Export', color='white')
    export_button.drawon = False

    return plot_button, select_button, delete_button, reset_button, export_button

def get_parser():
    a = argparse.ArgumentParser()
    a.add_argument('candfile', type=str, help="Path to the file containing candidates")
    a.add_argument('-sep', type=str, help="Delimeter to use when parsing the file (def = \s+)", default=None)
    a.add_argument('-skiprows', type=int, help="No of lines to skip at the top(def = 1)", default=1)
    a.add_argument('-skip_footer', type=int, help="No of lines to skip at the end (def = 0)", default=0)
    
    args = a.parse_args()
    return args

def run_plotter(df, title = " "):
    fig = plt.figure(figsize=(16.5, 5))
    data = MyCollection(df)
    
    button_box_facecolor = "lightgoldenrodyellow"
    axis_selector_button_active_color = "red"

    ax_main, ax_x, ax_y = make_main_axes(fig)
    main_ax = MainAxis(data, ax_main, fig)
    hist_x = HistAxes(data, 'X_label', ax_x, fig, 20)
    hist_y = HistAxes(data, 'Y_label', ax_y, fig, 20)

    plot_button, select_button, delete_button, reset_button, export_button = make_select_button_axes(fig)

    def rect_select_action(eclick, erelease):
        x1 = eclick.xdata
        y1 = eclick.ydata
        x2 = erelease.xdata
        y2 = erelease.ydata
        data.save_region_mask(x1, x2, y1, y2)

    def select_button_action(_):
        data.select_mask()
        plot_button_action(0)

    def delete_button_action(_):
        data.deselect_mask()
        plot_button_action(0)

    def reset_button_action(_):
        data.reset_df()
        plot_button_action(0)
    
    def export_button_action(_):
        #outname=input("Enter the name of the output filename (hit enter for default):\n")
        outname = ""
        data.export_df(outname)
    
    rect_selector = RectangleSelector(ax_main, rect_select_action, drawtype='box', button=[3], interactive=True, useblit=True)

    ax1_radio_axis, ax2_radio_axis, ax3_radio_axis, ax4_radio_axis = make_label_selector_axes(fig, button_box_facecolor)
    ax1_radio_axis.set_title("Y-axis")
    ax2_radio_axis.set_title("X-axis")
    ax3_radio_axis.set_title("Size")
    ax4_radio_axis.set_title("Color")

    X_def = min([len(data.keys), D.X_default])
    Y_def = min([len(data.keys), D.Y_default])
    S_def = min([len(data.keys), D.S_default])
    C_def = min([len(data.keys), D.C_default])

    x_radio_buttons = RadioButtons(ax2_radio_axis, labels=data.keys, active=X_def, activecolor=axis_selector_button_active_color)
    y_radio_buttons = RadioButtons(ax1_radio_axis, labels=data.keys, active=Y_def, activecolor=axis_selector_button_active_color)
    s_radio_buttons = RadioButtons(ax3_radio_axis, labels=data.keys, active=S_def, activecolor=axis_selector_button_active_color)
    c_radio_buttons = RadioButtons(ax4_radio_axis, labels=data.keys, active=C_def, activecolor=axis_selector_button_active_color)

    zoom_histx_minus_button, zoom_histx_plus_button, zoom_histy_minus_button, zoom_histy_plus_button = make_zoom_buttons(fig)

    plt.subplots_adjust(left=0.01, right=0.99, wspace=0.25)

    def plot_button_action(x):
        main_ax.plot()
        hist_x.plot()
        hist_y.plot()

    x_radio_buttons.on_clicked(data.set_X_label)
    y_radio_buttons.on_clicked(data.set_Y_label)
    s_radio_buttons.on_clicked(data.set_size_label)
    c_radio_buttons.on_clicked(data.set_color_label)
    plot_button.on_clicked(plot_button_action)
    zoom_histx_plus_button.on_clicked(hist_x.increase_nbins)
    zoom_histy_plus_button.on_clicked(hist_y.increase_nbins)
    zoom_histx_minus_button.on_clicked(hist_x.decrease_nbins)
    zoom_histy_minus_button.on_clicked(hist_y.decrease_nbins)  
    select_button.on_clicked(select_button_action)
    delete_button.on_clicked(delete_button_action) 
    reset_button.on_clicked(reset_button_action)
    export_button.on_clicked(export_button_action)
    
    fig.canvas.mpl_connect('pick_event', data.on_pick)
    fig.suptitle(title)

    data.set_X_label(data.keys[X_def])
    data.set_Y_label(data.keys[Y_def])
    data.set_size_label(data.keys[S_def])
    data.set_color_label(data.keys[C_def])
    plot_button_action(0)
    plt.show()

def main():
    args = get_parser()
    sep = "\t"
    if args.sep:
        sep = args.sep
    with open(args.candfile, 'r') as ff:
        while True:
            line = ff.readline()
            if line.strip() == "":
                continue
            print("Inferring Header keys from the first non-empty line - \n", line)
            HDR_keys = line.strip().strip('#').strip().split(sep)
            break
    print(f"Header keys = {HDR_keys}")
    df = pd.read_csv(args.candfile, skiprows=args.skiprows, skipfooter=args.skip_footer, sep=sep, header = 0, names = HDR_keys)
    run_plotter(df, title = args.candfile)
    
if __name__ == '__main__':
    main()
  
