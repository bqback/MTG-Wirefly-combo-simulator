from datavis import plot_data, log


def summarize(data, plot_mode, log_name):

    result = f"Opponent started at {data.opp_hp} HP, {data.flips} flips per attempt" \
             f"\nSuccess rate: {data.success / data.n * 100:.3f}% ({data.success} out of {data.n} attempts)\n" \
             f"Max wireflies used: {data.max_wf}\n" \
             f"Max flips: {data.max_flips}, with sequence\n{data.max_sequence}"

    plot_data(sim_data=data.wf_data,
              title=f"n = {data.n} with {data.flips} flips per attempt,\nsuccessful = {data.success} "
                    f"({data.success / data.n * 100:.3f}%)",
              xlabel="Wireflies used",
              plot_mode=plot_mode,
              filename="wf_graph.png"
              )
    plot_data(sim_data=data.flip_data,
              title=f"n = {data.n} with {data.flips} flips per attempt,\nsuccessful = {data.success} "
                    f"({data.success / data.n * 100:.3f}%)",
              xlabel="Flips used",
              plot_mode=plot_mode,
              filename="flip_graph.png"
              )
    log(log_name, result)