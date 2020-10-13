#!/usr/bin/env python
# import subprocess
# src = "/data/prod/"
# dest = "/data/prod_backup/"
# subprocess.call(["rsync", "-arq", src, dest])

import subprocess
from multiprocessing import Pool
import os
def backup(src):
    dest = os.getcwd() + "/data/prod_backup/"
    print("Backing up {} into {}".format(src,dest))
    subprocess.call(["rsync","-arq",src,dest])

if __name__=="__main__":
    src = os.getcwd() + "/data/prod/"
    list_of_files = os.listdir(src)
    all_files = []

    for value in list_of_files:
        full_path = os.path.join(src,value)
        all_files.append(full_path)

    pool = Pool(len(all_files))
    pool.map(backup,all_files)
