from flask import Flask, render_template, request
import pandas as pd
import joblib

# Load trained model
model = joblib.load("traffic_model.pkl")

# Initialize app
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input values from form
        car = int(request.form['car'])
        bike = int(request.form['bike'])
        bus = int(request.form['bus'])
        truck = int(request.form['truck'])

        # Create dataframe
        sample = pd.DataFrame([[car, bike, bus, truck]],
                              columns=['CarCount', 'BikeCount', 'BusCount', 'TruckCount'])

        # Predict
        prediction = model.predict(sample)

        # Convert to label
        traffic_labels = {
            0: "Low Traffic",
            1: "Normal Traffic",
            2: "High Traffic",
            3: "Heavy Traffic"
        }

        result = traffic_labels[int(prediction[0])]

        return render_template('index.html', prediction_text="Traffic Condition: " + result)

    except:
        return render_template('index.html', prediction_text="Error in input")

# Run app
if __name__ == "__main__":
    app.run(debug=True)