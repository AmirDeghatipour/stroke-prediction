import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,OrdinalEncoder, StandardScaler
from src.exception import CustomException
from src.logger import logging
from src.utlis import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_features = ['age', 'bmi', 'avg_glucose_level']
            binary_features = ['gender', 'ever_married', 'Residence_type']
            categorical_features = ['work_type', 'smoking_status']


            num_pipleline = Pipeline(
                [
                ("imputer", SimpleImputer(strategy = 'median')),
                ("scaler", StandardScaler())
                ]
            )

            binary_pipeline = Pipeline(
                [("label_encoder", OrdinalEncoder())]
            )
            
            cat_pipeline = Pipeline(
                [("one_hot_encoder", OneHotEncoder(drop='first', sparse_output=False))]
            )

            logging.info("Numerical Columns Standard Scaling completed")
            logging.info("Binary Columns Encoding completed")
            logging.info("Categorical Columns Encoding completed")

            preprocessor = ColumnTransformer(
                [
                ('num', num_pipleline, numerical_features),
                ('bin', binary_pipeline, binary_features),
                ('cat', cat_pipeline, categorical_features)
                ],
                remainder='passthrough'
            )

            return preprocessor
            
        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_data_transformer(self, train_path, test_path):
        try:
            logging.info("Read Train and Test data Completed")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Obtaining Preprocessing Object")
            preprocessing_obj = self.get_data_transformer_object()


            X_train = train_df.drop(columns=['id','stroke'], axis=1)
            X_train['gender'] = X_train['gender'].replace(['Other'], 'Female')
            y_train = train_df['stroke']
            X_train['work_type'] = X_train['work_type'].replace(['Never_worked', 'children'], 'Other')


            X_test = test_df.drop(columns=['id','stroke'], axis=1)
            X_test['gender'] = X_test['gender'].replace(['Other'], 'Female')
            y_test = test_df['stroke']
            X_test['work_type'] = X_test['work_type'].replace(['Never_worked', 'children'], 'Other')

            logging.info("Applying preprocessing object on training dataframe and testing dataframe.")
            X_train_arr = preprocessing_obj.fit_transform(X_train)
            X_test_arr = preprocessing_obj.transform(X_test)

            train_arr = np.c_[X_train_arr, np.array(y_train)]
            test_arr = np.c_[X_test_arr, np.array(y_test)]

            logging.info("Saved preprocessing object.")
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)