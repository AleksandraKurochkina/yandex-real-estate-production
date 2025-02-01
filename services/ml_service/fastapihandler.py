import joblib
import pandas as pd
import os

class FastApiHandler:
    
    def __init__(self):
        self.param_types = {
            "user_id": str,
            "model_params": dict
        }

        self.required_model_params = ['id', 'building_id', 'floor', 'kitchen_area',
                                      'living_area', 'rooms', 'is_apartment', 
                                      'studio', 'total_area',
                                      'build_year', 'building_type_int',
                                      'latitude', 'longitude', 'ceiling_height',
                                      'flats_count', 'floors_total', 'has_elevator']
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, "..", "models", "pipeline.pkl")
        self.load_model(model_path=model_path)

    def load_model(self, model_path: str):
        try:
            self.model = joblib.load(model_path)
        except Exception as e:
            print(f"Failed to load model: {e}")

    def price_predict(self, model_params: dict) -> float:
        for key in model_params:
             model_params[key] = [model_params[key]]
        return self.model.predict(pd.DataFrame(model_params))
        
    def check_required_query_params(self, query_params: dict) -> bool:
        if "user_id" not in query_params or "model_params" not in query_params:
                return False
        
        if not isinstance(query_params["user_id"], self.param_types["user_id"]):
                return False
                
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
                return False
        return True

    
    def check_required_model_params(self, model_params: dict) -> bool:
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False
            

    def validate_params(self, params: dict) -> bool:
        if self.check_required_query_params(params):
                print("All query params exist")
        else:
                print("Not all query params exist")
                return False
        
        if self.check_required_model_params(params["model_params"]):
                print("All model params exist")
        else:
                print("Not all model params exist")
                return False
        return True
                
                
    def handle(self, params):
        try:
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                model_params = params["model_params"]
                user_id = params["user_id"]
                print(f"Predicting for user_id: {user_id} and model_params:\n{model_params}")
                predicted_price = self.price_predict(model_params)
                response = {
                        "user_id": user_id, 
                        "prediction": int(predicted_price[0])
                    }
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            return response

if __name__ == "__main__":

    # создаём тестовый запрос
    test_params = {
        "user_id": '123',
        "model_params": {'id': 91587, 'building_id': 10448, 'floor': 6, 
                   'kitchen_area': 5.8, 'living_area': 43.0, 'rooms': 3, 
                   'is_apartment': 'false', 'studio': 'false', 
                   'total_area': 58.2, 'build_year': 1973,
                   'building_type_int': 4, 'latitude': 55.71713638305664, 
                   'longitude': 37.46078109741211, 
                   'ceiling_height': 2.4800000190734863, 'flats_count': 143,
                   'floors_total': 9,
                   'has_elevator': 'true'}
                        }

    # создаём обработчик запросов для API
    handler = FastApiHandler()

    # делаем тестовый запрос
    response = handler.handle(test_params)
    print(f"Response: {response}") 