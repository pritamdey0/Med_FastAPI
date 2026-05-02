from fastapi import FastAPI
import json
app = FastAPI()

def load_data():
    with open('patients.json','r') as file:
        data=json.load(file)
    return data


@app.get("/")
def hello():
    return {'message':'hello world'}

@app.get("/about")
def about():
    return{'message':'Med details'}

@app.get("/view")
def view():
    data=load_data()
    return data

@app.get("/patients/{patient_id}")
def view_specific_patient(patient_id):
    data=load_data()
    for i in data:
        if(i==patient_id):
            return data[i]
        else:
            return "no patient"
