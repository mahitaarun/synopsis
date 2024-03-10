import sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load training data
training_data = pd.read_csv(sys.argv[1])

# Encode the 'crop' column
label_encoder = LabelEncoder()
training_data['crop_encoded'] = label_encoder.fit_transform(training_data['crop'])

# Separate features (temperature and humidity) and target variable (crop)
X = training_data[['temperature', 'humidity']]
y = training_data['crop_encoded']

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Function to calculate average temperature and humidity over a day
def calculate_average_data(new_data):
    average_data = new_data.groupby(new_data.index // 24)[['temperature', 'humidity']].mean().reset_index(drop=True)
    return average_data

# Load and preprocess new data
new_data = pd.read_csv(sys.argv[2])
average_data = calculate_average_data(new_data)

# Make predictions using the model
predictions = model.predict(average_data[['temperature', 'humidity']])

# Convert predicted labels back to original crop names
predicted_crops = label_encoder.inverse_transform(predictions)

# Print predictions
print("Predicted crops for new data:")
for i, pred in enumerate(predicted_crops):
    print(f"Day {i+1}: Average Temperature: {average_data['temperature'][i]}, Average Humidity: {average_data['humidity'][i]} -> Predicted Crop: {pred}")

