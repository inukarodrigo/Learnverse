import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from datasets import Dataset
import seaborn as sns
import statsmodels.api as sm

# Note: This is the modelTraining.ipynb file in .py format and I ignored some codes written in the original file

# Reading the csv file
dataset = pd.read_csv('E:/Apps/Python/Pycharm Projects/Learnverse/Exam Paper Generation/Model '
                      'Training/table_to_train_the_model.csv')

X = dataset[["RelatedLesson", "no_of_occurance"]]
y = dataset[["no_of_occurance_future"]]

# Splitting the dataset into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)


# In[10]:


# Creating dummy columns for the categorical columns
X_train = pd.get_dummies(X_train,
                         columns=["RelatedLesson"],
                         drop_first=True)

X_test = pd.get_dummies(X_test,
                        columns=["RelatedLesson"],
                        drop_first=True)

# In[11]:


standardScaler = StandardScaler()
standardScaler.fit(X_train)
X_train = standardScaler.transform(X_train)
X_test = standardScaler.transform(X_test)

# Creating a linear regression model
linearRegression = LinearRegression()
linearRegression.fit(X_train, y_train)
y_pred = linearRegression.predict(X_test)


# Creating a function to use the model
def useModel(lessonName, noOfQuestionsAnsweredIncorrectly):
    # Reading the csv file for prediction
    df1 = pd.read_csv('E:/Apps/Python/Pycharm Projects/Learnverse/Exam Paper Generation/Model '
                      'Training/table_to_use_in_the_model_for_prediction.csv')
    df1.loc[len(df1.index)] = [lessonName, noOfQuestionsAnsweredIncorrectly]
    indexNum = len(df1.index) - 1
    # Creating dummy columns for the categorical columns
    df1 = pd.get_dummies(df1,
                         columns=["RelatedLesson"],
                         drop_first=True)

    global standardScaler
    df1 = standardScaler.transform(df1)

    global linearRegression
    return np.round(linearRegression.predict(df1)[indexNum])
