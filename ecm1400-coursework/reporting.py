import numpy as np
import pandas as pd
import datetime

def parse_data(dataframe:pd.DataFrame) -> pd.DataFrame:
    """
    Modifies the input dataframe in the following ways:

        1: Replaces 'No data' values with NaN in order to make pandas methods work with the dataframe
        2: Converts pollutants column from string format to float to allow applying functions on each column
        3: Replaces 24:00:00 with 00:00:00 in order to make data suitable for conversion to datetime object
        4: Combines date and time columns into one column 'datetime' and converts data into datetime object
        5: Sets datetime column as the index of the dataframe

    Arguments:
        dataframe: original dataframe
    Returns:
        dataframe: modified dataframe   
    """
    dataframe = dataframe.replace('No data',np.NaN) #1

    dataframe.no = dataframe.no.astype(float) #2
    dataframe.pm10 = dataframe.pm10.astype(float)
    dataframe.pm25 = dataframe.pm25.astype(float)

    dataframe.time = dataframe.time.replace('24:00:00', '00:00:00') #3

    dataframe.loc[:,'datetime'] = pd.to_datetime(dataframe.date + ' ' + dataframe.time, format='%Y-%m-%d %H:%M:%S') #4
    dataframe = dataframe.drop(columns=['date','time'])

    dataframe = dataframe.set_index('datetime') #5
    return dataframe

def import_data() -> pd.DataFrame:
    """
    Procedure used to import CSVs from data folder and processes them accordingly:
        
        - Applies parse_data() function on each station
        - Merges dataframes for each station into one large dataframe

    Returns:
        all_data: dataframe with time-indexed pollutant data for all stations 
    """
    data_harlington = pd.read_csv("data/Pollution-London Harlington.csv")       # Import CSV into dataframe
    data_marylebone = pd.read_csv("data/Pollution-London Marylebone Road.csv")
    data_kensington = pd.read_csv("data/Pollution-London N Kensington.csv")

    data_harlington = parse_data(data_harlington)       # Parse data for each dataframe
    data_marylebone = parse_data(data_marylebone)
    data_kensington = parse_data(data_kensington)

    stations_data = [data_harlington, data_marylebone, data_kensington]                                             
    all_data = pd.concat(stations_data, keys=['Harlington','Marylebone Road','N Kensington'], names=['station'])    # Concatenates dataframes together into one large dataframe
    return all_data

def daily_average(data:pd.DataFrame, monitoring_station:str, pollutant:str) -> np.ndarray:
    """
    Resamples the input dataframe for a selected monitoring station and pollutant and returns a list of the daily averages
    
    Arguments:
        data (DataFrame): time-indexed pollutant data
        monitoring_station (str): selected monitoring station
        pollutant (str): selected pollutant
    Returns:
        d_averages_array (ndarray): list of all daily averages for specified station and pollutant
    """
    query = data.loc[monitoring_station]                    # Filters values for chosen monitoring station
    d_averages = query.resample('D').mean()                 # Resamples hourly data into daily average
    d_averages_array = d_averages[pollutant].to_numpy()     # Exports pollutant data into array
    return d_averages_array 

def daily_median(data:pd.DataFrame, monitoring_station:str, pollutant:str) -> np.ndarray:
    """
    Resamples the input dataframe for a selected monitoring station and pollutant and returns a list of the daily medians
    
    Arguments:
        data (DataFrame): time-indexed pollutant data
        monitoring_station (str): selected monitoring station
        pollutant (str): selected pollutant
    Returns:
        d_medians_array (ndarray): list of all daily medians for specified station and pollutant
    """
    query = data.loc[monitoring_station]
    d_medians = query.resample('D').median()                # Resamples hourly data into daily median
    d_medians_array = d_medians[pollutant].to_numpy()
    return d_medians_array

def hourly_average(data:pd.DataFrame, monitoring_station:str, pollutant:str) -> np.ndarray:
    """
    Groups the input dataframe by hour of day for selected monitoring station and pollutant and returns a list of hourly averages
    
    Arguments:
        data (DataFrame): time-indexed pollutant data
        monitoring_station (str): selected monitoring station
        pollutant (str): selected pollutant
    Returns:
        h_averages_array (ndarray): list of hourly averages for specified station and pollutant
    """
    query = data.loc[monitoring_station]                        
    h_averages = query.groupby([query.index.hour]).mean()       # Groups all values by hour of day (0-23H)
    h_averages_array = h_averages[pollutant].to_numpy()         
    h_averages_array = np.roll(h_averages_array, -1)            # Moves first element in array to last (0H = 24H) to correspond with last hour of the day
    return h_averages_array

def monthly_average(data:pd.DataFrame, monitoring_station:str, pollutant:str) -> np.ndarray:
    """
    Resamples the input dataframe for a selected monitoring station and pollutant and returns a list of the monthly averages
    
    Arguments:
        data (DataFrame): time-indexed pollutant data
        monitoring_station (str): selected monitoring station
        pollutant (str): selected pollutant
    Returns:
        m_averages_array (ndarray): list of all monthly averages for specified station and pollutant
    """
    query = data.loc[monitoring_station]
    m_averages = query.resample('M').mean()                   # Resamples hourly data into monthly average
    m_averages_array = m_averages[pollutant].to_numpy()
    return m_averages_array

def peak_hour_date(data:pd.DataFrame, date:str, monitoring_station:str, pollutant:str)-> tuple:
    """
    Finds the highest pollution level for a selected date, monitoring station and pollutant and returns a tuple with pollution value and corresponding hour of day
    
    Arguments:
        data (DataFrame): time-indexed pollutant data
        date (str): selected date
        monitoring_station (str): selected monitoring station
        pollutant (str): selected pollutant
    Returns:
        peak_hour_tuple (tuple): pollutant level and corresponding time of day
    """
    station_query = data.loc[monitoring_station]            
    date_query = station_query.loc[date]                                    # Filters values for chosen date
    peak_hour = date_query[pollutant].max()
    peak_hour_index = str(date_query[pollutant].argmax()+1).zfill(2)        # Finds index of highest value (0-23), adds 1 to give hour of day (1-24) and pads string (01-24)
    peak_hour_tuple = (peak_hour_index +':00',peak_hour)                    # Concatenates padded string (hour of day) and minutes (':00')
    return peak_hour_tuple

def count_missing_data(data:pd.DataFrame, monitoring_station:str, pollutant:str) -> int:
    """
    Counts 'No data' entries for a selected monitoring station and pollutant
    
    Arguments:
        data (DataFrame): time-indexed pollutant data
        monitoring_station (str): selected monitoring station
        pollutant (str): selected pollutant
    Returns:
        md_count (int): number of 'No data' entries
    """
    query = data.loc[monitoring_station]
    md_count = query[pollutant].isna().sum()        # Counts the number of rows in the pollutant column with 'No data' entries
    return md_count

def fill_missing_data(data:pd.DataFrame, new_value, monitoring_station:str, pollutant:str) -> pd.DataFrame:
    """
    Replaces 'No data' entries with specified new value for a selected monitoring station and pollutant
    
    Arguments:
        data (DataFrame): time-indexed pollutant data
        new_value: value replacing 'No data' entries
        monitoring_station (str): selected monitoring station
        pollutant (str): selected pollutant
    Returns:
        md_copy (DataFrame): copy of DataFrame with 'No data' entries replaced with new_value
    """
    query = data.loc[monitoring_station]
    md_copy = query[pollutant].replace(np.NaN,new_value)     #Replace NaN values (see parse_data function) with new_value
    return md_copy