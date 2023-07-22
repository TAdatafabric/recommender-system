from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load model dari file pickle
model_file = open('model.pkl', 'rb')
model = pickle.load(model_file, encoding='bytes')

@app.route('/')
def home():
    return render_template('index.html', output=0)

@app.route('/predict', methods=['POST'])
def predict():
    month, day_name, hour, payment_type, city_name, usage_unit = [x for x in request.form.values()]
    
    x = []
    
    x.append(int(month))
    x.append(int(day_name))
    x.append(int(hour))
    x.append(int(payment_type))
    x.append(int(city_name))
    x.append(float(usage_unit))
    # Melakukan prediksi menggunakan model
    
    data = pd.DataFrame([x], columns=['month', 'day_name', 'hour', 'payment_type', 'city_name', 'usage_unit'])
    prediction = model.predict(data)
    output = prediction[0]
    if prediction == '0':
        output = 'CONTEN'
    elif prediction == '1':
        output = 'SMSBAS'
    elif prediction == '2':
        output = 'NATNAL'
    elif prediction == '3':
        output = 'VASOCC'
    elif prediction == '4':
        output = 'INTNAL'
    elif prediction == '5':
        output = 'SPVOIC'
    elif prediction == '6':
        output = 'SPCSMS'  
    # Mengirimkan hasil prediksi ke template HTML
    return render_template('index.html', prediction=prediction, output=output, month=month, day_name=day_name, hour=hour, payment_type=payment_type, city_name=city_name, usage_unit=usage_unit)

if __name__ == '__main__':
    app.run(debug=True)
