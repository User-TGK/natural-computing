from sklearn.model_selection import train_test_split
from sklearn.datasets import load_wine
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import zero_one_loss
from sklearn.tree import DecisionTreeClassifier

import numpy as np
import matplotlib.pyplot as plt

n_estimators = 10

X, y = load_wine(return_X_y=True)

# Use 75% for training, 25% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Stump classifier
clf_stump = DecisionTreeClassifier(max_depth=1)
clf_stump.fit(X, y)

clf_stump_err = 1.0 - clf_stump.score(X_test, y_test)

# Small tree classifier
clf_base = DecisionTreeClassifier(max_depth=2)
clf_base.fit(X, y)

clf_base_err = 1.0 - clf_base.score(X_test, y_test)

# Adaboost classifier
clf_adaboost = AdaBoostClassifier(n_estimators=n_estimators)
clf_adaboost.fit(X, y)

clf_adaboost_err = np.zeros((n_estimators,))
for i, y_pred in enumerate(clf_adaboost.staged_predict(X_test)):
    clf_adaboost_err[i] = zero_one_loss(y_pred, y_test)

plt.plot([1, n_estimators], [clf_stump_err] * 2, label="Decision Stump", color="black", linestyle='dashed')
plt.plot([1, n_estimators], [clf_base_err] * 2, label="Single Classifier", color="grey", linestyle='dashed')
plt.plot(np.arange(n_estimators) + 1, clf_adaboost_err, label="AdaBoost Ensemble")

plt.xlabel('Ensemble size')
plt.ylabel('Error margin')

plt.legend()
plt.show()
