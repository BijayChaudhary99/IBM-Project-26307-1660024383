import numpy as np
import os
from PIL import Image
from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename, redirect
from gevent.pywsgi import WSGIServer
from flask import send_from_directory
from joblib import Parallel, delayed
import joblib
import pandas as pd
from scipy.sparse import issparse
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "OVk_2Ft8CV8IyLf1-x_OMFJIsbmSOO6Kk8-QIw43Maub"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
# payload_scoring = {"input_data": [{"field": ['Gender', 'Married', 'Dependents', 'Education',
#                                            'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome',
#                                           'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area'], "values": [
# array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}
#
# response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/50da8085-b252-4242-a6b7-03d28ccfb5c3/predictions?version=2022-11-18', json=payload_scoring,
#                                headers={'Authorization': 'Bearer ' + mltoken})
#print("Scoring response")


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/predict')
def predict():
    return render_template('predict.html')


@app.route('/result', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        lend_data = request.form.get('lend')
        data = [[request.form.get('gender'), request.form.get('married'), request.form.get('dep'), request.form.get('edu'), request.form.get(
            'se'), request.form.get('ai'), request.form.get('cai'), request.form.get('la'), request.form.get('lat'), request.form.get('ch'), request.form.get('pa')]]

        df = pd.DataFrame(data, columns=['Gender', 'Married', 'Dependents', 'Education',
                                         'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome',
                                         'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area'])

        gh = joblib.load('C:/Users/BIJAY/Desktop/New folder/rdf.pkl')
        num = gh.predict(df)
        a = ''
        lend_data = int(lend_data)
        if (num == 0):
            if (lend_data == 1):
                a = 'It is not advisable to provide loan for this applicant.'
            else:
                a = 'Your Loan application will be Rejected.'
        else:
            if (lend_data == 1):
                a = 'This applicant can be provided with the loan amount requested.'
            else:
                a = 'Your Loan application will be succesfull.'
        return render_template('submit.html', num=a)


if __name__ == '__main__':
    app.run(debug=True, threaded=False)
