import os
import sys
from dataclasses import dataclass
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Split Traine and Test input Data")
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )

            models = {
                "Logistic Regression": LogisticRegression(class_weight='balanced'),
                "Decision Tree": DecisionTreeClassifier(class_weight='balanced'),
                "Random Forest Classifier": RandomForestClassifier(class_weight='balanced'),
                "K-Neighbors Classifier": KNeighborsClassifier(),
                "XGBClassifier": XGBClassifier(), 
                "CatBoosting Classifier": CatBoostClassifier(verbose=False),
            }

            hyperparameters = {
                "Logistic Regression": {
                    'C': [0.01, 0.1, 1, 10, 100],
                    'solver': ['liblinear', 'saga'],
                    # 'penalty': ['l1', 'l2'],
                    # 'max_iter': [100, 500, 1000]
                },
                
                "Decision Tree": {
                    'max_depth': [None, 5, 10, 20, 50],
                    'min_samples_split': [2, 5, 10],
                    # 'min_samples_leaf': [1, 2, 5],
                    # 'criterion': ['gini', 'entropy', 'log_loss']
                },
                
                "Random Forest Classifier": {
                    'n_estimators': [100, 200, 500],
                    'max_depth': [None, 5, 10, 20,],
                    # 'min_samples_split': [2, 5, 10],
                    # 'min_samples_leaf': [1, 2, 5],
                    # 'max_features': ['sqrt', 'log2', None],
                    # 'bootstrap': [True, False]
                },
                
                "XGBClassifier": {
                    'n_estimators': [100, 200, 500],
                    'max_depth': [3, 5, 10],
                    'learning_rate': [0.01, 0.05, 0.1, 0.2],
                    # 'subsample': [0.6, 0.8, 1.0],
                    # 'colsample_bytree': [0.6, 0.8, 1.0],
                    # 'gamma': [0, 0.1, 0.5, 1],
                    # 'reg_alpha': [0, 0.01, 0.1],
                    # 'reg_lambda': [1, 1.5, 2.0]
                },

                "K-Neighbors Classifier": {
                    'n_neighbors': [3, 5, 7, 10, 15],
                    # 'weights': ['uniform', 'distance'],
                    # 'metric': ['euclidean', 'manhattan', 'minkowski']
                },
                
                
                "CatBoosting Classifier": {
                    'iterations': [100, 300, 500],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'depth': [4, 6, 10],
                    'l2_leaf_reg': [1, 3, 5, 7],
                    'border_count': [32, 64, 128],
                    'bagging_temperature': [0, 0.5, 1]
                }
            }

            model_report:dict = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                params = hyperparameters)


            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found")
            logging.info("Best found model on both training and testing dataset")

            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(X_test)
            accuracy = accuracy_score(y_test, predicted)

            return accuracy


        except Exception as e:
            raise CustomException(e, sys)