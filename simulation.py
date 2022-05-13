import curses
from random import random
from classes import Data, Result
from datavis import progress_bar


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
        coin = True if random() <= 0.5 else False
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


def sim_wrap(n, flips, opp_hp):
    data = curses.wrapper(sim_scr, n, flips, opp_hp)
    return data


def sim_scr(stdscr, n: int, flips: int, opp_hp: int):
    data = Data(n, flips, opp_hp)

    for i in range(n):
        attempt = combo(flips, opp_hp)
        if attempt.outcome:
            data.parse(attempt)
        if stdscr is not None:
            stdscr.nodelay(True)
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

    return data


def sim_silent(n: int, flips: int, opp_hp: int):
    data = Data(n, flips, opp_hp)

    for i in range(n):
        attempt = combo(flips, opp_hp)
        if attempt.outcome:
            data.parse(attempt)

    return data
