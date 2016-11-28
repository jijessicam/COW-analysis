####----------------------------------------------------------------------------------------------------------------####
#### Jessica Ji (jmj5)
#### IW07, Fall 2016
####----------------------------------------------------------------------------------------------------------------####
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# def slice():
# Import CSV and load data into a pandas dataframe w/ consolidated date columns
war_data = pd.read_csv("interstate_wars.csv",
                       parse_dates={'StartDate1': ['StartMonth1', 'StartDay1', 'StartYear1'],
                                                           'StartDate2': ['StartMonth2', 'StartDay2', 'StartYear2'],
                                                           'EndDate1': ['EndMonth1', 'EndDay1', 'EndYear1'],
                                                           'EndDate2': ['EndMonth2', 'EndDay2', 'EndYear2']})
alliance_data = pd.read_csv("formal_alliances.csv",
                    parse_dates={'AllStartDate': ['all_st_day', 'all_st_month', 'all_st_year'],
                                                           'AllEndDate': ['all_end_day', 'all_end_month', 'all_end_year'],
                                                           'MemStartDate': ['mem_st_day', 'mem_st_month', 'mem_st_year'],
                                                           'MemEndDate': ['mem_end_day', 'mem_end_month', 'mem_end_year']})

# Clean up date formatting in alliance dataset (account for blank rows)
alliance_data['AllEndDate'] = pd.to_datetime(alliance_data['AllEndDate'], format='%d %m %Y', errors="coerce")
alliance_data['AllStartDate'] = pd.to_datetime(alliance_data['AllStartDate'], format='%d %m %Y', errors="coerce")
alliance_data['MemStartDate'] = pd.to_datetime(alliance_data['MemStartDate'], format='%d %m %Y', errors="coerce")
alliance_data['MemEndDate'] = pd.to_datetime(alliance_data['MemEndDate'], format='%d %m %Y', errors='coerce')

# Note to self: date columns are of type datetime64[ns]

# Get indexes (axis labels, metadata) of both datasets
war_index = war_data.index
alliance_index = alliance_data.index

# Create list of allies within the time period of the war
allies_within_war = []
allies_before_war = []
allies_after_war = []

# FOR ALLIANCE DATASET SLICING???
# began_during_war_list = []
# ended_during_war_list = []

# For each country in each war:
for index, war_id in war_data.iterrows():
    country = war_id[['ccode']].item() # the country we're looking at
    war_start_date = war_id[['StartDate1']].item() # These are Timestamp objects
    war_end_date = war_id[['EndDate1']].item()

    temp_list = alliance_data[(alliance_data['ccode'] == country)] # Dataframe, all rows corresponding to that country code
    temp_series = temp_list['version4id'].tolist()
    print "Number of alliances: ", len(temp_series)

    # Reindex to get all alliances
    by_country = pd.DataFrame()
    for alliance in temp_series:
        alliance_mask = ((alliance_data['version4id'] == alliance) & (alliance_data['ccode'] != country))
        by_country = by_country.append(alliance_data[alliance_mask])

    # Only select rows in which the dates are: 1) within the war period, 2) 2 years before, 3) 2 years after
    # CHOICE: USING "ALL START/END DATE" INSTEAD OF "MEM START/END DATE"

    date_within_mask = (((by_country['AllStartDate'] <= war_start_date) & (by_country['AllEndDate'] >= war_end_date)) |
                        ((by_country['AllStartDate'] <= war_start_date) & (by_country['AllEndDate'] == 'NaT')))

    date_before_mask = ((((by_country['AllStartDate'] + pd.DateOffset(years=2)) <= war_start_date) & (by_country['AllEndDate'] >= war_end_date)) |
                        (((by_country['AllStartDate'] + pd.DateOffset(years=2)) <= war_start_date) & (by_country['AllEndDate'] == 'NaT')))

    date_after_mask = (((by_country['AllStartDate'] <= war_start_date) & ((by_country['AllEndDate'] + pd.DateOffset(years=2)) >= war_end_date)) |
                        ((by_country['AllStartDate'] <= war_start_date) & (by_country['AllEndDate'] == 'NaT')))

    # Slice into sub-dataframes using date masks
    by_country_within = by_country[date_within_mask]
    by_country_before = by_country[date_before_mask]
    by_country_after = by_country[date_after_mask]

    # print("ALLIANCES WITHIN WAR PERIOD:")
    # print by_country

    allies_within = []
    allies_before = []
    allies_after = []
    if by_country_within.empty:     # Error handling
        allies_within.append("None")
        allies_within_war.append(allies_within)
    else:
        for index, row in by_country_within.iterrows():
            allies_within.append(row[['ccode']].item())
        allies_within_war.append(allies_within)

    if by_country_before.empty:  # Error handling
        allies_before.append("None")
        allies_before_war.append(allies_before)
    else:
        for index, row in by_country_before.iterrows():
            allies_before.append(row[['ccode']].item())
        allies_before_war.append(allies_before)

    if by_country_after.empty:   # Error handling
        allies_after.append("None")
        allies_after_war.append(allies_after)
    else:
        for index, row in by_country_after.iterrows():
            allies_after.append(row[['ccode']].item())
        allies_after_war.append(allies_after)

# print("ALLIES DURING WAR (LIST):")
# print allies_within_war
# print "Length of ally list: ", len(allies_within_war)
# print "Number of rows in war dataset: ", len(data.index)

allies_dw_series = pd.Series(allies_within_war)
allies_bw_series = pd.Series(allies_before_war)
allies_aw_series = pd.Series(allies_after_war)

# Append to dataset as new columns
war_data['AlliesWithinWar'] = allies_dw_series.values
war_data['AlliesBeforeWar'] = allies_bw_series.values
war_data['AlliesAfterWar'] = allies_aw_series.values
# print data['AlliesWithinWar']
# print data['AlliesBeforeWar']
# print data['AlliesAfterWar']

    # # Return sliced dataframe
    # return war_data, alliance_data

#--------------------------------------------------------------------------------------------------------------------#

# war_data, alliance_data = slice()

# What alliance type is the most common?
alliance_data['ss_type'].value_counts().plot(kind='bar')

# Which state makes the most alliances?
alliance_data['state_name'].value_counts().plot(kind='bar')

        # What percentage of alliances begin during a war?

        # What percentage of alliances end during a war?


    # 1a) In what percentage of wars do existing alliances end during the war?

    # 1b) In what percentage of wars do existing alliances end within 2 years before the war begins?

    # 1c) In what percentage of wars do existing alliances end within 2 years after the war ends?

    #-----------------------------------------------------------------------------------------------------#

    # 2a) In what percentage of wars are new alliances formed during the war?

    # 2b) In what percentage of wars do new alliances form within 2 years before the war begins?

    # 2c) In what percentage of wars do new alliances form within 2 years after the end of the war?

#--------------------------------------------------------------------------------------------------------------------#



