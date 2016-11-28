####----------------------------------------------------------------------------------------------------------------####
#### Jessica Ji (jmj5)
#### IW07, Fall 2016
####----------------------------------------------------------------------------------------------------------------####
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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

# What percentage of countries are actually allied with countries on the same side during each war?

percent_allied_with_same_side = []

fight_with_former_allies = []

ally_with_former_enemies = []

# For each country in each war...
for index, war_id in war_data.iterrows():
    country = war_id[['ccode']].item() # the country we're looking at
    war_num = war_id[['WarNum']].item() # the war we're looking at
    side = war_id[['Side']].item() # side the country was on

    side_list = war_id[['SameSide']].item() # list of countries on same side in war
    opp_side_list = war_id[['OppositeSide']].item() # list of countries on opposite side in war

    allies_list = war_id[['AlliesWithinWar']].item() # list of allies during that war
    allies_before = war_id[['AlliesBeforeWar']].item() # list of allies before that war
    allies_after = war_id[['AlliesAfterWar']].item() # list of allies after that war

    side_count = len(side_list)
    ally_count = len(allies_list)
    both_count = 0.0
    percent = 0.0

    # Loop through list of countries on same side
    if (side_count != 0):
        for item in side_list:
            if (item in allies_list):
                both_count = both_count + 1
        percent = both_count / side_count
    # elif (side_count == 0):
    #     percent = None
    percent_allied_with_same_side.append(percent)

    allied_with_former_enemy_count = 0.0
    fought_against_former_ally_count = 0.0
    allied_with_former_enemy_percent = 0.0
    fought_against_former_ally_percent = 0.0
    num_enemies = len(opp_side_list)

    for item in opp_side_list:
        if item in allies_before:
            fought_against_former_ally_count = fought_against_former_ally_count + 1
        if item in allies_after:
            allied_with_former_enemy_count = allied_with_former_enemy_count + 1
    fought_against_former_ally_percent = fought_against_former_ally_count / num_enemies
    allied_with_former_enemy_percent = allied_with_former_enemy_count / num_enemies
    fight_with_former_allies.append(fought_against_former_ally_percent)
    ally_with_former_enemies.append(allied_with_former_enemy_percent)

print "Number of countries (rows in war_data): ", len(war_data.index)
print "Length of percent list: ", len(percent_allied_with_same_side)
print percent_allied_with_same_side
print len(fight_with_former_allies)
print fight_with_former_allies
print len(ally_with_former_enemies)
print ally_with_former_enemies