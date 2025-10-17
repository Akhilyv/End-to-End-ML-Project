import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass

class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts',"preprocessor.pkl")       # Initializing a variable

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()        # Creating the variables and planning the paths

    def get_data_transformer_object(self):
        '''

        This function is responsible for data tranformation

        '''

        try:
            numerical_columns = ["writing_score", "reading_score"]      # Defining the numerical columns
            categorical_columns = [                                     # Defining the categorical columns
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]

            num_pipeline = Pipeline(                                    # Creating the numeric pipeline
                steps = [
                    ("imputer", SimpleImputer(strategy="median")),      # Fills missing numeric values with the median of that column.
                    ("Scaler", StandardScaler())                        # Scales/standardizes the values [bigger vales like {100, 110, 150} dominates the scores], we scale them to {0-5}]
                ]
            )

            cat_pipeline = Pipeline(                                    # Creating the categorical pipeline
                steps = [
                    ("imputer", SimpleImputer(strategy="most_frequent")),   # Fills missing categorical values with the most common category.
                    ("one_hot_encoder", OneHotEncoder()),                   # Converts categories into multiple binary (0/1) columns.
                    ("scaler", StandardScaler(with_mean=False))             # Scales one-hot encoded data but doesn’t subtract the mean
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor = ColumnTransformer(                              # It combines multiple preprocessing pipelines into one transformer.
                [
                    ("num_pipeline", num_pipeline, numerical_columns),     # Naming the pipeline (Calling the pipeline and using the numerical columns)
                    ("cat_pipelines", cat_pipeline, categorical_columns)   # Naming the pipeline (Calling the pipeline and using the numerical columns)
                ]
            )

            return preprocessor                                            # returning the preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)                             # Reading the dataset
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()         # We get the preprocessor from get_data_transformer_object()
            target_column_name = "math_score"                              # Defining a target column
            numerical_columns = ["writing_score", "reading_score"]         # Defining a numerical columns

            input_feature_train_df = train_df.drop(columns = [target_column_name], axis=1)      # Removing the target column from the training data frame
            target_feature_train_df = train_df[target_column_name]                              # Selecting only the target column from training data frame

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)          # Removing the target column from the testing data frame
            target_feature_test_df = test_df[target_column_name]                                # Selecting only the target column from testing data frame

            logging.info(
                 f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            # Fit the preprocessor on the training data (learn medians, encodings, scaling parameters) and then transform the training features into a numeric array.
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            # Use the already-fitted preprocessor to transform the test data (applying the same learned rules from training — no refitting here).

            train_arr = np.c_[
                 input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)