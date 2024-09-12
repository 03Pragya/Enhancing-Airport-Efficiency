from Fetch import getAirTrafficLandingData, getAirTrafficPassengerData
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns

def analysis1():
    landing_data = getAirTrafficLandingData()
    passenger_data = getAirTrafficPassengerData()

    print(landing_data.head())
    print(passenger_data.head())

    

    # Assuming landing_data and passenger_data are DataFrames obtained from your functions

    # Statistical Analysis
    landing_stats = landing_data.describe()
    passenger_stats = passenger_data.describe()

    # Display statistical summaries
    print("Landing Data Statistics:")
    print(landing_stats)

    print("\nPassenger Data Statistics:")
    print(passenger_stats)

    # Assuming landing_data and passenger_data are already loaded DataFrames

    # Histograms for numerical data in landing_data
    for column in landing_data.select_dtypes(include=['float64', 'int64']).columns:
        plt.figure(figsize=(8, 4))
        sns.histplot(landing_data[column], kde=False)
        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.show()

    # Boxplots for numerical data in passenger_data
    for column in passenger_data.select_dtypes(include=['float64', 'int64']).columns:
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=passenger_data[column])
        plt.title(f'Boxplot of {column}')
        plt.show()

    # Bar charts for categorical data in landing_data
    for column in landing_data.select_dtypes(include=['object']).columns:
        plt.figure(figsize=(10, 5))
        sns.countplot(y=landing_data[column])
        plt.title(f'Frequency of {column}')
        plt.xlabel('Frequency')
        plt.ylabel(column)
        plt.show()
