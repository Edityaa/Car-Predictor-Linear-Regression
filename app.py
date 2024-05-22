import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify,redirect
import pickle

app = Flask(__name__)
df = pd.read_csv('Final_data.csv')
pipe = pickle.load(open('model.pkl','rb'))


@app.route('/')
def index():
    return render_template('index.html', car_data=mapper(df))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        brand = data.get('brand')
        model = data.get('model')
        kilometers = data.get('kilometers')
        transmission = data.get('transmission')
        year = data.get('year')
        fuel_type = data.get('fuel_type')
        owner_type = data.get('owner_type')
    
    
        temp = ''
        for word in owner_type.split():
            temp +=' '
            temp+= word.capitalize()
        temp = temp.strip()
        owner_type = temp
    
        ls = [model, int(year), int(kilometers), fuel_type.capitalize(), 'Individual', transmission.capitalize(), owner_type, brand]
        pred = pipe.predict(pd.DataFrame([ls],columns=['name', 'year', 'km_driven', 'fuel', 'seller_type',
                                                      'transmission','owner', 'Brand']))
    
        # print(pred)
        if pred[0] < 0 :
            pred[0] = 0
    
        # Dummy response for demonstration
        response_data = {
            'brand': brand,
            'model': model,
            'price': '₹ ' + str(np.round(pred[0])),  # Dummy price
            'imageURL': 'https://via.placeholder.com/300x200',  # Dummy image URL
            'equation': '₹ ' +str(np.round(pred[0])),  # Dummy equation
        }
    except Exception as e:
        print(e)
    return jsonify((response_data))
def mapper(df):
    map = {}
    brands = df['Brand'].unique()
    for brand in brands:
        models = np.unique(df[df['Brand']==brand]['name']).tolist()
        years = np.unique(df[df['Brand']==brand]['year']).tolist()
        trans = np.unique(df[df['Brand']==brand]['transmission']).tolist()
        map[brand] = {}
        for model in models:
            dct = {}

            map[brand][model] = {}
            map[brand][model] = {'transmission' :np.unique(df[df['name']==model]['transmission']).tolist()
                                 ,'fuel_types' :np.unique(df[df['name']==model]['fuel']).tolist(),
                                 'owner_types':np.unique(df[df['name']==model]['owner']).tolist(),
                                 'years': [str(i) for i in np.unique(df[df['name']==model]['year']).tolist()]}

    return map

if __name__ == '__main__':
    app.run())





