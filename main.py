from fastapi import FastAPI, Path,HTTPException,Query
import json
app = FastAPI()

def load_data():
    with open('patients.json','r') as file:
        data=json.load(file)
    return data


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

dataa= {
    101:{"name":"hey wa", "risk":"low", "rate":10},
    102:{"name":"hey ca", "risk":"low", "rate":11},
    103:{"name":"hey sa", "risk":"low", "rate":12},
    104:{"name":"hey ta", "risk":"low", "rate":13}
}

@app.get("/")
def home():
    return {"msg":"hey there !"}

@app.get("/fet/{id_no}")
def fetc(id_no:int):
    if id_no not in dataa:
        return {"error": f"the id {id_no} is invalid or not present"}
    else:

        return {
            "name":dataa[id_no]["name"],
            "risk":dataa[id_no]["risk"],
            "rate":dataa[id_no]["rate"]
        }

@app.get("/name/{mod_no}/class/{id_no}")  
def cl(mod_no: int , id_no:int): 
    return{
        "model_no":mod_no,
        "name":dataa[id_no]["name"],
        "risk":dataa[id_no]["risk"],
        "rate":dataa[id_no]["rate"]
    }

li=[
    {"id":101, "city":"beng", "risk":"low"},
    {"id":102, "city":"kol", "risk":"high"},
    {"id":103, "city":"beng", "risk":"low"},
    {"id":104, "city":"bguv", "risk":"high"},
    {"id":105, "city":"kol", "risk":"high"},
]

@app.get("/quer")
def quer(city:str , risk:str, pul:int=1):
    filter=[]
    # filter=[
    #     i for i in li
    #     if(i["city"]==city and i["risk"]==risk)
    # ]
    #filter = [i for i in li if i["city"] == city and i["risk"] == risk][:pul]

    for i in li:
        if i["city"] == city and i["risk"] == risk:
            filter.append(i)

            # Check if we have gathered enough results requested by 'pul'
            if len(filter) == pul:
                break  # Stops the loop immediately for system efficiency!

    return {
        "city":city,
        "risk":risk,
        "count": len(filter),
        "result": filter,
        "pul":pul

    }