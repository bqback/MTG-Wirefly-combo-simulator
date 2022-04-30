import random
import matplotlib.pyplot as plt
import os.path
import curses
from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class Result:
    outcome: bool
    wireflies: int
    flips: int
    sequence: str


@dataclass
class Data:
    wf_data: Dict = field(default_factory=dict)
    flip_data: Dict = field(default_factory=dict)
    success: int = 0
    last_wf: int = 0
    last_flips: int = 0
    last_sequence: str = ""
    max_wf: int = 0
    max_flips: int = 0
    max_sequence: str = ""

    def parse(self, result: Result):
        self.success += 1
        self.last_wf = result.wireflies
        self.last_flips = result.flips
        self.last_sequence = result.sequence
        try:
            self.wf_data[result.wireflies] += 1
        except KeyError:
            self.wf_data.update({result.wireflies: 1})
        try:
            self.flip_data[result.flips] += 1
        except KeyError:
            self.flip_data.update({result.flips: 1})
        if self.max_wf < result.wireflies:
            self.max_wf = result.wireflies
        if self.max_flips < result.flips:
            self.max_flips = result.flips
            self.max_sequence = result.sequence


def combo(attempts: int, hp: int) -> Result:
    """
    Simulates a single attempt of the Wirefly Hive combo.
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
                """
                print(f"Succeeded with {wireflies} wireflies after {len(seq)} coin flips\nSequence: {seq}")
                """
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
        fig_width=1650,
        fig_height=900,
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
    :param fig_width:
        Width of the resulting data plot;
        default: 1650
    :param fig_height:
        Width of the resulting data plot;
        default: 900
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
    fig = plt.figure(figsize=(fig_width / dpi, fig_height / dpi))
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


def progress_bar(current, total, bar_length=75):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    return f'Progress: [{arrow}{padding}] {fraction*100:.2f}% ({current}/{total})'


def sim(stdscr, n, flips, opp_hp):
    data = Data()

    stdscr.nodelay(True)

    for i in range(n):
        attempt = combo(flips, opp_hp)
        if attempt.outcome:
            data.parse(attempt)
        stdscr.clear()
        stdscr.addstr(0, 0, f"Last success wireflies: {data.last_wf}")
        stdscr.addstr(1, 0, f"Last success flips: {data.last_flips}")
        stdscr.addstr(2, 0, f"Last successful sequence: {data.last_sequence}")
        stdscr.addstr(3, 0, f"Max wireflies: {data.max_wf}")
        stdscr.addstr(4, 0, f"Max flips: {data.max_flips}")
        stdscr.addstr(5, 0, f"Max successful sequence: {data.max_sequence}")
        bar = progress_bar(i, n)
        stdscr.addstr(6, 0, bar)
        stdscr.refresh()
        c = stdscr.getch()
        if c == 3:
            stdscr.addstr(0, 0, "getch() got Ctrl+C")
            stdscr.refresh()
            raise KeyboardInterrupt
        else:
            curses.flushinp()

    plot_data(sim_data=data.wf_data, xlabel="Wireflies used", display_mode="save", filename="wf_graph.png")
    # plot_data(sim_data=wf_data, xlabel="Wireflies used", display_mode="show")
    plot_data(sim_data=data.flip_data, xlabel="Flips used", display_mode="save", filename="flip_graph.png")
    # plot_data(sim_data=flip_data, xlabel="Flips used", display_mode="show")

    return data.success, data.max_wf, data.max_flips, data.max_sequence


def main():
    n = 20000000  # number of simulations
    flips = 400  # number of coin flips per simulation, 1e8 sims haven't showed more than 72 flips, but who knows
    opp_hp = 4  # opponent's starting HP
    success, max_wf, max_flips, max_sequence = curses.wrapper(sim, n, flips, opp_hp)

    print(
        f"\nSuccess rate: {success / n * 100}%\n"
        f"Max wireflies used: {max_wf}\n"
        f"Max flips: {max_flips}, with sequence\n{max_sequence}"
    )


if __name__ == "__main__":
    main()
