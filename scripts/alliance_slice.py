import pandas as pd

# Import CSV and load data into a pandas dataframe w/ consolidated date columns
war_data = pd.read_csv("interstate_wars_cropped1.csv",
                       parse_dates={'StartDate1': ['StartMonth1', 'StartDay1', 'StartYear1'],
                                                           'StartDate2': ['StartMonth2', 'StartDay2', 'StartYear2'],
                                                           'EndDate1': ['EndMonth1', 'EndDay1', 'EndYear1'],
                                                           'EndDate2': ['EndMonth2', 'EndDay2', 'EndYear2']})
alliance_data = pd.read_csv("formal_alliances_cropped1.csv",
                    parse_dates={'AllStartDate': ['all_st_day', 'all_st_month', 'all_st_year'],
                                                           'AllEndDate': ['all_end_day', 'all_end_month', 'all_end_year'],
                                                           'MemStartDate': ['mem_st_day', 'mem_st_month', 'mem_st_year'],
                                                           'MemEndDate': ['mem_end_day', 'mem_end_month', 'mem_end_year']})

# Clean up date formatting in alliance dataset (account for blank rows)
alliance_data['AllEndDate'] = pd.to_datetime(alliance_data['AllEndDate'], format='%d %m %Y', errors="coerce")
alliance_data['AllStartDate'] = pd.to_datetime(alliance_data['AllStartDate'], format='%d %m %Y', errors="coerce")
alliance_data['MemStartDate'] = pd.to_datetime(alliance_data['MemStartDate'], format='%d %m %Y', errors="coerce")
alliance_data['MemEndDate'] = pd.to_datetime(alliance_data['MemEndDate'], format='%d %m %Y', errors='coerce')

# # ALLIANCE DATA LOOP -- For each alliance: --------------------------------------------------------------------------

# For appending to alliance_data
start_during_war = []
end_during_war = []
start_2yr_before_war = []
end_2yr_before_war = []
start_2yr_after_war = []
end_2yr_after_war = []

# For each alliance, ask: did it start/end during this war?
for index2, alliance_id in alliance_data.iterrows():

    # What's the country we're looking at?

    start_date = alliance_id[['AllStartDate']].item()
    end_date = alliance_id[['AllEndDate']].item()



    for index3, war_id in war_data.iterrows():

        # Get war start and end date for that war
        war_start_date = war_id[['StartDate1']].item()  # These are Timestamp objects
        war_end_date = war_id[['EndDate1']].item()

        # Did it start during this war? 1=yes, 0=no
        if ((start_date >= war_start_date) & (start_date <= war_end_date)):
            start_during_war.append(1)
            start_2yr_before_war.append(0)
            start_2yr_after_war.append(0)
        # Did it start 2 years before this war started?
        elif ((start_date >= (war_start_date - pd.DateOffset(years=2))) & (start_date <= war_end_date)):
            start_2yr_before_war.append(1)
            start_during_war.append(0)
            start_2yr_after_war.append(0)
        # Did it start 2 years after this war ended?
        elif ((start_date >= (war_start_date)) & (start_date <= (war_end_date + pd.DateOffset(years=2)))):
            start_2yr_after_war.append(1)
            start_during_war.append(0)
            start_2yr_before_war.append(0)
        else:
            start_during_war.append(0)
            start_2yr_before_war.append(0)
            start_2yr_after_war.append(0)

        # Did it end during this war? 1=yes, 0=no
        if ((end_date >= war_start_date) & (end_date <= war_end_date)):
            end_during_war.append(1)
            end_2yr_after_war.append(0)
            end_2yr_before_war.append(0)
        # Did it end within 2 years before this war started?
        elif ((end_date >= (war_start_date - pd.DateOffset(years=2))) & (end_date <= war_end_date)):
            end_2yr_before_war.append(1)
            end_during_war.append(0)
            end_2yr_after_war.append(0)
        # Did it end within 2 years after this war ended?
        elif ((end_date >= (war_start_date)) & (end_date <= (war_end_date + pd.DateOffset(years=2)))):
            end_2yr_after_war.append(1)
            end_during_war.append(0)
            end_2yr_before_war.append(0)
        else:
            end_during_war.append(0)
            end_2yr_before_war.append(0)
            end_2yr_after_war.append(0)

# END ALLIANCE_DATA LOOP

print "Length of alliance_data.index: ", len(alliance_data.index)
print "Length of start_during_war: ", len(start_during_war)
print "Length of end_during_war: ", len(end_during_war)
print "Length of start_2yr_before_war: ",


alliance_data['StartedDuringWar'] = start_during_war
alliance_data['Started2YearsBeforeWar'] = start_2yr_before_war
alliance_data['Started2YearsAfterWar'] = start_2yr_after_war
alliance_data['EndedDuringWar'] = end_during_war
alliance_data['Ended2YearsBeforeWar'] = end_2yr_before_war
alliance_data['Ended2YearsAfterWar'] = end_2yr_after_war