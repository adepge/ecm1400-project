import pandas as pd
import numpy as np
import datetime


def get_live_data_from_api(site_code='MR8',species_code='PM10',start_date=None,end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API. 
    
    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """
    import requests
    import datetime
    start_date = datetime.date(2022,1,1) if start_date is None else start_date
    end_date = start_date + datetime.timedelta(days=1)if end_date is None else end_date

    
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
   
    url = endpoint.format(
        site_code = site_code,
        species_code = species_code,
        start_date = start_date,
        end_date = end_date
    )
    
    res = requests.get(url)
    return res.json()

def parse_json(json_data:dict) -> pd.DataFrame:
    """
    Parses data from json format into dataframe:

        1: Splits 'Data' column into two according to date and value
        2: Renames columns with appropriate values
        3: Converts 'Date' column data from string to datetime object
        4: Sets date as the index of the dataframe
        5: Sets value column as float
        6: Discards all missing data values

    Arguments:
        json_data (dict): json dictionary (output, see: get_live_data_from_api)
    Returns:
        aq_data: dataframe with rearranged data values
    """
    aq_data = pd.DataFrame(json_data['RawAQData'])
    aq_data = pd.concat([aq_data.drop(['Data'], axis=1), aq_data['Data'].apply(pd.Series)], axis=1) #1
    aq_data = aq_data.rename(columns={"@SiteCode": "Site", "@SpeciesCode": "Pollutant", "@MeasurementDateGMT": "Date", "@Value": "Value"}) #2
    aq_data.loc['Date'] = pd.to_datetime(aq_data['Date'], format='%Y-%m-%d %H:%M:%S') #3
    aq_data = aq_data.set_index('Date') #4
    aq_data = aq_data.replace(r'^\s*$', np.nan, regex=True)
    aq_data['Value'] = aq_data['Value'].astype(float)  #5
    aq_data = aq_data.dropna() #6
    return aq_data

def special_print(dataframe:pd.DataFrame):
    """
    Displays data from dataframe in text-based table format

    Arguments:
        dataframe: parsed dataframe (see: parse_json())
    """
    columns = dataframe.columns.tolist()                            # Adds headers of dataframe into list
    columns.insert(0,dataframe.index.name)
    dataframe['Value'] = dataframe['Value'].astype(str)
    
    date_cl = int(dataframe.index.str.len().max())
    site_cl = int(dataframe['Site'].str.len().max())
    pollutant_cl = int(dataframe['Pollutant'].str.len().max())
    value_cl = int(dataframe['Value'].str.len().max())
    cl = [date_cl,site_cl,pollutant_cl,value_cl]                    # Generates list of column widths based on data length

    for x in range(len(columns)):                                   # Finds whichever is longer: header length or data length
        if len(columns[x]) > cl[x]:
            cl[x] = len(columns[x])

    hline,header = [],[]
    for i in range(len(cl)):                                        # Generate header/footer lines, spaced by values in list (cl)
        hline.append('+')
        hline.append('-'*int(cl[i]+4))
        header.append(columns[i] + ' '*int(cl[i]-len(columns[i])))
    hline.append('+')
    
    rl_start,rl_end,rl_mid = '|  ','  |','  |  '                    # Row line strings (used to construct separators)

    print(''.join(hline))
    print(rl_start + rl_mid.join(header) + rl_end)
    print(''.join(hline))
    for row in range(len(dataframe.index)):                         # For each row pad values with sufficient space (whitespace width: column width - data width)
        row_list = dataframe.iloc[row].tolist()
        row_list.insert(0,dataframe.index[row]) #
        for i in range(len(cl)):
             if len(row_list[i]) < cl[i]:
                row_list[i] = str(row_list[i]) + str(' '*int(cl[i]-len(row_list[i])))
        print(rl_start + rl_mid.join(row_list) + rl_end)
    print(''.join(hline))
       
def text_graph(dataframe:pd.DataFrame,height:int=10,view:int=0):
    """
    Generates text-based graph based on input dataframe
    Can generate multiple views:
        view = 0: normal graph
        view = 1: coloured bars by time
        view = 2: coloured bars by value
    Arguments:
        dataframe: parsed dataframe (see: parse_json())
        height (int): height of bars on graph
        view (int): integer between 0 and 2
    """
    max_value = dataframe['Value'].max()                                                # Reads variables from dataframe to generate axes data
    increment = max_value / height 
    values = dataframe['Value'].tolist()
    columns = dataframe.columns.tolist() 

    time_start,time_end = dataframe.index[0],dataframe.index[-1]                        # Find the time difference in seconds between start and end time of graph
    time_start = pd.to_datetime(time_start, format='%Y-%m-%d %H:%M:%S')
    time_end = pd.to_datetime(time_end, format='%Y-%m-%d %H:%M:%S')
    time_diff = time_end - time_start
    duration = time_diff.total_seconds()

    if duration > 3153000:
        time_start,time_end = time_start.strftime("%Y"),time_end.strftime("%Y")         # Displays different time formats based on time interval between start and finish
    elif duration > 2592000:
        time_start,time_end = time_start.strftime("%b"),time_end.strftime("%b")    
    elif duration > 86400:
        time_start,time_end = time_start.strftime("%b %d"),time_end.strftime("%b %d")
    else:
        time_start,time_end = time_start.strftime("%H:%M"),time_end.strftime("%H:%M")

    bar_height = [i // increment for i in values]
    chart_array = np.zeros((len(values),height),dtype='object')                         # Generates 2D array representing graph (y values = rows, x values = columns)
    for y in range(len(chart_array)):                                                   
         for x in range(int(bar_height[y])):                                            # Bars are coloured differently dependening on the value of view
            if view == 2:
                if x > 5:
                    chart_array[y,x] = '\033[0m\033[0;31m\u25ae\033[0;31m\033[0m'
                elif x > 2:
                    chart_array[y,x] = '\033[0m\033[1;33m\u25ae\033[1;33m\033[0m'
                else:
                    chart_array[y,x] = '\033[0m\033[0;32m\u25ae\033[0;32m\033[0m'   
            elif view == 1:   
                if int(bar_height[y]) > 6:
                    chart_array[y,x] = '\033[0m\033[0;31m\u25ae\033[0;31m\033[0m'
                elif int(bar_height[y]) > 3:
                    chart_array[y,x] = '\033[0m\033[1;33m\u25ae\033[1;33m\033[0m'
                else:
                    chart_array[y,x] = '\033[0m\033[0;32m\u25ae\033[0;32m\033[0m' 
            elif view == 0:
                chart_array[y,x] = '\u25ae'
            else:
                chart_array[y,x] = '\u25ae'
            
    y_axis = np.zeros(height,dtype='object')
    padding = '     '
    y_axis[::2] = padding                                       # Alternate values = whitespace
    for i in range(len(y_axis)):                                # Generates y axis values
        if y_axis[i] == 0:
            char = str(round(increment*i,1))
            y_axis[i] = char + ' '*int(len(padding)-len(char))

    chart_array = np.insert(chart_array,0,y_axis,axis=0)        # Insert y axis into 2D array
    chart_array = np.swapaxes(chart_array,0,1)                  # Swaps axes (x values = rows, y values = columns)
    chart_array = np.flip(chart_array, axis = 0)
    print(columns[0] + ':' + dataframe[columns[0]].iloc[0] + '\n' + columns[1] + ':' + dataframe[columns[1]].iloc[0] + '\n')

    x_axis = np.zeros(int(len(values)+1),dtype='object')
    x_axis[1:-2] = ' '                                          
    x_axis[0],x_axis[-1] = time_start,time_end                  # Time values are placed at start and end of the x axis
    chart_array = np.concatenate((chart_array,[x_axis]),axis=0) # Insert x axis in 2D array
    chart_array[np.where(chart_array[:] == 0)] = ' '            # Non-bar values = whitespace
    for row in chart_array:
        print(''.join(row))

def time_aggregate(dataframe:pd.DataFrame,start_date:datetime.datetime,end_date:datetime.datetime,interval:str) -> pd.DataFrame:
    """
    Finds subset of dataframe according to the start and end dates, resamples by specified interval

    Arguments:
        dataframe: parsed dataframe
        start_date (datetime): start of date range
        end_date (datetime): end of date range
        interval (str): specified interval (Min,H,M,D,Y)
    Returns:
        query (dataframe): resampled dataframe
    """
    dataframe.index = pd.to_datetime(dataframe.index)
    #dataframe['Value'] = dataframe['Value'].astype(int)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    query = dataframe.loc[start_date:end_date]
    query = query.resample(interval).mean()
    return query
