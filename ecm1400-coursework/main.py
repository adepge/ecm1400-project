import datetime,time
import pandas as pd
import numpy as np

splash = '\n\033[0m\u001b[36m       d8888  .d8888b.   .d88888b.  888     888       d8888\n      d88888 d88P  Y88b d88P" "Y88b 888     888      d88888\n     d88P888 888    888 888     888 888     888     d88P888\n    d88P 888 888        888     888 888     888    d88P 888\n   d88P  888 888        888     888 888     888   d88P  888\n  d88P   888 888    888 888 Y8b 888 888     888  d88P   888\n d8888888888 Y88b  d88P Y88b.Y8b88P Y88b. .d88P d8888888888\nd88P     888  "Y8888P"   "Y888888"   "Y88888P" d88P     888\n                               Y8b                         \u001b[36m\033[0m\n'                          


def main_menu():
    """
    Main menu procedure: user interface for selecting a module in ACQUA system

    Available activities
        R:  reporting()
        I:  intelligence()
        M:  monitoring()
        A:  candidate info
        Q:  prompt to quit program
    Inputs:
        valid: R,I,M,A,Q
        invalid: everything else
    """
    valid = False
    while valid == False:
        prompt = input('_'*59 + '\n'*3 + ' '*8 + 'Select one of the following:\n' + 
                                        ' '*8 + 'R - Access the PR (Pollution Reporting) module\n' +
                                        ' '*8 + 'I - Access the MI (Mobility Intelligence) module\n' + 
                                        ' '*8 + 'M - Access the RM (Real-time Monitoring) module\n' +
                                        ' '*8 + 'A - Print the About text\n' +
                                        ' '*8 + 'Q - Quit the application\n' + '\n'*2 + '_'*59 + '\n\nSelection: ')
        if prompt.lower() == 'r':    
            valid = True
            return reporting_menu()
        elif prompt.lower() == 'i':
            valid = True
            return intelligence_menu()
        elif prompt.lower() == 'm':
            valid = True
            return monitoring_menu()
        elif prompt.lower() == 'a':
            valid = True
            return about()
        elif prompt.lower() == 'q':
            valid = True
            return quit()
        else:
            valid = False
    
def reporting_menu():
    """
    Procedure to access monitoring menu

    Available activities
        For a selected monitoring site and pollutant:
            A: Find daily average
            B: Find daily median
            C: Find hourly average
            D: Find monthly average
            E: Find peak hour for selected date
    """
    import reporting                                                          
    all_data = reporting.import_data()
    selection_complete = False
    while selection_complete == False:
        site_valid = False
        site = ' '
        while site_valid == False:
            prompt = input('_'*59 + '\n\n[Enter Q to go back to main menu]' + '\n'*3 + 
                                            ' '*8 + 'PR (Pollution reporting) module \n\n' + 
                                            ' '*8 + 'Select data below to begin:\n\n' +
                                            ' '*8 + f'Site: {site}\n\n' + 
                                            ' '*8 + 'M - Marylebone Road\n' +
                                            ' '*8 + 'K - N. Kensington\n' +
                                            ' '*8 + 'H - Harlington\n\n' +
                                            '_'*59 + '\n\nSite: ')
            if prompt.lower() == 'm':
                site_valid = True    
                site = 'Marylebone Road'
            elif prompt.lower() == 'k':
                site_valid = True
                site = 'N Kensington'
            elif prompt.lower() == 'h':
                site_valid = True
                site = 'Harlington'
            elif prompt.lower() == 'q':
                site_valid = True
                return main_menu()
            else:
                site_valid = False
        pollutant_valid = False
        pollutant = ' '
        while pollutant_valid == False:                                                        
            prompt = input('_'*59 + '\n\n[Enter Q to go back to main menu]' + '\n'*3 + 
                                            ' '*8 + 'PR (Pollution reporting) module \n\n' + 
                                            ' '*8 + 'Select data below to begin:\n\n' +
                                            ' '*8 + f'Site: {site}\n\n' + 
                                            ' '*8 + f'Pollutant: {pollutant}\n' +
                                            ' '*8 + 'N - NO \n' +
                                            ' '*8 + 'O - PM10\n' +
                                            ' '*8 + 'P - PM25\n\n' +
                                            '_'*59 + '\n\nPollutant: ')
            if prompt.lower() == 'n':
                pollutant_valid = True    
                pollutant = 'no'
            elif prompt.lower() == 'o':
                pollutant_valid = True
                pollutant = 'pm10'
            elif prompt.lower() == 'p':
                pollutant_valid = True
                pollutant = 'pm25'
            elif prompt.lower() == 'q':
                pollutant_valid = True
                return main_menu()
            else:
                pollutant_valid = False
        operation_valid = False
        while operation_valid == False:                                                        
            prompt = input('_'*59 + '\n\n[Enter Q to go back to main menu]' + '\n'*3 + 
                                            ' '*8 + 'PR (Pollution reporting) module \n\n' + 
                                            ' '*8 + 'Select a procedure you would like to do:\n\n' +
                                            ' '*4 + f'Site: {site}      Pollutant: {pollutant}\n\n' + 
                                            ' '*8 + 'A - Find daily average \n' +
                                            ' '*8 + 'B - Find daily median \n' +
                                            ' '*8 + 'C - Find hourly average \n' +
                                            ' '*8 + 'D - Find monthly average \n' +
                                            ' '*8 + 'E - Find peak hour (for a given date)\n' +
                                            '_'*59 + '\n\nChoice (A-E): ')
            if prompt.lower() == 'a':
                operation_valid = True
                print(reporting.daily_average(all_data, site, pollutant))
                time.sleep(1)
                return reporting_menu()
            elif prompt.lower() == 'b':
                operation_valid = True
                print(reporting.daily_median(all_data, site, pollutant))
                time.sleep(1)
                return reporting_menu()                
            elif prompt.lower() == 'c':
                operation_valid = True
                print(reporting.hourly_average(all_data, site, pollutant))
                time.sleep(1)
                return reporting_menu()                
            elif prompt.lower() == 'd':
                operation_valid = True
                print(reporting.monthly_average(all_data, site, pollutant))  
                time.sleep(1)
                return reporting_menu() 
            elif prompt.lower() == 'e':    
                operation_valid = True                                               
                sel_date = select_date(0)
                print(reporting.peak_hour_date(all_data,sel_date,site,pollutant))
                time.sleep(1)
                return reporting_menu()
            else:
                operation_valid = False

def select_date(order):
    import calendar
    keyword = ['starting','ending']
    month_valid = False
    year,month,day,hour = 2021,'MM','DD','HH'
    while month_valid == False:
        prompt = input('_'*59 + '\n\n[Enter Q to go back to main menu]' + '\n'*3 + 
                                        ' '*8 + 'Date selection\n\n' + 
                                        ' '*8 + 'Select data below to begin:\n\n' +
                                        ' '*8 + '1:Jan   2:Feb     3:Mar   4:Apr\n' +
                                        ' '*8 + '5:May   6:Jun     7:Jul   8:Aug\n' +
                                        ' '*8 + '9:Sep  10:Oct    11:Nov  12:Dec\n\n' +
                                        '_'*59 + f'\n\nSelect {keyword[order]} month number: ')
        if prompt.lower() == 'q':
            month_valid = True
            return main_menu()
        elif len(prompt) > 0:
            prompt = int(prompt) 
        if prompt in range(1,13): 
            month_valid = True  
            month = int(str(prompt).zfill(2))
        else:
            month_valid = False
    day_valid = False
    month_cal = calendar.month(year,month)
    num_days = int(calendar.monthrange(year,month)[1]) + 1
    print(range(1,num_days))
    while day_valid == False:
        prompt = input('_'*59 + '\n\n[Enter Q to go back to main menu]' + '\n'*3 + 
                                        ' '*8 + 'Date selection \n\n' + 
                                        ' '*8 + 'Select data below to begin:\n\n' +
                                        '\n\n' + f'{month_cal}' + 
                                        '_'*59 + f'\n\nSelect {keyword[order]} day: ')
        if prompt.lower() == 'q':
            day_valid = True
            return main_menu()
        elif len(prompt) > 0:
            prompt = int(prompt) 
        if prompt in range(1,num_days): 
            day_valid = True  
            day = int(str(prompt).zfill(2))

        else:
            day_valid = False
    sel_time = str(year) + '-' + str(month) + '-' + str(day)
    return sel_time

def monitoring_menu():
    """
    Procedure to access monitoring menu

    Available activities
        A: Make API request
        B: Print request as formatted table
        C: Print request as graph
        D: Change date range of request
    """
    import monitoring,time
    request = monitoring.get_live_data_from_api()
    choice = False
    while choice == False:
        prompt = input('_'*59 + '\n\n[Enter Q to go back to main menu]' + '\n'*3 + 
                                            ' '*8 + 'RM (Realtime-monitoring) module \n\n' + 
                                            ' '*8 + 'Select data below to begin:\n\n' +
                                            ' '*8 + 'A - Input site/species code and date\n' +
                                            ' '*8 + 'B - Print data in table\n' +
                                            ' '*8 + 'C - Show data as graph\n' +
                                            ' '*8 + 'D - Selecte time range\n\n' +
                                            '_'*59 + '\n\nChoice (A,B,C,D): ')
        if prompt.lower() == 'a':   
            choice = True 
            code = input("Input site code: ")
            species = input("Input species code: ")
            start_date = select_date(0)
            end_date = select_date(1)
            request = monitoring.get_live_data_from_api(code,species,start_date,end_date)
            print('Warning: Selecting a large range of time may take longer to request')
            return monitoring_menu()
        elif prompt.lower() == 'b':
            choice = True
            monitoring.special_print(monitoring.parse_json(request))
            time.sleep(4)
            return monitoring_menu()
        elif prompt.lower() == 'c':
            choice = True
            schoice = False
            while schoice == False:
                prompt = input('_'*59 + '\n\n[Enter Q to go back to main menu]' + '\n'*3 + 
                                            ' '*8 + 'MI (Mobility intelligence) module \n\n' + 
                                            ' '*8 + 'Select graph view:\n\n' +
                                            ' '*8 + 'A - Normal view\n' +
                                            ' '*8 + 'B - Heatmap(x)\n' +
                                            ' '*8 + 'C - Heatmap(y)\n' +
                                            '_'*59 + '\n\nChoice (A,B,C): ')
                if prompt.lower() == 'a':
                    schoice = True 
                    monitoring.text_graph(monitoring.parse_json(request),view=0)
                    time.sleep(2)
                    return monitoring_menu()
                elif prompt.lower() == 'b':
                    schoice = True 
                    monitoring.text_graph(monitoring.parse_json(request),view=1)
                    time.sleep(2)
                    return monitoring_menu()
                elif prompt.lower() == 'c':
                    schoice = True 
                    monitoring.text_graph(monitoring.parse_json(request),view=2)
                    time.sleep(2)
                    return monitoring_menu()
                elif prompt.lower() == 'q':
                    schoice = True
                    return main_menu()
                else:
                    schoice = False
        elif prompt.lower() == 'd':
            choice = True 
            begin = select_date(0)
            end = select_date(1)
            tvalid = False
            while tvalid == False:
                interval = input("Enter a valid time interval:")
                if interval == 'M': tvalid = True
                elif interval == 'D': tvalid = True
                elif interval == 'H': tvalid = True
                else: tvalid = False
            monitoring.time_aggregate(monitoring.parse_json(request), datetime.date.strftime(begin, format="%Y-%m-%d"), datetime.date.strftime(end, format="%Y-%m-%d"))
            return monitoring_menu()
        elif prompt.lower() == 'q':
            choice = True
            return main_menu()
        else:
            choice = False

def intelligence_menu():
    """
    Procedure to access intelligence menu
    
    Available activities
        A: Find red pixels
        B: Find cyan pixels
        C: Find connected components
    """
    import intelligence,os.path
    choice = False
    while choice == False:
        prompt = input('_'*59 + '\n\n[Enter Q to go back to main menu]' + '\n'*3 + 
                                            ' '*8 + 'MI (Mobility intelligence) module \n\n' + 
                                            ' '*8 + 'Select data below to begin:\n\n' +
                                            ' '*8 + 'A - Find red pixels\n' +
                                            ' '*8 + 'B - Find cyan pixels\n' +
                                            ' '*8 + 'C - Find connected components\n\n' +
                                            '_'*59 + '\n\nChoice (A,B,C): ')
        if prompt.lower() == 'a':   
            choice = True 
            intelligence.find_red_pixels('data/map.png')
            return intelligence_menu()
        elif prompt.lower() == 'b':
            choice = True
            intelligence.find_cyan_pixels('data/map.png')
            return intelligence_menu()
        elif prompt.lower() == 'c':
            schoice = False
            while schoice == False:
                prompt = input('_'*59 + '\n\n[Enter Q to go back to main menu]' + '\n'*3 + 
                                            ' '*8 + 'MI (Mobility intelligence) module \n\n' + 
                                            ' '*8 + 'Select data below to begin:\n\n' +
                                            ' '*8 + 'A - Find connected components for red pixels\n' +
                                            ' '*8 + 'B - Find connected components for cyan pixels\n' +
                                            '_'*59 + '\n\nChoice (A,B): ')
                if prompt.lower() == 'a':
                    schoice = True 
                    if os.path.exists('data/map-red-pixels.jpg') == False:
                        intelligence.find_red_pixels('data/map.png')
                    intelligence.detect_connected_components_sorted(intelligence.detect_connected_components('data/map-red-pixels.jpg'))
                    return intelligence_menu()
                elif prompt.lower() == 'b':
                    schoice = True 
                    if os.path.exists('data/map-cyan-pixels.jpg') == False:
                        intelligence.find_cyan_pixels('data/map.png')
                    intelligence.detect_connected_components_sorted(intelligence.detect_connected_components('data/map-cyan-pixels.jpg'))
                    return intelligence_menu()
                elif prompt.lower() == 'q':
                    schoice = True
                    return main_menu()
                else:
                    schoice = False
        elif prompt.lower() == 'q':
            choice = True
            return main_menu()
        else:
            choice = False

def about():
    """
    Prints vital information about a student with the following qualities:
        - Stressed
        - Starts projects a little later than he should
        - Average coding skill
        - Tends to be sleepy
    """
    print('\nModule number: ECM1400')
    print('Candidate number: 247675\n')
    time.sleep(2)
    main_menu()

def quit():
    """
    Procedure to quit ACQUA program

    Inputs:
        yes/y (valid): quits program
        no/n (valid): returns to main menu
        other (invalid): reprompts user
    """
    import sys
    valid = False
    while valid == False:
        prompt = input('_'*31 + '\n' + ' '*30 + '\nAre you sure you want to quit?\n' + ' '*30 + '\n    [Yes: Y]       [No: N]    ' + '\n' + '_'*31 + '\n\nPrompt:')
        if prompt.lower() == 'y' or prompt.lower() == 'yes':        
            valid = True
            print(splash)
            time.sleep(1)
            sys.exit()
        elif prompt.lower() == 'n' or prompt.lower() == 'no':
            valid = True
            return main_menu()
        else:
            valid = False

if __name__ == '__main__':
    print(splash)
    time.sleep(1)
    main_menu()