from risk import *
import numpy as np
import pylab as plt
import pandas as pd

FIXED_RANGE = range(2, 30)
EQUAL_RANGE = range(2, 30)

def single_sim(num_trials=1000, def_troops=2, att_troops=2, max_dice=(2,3)):
    """
    Runs a single simulation with the given parameters, enabling user-defined max_dice args.
    Args:
        num_trials (int): Default = 1000. Number of simulation trials to run.
        def_troops (int): Default = 2. Number of defending troops in territory.
        att_troops (int): Default = 2. Number of attacking troops in territory - INCLUDES 1 left behind as per risk.Attacker.__init__
        max_dice (tup): Default = (2, 3). Maximum dice available for (defender, attacker) 
    Returns:
        results (list): 1s and 0s depending on whether the defender wins or loses.
    """
    results = []
    for i in range(num_trials):
        defence = Defender(def_troops, max_dice[0])
        attack = Attacker(att_troops, max_dice[1])
        battle = Battle(attack, defence)
        results.append(battle.run_battle()[0])
    # return np.array(results)
    return results

def analysis(results, verbose=False):
    """
    Calculates mean of results to 3dp
    Args:
        results (list): List of numbers
    """
    if verbose:
        print("\n----------------------------------------\n")
        print("Defender wins {} of the time.".format(np.mean(results)))
    return round(sum(results) / len(results), 3)

def debug():
  r = single_sim(def_troops=5, att_troops=5)
  analysis(r, verbose=True)

# debug()

def equal_sim(verbose=False, max_dice=(2,3)):
    """
    Runs single_sim for all of the values in the range, with equal numbers of attackers and defenders.
    (adjusted for 1 more attacker)
    """
    full_results = {k: [] for k in EQUAL_RANGE}
    summarised_results = {}
    for i in EQUAL_RANGE:
        if verbose:
            print("Currently at:", i)
        for j in range(5):
            r = single_sim(def_troops = i, att_troops = i, max_dice = max_dice)#def can be i-1
            full_results[i].append(analysis(r))
    for l in full_results:
        summarised_results[l] = analysis(full_results[l])
    if verbose:
        print("Results as follows:", summarised_results)
        plt.plot(list(summarised_results.keys()), list(summarised_results.values()))
        plt.title("Equal numbers of defending and attacking troops")
        plt.xlabel("Number of troops")
        plt.ylabel("Probability of defender winning")
        plt.show()
    return summarised_results

# equal_sim(verbose=True)

def fixed_sim(def_troops=None, att_troops=None, verbose=False, max_dice=(2,3)):
    """
    Runs single_sim for values in range with a fixed number of defenders against changing attackers (or vice versa)
    """
    if (def_troops and att_troops) or not (def_troops or att_troops):
        raise ValueError("Set one of defence or attack troops")
    full_results = {k: [] for k in FIXED_RANGE}
    summarised_results = {}
    for i in FIXED_RANGE:
        if verbose:
            print("Currently at:", i)
        for j in range(3): #delete at home
            if def_troops:
                r = single_sim(def_troops = def_troops, att_troops = i, max_dice = max_dice)
            else:
                r = single_sim(def_troops = i, att_troops = att_troops, max_dice = max_dice)
            full_results[i].append(analysis(r))
    for l in full_results:
        summarised_results[l] = analysis(full_results[l])
    if verbose:
        print("Results as follows:", summarised_results)
        plt.plot(list(summarised_results.keys()),list(summarised_results.values()))
        if def_troops:
            plt.title("Fixed number of defending troops ({}), changing attacking troops".format(def_troops))
            plt.xlabel("Number of attacking troops")
        else:
            plt.title("Fixed number of attacking troops ({}), changing defending troops".format(att_troops))
            plt.xlabel("Number of defending troops")
        plt.ylabel("Probability of defender winning")
        plt.show()
    return summarised_results
    
# fixed_sim(def_troops = 3, verbose=True)

def dice_sim(def_troops=None, att_troops=None, verbose=False):
    """
    Runs either single_sim of  for values in range with a fixed number of defenders against changing attackers (or vice versa)
    """
    results = {}
    ylabel = "Probability of defender winning"
    if def_troops or att_troops:
        results["d1a1"] = fixed_sim(def_troops=def_troops, att_troops=att_troops, max_dice=(1,1))
        results["d1a2"] = fixed_sim(def_troops=def_troops, att_troops=att_troops, max_dice=(1,2))
        results["d1a3"] = fixed_sim(def_troops=def_troops, att_troops=att_troops, max_dice=(1,3))
        results["d2a1"] = fixed_sim(def_troops=def_troops, att_troops=att_troops, max_dice=(2,1))
        results["d2a2"] = fixed_sim(def_troops=def_troops, att_troops=att_troops, max_dice=(2,2))
        results["d2a3"] = fixed_sim(def_troops=def_troops, att_troops=att_troops, max_dice=(2,3))
        xvals = [k for k in FIXED_RANGE] # change if fixed_sim changes
        if def_troops:
            title = "P(defender wins) with different max_dice numbers and a fixed number of defenders"
            xlabel = "Number of attacking troops"
        else:
            title = "P(defender wins) with different max_dice numbers and a fixed number of attackers"
            xlabel = "Number of defending troops"
    else:
        results["d1a1"] = equal_sim(max_dice=(1,1))
        results["d1a2"] = equal_sim(max_dice=(1,2))
        results["d1a3"] = equal_sim(max_dice=(1,3))
        results["d2a1"] = equal_sim(max_dice=(2,1))
        results["d2a2"] = equal_sim(max_dice=(2,2))
        results["d2a3"] = equal_sim(max_dice=(2,3))
        xvals = [k for k in EQUAL_RANGE] # change if equal_sim range changes
        xlabel = "Number of troops"
        title = "P(defender wins) with different max_dice numbers and equal numbers of attackers and defenders"
    if verbose:
        print("Results as follows:", results)
        plt.plot(xvals, list(results["d1a1"].values()), "r-", label="D1A1")
        plt.plot(xvals, list(results["d1a2"].values()), "r--", label="D1A2")
        plt.plot(xvals, list(results["d1a3"].values()), "ro", label="D1A3")
        plt.plot(xvals, list(results["d2a1"].values()), "b-", label="D2A1")
        plt.plot(xvals, list(results["d2a2"].values()), "b--", label="D2A2")
        plt.plot(xvals, list(results["d2a3"].values()), "bo", label="D2A3")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()

# dice_sim(3, None, True)    
dice_sim(verbose=True)

def dice_sim(def_troops=None, att_troops=None, verbose=False):
    """
    Runs either single_sim of  for values in range with a fixed number of defenders against changing attackers (or vice versa)
    """
    ylabel = "Probability of defender winning"
    if def_troops or att_troops:
        data = []
        headers = []
        title = "P(defender wins) with different max_dice numbers and a fixed number of {} ({})".format("defenders" if def_troops else "attackers", str(def_troops) if def_troops else str(att_troops))
        xlabel = "Number of {} troops".format("attacking" if def_troops else "defending")
        for d in range(1, 3):
            for a in range(1, 4):
                data.append(fixed_sim(def_troops=def_troops, att_troops=att_troops, max_dice=(d, a)))
                headers.append("d" + str(d) + "a" + str(a))
        results = pd.DataFrame(data, headers).T
    else:
        data = []
        headers = []
        title = "P(defender wins) with different max_dice numbers\n and equal numbers of attackers and defenders"
        xlabel = "Number of troops"
        for d in range(1, 3):
            for a in range(1, 4):
                data.append(equal_sim(max_dice=(d,a)))
                headers.append("d" + str(d) + "a" + str(a))
        results = pd.DataFrame(data, headers).T
    if verbose:
        print("Results as follows:\n-", results)
        results.plot(title=title, xlabel=xlabel, ylabel=ylabel, legend=True, style=['r-', 'r--', 'ro', 'b-', 'b--', 'bo'])
        
# dice_sim(verbose=True)
