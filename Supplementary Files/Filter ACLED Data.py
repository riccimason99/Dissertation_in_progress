#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 19:57:39 2024

@author: riccimason99
"""

### ACLED KEY: OGz-I3Os*rU5hFozWRng

import pandas as pd
import numpy as np
import re


#  list of values you want to remove from the 'tags' column
values_to_remove = [
    'crowd size=dozens',
    'crowd size=no report',
    'crowd size=about a dozen',
    'crowd size=small',
    'crowd size=no report; local administrators',
    'crowd size=around a dozen',
    'counter-demonstration; crowd size=no report',
    'counter-demonstration; crowd size=dozens',
    'crowd size=four',
    'crowd size=eighteen',
    'crowd size=five',
    'crowd size=two',
    'crowd size=more than four',
    'crowd size=one',
    'crowd size=over a dozen',
    'counter-demonstration; crowd size=more than several',
    'counter-demonstration; crowd size=several',
    'crowd size=seven',
    'crowd size=a large group',
    'crowd size=a dozen',
    'crowd size=three',
    'crowd size=dozens to hundreds',
    'crowd size=thirty',
    'crowd size=four',
    'crowd size=eighteen',
    'crowd size=five',
    'crowd size=two',
    'crowd size=more than four',
    'crowd size=one',
    'crowd size=over a dozen',
    'counter-demonstration; crowd size=more than several',
    'counter-demonstration; crowd size=several',
    'crowd size=seven',
    'crowd size=a large group',
    'crowd size=a large group; suggested agents provocateurs',
    'crowd size=some',
    'crowd size=several groups; suggested agents provocateurs',
    'crowd size=several', 'crowd size=at least two',
    'armed; crowd size=no report',
    'armed; counter-demonstration; crowd size=no report',
    'crowd size=six',
    'car ramming; crowd size=no report',
    'armed; counter-demonstration; crowd size=more than three',
    'crowd size=a few',
    'crowd size=a few dozen',
    'armed; counter-demonstration; crowd size=dozens',
    'armed; armed presence; counter-demonstration; crowd size=several dozen',
    'crowd size=dozens to about 150',
    'crowd size=large group',
    'crowd size=about three dozen',
    'counter-demonstration; crowd size=several dozen',
    'crowd size=at least five',
    'counter-demonstration; crowd size=no report; stop the steal',
    'crowd size=at least three; women targeted: girls',
    'crowd size=more than a dozen',
    'crowd size=no report; women targeted: girls',
    'crowd size=eight',
    'crowd size=no report; statue',  'crowd size=over two dozen',
     'crowd size=a crowd',
     'crowd size=a group',
     'counter-demonstration; crowd size=a large group',
     'counter-demonstration; crowd size=more than a few dozen',
     'crowd size=no report; suggested agents provocateurs',
     'armed; counter-demonstration; crowd size=several dozen',
     'crowd size=a small group; statue',
     'armed; armed presence; crowd size=no report',
     'crowd size=a large group; detentions',
     'armed; counter-demonstration; crowd size=more than a few dozen',
     'crowd size=no size; statue',
     'armed; crowd size=dozens; local administrators',
     'crowd size=a crowd; statue',
     'crowd size=at least dozens; statue',
     'counter-demonstration; crowd size=a crowd',
     'crowd size=no report', 'crowd size=dozens', 'crowd size=large' 'crowd size=around 20',
     'crowd size=handful', 'crowd size=many', 'crowd size=sizeable']


# Function to remove smaller values
# Enhanced function to extract the first number, considering ranges and textual descriptions
def extract_number(text):
    # Check for and handle textual numbers
    if 'a few hundred' in text:
        return 300  # Approximate "a few hundred" as 300 for filtering
    if 'dozens' in text:
        return np.nan  # "Dozens" is indeterminate but likely less than 300, so we'll ignore these
    
    # Find all numbers or ranges in the text
    numbers_or_ranges = re.findall(r'\d+-\d+|\d+', text)
    if numbers_or_ranges:
        # Handle the first found number or range
        first_number_or_range = numbers_or_ranges[0]
        if '-' in first_number_or_range:
            # If it's a range, take the first part
            return int(first_number_or_range.split('-')[0])
        else:
            # Otherwise, just return the number
            return int(first_number_or_range)
    return np.nan  # Return NaN if no numbers found


# Load and look at data
violent_2017 = pd.read_csv("[...].csv")
#violent_2017 = pd.read_csv("[...].csv")


# REMOVE VALUES OF SMALL PROTEST

# Apply the function to the 'tags' column
violent_2017['first_number'] = violent_2017['tags'].apply(extract_number)
# Filter rows: keep rows where first_number is NaN or first_number >= 100
filtered_violent_2017 = violent_2017[(violent_2017['first_number'] >= 100) | (violent_2017['first_number'].isna())]
print(filtered_violent_2017['tags'].unique())
filtered_violent_2017.shape

# Remove rows we dont want from values to remove
filtered_violent_2017 = filtered_violent_2017[~filtered_violent_2017['tags'].isin(values_to_remove)]
print(filtered_violent_2017.tags.unique())
filtered_violent_2017.shape

# Drop some more observations
words_to_drop = ['no report', 'couple', 'a hundred', 'dozen', 'dozens', 'large', 'dozens', 'scores']
# Use DataFrame.apply() with a lambda function to check if any of the words_to_drop are in the 'tags' column
mask = filtered_violent_2017['tags'].apply(lambda x: any(word in x for word in words_to_drop))
# Invert the mask to keep rows that do not contain any of the words_to_drop
violent_protests = filtered_violent_2017[~mask]
violent_protests.shape    


# Remove useless columns
violent_protests.columns
violent_protests = violent_protests.drop(['time_precision', 
        'sub_event_type', 'first_number', 'event_type', 'actor1',  'inter1', 
        'actor2', 'timestamp', 'region', 'geo_precision',  'source_scale', 'iso', 
        'inter2', 'interaction', 'event_id_cnty', 'civilian_targeting',
        'admin3', 'country', 'disorder_type'], axis  = 1)
violent_protests.reset_index(drop = True, inplace = True)

# Create a column with protest date in date time format 
violent_protests["date_time"] = pd.to_datetime(violent_protests["event_date"], format = '%d %B %Y')



# CREATE ANOTHER DATA FRAME OF ONLY ESSENTIAL COLUMNS

# Remove non-essential columns
violent_essential = violent_protests.drop(columns = ['year', 'assoc_actor_2', 'admin2', 
                                           'latitude', 'longitude', 'source','fatalities'])
# Create a column of dates string in the format that lesix nexis news takes,
# make it easier to search articles 
violent_essential['date_string'] = violent_essential['date_time'].dt.strftime('%d/%m/%Y')


##############################################################################################################
##############################################################################################################
#  Lets do the same thing for NON_VIOLENT Protests
##############################################################################################################
##############################################################################################################


data_peace = pd.read_csv("[...].csv")
#print(data_peace.tags.head(50))
#print(data_peace.tags.unique())
#data_peace.shape # 59564 observations


# REMOVE VALUES OF SMALL PROTEST

## This code removes a lot of values which the first number is below 100
def check_number(s):
    # Ensure the input is a string
    if isinstance(s, str):
        # Search for numbers in the string
        numbers = re.findall(r'\d+', s)
        if numbers:
            # Convert the first found number to integer
            num = int(numbers[0])
            # Return False if the number is less than 200 (indicating removal)
            return num >= 200
    # Return True if no number is found or the input is not a string (indicating retention)
    return True

# Apply the function to the 'tags' column and filter the DataFrame
peace_ = data_peace[data_peace['tags'].apply(check_number)]
# Show the filtered DataFrame
#peace_.shape  # we lost a lot of observations
#print(peace_.tags.unique())


# remove values in "values_to_remove"
filtered_peace_ = peace_[~peace_['tags'].isin(values_to_remove)]
#filtered_peace_.shape
   
# remove useless columns 
filtered_peace_ = filtered_peace_.drop(columns = ['time_precision', 
        'sub_event_type', 'event_type', 'actor1',  'inter1', 
        'actor2', 'timestamp', 'region', 'geo_precision',  'source_scale', 'iso', 
        'inter2', 'interaction', 'event_id_cnty', 'civilian_targeting',
        'admin3', 'country', 'disorder_type'], axis  = 1)


# Convert 'tags' column to string type and then filter out rows
filtered_peace_['tags'] = filtered_peace_['tags'].astype(str)
filtered_peace_ = filtered_peace_[~filtered_peace_['tags'].str.contains('|'.join(words_to_drop))]
filtered_peace_.reset_index(drop = True, inplace = True)

# Create a column with protest date in date time format 
filtered_peace_["date_time"] = pd.to_datetime(filtered_peace_["event_date"], format = '%d %B %Y')


# CREATE ANOTHER DATA FRAME OF ONLY ESSENTIAL COLUMNS

# Remove non-essential columns
peace_essential = filtered_peace_.drop(columns = ['year', 'assoc_actor_2', 'admin2', 
                                           'latitude', 'longitude', 'source','fatalities'])

# Create a column of dates string in the format that lesix nexis news takes,
# make it easier to search articles 
peace_essential['date_string'] = peace_essential['date_time'].dt.strftime('%d/%m/%Y')
##







