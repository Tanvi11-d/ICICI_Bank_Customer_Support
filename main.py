from fastapi import FastAPI,HTTPException
from utils import icici_support

app=FastAPI()


@app.get("/")
def root():
    return {"message":"Fastapi is working"}

@app.post("/question/")
def create_query(question:str):
    try:
       
        
        response=icici_support(question)
        return response.get("messages")[-1].content
    
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
