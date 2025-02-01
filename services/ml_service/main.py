from fastapi import FastAPI
from ml_service.fastapihandler import FastApiHandler

app = FastAPI()
app.handler = FastApiHandler()

@app.post("/predict/{user_id}")
def predict(user_id:str, model_params:dict):
    all_params = {"user_id": user_id, "model_params": model_params}
    return app.handler.handle(all_params)