import time
import pandas as pd
import numpy as np

# Create variable to store city data
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please enter the name of the city (chicago, new york city, washington): ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid city name. Please choose from the provided options.')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please enter the name of the month (all, january, february, ..., june): ').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Invalid month name. Please choose from the provided options.')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please enter the name of the day of the week (all, monday, tuesday, ..., sunday): ').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Invalid day name. Please choose from the provided options.')

    print('-'*40)
    return city, month, day


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
    # Load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Start Time'].dt.month == month]

    # Filter by day of the week if applicable
    if day != 'all':
        df = df[df['Start Time'].dt.day_name() == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if 'Start Time' in df.columns:
        print('\n' + ' Calculating The Most Frequent Times of Travel '.center(78, '='))
        start_time = time.time()

        # Convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # Calculate and display the most common month
        popular_month = df['Start Time'].dt.month.mode()[0]
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        print('Most common Month'.ljust(40, '.'), months[popular_month - 1])

        # Calculate and display the most common day of week
        popular_day = df['Start Time'].dt.day_name().mode()[0]
        print('Most common day of the week'.ljust(40, '.'), popular_day)

        # Calculate and display the most common start hour
        popular_hour = df['Start Time'].dt.hour.mode()[0]
        print('Most common Start Hour'.ljust(40, '.'), popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if 'Start Station' in df.columns:
        popular_start_station = df['Start Station'].mode()[0]
        print('Most commonly used Start station'.ljust(40, '.'), popular_start_station)

    # Display most commonly used end station
    if 'End Station' in df.columns:
        popular_end_station = df['End Station'].mode()[0]
        print('Most commonly used End station'.ljust(40, '.'), popular_end_station)

    # Display most frequent combination of start station and end station trip
    if 'Start Station' in df.columns and 'End Station' in df.columns:
        df['route'] = df['Start Station'] + ' -> ' + df['End Station']
        popular_route = df['route'].mode()[0]
        print('Most frequent route'.ljust(40, '.'), popular_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time, 'seconds')

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if 'User Type' in df.columns:
        print('\n' + ' User type stats '.center(78, '-'))
        print(df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\n' + ' Gender stats '.center(78, '-'))
        df['Gender'].replace(np.nan, 'not disclosed', inplace=True)
        print(df['Gender'].value_counts(dropna=False))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\n' + ' Age stats '.center(78, '-'))
        print('Earliest Birth Year'.ljust(40, '.'), int(df['Birth Year'].min()))
        print('Most recent Birth Year'.ljust(40, '.'), int(df['Birth Year'].max()))
        print('Most common Birth Year'.ljust(40, '.'), int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays 5 rows of individual trip data and asks the user if they want to continue."""

    start_loc = 0
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no: ').lower()

    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input('Do you wish to continue? Enter yes or no: ').lower()

        while view_data not in ['yes', 'no']:
            print('Invalid input. Please enter yes or no.')
            view_data = input('Do you wish to continue? Enter yes or no: ').lower()

    print('Thank you for using the data viewer!')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        display_data(df)  # Call to display 5 rows of station-related data
        trip_duration_stats(df)
        display_data(df)  # Call to display 5 rows of trip duration-related data
        user_stats(df)
        display_data(df)  # Call to display 5 rows of user-related data

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Stop program !')
            break


if __name__ == "__main__":
	main()
