import os
import datetime
import matplotlib.pyplot as plt
from typing import Dict


def next_name(filename: str) -> str:
    name, ext = os.path.splitext(filename)
    counter = 0
    new_name = filename
    while os.path.exists(new_name):
        counter += 1
        new_name = f"{name} ({counter}){ext}"
    return new_name


def plot_data(
        sim_data: Dict,
        xlabel: str,
        title='',
        fig_width=1650,
        fig_height=900,
        plot_mode='save',
        filename='graph.png',
        overwrite=False
) -> None:
    """

    Plots provided data, either saving it to a file or showing in a new window

    :param title:
        Title of the plot
    :param sim_data:
        Data, formatted as {x_1: y_1, x_2: y_2, ...}
    :param xlabel:
        String that will be used as the x-axis label
    :param fig_width:
        Width of the resulting data plot;
        default: 1650
    :param fig_height:
        Width of the resulting data plot;
        default: 900
    :param plot_mode:
        Either "save" or "show";
        "save": the graph is saved to a file;
        "show": the graph is displayed in a window;
        default: save
    :param filename:
        (If plot_mode == save)
        Filename for the graph image;
        default: graph.png
    :param overwrite:
        (If plot_mode == save)
        If True, the graph file will be silently overwritten;
        if False, the graph file will get an additional sequential number;
        default: True

    :return:
        None

    :raises:
        ValueError if the wrong display_name value is provided
    """

    dpi = plt.rcParams["figure.dpi"]
    fig, ax = plt.subplots(figsize=(fig_width / dpi, fig_height / dpi), constrained_layout=True)
    rects = ax.bar(sim_data.keys(), sim_data.values())
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Number of occurrences")
    ax.set_xticks(list(sim_data.keys()))
    ax.bar_label(rects, padding=3, rotation=30)

    if plot_mode == "save":
        if os.path.exists(filename) & (not overwrite):
            filename = next_name(filename)
        plt.savefig(filename, bbox_inches='tight')
    elif plot_mode == "show":
        plt.show()
    else:
        error_msg = f"plot_mode must be either show or save (provided value: {plot_mode})"
        raise ValueError(error_msg)


def progress_bar(current: int, total: int, bar_length=75):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    return f'Progress: [{arrow}{padding}] {fraction * 100:.2f}% ({current}/{total})'


def log(log_name: str, result: str):
    if os.path.exists(log_name):
        with open(log_name, 'r') as original:
            contents = original.read()
        with open(log_name, 'w') as modified:
            modified.write(datetime.datetime.now().strftime("%X %x") + "\n" + result + "\n\n" + contents)
    else:
        with open(log_name, 'w+') as file:
            file.write(datetime.datetime.now().strftime("%X %x") + "\n" + result)

    print(result)