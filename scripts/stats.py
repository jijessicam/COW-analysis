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

# What percentage of alliances begin during a war?
# What percentage of alliances end during a war?

def count_allies(list):
    if ('None' in list):
        return 0
    else:
        return len(list)

war_data['NumAlliesGained'] = war_data['AlliesGainedDuringWar'].apply(count_allies)
war_data['NumAlliesLost'] = war_data['AlliesLostDuringWar'].apply(count_allies)
war_data['NumAlliesGained2YearsBefore'] = war_data['AlliesGained2YearsBeforeWar'].apply(count_allies)
war_data['NumAlliesLost2YearsBefore'] = war_data['AlliesLost2YearsBeforeWar'].apply(count_allies)
war_data['NumAlliesGained2YearsAfter'] = war_data['AlliesGained2YearsAfterWar'].apply(count_allies)
war_data['NumAlliesLost2YearsAfter'] = war_data['AlliesLost2YearsAfterWar'].apply(count_allies)

# # Group war_data by war ID number, keeping it in time order
grouped_by_war = war_data.groupby(['WarName'], sort=False)

allies_gained = war_data.groupby(['WarName'], sort=False)['NumAlliesGained'].sum().reset_index()
allies_lost = war_data.groupby(['WarName'], sort=False)['NumAlliesLost'].sum().reset_index()
allies_gained_before = war_data.groupby(['WarName'], sort=False)['NumAlliesGained2YearsBefore'].sum().reset_index()
allies_lost_before = war_data.groupby(['WarName'], sort=False)['NumAlliesLost2YearsBefore'].sum().reset_index()
allies_gained_after = war_data.groupby(['WarName'], sort=False)['NumAlliesGained2YearsAfter'].sum().reset_index()
allies_lost_after = war_data.groupby(['WarName'], sort=False)['NumAlliesLost2YearsAfter'].sum().reset_index()

data_by_war = pd.merge(allies_gained, allies_lost, on=['WarName'])
data_by_war = data_by_war.merge(allies_gained_before, on=['WarName'])
data_by_war = data_by_war.merge(allies_lost_before, on=['WarName'])
data_by_war = data_by_war.merge(allies_gained_after, on=['WarName'])
data_by_war = data_by_war.merge(allies_lost_after, on=['WarName'])


# # PLOT: MOST COMMON ALLIANCE TYPE  ----------------------------------------------------------------------------------
# most_common_alliance_type_plot = sns.countplot(x='ss_type', data=alliance_data)
# plt.xlabel('Alliance Type', fontsize=14)
# plt.ylabel('Number of Alliances Made', fontsize=14)
# plt.xticks(rotation=30)
# plt.tick_params(axis='both', labelsize=12)
# plt.title("Number of Alliances Made by Type", fontsize=24)
# plt.tight_layout()
# plt.savefig('most_common_alliance_type.jpg', bbox_inches='tight')
# # -------------------------------------------------------------------------------------------------------------------
# # PLOT: NUMBER OF ALLIANCES BY STATE --------------------------------------------------------------------------------
# plt.figure(figsize=(200, 100))
# alliances_by_country_plot = sns.countplot(x='state_name', data=alliance_data)
# plt.xticks(rotation=90)
# plt.xlabel('State Name', fontsize=50)
# plt.ylabel('Number of Alliances Made', fontsize=50)
# plt.tick_params(axis='both', labelsize=36)
# plt.title("Number of Alliances Made by Country", fontsize=96)
# plt.tight_layout()
# plt.savefig('alliances_made_by_country.jpg', bbox_inches='tight')
# # -------------------------------------------------------------------------------------------------------------------
# # PLOT: NUMBER OF ALLIES GAINED PER WAR -----------------------------------------------------------------------------
# sns.set(font_scale=1.8)
# allies_gained_plot = sns.factorplot(x='WarName', y='NumAlliesGained', data=data_by_war, kind="bar", size=8, aspect=5)
# allies_gained_plot.set_axis_labels("War", "Number of Allies Gained")
# allies_gained_plot.set_xticklabels(rotation=90)
# plt.title("Total Number of Allies Gained By War")
# plt.savefig('allies_gained_by_war.jpg', bbox_inches='tight')
# # -------------------------------------------------------------------------------------------------------------------
# # PLOT: NUMBER OF ALLIES LOST PER WAR -----------------------------------------------------------------------------
# sns.set(font_scale=1.8)
# allies_lost_plot = sns.factorplot(x='WarName', y='NumAlliesLost', data=data_by_war, kind="bar", size=8, aspect=5)
# allies_lost_plot.set_axis_labels("War", "Number of Allies Lost")
# allies_lost_plot.set_xticklabels(rotation=90)
# plt.title("Total Number of Allies Lost By War")
# plt.savefig('allies_lost_by_war.jpg', bbox_inches='tight')
# # -------------------------------------------------------------------------------------------------------------------
# # -------------------------------------------------------------------------------------------------------------------
# # PLOT: NUMBER OF ALLIES GAINED 2 YEARS BEFORE WAR ------------------------------------------------------------------
# sns.set(font_scale=1.8)
# allies_gained_before_plot = sns.factorplot(x='WarName', y='NumAlliesGained2YearsBefore', data=data_by_war, kind="bar", size=8, aspect=5)
# allies_gained_before_plot.set_axis_labels("War", "Number of Allies Gained")
# allies_gained_before_plot.set_xticklabels(rotation=90)
# plt.title("Total Number of Allies Gained in 2 Years Before War Started")
# plt.savefig('allies_gained_2_years_before_by_war.jpg', bbox_inches='tight')
# # -------------------------------------------------------------------------------------------------------------------
# # -------------------------------------------------------------------------------------------------------------------
# # PLOT: NUMBER OF ALLIES LOST 2 YEARS BEFORE WAR ------------------------------------------------------------------
# sns.set(font_scale=1.8)
# allies_lost_before_plot = sns.factorplot(x='WarName', y='NumAlliesLost2YearsBefore', data=data_by_war, kind="bar", size=8, aspect=5)
# allies_lost_before_plot.set_axis_labels("War", "Number of Allies Lost")
# allies_lost_before_plot.set_xticklabels(rotation=90)
# plt.title("Total Number of Allies Lost in 2 Years Before War Started")
# plt.savefig('allies_lost_2_years_before_by_war.jpg', bbox_inches='tight')
# # -------------------------------------------------------------------------------------------------------------------
# # -------------------------------------------------------------------------------------------------------------------
# # PLOT: NUMBER OF ALLIES GAINED 2 YEARS AFTER WAR -------------------------------------------------------------------
# sns.set(font_scale=1.8)
# allies_gained_after_plot = sns.factorplot(x='WarName', y='NumAlliesGained2YearsAfter', data=data_by_war, kind="bar", size=8, aspect=5)
# allies_gained_after_plot.set_axis_labels("War", "Number of Allies Gained")
# allies_gained_after_plot.set_xticklabels(rotation=90)
# plt.title("Total Number of Allies Gained in 2 Years After War Ended")
# plt.savefig('allies_gained_2_years_after_by_war.jpg', bbox_inches='tight')
# # -------------------------------------------------------------------------------------------------------------------
# # -------------------------------------------------------------------------------------------------------------------
# # PLOT: NUMBER OF ALLIES LOST 2 YEARS AFTER WAR ---------------------------------------------------------------------
# sns.set(font_scale=1.8)
# allies_lost_after_plot = sns.factorplot(x='WarName', y='NumAlliesLost2YearsAfter', data=data_by_war, kind="bar", size=8, aspect=5)
# allies_lost_after_plot.set_axis_labels("War", "Number of Allies Lost")
# allies_lost_after_plot.set_xticklabels(rotation=90)
# plt.title("Total Number of Allies Lost in 2 Years After War Ended")
# plt.savefig('allies_lost_2_years_after_by_war.jpg', bbox_inches='tight')
# # -------------------------------------------------------------------------------------------------------------------

# 1a) In what percentage of wars do existing alliances end during the war?
percent_alliances_end_during_war = \
    ((float(len(data_by_war[data_by_war.NumAlliesLost > 0].index)))/(float(len(data_by_war.index))))*100
print "Percentage of wars during which existing alliances ended: ", percent_alliances_end_during_war, "%"

# 2a) In what percentage of wars are new alliances formed during the war?
percent_alliances_start_during_war = \
    ((float(len(data_by_war[data_by_war.NumAlliesGained > 0].index)))/(float(len(data_by_war.index))))*100
print "Percentage of wars during which new alliances began: ", percent_alliances_start_during_war, "%"

#-----------------------------------------------------------------------------------------------------#

# 1b) In what percentage of wars do existing alliances end within 2 years before the war begins?
percent_alliances_end_before_war = \
    ((float(len(data_by_war[data_by_war.NumAlliesLost2YearsBefore > 0].index)))/(float(len(data_by_war.index))))*100
print "Percentage of wars during which existing alliances ended in the 2 years before the war began: ", \
    percent_alliances_end_before_war, "%"

# 1c) In what percentage of wars do existing alliances end within 2 years after the war ends?
percent_alliances_end_after_war = \
    ((float(len(data_by_war[data_by_war.NumAlliesLost2YearsAfter > 0].index)))/(float(len(data_by_war.index))))*100
print "Percentage of wars during which existing alliances ended in the 2 years after the war ended: ", \
    percent_alliances_end_after_war, "%"

#-----------------------------------------------------------------------------------------------------#

# 2b) In what percentage of wars do new alliances form within 2 years before the war begins?
percent_alliances_start_before_war = \
    ((float(len(data_by_war[data_by_war.NumAlliesGained2YearsBefore > 0].index)))/(float(len(data_by_war.index))))*100
print "Percentage of wars during which new alliances started in the 2 years before the war began: ", \
    percent_alliances_start_before_war, "%"

# 2c) In what percentage of wars do new alliances form within 2 years after the end of the war?
percent_alliances_start_after_war = \
    ((float(len(data_by_war[data_by_war.NumAlliesGained2YearsAfter > 0].index)))/(float(len(data_by_war.index))))*100
print "Percentage of wars during which new alliances started in the 2 years after the war ended: ", \
    percent_alliances_start_after_war, "%"

#-------------------------------------------------------------------------------------------------------------------#

plt.show()

#--------------------------------------------------------------------------------------------------------------------#