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

_username = input("username : ")
allusers = ["aa", "tsuyoshi", "yamada", "nishimura"]

def read_ceps(username):
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
    #x = []
    #y = []
    train_x = []
    train_y = []
    test_x = []
    test_y = []
    userindex = None
    for value, username in enumerate(allusers):
        x, y = read_ceps(username)
        if username == _username:
            userindex = value
            test_x.append(x.tolist())
            test_y.append(y.tolist())
        else:
            train_x += x.tolist()
            train_y += y.tolist()
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

    result = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    svc.fit(train_x, train_y)
    for _x, _y in zip(test_x, test_y):
        prediction_label = svc.predict(_x)
        cm = confusion_matrix(_y, prediction_label)
        result += cm

        acc_parcent = accuracy_score(_y, prediction_label)
        print(acc_parcent)
        print(cm)
    print(result)
