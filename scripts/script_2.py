####----------------------------------------------------------------------------------------------------------------####
#### Jessica Ji (jmj5)
#### IW07, Fall 2016
####----------------------------------------------------------------------------------------------------------------####
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
from ast import literal_eval

# Read in dataframes from CSV (created/cleaned by script.py)
war_data = pd.read_csv("war_data.csv")
alliance_data = pd.read_csv("alliance_data.csv")

# Parse list elements as lists instead of strings

war_data.SameSide = war_data.SameSide.apply(literal_eval)
war_data.OppositeSide = war_data.OppositeSide.apply(literal_eval)

war_data.AlliesWithinWar = war_data.AlliesWithinWar.apply(literal_eval)
war_data.AlliesBeforeWar = war_data.AlliesBeforeWar.apply(literal_eval)
war_data.AlliesAfterWar = war_data.AlliesAfterWar.apply(literal_eval)

war_data.AlliesGainedDuringWar = war_data.AlliesGainedDuringWar.apply(literal_eval)
war_data.AlliesLostDuringWar = war_data.AlliesLostDuringWar.apply(literal_eval)

war_data.AlliesGained2YearsBeforeWar = war_data.AlliesGained2YearsBeforeWar.apply(literal_eval)
war_data.AlliesLost2YearsBeforeWar = war_data.AlliesLost2YearsBeforeWar.apply(literal_eval)

war_data.AlliesGained2YearsAfterWar = war_data.AlliesGained2YearsAfterWar.apply(literal_eval)
war_data.AlliesLost2YearsAfterWar = war_data.AlliesLost2YearsAfterWar.apply(literal_eval)

#--------------------------------------------------------------------------------------------------------------------#

# GOAL: read in Bilateral Trade dataset for each country in each war
