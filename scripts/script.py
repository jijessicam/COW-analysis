####----------------------------------------------------------------------------------------------------------------####
#### Jessica Ji (jmj5)
#### IW07, Fall 2016
####----------------------------------------------------------------------------------------------------------------####
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

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
alliances_started_during_war = []
alliances_ended_during_war = []
alliances_started_before_war = []
alliances_ended_before_war = []
alliances_started_after_war = []
alliances_ended_after_war = []

countries_on_same_side = []
countries_on_opposite_side = []

# WAR DATA LOOP -- For each country in each war: --------------------------------------------------------------------
for index, war_id in war_data.iterrows():

    # For appending to war_data
    allies_within = []
    allies_before = []
    allies_after = []

    alliances_started_during = []
    alliances_ended_during = []

    alliances_started_before = []
    alliances_ended_before = []
    alliances_started_after = []
    alliances_ended_after = []

    same_side = []
    opposite_side = []

    country = war_id[['ccode']].item() # the country we're looking at
    war_num = war_id[['WarNum']].item() # the war we're looking at
    side = war_id[['Side']].item() # side the country was on

    war_start_date = war_id[['StartDate1']].item() # These are Timestamp objects
    war_end_date = war_id[['EndDate1']].item()

    temp_list = alliance_data[(alliance_data['ccode'] == country)] # Dataframe, all rows corresponding to that country code
    temp_series = temp_list['version4id'].tolist()

    # Get all countries involved in this specific war
    countries_in_war = war_data[(war_data['WarNum'] == war_num)] # Dataframe, all rows for this specific war
    for index, row in countries_in_war.iterrows():
        if ((row[['Side']].item() == side) & (row[['ccode']].item() != country)):
            same_side.append(row[['ccode']].item())
        elif ((row[['Side']].item() != side) & (row[['ccode']].item() != country)):
            opposite_side.append(row[['ccode']].item())
    countries_on_same_side.append(same_side)
    countries_on_opposite_side.append(opposite_side)

    if not temp_series:
        # Error handling: country has zero alliances, ever (wow)
        allies_within.append("None")
        allies_within_war.append(allies_within)

        allies_before.append("None")
        allies_before_war.append(allies_before)

        allies_after.append("None")
        allies_after_war.append(allies_after)

        alliances_started_during.append("None")
        alliances_started_during_war.append(alliances_started_during)

        alliances_ended_during.append("None")
        alliances_ended_during_war.append(alliances_ended_during)

        alliances_started_before.append("None")
        alliances_started_before_war.append(alliances_started_before)

        alliances_ended_before.append("None")
        alliances_ended_before_war.append(alliances_ended_before)

        alliances_started_after.append("None")
        alliances_started_after_war.append(alliances_started_after)

        alliances_ended_after.append("None")
        alliances_ended_after_war.append(alliances_ended_after)

    else:
        # Reindex to get all alliances made by that country (with all other countries)
        by_country = pd.DataFrame()
        for alliance in temp_series:
            alliance_mask = ((alliance_data['version4id'] == alliance) & (alliance_data['ccode'] != country))
            by_country = by_country.append(alliance_data[alliance_mask])

        # Only select rows in which the dates are: 1) within the war period, 2) 2 years before, 3) 2 years after
        # CHOICE: USING "ALL START/END DATE" INSTEAD OF "MEM START/END DATE"

        date_within_mask = (((by_country['AllStartDate'] <= war_start_date) & (by_country['AllEndDate'] >= war_end_date)) |
                            ((by_country['AllStartDate'] <= war_start_date) & (by_country['AllEndDate'] == 'NaT')))

        date_before_mask = (((by_country['AllStartDate'] <= (war_start_date - pd.DateOffset(years=2))) & (by_country['AllEndDate'] >= war_end_date)) |
                            (((by_country['AllStartDate'] <= (war_start_date - pd.DateOffset(years=2))) & (by_country['AllEndDate'] == 'NaT'))))

        date_after_mask = ((by_country['AllStartDate'] <= war_start_date) & (by_country['AllEndDate'] >= (war_end_date + pd.DateOffset(years=2))) |
                            ((by_country['AllStartDate'] <= war_start_date) & (by_country['AllEndDate'] == 'NaT')))

        # Did any alliances start during this war?
        start_during_war_mask = ((by_country['AllStartDate'] >= war_start_date) & (by_country['AllStartDate'] <= war_end_date))

        # Did any alliances end during this war?
        end_during_war_mask = ((by_country['AllEndDate'] != 'NaT') & (by_country['AllEndDate'] >= war_start_date) & (by_country['AllEndDate'] <= war_end_date))

        # Did any alliances start within the 2 years before this war?
        start_before_mask = (by_country['AllStartDate'] >= (war_start_date - pd.DateOffset(years=2))) & (by_country['AllStartDate'] <= war_start_date)

        # Did any alliances end within the 2 years before this war?
        end_before_mask = (by_country['AllEndDate'] >= (war_start_date - pd.DateOffset(years=2))) & (by_country['AllEndDate'] <= war_start_date)

        # Did any alliances start within 2 years after this war?
        start_after_mask = (by_country['AllStartDate'] <= (war_end_date + pd.DateOffset(years=2))) & (by_country['AllStartDate'] >= war_end_date)

        # Did any alliances end within 2 years after this war?
        end_after_mask = (by_country['AllEndDate'] <= (war_end_date + pd.DateOffset(years=2))) & (by_country['AllEndDate'] >= war_end_date)


        # Slice into sub-dataframes using date masks
        by_country_within = by_country[date_within_mask]
        by_country_before = by_country[date_before_mask]
        by_country_after = by_country[date_after_mask]

        alliances_started_within = by_country[start_during_war_mask]
        alliances_ended_within = by_country[end_during_war_mask]

        alliances_started_before_temp = by_country[start_before_mask]
        alliances_ended_before_temp = by_country[end_before_mask]
        alliances_started_after_temp = by_country[start_after_mask]
        alliances_ended_after_temp = by_country[end_after_mask]


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


        if alliances_started_within.empty:   # Error handling
            alliances_started_during.append("None")
            alliances_started_during_war.append(alliances_started_during)
        else:
            for index, row in alliances_started_within.iterrows():
                alliances_started_during.append(row[['ccode']].item())
            alliances_started_during_war.append(alliances_started_during)


        if alliances_ended_within.empty:   # Error handling
            alliances_ended_during.append("None")
            alliances_ended_during_war.append(alliances_ended_during)
        else:
            for index, row in alliances_ended_within.iterrows():
                alliances_ended_during.append(row[['ccode']].item())
            alliances_ended_during_war.append(alliances_ended_during)


        if alliances_started_before_temp.empty:    # Error handling
            alliances_started_before.append("None")
            alliances_started_before_war.append(alliances_started_before)
        else:
            for index, row in alliances_started_before_temp.iterrows():
                alliances_started_before.append(row[['ccode']].item())
            alliances_started_before_war.append(alliances_started_before)

        if alliances_ended_before_temp.empty:    # Error handling
            alliances_ended_before.append("None")
            alliances_ended_before_war.append(alliances_ended_before)
        else:
            for index, row in alliances_ended_before_temp.iterrows():
                alliances_ended_before.append(row[['ccode']].item())
            alliances_ended_before_war.append(alliances_ended_before)

        if alliances_started_after_temp.empty:    # Error handling
            alliances_started_after.append("None")
            alliances_started_after_war.append(alliances_started_after)
        else:
            for index, row in alliances_started_after_temp.iterrows():
                alliances_started_after.append(row[['ccode']].item())
            alliances_started_after_war.append(alliances_started_after)

        if alliances_ended_after_temp.empty:    # Error handling
            alliances_ended_after.append("None")
            alliances_ended_after_war.append(alliances_ended_after)
        else:
            for index, row in alliances_ended_after_temp.iterrows():
                alliances_ended_after.append(row[['ccode']].item())
            alliances_ended_after_war.append(alliances_ended_after)

# WAR DATA LOOP ENDS HERE -- For each country in each war: ----------------------------------------------------------

# allies_dw_series = pd.Series(allies_within_war)
# allies_bw_series = pd.Series(allies_before_war)
# allies_aw_series = pd.Series(allies_after_war)
#
# allies_start_during = pd.Series(alliances_started_during_war)
# allies_end_during = pd.Series(alliances_ended_during_war)
#
# # Append to dataset as new columns
# war_data['AlliesWithinWar'] = allies_dw_series.values
# war_data['AlliesBeforeWar'] = allies_bw_series.values
# war_data['AlliesAfterWar'] = allies_aw_series.values
# war_data['AlliesGainedDuringWar'] = allies_start_during.values
# war_data['AlliesLostDuringWar'] = allies_end_during.values

war_data['SameSide'] = countries_on_same_side
war_data['OppositeSide'] = countries_on_opposite_side

war_data['AlliesWithinWar'] = allies_within_war
war_data['AlliesBeforeWar'] = allies_before_war
war_data['AlliesAfterWar'] = allies_after_war

war_data['AlliesGainedDuringWar'] = alliances_started_during_war
war_data['AlliesLostDuringWar'] = alliances_ended_during_war

war_data['AlliesGained2YearsBeforeWar'] = alliances_started_before_war
war_data['AlliesLost2YearsBeforeWar'] = alliances_ended_before_war

war_data['AlliesGained2YearsAfterWar'] = alliances_started_after_war
war_data['AlliesLost2YearsAfterWar'] = alliances_ended_after_war


# Export war_data and alliance_data to CSV
war_data.to_csv('war_data.csv')
# alliance_data.to_csv('alliance_data.csv')





