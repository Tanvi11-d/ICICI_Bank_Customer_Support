from fastapi import FastAPI,HTTPException
from utils import icici_support

app=FastAPI()


@app.get("/")
def root():
    return {"message":"Fastapi is working"}

@app.post("/question/")
async def create_query(question:str):
    try:
       
        
        response=await icici_support(question)
        return response.get("messages")[-1].content
    
    except Exception as e:
        print("error",e)
        raise HTTPException(status_code=404,detail=str(e))
