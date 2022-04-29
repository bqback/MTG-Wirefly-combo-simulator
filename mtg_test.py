import random
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Result:
    outcome: bool
    wireflies: int
    flips: int
    sequence: str


def combo(attempts: int, hp: int) -> Result:
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


def plot_data(sim_data: Dict) -> None:
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar(sim_data.keys, sim_data.values())
    plt.show()


if __name__ == "__main__":

    n = 100000000  # number of simulations
    flips = 1000000  # number of coin flips per simulation
    opp_hp = 4  # opponent's starting HP
    success = 0  # successful combo counter
    max_wf = 0  # maximum amount of wireflies in a successful combo
    max_flips = 0  # maximum amount of flips in a successful combo
    max_sequence = ""  # sequence of flips corresponding to the maximum amount
    data = {}  # data for a histogram

    for i in range(n):
        attempt = combo(flips, opp_hp)
        if attempt.outcome:
            success += 1
            try:
                data[attempt.wireflies] += 1
            except KeyError:
                data.update({attempt.wireflies: 1})
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

    plot_data(data)
