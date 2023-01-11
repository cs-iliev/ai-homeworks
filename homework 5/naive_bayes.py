import pandas as pd
import numpy as np

from decimal import *
from sklearn.model_selection import KFold
from model import generative_model, discriminative_model, get_accuracy

dataset = pd.read_csv('house-votes-84.data', header=None,
                      true_values=['y'], false_values=['n', '?'])

names = ['label'] + [f'vote_{i}' for i in range(16)]
dataset.columns = names

dataset['label'] = pd.Categorical(dataset['label'])

kf = KFold(n_splits=10, random_state=None, shuffle=True)

X = np.array(dataset.iloc[:, 1:])
Y = dataset['label'].cat.codes

accuraccies = []
count = 1

for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index, :], X[test_index, :]
    Y_train, Y_test = Y.iloc[train_index], Y.iloc[test_index]

    prob_label, prob_votes = generative_model(X_train, Y_train)
    predictions = discriminative_model(prob_label, prob_votes, X_test)

    accuracy = get_accuracy(Y_test, predictions)
    accuraccies.append(accuracy)
    print(f"Fold {count} accuracy:", accuracy)
    count += 1

print("\nAverage accuracy:", np.average(accuraccies))
