import os
import glob
import numpy as np
from Config import config

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.utils import resample
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score, cross_val_predict

username = input("username : ")

def read_ceps():
    base_dir = os.getcwd()
    x, y =  make_arr(username)
    return x, y

def make_arr(mode):
    x, y = [], []
    base_dir = os.getcwd()
    name_list = make_namelist(mode)
    for label,name in enumerate(name_list):
        #print(os.path.join(base_dir, mode, name))
        for fn in glob.glob(os.path.join(base_dir, mode, name, "*.ceps.npy")):
            ceps = np.load(fn)
            #print(mode, label, ceps, fn)
            num_ceps = len(ceps)
            x.append(ceps)
            y.append(label)
    return np.array(x),np.array(y)

def make_namelist(mode):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    name_list = []
    folders = os.listdir(os.path.join(base_dir, mode))
    for f in folders:
        name_list.append(str(f))
    return name_list

if __name__ == '__main__':
    x, y = read_ceps()
    num_class = 10
    faces_class = 5
    svc = SVC(kernel="linear",
        C=0.001,
        degree=3,
        gamma='auto',
        cache_size=3,
        class_weight=None,
        coef0=0.0,
        decision_function_shape=None,
        max_iter=-1,
        probability=False,
        random_state=None,
        shrinking=True,
        tol=0.001,
        verbose=False) #linear, rbf, poly
    scores = cross_val_score(svc, x, y, cv=10)
    print(scores)
    #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    result = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    for j in range(num_class):
        #print("---", x.shape, "---")
        train_x = x.tolist()
        train_y = y.tolist()
        test_x = []
        test_y = []
        for i in range(int(len(y)/num_class)):
            test_x.append(x[num_class*i + j])
            test_y.append(y[num_class*i + j])
            train_x.pop(num_class*i + j - i)
            train_y.pop(num_class*i + j - i)
        #print(np.array(test_x), np.array(train_x))
        svc.fit(train_x, train_y)
        prediction_label = svc.predict(test_x)
        cm = confusion_matrix(test_y, prediction_label)
        result += cm

        acc_parcent = accuracy_score(test_y, prediction_label)
        print(acc_parcent)
        print(cm)
    print(result)
