# -*- coding: utf-8 -*-
"""diabetes

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XTK2A1no7d_JH_zxBomA0-kEEfsiqic2

**Context:**
This dataset is originally from the National Institute of Diabetes and Digestive and Kidney Diseases. The objective of the dataset is to diagnostically predict whether or not a patient has diabetes, based on certain diagnostic measurements included in the dataset. Several constraints were placed on the selection of these instances from a larger database. In particular, all patients here are females at least 21 years old of Pima Indian heritage.

**Content:**
The datasets consists of several medical predictor variables and one target variable, Outcome. Predictor variables includes the number of pregnancies the patient has had, their BMI, insulin level, age, and so on.
"""

# Importing the libraries

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Importing the dataset

dataset = pd.read_csv('diabetes.csv')

print(dataset.describe())

"""First, whenever we have a data in hand, we should check out for the total number of instances which represents rows and total number of features (both independent and dependent) which are columns."""

print(dataset.info())       # this will print out the non null counts
print(dataset.info)       # This line is without () for info, this will just print out the whole dataset
print(dataset[['Outcome']].info())        # the info can be obtained for specific columns too

"""Here the range index provides information about the number of instances and the data columns for number of columns. Here we have 768 rows and 9 columns in the dataset.

After checking for the size of the dataset, we must check for any missing entries in the data values.
In the above table each row represents each column in the dataset.
As we can notice we have Non-Null count column which basically says how many
values in that specific column is not a null. If this number is equal to the total number of rows in the dataset,
then we have no missing values as we have in this case.
"""

print(dataset.shape[0])       # this will give the first index value of shape of a dataset, [0] for number of rows and [1] for number of columns
print(dataset.shape[1])

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

"""There are many rows with 0 values for the features, if we have many 0 values and if fill it with mean values by scaling it will give the model a wrong perspective, it is better to know before the dataset is used in the model."""

x_axis = [i for i in dataset]
y_axis = [j for j in (dataset == 0).sum(axis=0)]

x_axis.pop()        # this is to remove the 'outcome' column from the plot
y_axis.pop()

plt.barh(x_axis, y_axis)
plt.title('Zero values (out of {} values)'.format(dataset.shape[0]))
plt.xlabel('Number of zeroes')
plt.show()

"""As we can clearly see here the columns Insulin and Skin thickness has a lot of zero values. This might bring down the accuracy of the model.

Let us see what how many of the considered instances are with diabetes and without
"""

# Analyzing the percentage of people who developed diabetes and who did not from the total number of instances

positive = ((dataset['Outcome'][dataset['Outcome'] == 1].count() / (dataset.shape[0])) * 100)

negative = ((dataset['Outcome'][dataset['Outcome'] == 0].count() / (dataset.shape[0])) * 100)


print('Percentage of people who developed diabetes: {:.2f}%'.format(positive))
print('Percentage of people who did not develop diabetes: {:.2f}%'.format(negative))

x_axis = ['Positive', 'Negative']
y_axis = [positive, negative]

plot = plt.bar(x_axis, y_axis)
plot[0].set_color('r')
plot[1].set_color('g')
plt.title('Overall percentage of people with diabetes and without')
plt.show()

"""34.90 % of people in the dataset has been recorded diabetic and 65.10 % of people has been recorded non-diabetic."""

# Plotting the relationship of each feature to the outcome

sns.set(style="ticks", context="talk")
sns.set(font_scale=2)

# All features visualised in for loop

for i in dataset.drop('Outcome', axis=1):
    sns.barplot(y=str(i), x='Outcome', data=dataset)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.show()

# Assigning the independent var into x and dependent into y

x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Spitting the data into train and test set

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)


# Feature scaling

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

model_acc = []      # To collect all the model accuracies
model_names = ['Logistic regression', 'KNN', 'kernel SVM',
               'Naive bayes', 'Decision tree', 'Random forest']


def accuracy(predictor):
    # Predicting the test set and making confusion matrix and accuracy score

    from sklearn.metrics import confusion_matrix, accuracy_score

    y_pred = classifier.predict(x_test)
    cm = confusion_matrix(y_pred, y_test)
    print(cm)
    print(accuracy_score(y_pred, y_test))

    # Applying K_fold cross validation

    from sklearn.model_selection import cross_val_score

    accuracies = cross_val_score(estimator=predictor, X=x_train, y=y_train, cv=10)

    print("Accuracy with K-fold: {:.2f} %".format(accuracies.mean() * 100))
    print("Standard deviation with K-fold: {:.2f} %".format(accuracies.std() * 100))

    model_acc.append(accuracies.mean() * 100)


# Model creation and collecting the accuracies

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


models = [LogisticRegression(), KNeighborsClassifier(n_neighbors=10, metric='minkowski', p=2),
          SVC(kernel='rbf', random_state=0), GaussianNB(), DecisionTreeClassifier(criterion='entropy', random_state=0),
          RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=0)]

for i in models:
    classifier = i
    classifier.fit(x_train, y_train)
    accuracy(classifier)

for i in range(len(model_acc)):
    print("model name: {}, accuracy: {:.2f}".format(str(model_names[i]), model_acc[i]))

sns.barplot(y=model_names, x=model_acc)
plt.title('Accuracies among each model')
plt.show()

"""Among all the models considerd here logistic regression shows the best results with slightly greater than 77%.

The dataset can be altered to get rid of the 0 values and considerig the training again will surely improve the accuracy score of the models.
"""