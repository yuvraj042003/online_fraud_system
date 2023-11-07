import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from fraud_detection_app.models import Transaction, FraudCase
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.exceptions import DataConversionWarning
import warnings

# Suppress warnings
warnings.filterwarnings(action='ignore', category=DataConversionWarning)


# Function to predict fraud based on from_account_number and to_account_number
def predict_fraud(from_account, to_account):
    # Fetch data from the Django models
    transactions = Transaction.objects.all()
    fraud_cases = FraudCase.objects.all()

    # Create DataFrames from the fetched data
    transactions_df = pd.DataFrame(list(transactions.values()))
    fraud_cases_df = pd.DataFrame(list(fraud_cases.values()), columns=['transaction_id', 'isfraud'])

    print(transactions_df)
    print('--------------------------------------------1')
    print(fraud_cases_df)
    print('--------------------------------------------2')    
    # Ensure 'transaction_id' column data type is consistent
    transactions_df['transaction_id'] = transactions_df['transaction_id'].astype(int)
    fraud_cases_df['transaction_id'] = fraud_cases_df['transaction_id'].astype(int)

    # Merge the two DataFrames on 'transaction_id' to determine if a transaction is fraudulent
    data = pd.merge(transactions_df, fraud_cases_df, on='transaction_id', how='left')

    # If 'isfraud' is boolean, convert it to integer (1 for True, 0 for False)
    # data['isfraud'] = data['isfraud'].astype(int)
    data['isfraud'] = data['isfraud'].fillna(1).astype(int)

    print('----------------------------------------')
    print(data)
    print('----------------------------------------')
    # Identify numerical and categorical columns
    numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
    categorical_columns = data.select_dtypes(include=['object']).columns

    # Fill missing values for numerical columns
    for col in numerical_columns:
        data[col].fillna(data[col].mean(), inplace=True)

    # Fill missing values for categorical columns
    for col in categorical_columns:
        data[col].fillna(data[col].mode()[0], inplace=True)

    # Encode categorical variables (if any)
    label_encoders = {}
    for col in categorical_columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        label_encoders[col] = le

    # Split data into features and target
    X = data[['from_user_account_id', 'to_user_account_id']]  # Features
    y = data['isfraud']  # Target variable

    print('------------------------------------------XxXXX')
    print(X)
    print('-----------------------------------------YYYY')
    print(y)
    # Normalize or scale numerical features (if needed)
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Create and train a random forest classifier
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(X, y)  # Train the model on the entire dataset
    # Predict on the test set


    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train a random forest classifier
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(X_train, y_train)

    # Predict on the test set
    y_pred = rf_classifier.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    print(f'Accurcay of model {accuracy*100} %')
    # Create a 2D array with the given accounts
    input_data = scaler.transform([[from_account, to_account]])

    print(f'input data {from_account, to_account}')
    # Make a prediction
    prediction = rf_classifier.predict(input_data)
    print(f'prediction {prediction}')
    if prediction[0] == 1:
        return "Fraud"
    else:
        return "Not Fraud"

