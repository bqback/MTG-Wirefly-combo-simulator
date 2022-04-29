import random
import matplotlib.pyplot as plt
import os.path
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Result:
    outcome: bool
    wireflies: int
    flips: int
    sequence: str


def combo(attempts: int, hp: int) -> Result:
    """
    Simulates a single attempt the Wirefly Hive combo.
    See https://www.youtube.com/watch?v=mKZ-ibOkRzs for details.

    :param attempts:
        Maximum number of flips before the simulation gives up
    :param hp:
        Amount of enemy HP at the start of the combo

    :return:
        Result object containing the outcome (True on success, False otherwise),
        the amount of wireflies used to attack (-1 if the combo failed),
        the amount of coin flips preceding the attack (-1 if the combo failed),
        sequence of coin flips, coded as H for heads and T for tails (empty if the combo failed)
    """
    wireflies = 0
    seq = ""

    for j in range(attempts):
        coin = random.choice([True, False])
        if coin:
            seq += "H"
            hp += 1
            wireflies += 1
            if wireflies * 2 >= hp:
                print(f"Succeeded with {wireflies} wireflies after {len(seq)} coin flips\nSequence: {seq}")
                return Result(True, wireflies, len(seq), seq)
        else:
            wireflies = 0
            seq += "T"
    return Result(False, -1, -1, "")


def next_name(filename: str) -> str:
    name, ext = os.path.splitext(filename)
    counter = 0
    new_name = filename
    while os.path.exists(filename):
        counter += 1
        new_name = f"{name} (counter){ext}"
    return new_name


def plot_data(
        sim_data: Dict,
        xlabel: str,
        display_mode='save',
        filename='graph.png',
        overwrite=True
) -> None:
    """

    Plots provided data, either saving it to a file or showing in a new window

    :param sim_data:
        Data, formatted as {x_1: y_1, x_2: y_2, ...}
    :param xlabel:
        String that will be used as the x-axis label
    :param display_mode:
        Either "save" or "show";
        "save": the graph is saved to a file;
        "show": the graph is displayed in a window;
        default: save
    :param filename:
        (If display_mode == save)
        Filename for the graph image;
        default: graph.png
    :param overwrite:
        (If display_mode == save)
        If True, the graph file will be silently overwritten;
        if False, the graph file will get an additional sequential number;
        default: True

    :return:
        None

    :raises:
        ValueError if the wrong display_name value is provided
    """

    dpi = plt.rcParams["figure.dpi"]
    fig = plt.figure(figsize=(1280/dpi, 960/dpi))
    ax = fig.add_axes([0, 0, 1, 1])
    rects = ax.bar(sim_data.keys(), sim_data.values())
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Number of occurrences")
    ax.set_xticks(list(sim_data.keys()))
    ax.bar_label(rects, padding=3)

    fig.tight_layout()

    if display_mode == "save":
        if os.path.exists(filename) & (not overwrite):
            filename = next_name(filename)
        plt.savefig(filename, bbox_inches='tight')
    elif display_mode == "show":
        plt.show()
    else:
        error_msg = f"display_mode must be either show or save (provided value: {display_mode})"
        raise ValueError(error_msg)


def sim():
    n = 1000000  # number of simulations
    flips = 1000  # number of coin flips per simulation
    opp_hp = 4  # opponent's starting HP
    success = 0  # successful combo counter
    max_wf = 0  # maximum amount of wireflies in a successful combo
    max_flips = 0  # maximum amount of flips in a successful combo
    max_sequence = ""  # sequence of flips corresponding to the maximum amount
    wf_data = {}  # wirefly data for a bar graph
    flip_data = {}  # flip data for a bar graph

    for i in range(n):
        attempt = combo(flips, opp_hp)
        if attempt.outcome:
            success += 1
            try:
                wf_data[attempt.wireflies] += 1
            except KeyError:
                wf_data.update({attempt.wireflies: 1})
            try:
                flip_data[attempt.flips] += 1
            except KeyError:
                flip_data.update({attempt.flips: 1})
            if max_wf < attempt.wireflies:
                print(f"New wirefly max: {attempt.wireflies} wireflies")
                max_wf = attempt.wireflies
            if max_flips < attempt.flips:
                print(f"New flip max: {i} flips")
                max_flips = attempt.flips
                max_sequence = attempt.sequence

    print(
        f"Success rate: {success / n * 100}%\n"
        f"Max wireflies used: {max_wf}\n"
        f"Max flips: {max_flips}, with sequence\n{max_sequence}"
    )

    plot_data(wf_data, "Wireflies used", "save", "wf_graph.png")
    # plot_data(wf_data, "Wireflies used", "show")
    plot_data(flip_data, "Flips used", "save", "flip_graph.png")
    # plot_data(flip_data, "Flips used", "show")


if __name__ == "__main__":
    sim()
