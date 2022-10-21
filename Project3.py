import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}

# MOnths of the year for input validation              
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'NOv', 'Dec']

# Days of the week format for input validation
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
DAYS_IN_FULL = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MONTHS_IN_FULL = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which City would you like to explore? chicago, new york or washington.\n')
    while city.lower() not in CITY_DATA:
        city = input("INPUT ERROR! Please enter a city in this format - 'new york' or 'chicago' or 'washington'")
    print(f'Great! Here is a list of {city.capitalize()} statistics.\n')

    # get user input for month (all, january, february, ... , june)
    filters = input('Would you like to filter the data by month and day or none? Type "none" if you do not want to filter. \n')
    if filters == "None" or filters.lower() == "none":
        month = 'none'
        day = 'none'
        return city.lower(), month, day
    else:
        month = input('Please select a month you would like to explore (January to June). Please use this formart Jan Feb Mar Apr May Jun\n')
        while month not in MONTHS:
            month = input('ERROR:INVALID INPUT.\nPlease select month in this format. Jan Feb Mar Apr May Jun\n')
        month = month.capitalize()
    # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('Please select a day of the week in this format - Mon, Tue, Wed, Thu, Fri, Sat, Sun\n')
        while day not in DAYS:
            day = input('ERROR: INVALID INPUT.\nPlease use this format - Mon, Tue, Wed, Thu, Fri, Sat, Sun\n')
        day = day.capitalize()
    return city.lower(), month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    if month == 'none' or day == 'none':
        return df
    else:
        mes = MONTHS.index(month) + 1
        month_filter_map = df['Start Time'].dt.month == mes
        filtered_df = df[month_filter_map]
        dia = DAYS.index(day)
        day_filter_map = filtered_df['Start Time'].dt.dayofweek == dia
        overall_filtered_data = filtered_df[day_filter_map]
        #print(overall_filtered_data['Start Time'].dt.hour.value_counts())
        return overall_filtered_data


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months_data = dict(df['Start Time'].dt.month.value_counts())
    months_in_list = list(months_data.keys())
    pop_month = months_in_list[0]
    pop_month_stats = months_data[pop_month]
    print(f'Most Popular month for riding bikes is {MONTHS_IN_FULL[pop_month]}, Count: {pop_month_stats}')
    
    # display the most common day of week
    days_data = dict(df['Start Time'].dt.dayofweek.value_counts())
    days_in_list = list(days_data.keys())
    pop_day = days_in_list[0]
    pop_day_stats = days_data[pop_day]
    print(f'Most Popular day for riding bikes is {DAYS_IN_FULL[pop_day]}')
    
    # display the most common start hour
    hours_data = dict(df['Start Time'].dt.hour.value_counts())
    hours_in_list = list(hours_data.keys())
    pop_hour = hours_in_list[0]
    pop_hour_stats = hours_data[pop_hour] 
    print(f'Most Popular hour for riding bikes on {DAYS_IN_FULL[pop_day]} is {pop_hour}:00 HRS')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stations = dict(df['Start Station'].value_counts())
    pop_start_station = list(start_stations.keys())
    print(f'The most popular Start Station: {pop_start_station[0]}, Count = {start_stations[pop_start_station[0]]}\n')

    # display most commonly used end station
    end_stations = dict(df['End Station'].value_counts())
    pop_end_station = list(end_stations.keys())
    print(f'End Station: {pop_start_station[0]} Count = {end_stations[pop_end_station[0]]}\n')

    # display most frequent combination of start station and end station trip
    trips_df = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Next Statistic...Most Popular Trip\n')
    print(f'Trip: {trips_df}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(f'Total Duration: {df["Trip Duration"].sum()}s, Count: {df["Trip Duration"].count()} trips.\n')

    # display mean travel time
    print(f'Average Duration: {df["Trip Duration"].mean()}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = dict(df['User Type'].value_counts())
    print(user_types)

    # Display counts of gender
    try:
        genders = dict(df['Gender'].value_counts())
        print(genders)
    except:
        print('Sorry! Washington does not have Gender data.\n')

    # Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    response = input('Would you like to view 5 rows of individual trip data? Enter yes or no.\n ')
    start_loc = 0
    while response.lower() != 'no':
        print(df[start_loc:start_loc+5])
        response = input('Do you wish to continue? Enter yes or no.\n')
        start_loc += 5
    return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
