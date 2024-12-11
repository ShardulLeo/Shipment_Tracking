import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load dataset
data = pd.read_csv(r"D:\Data Projects\Shipment_Tracking\data\label_data_pred_cancel_order.csv")

data['estimated_delivery'] = pd.to_datetime(data['estimated_delivery'])
data['delivery_day'] = data['estimated_delivery'].dt.day
data['delivery_month'] = data['estimated_delivery'].dt.month
data['delivery_year'] = data['estimated_delivery'].dt.year
data['delivery_weekday'] = data['estimated_delivery'].dt.weekday

# Features (X) and target (y)
X = data.drop(columns=['tracking_number', 'estimated_delivery', 'is_canceled', 'status'])
y = data['is_canceled']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, 'models/cancellation_model.pkl')

