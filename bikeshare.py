import time 
import pandas as pd
import numpy as np

#City data as a dictionary of city names and the corresponding CSV's.
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# Initialize the month data list, made it global for use in multiple functions
MONTH_DATA = ['all','january','february','march', 'april','may','june']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \n')
    # Initialize empty city variable
    city = ''
    #While loop to verify input is correct
    while city not in CITY_DATA.keys():
        city = input('Would you like to explore data for Chicago, New York City, or Washington? \n\nPlease enter the full name of the city : ' ).strip().lower()      
        if city not in CITY_DATA.keys():
            print('That input is invalid, please select one of that available cities (Chicago, New York City or Washington), re-prompting...')
    print('\nYou have chosen {} as your city'.format(city.title()))
    # Get user input for month (all, january, february, ... , june)
    # Initalize empty month variable
    month = ''
    # While loop to verify input is correct
    while month not in MONTH_DATA:
        month = input('\nPlease select which month you would like to view the data for. \n\nYou may select any month January through June. \n\nYou may also view data for all months combined by typing ALL (not case sensitive) : ').strip().lower()
        if month not in MONTH_DATA:
            print('That input is invalid, please select one of the available months January through June, re-prompting...')
    print('\nYou have chosen {} as your month'.format(month.title()))
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    # Create a list to store the day info
    DAY_DATA = ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']
    # Initalize day variable
    day = ''
    #While loop to verify the input is correct.
    while day not in DAY_DATA:
        day = input('\nPlease select which day you would like to view the data for. \n\nYou may select day Sunday through Saturday. \n\nYou may also view data for all days by typing ALL (not case sensitive): ').strip().lower()
        if day not in DAY_DATA:
            print('That is not a valid day, please select a day Sunday through Saturday, re-prompting...')
    print('\nYou have chosen {} as your day of the week'.format(day.title()))

    print('\nYour final selections:\n\n CITY: {}, MONTH: {}, WEEKDAY: {}'.format(city.upper(), month.upper(), day.upper()))

    print('-'*40)
    # Return selections 
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
    # Import the data from the csv
    df = pd.read_csv(CITY_DATA[city])
    # Change the start time column from string datetime information for manipulation
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Filter by desired month using the index of MONTH_DATA
    if month != 'all':
        df = df[df['Start Time'].dt.month == MONTH_DATA.index(month)]
    # Filter by desired day    
    if day != 'all':
        df = df[df['Start Time'].dt.day_name() == day.title()]



  

    # Return the filtered data frame
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (dataframe) df - data frame we are working with.
        
    Returns:
        None
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print("\nThe most popular month is: ", MONTH_DATA[df['Start Time'].dt.month.mode()[0]].title())

    # Display the most common day of week
    print("\nThe most popular day is: ",df['Start Time'].dt.day_name().mode()[0])

    # Display the most common start hour
    print("\nThe most popular start hour is: ",df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        (dataframe) df - data frame we are working with.
        
    Returns:
        None
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('The most commonly used start station is: ',df['Start Station'].mode()[0])


    # Display most commonly used end station
    print('\nThe most commonly used end station is: ',df['End Station'].mode()[0])

    # Display most frequent combination of start station and end station trip
    print('\nThe most frequent combination of start and end stations is: ')
    print('Start Station: ', df.groupby(['Start Station','End Station']).size().idxmax()[0])
    print('End Station: ', df.groupby(['Start Station','End Station']).size().idxmax()[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        (dataframe) df - data frame we are working with.
        
    Returns:
        None
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    # Initalize minutes and seconds and assign them the output of divmod as values
    # Rounding to reduce decimals
    tot_minutes,tot_seconds = divmod(round(df['Trip Duration'].sum()),60)

    # Initialize hours and reassing based on the first index of the divmod
    # Reassigning minutes the second values of the divmod tuple now that we have hours.
    tot_hours,tot_minutes = divmod(tot_minutes,60)

    # Display mean travel time
    # Initalize average minutes and seconds and assign them the output of divmod as values
    # Rounding to reduce decimals
    avg_minutes, avg_seconds = divmod(round(df['Trip Duration'].mean()),60)

    # Initialize hours and reassing based on the first index of the divmod
    # Reassigning minutes the second values of the divmod tuple now that we have hours.
    avg_hours,avg_minutes = divmod(avg_minutes,60)

    # Print results
    print(f"The total trip duration is {tot_hours} Hours {tot_minutes} Minutes {tot_seconds} Seconds.\n")
    print(f"The average trip duration is {avg_hours} Hours {avg_minutes} Minutes {avg_seconds} Seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        (dataframe) df - data frame we are working with.
        
    Returns:
        None
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # Use value counts to display the count of subscribers and customers
    print('\nThe count of total users is:\n',df['User Type'].value_counts())


    # Display counts of gender
    # If there is no gender column in the data frame return unavailable, else print the counts
    if 'Gender' not in df.columns:
        print('There is no gender information available in this data set.')
    else:
        print('The count of users by genders is: \n',df['Gender'].value_counts())



    # Display earliest, most recent, and most common year of birth
    # If there is no birth year column then display the info
    if 'Birth Year' not in df.columns:
        print('There is no birth year information available in this data set.')
    else:
        print('\nThe earlist birth year is: ', int(df['Birth Year'].min()))
        print('\nThe most recent birth year is: ',int(df['Birth Year'].max()))
        print('\nThe most common birth year is: ', int(df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_display(df):
    '''
    Displays 5 rows of data from the slected csv file

    Args:
        (dataframe) df - data frame we are working with.
        
    Returns:
        None
    '''
    
    i = 0
    chunk_size = 5
    acceptable_responses = ['yes', 'no']
    user_input = ''
    # While loop to verify input is correct
    while user_input not in acceptable_responses:
        user_input = input('Would you like to see the first five lines of data? (yes/no): ').strip().lower()    
        if user_input not in acceptable_responses:
            print('\nThat input is invalid, please select yes or no, re-prompting...')
    # Start chunking the data if the user chooses yes        
    if user_input == 'yes':
        while i < len(df):
            chunk = df.iloc[i:i + chunk_size]
    
    # Print the current chunk
            print(chunk)
    
    # Update the starting index for the next chunk
            i += chunk_size
    
    # Ask the user if they want to see the next 5 items if there are more items to show
            if i < len(df):  
                user_input = input('Do you want to see the next 5 items? (yes/no): ').strip().lower() 
                while user_input not in acceptable_responses: 
                    user_input = ('That input is invalid, please select yes or no: ')
                if user_input != 'yes':
                    print("Exiting data display.")
                    break
            else:
                print("No more items to display.")

# Main function combining all functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        data_display(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
