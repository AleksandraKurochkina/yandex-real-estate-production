from fastapi import FastAPI
from ml_service.fastapihandler import FastApiHandler
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram, Counter, Gauge

app = FastAPI()
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

app.handler = FastApiHandler()

yandex_app_predictions = Histogram(
    # имя метрики
    "yandex_app_predictions",
    # описание метрики
    "Histogram of predictions",
    # указываем корзины для гистограммы
    buckets=(8600000, 11000000, 14450000, 16000000)
) 

yandex_app_morethanmedian = Counter("yandex_app_morethanmedian", "Number of predictions that are greater than median value in dataset")

yandex_app_gauge = Gauge('yandex_app_gauge', 'Last prediction')

@app.post("/predict/{user_id}")
def predict(user_id:str, model_params:dict):
    all_params = {"user_id": user_id, "model_params": model_params}
    response = app.handler.handle(all_params)
    if "prediction" in response:
        yandex_app_predictions.observe(response['prediction'])
        if response['prediction'] > 11000000:
            yandex_app_morethanmedian.inc()
        yandex_app_gauge.set(response['prediction'])
    
    return response