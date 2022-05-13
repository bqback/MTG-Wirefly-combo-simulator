from simulation import sim_wrap, sim_silent
from summarize import summarize


def sim_setup(show_progress: bool, plot_mode="save", log_name="log.txt"):
    n = 2000  # number of simulations
    flips = 150  # number of coin flips per simulation, 2e8 sims peaked at 84 flips once
    opp_hp = 4  # opponent's starting HP

    data = \
        sim_wrap(n, flips, opp_hp) if show_progress \
        else sim_silent(n, flips, opp_hp)

    summarize(data, plot_mode, log_name)


def main():
    # If show_progress=True, a nice progress window is showed, which also quadruples runtime
    sim_setup(show_progress=True, plot_mode="save", log_name="result_log.txt")


if __name__ == "__main__":
    main()
