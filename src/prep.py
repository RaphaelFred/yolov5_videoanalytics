import json
import os
import numpy as np
import sys
from numpy.random import default_rng
import shutil
import time
src_root = sys.argv[1]

IMAGE_PATH = sys.argv[2] # 'stage_2_transfer_learning'#'sordi_stage_2'

if os.path.exists('finished.touch'):
    sys.exit()

with open(os.path.join(src_root, 'id2path.json'), 'r') as f:
    j = json.load(f)
import zipfile
l = len(j)


t0 = time.time()
amount = l - 5
test = False
if test:
    files = os.listdir('tmp/')
    cs = []
    for f in files:
        cs.append(f.split('.')[0])
else:
    rng = default_rng()
    cs = rng.choice(l, size=amount, replace=False)

    with zipfile.ZipFile(os.path.join(src_root, 'labels.zip'), 'r') as zip_ref:
        zip_ref.extractall('.')

t1 = time.time()
print('extraction:', (t1-t0))


for i in range(amount):
    c = cs[i]
    if c == 0:
        continue
    split = j[str(c)].split(',')
    src = os.path.join(src_root, IMAGE_PATH, split[0], 'images', split[1])
    if test:
        src_l = os.path.join('tmp', str(c) + '.txt')
    else:
        src_l = os.path.join('labels', 'train', str(c) + '.txt')
    if i < amount*0.8:
        assigned = 'train'
    elif i < amount*1:
        assigned = 'val'
    else:
        assigned = 'test'
    dst = os.path.join('sordi', 'images', assigned, str(c) + '.jpg')
    dst_l = os.path.join('sordi', 'labels', assigned, str(c) + '.txt')
    if os.path.exists(src_l):
        shutil.copyfile(src, dst)
        shutil.copyfile(src_l, dst_l)

with open('finished.touch', 'w') as f:
    f.write('finish')
t2 = time.time()
print('copying:', (t2-t1))