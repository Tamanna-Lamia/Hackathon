import pandas as pd
import os
from pathlib import Path as PathlibPath
from app.Utils.utils import parse_file_name
from config import DirectoryPath, Config
from datetime import datetime


def clean_data(df):
    # Rename columns from Swedish to English
    column_mapping = {
        "Period": "Timestamp",  # Rename 'Period' to 'Timestamp'
        "Förbrukning": "Consumption"  # Rename 'Förbrukning' to 'Consumption'
    }
    df.rename(columns=column_mapping, inplace=True)

    # Check for null values
    print("Checking for null values...")
    print(df.isnull().sum())

    # Drop rows with null values
    df.dropna(inplace=True)

    #other df imputation techniques

    # Ensure the Timestamp column is in datetime format
    # Use `format` to explicitly parse the date and time
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

    # Drop rows where Timestamp conversion failed (optional, for invalid rows)
    df = df.dropna(subset=['Timestamp'])

    # Filter rows for the year 2023
    df = df[df['Timestamp'].dt.year == 2023]

    # Convert the Timestamp column to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Extract the date from the Timestamp
    df['Date'] = df['Timestamp'].dt.date

    # Group by the Date and calculate the total consumption for each day-daily total consumption
    df = df.groupby('Date')['Consumption'].sum().reset_index()

    print("Data Cleaned : \n")
    return df
    # # Save the cleaned data to a new CSV file
    # df.to_csv(output_file, index=False)

    # print(f"Cleaned data saved to: {output_file}")

def get_weather_data(school_name):
    weather_file = PathlibPath(DirectoryPath.WEATHER_DIRECTORY) / f"{school_name}.csv"
    data = pd.read_csv(weather_file, encoding='utf-8')
    return data



def add_weather_data(df, weather_df):
    
    # Convert the Date column in df to datetime format and reformat it
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True).dt.strftime('%d-%m-%Y')  # Change format to DD-MM-YYYY

    # Convert the time column in weather_df to datetime format and reformat it
    weather_df['time'] = pd.to_datetime(weather_df['time'], format='%m/%d/%y')  # Adjust format if needed
    weather_df['Date'] = weather_df['time'].dt.strftime('%d-%m-%Y')  # Change format to DD-MM-YYYY

    # Drop the 'time' column in weather_df as it is no longer needed
    weather_df = weather_df.drop(columns=['time'])

    # Select only the necessary columns from the weather dataframe
    weather_df = weather_df[['Date', 'weather_code (wmo code)', 'temperature_2m_max (°C)',
                            'daylight_duration (s)', 'rain_sum (mm)', 'snowfall_sum (cm)', 'wind_speed_10m_max (km/h)']]

    # Merge the dataframes on the Date column, avoiding duplicate columns
    merged_df = pd.merge(df, weather_df, on='Date', how='left')

    # Show the first few rows of the merged dataset
    print("Merged PDF : " , merged_df.head())
    
    return merged_df


def write_to_file(df):
    # Ensure the downloads folder exists
    os.makedirs(DirectoryPath.DOWNLOAD_FOLDER, exist_ok=True)

    # Create a unique filename using a timestamp
    #timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    #unique_filename = f"data_{timestamp}.csv"

    # Full path to the file
    file_path = os.path.join(DirectoryPath.DOWNLOAD_FOLDER, Config.DOWNLOAD_NAME)

    # Write the DataFrame to a CSV file
    df.to_csv(file_path, index=False)

    print(f"DataFrame successfully saved to {file_path}")

def standardise_file(filename, data): 
    print("Original Data", data)
    cleaned_data = clean_data(data)
    file_details = parse_file_name(filename)
    print(file_details)
    weather_data = get_weather_data(file_details["school_name"])
    print("Cleaned" , cleaned_data.head())
    print("Weather Data", weather_data.head())
    merged_data = add_weather_data(cleaned_data, weather_data)
    write_to_file(merged_data)
    
    
    

