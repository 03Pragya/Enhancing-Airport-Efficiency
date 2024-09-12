import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Fetch import getAirTrafficLandingData, getAirTrafficPassengerData
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import numpy as np


def DataAnalysis():
    # Load the datasets
    landing_data = getAirTrafficLandingData()
    passenger_data = getAirTrafficPassengerData()

    # Ensure 'activity_period' is of the same data type in both datasets
    landing_data['activity_period'] = landing_data['activity_period'].astype(str)
    passenger_data['activity_period'] = passenger_data['activity_period'].astype(str)
    # print("Columns in landing_data:", landing_data.columns)
    # print("Columns in passenger_data:", passenger_data.columns)
    # Merge datasets on common columns
    merged_data = pd.merge(landing_data, passenger_data, on=["activity_period", "operating_airline", "operating_airline_iata_code"])
    print(merged_data)
    MLAlgo(merged_data)
    

def MLAlgo(merged_data):
    merged_data['activity_period_start_date_year'] = merged_data['activity_period_start_date_y'].dt.year
    merged_data['activity_period_start_date_month'] = merged_data['activity_period_start_date_y'].dt.month
    merged_data['activity_period_start_date_day'] = merged_data['activity_period_start_date_y'].dt.day

    # Drop original datetime columns and other non-predictive columns
    columns_to_drop = ['activity_period_start_date_y', 'data_as_of_y', 'data_loaded_at_y', 
                    'activity_period', 'data_as_of_x', 'data_loaded_at_x']
    merged_data.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    # Select categorical columns for one-hot encoding
    categorical_cols = merged_data.select_dtypes(include=['object']).columns

    # Create a Column Transformer to One-Hot Encode categorical variables
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ])

    # Define the target variable (y) and features (X)
    X = merged_data.drop('passenger_count', axis=1)
    y = merged_data['passenger_count']

    # Apply the preprocessing to the dataset
    X = preprocessor.fit_transform(X)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a Random Forest Regressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    # Scatter plot of actual vs predicted values
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.title('Actual vs Predicted Passenger Counts')
    plt.xlabel('Actual Counts')
    plt.ylabel('Predicted Counts')
    plt.plot(np.unique(y_test), np.poly1d(np.polyfit(y_test, y_pred, 1))(np.unique(y_test)), color='red')  # regression line
    plt.show()

    # Get feature names after one-hot encoding
    onehot_columns = list(preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_cols))
    numeric_columns = merged_data.select_dtypes(include=[np.number]).columns.drop('passenger_count').tolist()
    all_columns = numeric_columns + onehot_columns

    # Get feature importances
    importances = model.feature_importances_

        # Get the feature names from the column transformer
    onehot_columns = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_cols)
    # If you have numeric features that are not encoded, add them to the list as well
    numeric_features = merged_data.select_dtypes(include=[np.number]).columns.drop('passenger_count')
    feature_names = np.concatenate((numeric_features, onehot_columns))

    # Sort feature importances in descending order and get the indices
    indices = np.argsort(importances)[::-1]

    # Define how many top features you want to display
    top_n = 10

    # Select the top N feature importances
    top_n_indices = indices[:top_n]
    top_n_importances = importances[top_n_indices]
    top_n_names = feature_names[top_n_indices]

    # Create the plot for the top N features
    plt.figure(figsize=(10, 6))
    plt.title("Top Feature Importances")
    plt.bar(range(top_n), top_n_importances, color='skyblue')
    plt.xticks(range(top_n), top_n_names, rotation=90)
    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.tight_layout()  # Adjust layout to fit all feature names
    plt.show()
