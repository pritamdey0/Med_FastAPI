from fastapi import FastAPI,Path,HTTPException,Query
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
def view_specific_patient(patient_id=Path(..., description='id of patiient', examples='P001')):
    data=load_data()
    for i in data:
        if(i==patient_id):
            return data[i]
        else:
            raise HTTPException(status_code=404, detail='patient not found')
    
@app.get("/sort")
def get_sort(sort_by:str=Query(...,description="enter the key in which you wanna see the data sorted")  ,order:str=Query('asc',description='enter the way or sorted data either asending or descending')):
    sort_key=['height','bmi','weight']

    if sort_by not in sort_key:
        raise HTTPException(status_code=400, detail=f"enter the key within the following items {sort_key}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail='enter asc or desc')
    
    data= load_data()
    s_o= False if order=='asc' else True
    sort_val=sorted(data.values(),key=lambda x:x.get(sort_by,0), reverse=s_o)

    return sort_val