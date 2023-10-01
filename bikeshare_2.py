import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while True:
        cities = ['chicago', 'new york city', 'washington']
        city = input(
            "\n Enter city you would like to analyse? (Chicago, New york city, Washington) \n").lower()
        if city in cities:
            break
        else:
            print("\n Invalid input. Please enter a valid city name")

    # get user input for month (all, january, february, ... , june)
    while True:
        months = ['january', 'february', 'march',
                  'april', 'june', 'may', 'all']
        month = input(
            "\n Enter the month? (January, February, March, April, May, June)? Type 'all' for no month filter\n").lower()
        if month in months:
            break
        else:
            print("\n Please enter a valid month")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['monday', 'tuesday', 'wednesday', 'thursday',
                'friday', 'saturday', 'sunday', 'all']
        day = input("\n Enter the day of the week? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)? Type 'all' for no day filter \n").lower()
        if day in days:
            break
        else:
            print("\n Please enter a valid day")
    print(city, month, day)
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.strftime('%B')
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != "all":
        print("Filter data by month\n")
        df = df[df['month'] == month.title()]
        print(df)

    if day != "all":
        print("Filter data by Day of week\n")
        df = df[df['day_of_week'] == day.title()]

    df = pd.DataFrame(df)
    print(df)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_stats = df["Start Time"].dt.month.value_counts()
    most_common_month = month_stats.idxmax()
    print("The most common month:", most_common_month)

    # display the most common day of week
    day_stats = df["Start Time"].dt.day_name().value_counts()
    most_common_day = day_stats.idxmax()
    print("The most common day:", most_common_day)

    # display the most common start hour
    hour_stats = df["Start Time"].dt.hour.value_counts()
    most_common_hour = hour_stats.idxmax()
    print("The most common hour: ", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df["Start Station"].value_counts()
    common_start_station = start_station.idxmax()
    print("Most commonly used start station: ", common_start_station)

    # display most commonly used end station
    end_stats_station = df["End Station"].value_counts()
    common_end_station = end_stats_station.idxmax()
    print("Most commonly used end station: ", common_end_station)

    # display most frequent combination of start station and end station trip
    group_combination = df.groupby(
        ['Start Station', 'End Station']).size().reset_index(name='count')
    most_frequent_station = group_combination.loc[group_combination['count'].idxmax(
    )]
    print("Most frequent combination:")
    print("Start station: ", most_frequent_station['Start Station'])
    print("End station: ", most_frequent_station['End Station'])
    print("Count: ", most_frequent_station['count'])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Trip Duration'] = df['Trip Duration'].astype('int')

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print("Total duration: {} (seconds)".format(total_duration))

    # display mean travel time
    mean_travel_time = df.groupby(["Start Station", "End Station"])[
        "Trip Duration"].mean()
    print("Mean travel time:")
    print(mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print('Number of user types:')
    print(user_types)

    # Display counts of gender
    genders_count = df["Gender"].value_counts()
    print('Counts of gender:')
    print(genders_count)

    # Display earliest, most recent, and most common year of birth
    earliest_year_of_birth = int(df["Birth Year"].min())
    print("The Earliest Year of birth: ", earliest_year_of_birth)

    most_recent_yob = int(df["Birth Year"].max())
    print("Most recent year of birth: ", most_recent_yob)

    year_stats = df["Birth Year"].value_counts()
    most_common_year_of_birth = year_stats.idxmax()
    print("Most common year of birth:", int(most_common_year_of_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """ Display raw data """
    i = 0
    view_raw = input("Do you want to view raw data? (yes/no)\n").lower()
    pd.set_option('display.max_columns', 200)

    while True:
        if view_raw == 'no':
            break
        elif view_raw == 'yes':
            print(df.iloc[i:(i+5)])
            view_raw = input(
                "Do you want to view more raw data? (yes/no)\n").lower()
            i += 5
        else:
            view_raw = input(
                "\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


def main():
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        except BaseException:
            print("The data is invalid!")


if __name__ == "__main__":
    main()
