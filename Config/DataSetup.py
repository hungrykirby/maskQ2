import os
import glob
import numpy as np
from Config import config

ver = input("version > ")

def read_ceps():
    base_dir = os.getcwd()
    train_x, train_y = [], []
    test_x, test_y = [], []
    train_x, train_y =  make_arr("./train" + ver)
    test_x, test_y = make_arr("./test" + ver)
    return train_x, train_y, test_x, test_y

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
    base_dir = os.getcwd()
    #mode = config.mode
    name_list = []
    folders = os.listdir(os.path.join(base_dir, mode))
    for f in folders:
        name_list.append(str(f))
    return name_list
