from DecisionTree import *
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold

header = ['Age', 'Menopause', 'Tumor_Size', 'Inv_Nodes', 'Nodes_Caps',
          'Deb_Malig', 'Breast', 'Breast_Quad', 'Irradiate', 'Class']
df = pd.read_csv('data_set/breast-cancer.csv')


kf = KFold(n_splits=5, random_state=None, shuffle=True)
X = np.array(df.iloc[:, 0:])

for train_index, test_index in kf.split(X):
    train_df, test_df = X[train_index, :].tolist(), X[test_index, :].tolist()

    tree = build_tree(train_df, header)

    max_accuracy = computeAccuracy(test_df, tree)

    print("*********** Tree with accuracy: " +
          str(max_accuracy*100) + "%  ************")

    predictions = []
    for row in test_df:
        predictions.append(classify(row, tree))

    # print(predictions)
