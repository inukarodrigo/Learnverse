import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import os
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from datasets import Dataset
import seaborn as sns
import statsmodels.api as sm

# Note: This is the modelTraining.ipynb file in .py format and I ignored some codes written in the original file

# Reading the csv file
current_dir = os.getcwd()
file_path = os.path.join(current_dir, '..', 'Model Training', 'table_to_train_the_model.csv')
abs_path = os.path.abspath(file_path)
# dataset = pd.read_csv(abs_path)

def trainModel(abs_path_for_the_csv_file):
    # abs_path_for_the_csv_file means the absolute path for the table_to_train_the_model.csv file
    # Something like 'E:/Apps/Python/Pycharm Projects/Learnverse/Exam Paper Generation/Model Training/table_to_train_the_model.csv'

    dataset = pd.read_csv(abs_path_for_the_csv_file)
    X = dataset[["RelatedLesson", "no_of_occurance"]]
    y = dataset[["no_of_occurance_future"]]

    # Splitting the dataset into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Creating dummy columns for the categorical columns
    X_train = pd.get_dummies(X_train,
                             columns=["RelatedLesson"],
                             drop_first=True)

    X_test = pd.get_dummies(X_test,
                            columns=["RelatedLesson"],
                            drop_first=True)

    standardScaler = StandardScaler()
    standardScaler.fit(X_train)
    X_train = standardScaler.transform(X_train)
    X_test = standardScaler.transform(X_test)

    # Creating a linear regression model
    linearRegression = LinearRegression()
    linearRegression.fit(X_train, y_train)
    y_pred = linearRegression.predict(X_test)

    return standardScaler, linearRegression





def useModel(abs_path_for_the_train_csv_file,abs_path,lessonName, noOfQuestionsAnsweredIncorrectly):
    # Abs path should be something like
    # 'E:/Apps/Python/Pycharm Projects/Learnverse/Exam Paper Generation/Model Training/table_to_use_in_the_model_for_prediction.csv'

    # abs_path_for_the_train_csv_file means the absolute path to the table_to_train_the_model.csv file

    df1 = pd.read_csv(abs_path)

    df1.loc[len(df1.index)] = [lessonName, noOfQuestionsAnsweredIncorrectly]
    indexNum = len(df1.index) - 1
    df1 = pd.get_dummies(df1, columns=["RelatedLesson"], drop_first=True)

    standardScaler, linearRegression = trainModel(abs_path_for_the_train_csv_file)
    df1 = standardScaler.transform(df1)

    return np.round(linearRegression.predict(df1)[indexNum])

