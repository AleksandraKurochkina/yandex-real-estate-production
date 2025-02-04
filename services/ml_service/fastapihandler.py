import joblib
import pandas as pd
import os
import json
import logging

class FastApiHandler:
    
    def __init__(self):
        self.param_types = {
            "user_id": str,
            "model_params": dict
        }

        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir,  "required_params.json"), "r") as file:
            config = json.load(file)

        self.required_model_params = config["params"]
        model_path = os.path.join(current_dir, "..", "models", "pipeline.pkl")
        self.load_model(model_path=model_path)

    def load_model(self, model_path: str):
        try:
            self.model = joblib.load(model_path)
        except Exception as e:
            logging.error(f"Failed to load model: {e}")

    def price_predict(self, model_params: dict) -> float:
        for key in model_params:
             model_params[key] = [model_params[key]]
        return self.model.predict(pd.DataFrame(model_params))
        
    def check_required_query_params(self, query_params: dict) -> bool:
        if "user_id" not in query_params:
            logging.error("There is no user_id")
            return False
        if "model_params" not in query_params:
            logging.error("There is no model params")
        if not isinstance(query_params["user_id"], self.param_types["user_id"]):
            logging.error("Wrong type of user_id")
            return False
                
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            logging.error("Wrong type of model_params")
            return False
        return True

    
    def check_required_model_params(self, model_params: dict) -> bool:
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False
            

    def validate_params(self, params: dict) -> bool:
        if self.check_required_query_params(params):
            logging.info("All query params exist")
        else:
            logging.error("Not all query params exist")
            return False
        
        if self.check_required_model_params(params["model_params"]):
            logging.info("All model params exist")
        else:
            logging.error("Not all model params exist")
            return False
        return True
                
                
    def handle(self, params):
        if not self.validate_params(params):
            logging.error("Error while handling request")
            response = {"Error": "Problem with parameters"}
        else:
            model_params = params["model_params"]
            user_id = params["user_id"]
            logging.info(f"Predicting for user_id: {user_id} and model_params:\n{model_params}")
            
        try:
            predicted_price = self.price_predict(model_params)
            response = {
                "user_id": user_id, 
                "prediction": int(predicted_price[0])
            }
        except Exception as e:
            logging.error(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            logging.info(response)
            return response

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir,  "test_params.json"), "r") as file:
        config = json.load(file)
    # создаём тестовый запрос
    test_params = config["test_params"]

    # создаём обработчик запросов для API
    handler = FastApiHandler()

    # делаем тестовый запрос
    response = handler.handle(test_params)