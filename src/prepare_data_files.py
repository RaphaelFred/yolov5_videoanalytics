import os
import struct

class UnknownImageFormat(Exception):
    pass

def get_image_size(file_path):
    """
    Return (width, height) for a given img file content - no external
    dependencies except the os and struct modules from core
    """
    size = os.path.getsize(file_path)

    with open(file_path, 'rb') as input:
        height = -1
        width = -1
        data = input.read(25)
        #data = str(data
        #data = data.decode('utf-8')
        #data = bytes(data)
        #print(data)
        if True:
            input.seek(0)
            input.read(2)
            b = input.read(1)
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = input.read(1)
                while (ord(b) == 0xFF): b = input.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    input.read(3)
                    h, w = struct.unpack(">HH", input.read(4))
                    break
                else:
                    input.read(int(struct.unpack(">H", input.read(2))[0])-2)
                b = input.read(1)
            width = int(w)
            height = int(h)
            return width,height

        if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
            # GIFs
            w, h = struct.unpack("<HH", data[6:10])
            width = int(w)
            height = int(h)
        elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n')
              and (data[12:16] == 'IHDR')):
            # PNGs
            w, h = struct.unpack(">LL", data[16:24])
            width = int(w)
            height = int(h)
        elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
            # older PNGs?
            w, h = struct.unpack(">LL", data[8:16])
            width = int(w)
            height = int(h)
        elif (size >= 2) and data.startswith('\377\330'):
            # JPEG
            msg = " raised while trying to decode as JPEG."
            input.seek(0)
            input.read(2)
            b = input.read(1)
            try:
                while (b and ord(b) != 0xDA):
                    while (ord(b) != 0xFF): b = input.read(1)
                    while (ord(b) == 0xFF): b = input.read(1)
                    if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                        input.read(3)
                        h, w = struct.unpack(">HH", input.read(4))
                        break
                    else:
                        input.read(int(struct.unpack(">H", input.read(2))[0])-2)
                    b = input.read(1)
                width = int(w)
                height = int(h)
            except struct.error:
                raise UnknownImageFormat("StructError" + msg)
            except ValueError:
                raise UnknownImageFormat("ValueError" + msg)
            except Exception as e:
                raise UnknownImageFormat(e.__class__.__name__ + msg)
        else:
            raise UnknownImageFormat(
                "Sorry, don't know how to get information from this file."
            )

    return width, height


import os
import json
import argparse
import time
parser = argparse.ArgumentParser()
parser.add_argument("--input_data", type=str)
#parser.add_argument("--yolo_data", type=str)
args = parser.parse_args()
root = args.input_data
print(os.listdir())
print(os.getcwd())
#root_out = args.yolo_data
os.mkdir('tmp2')
root_out = 'tmp2'

folders = os.listdir(root)
print('folders:', len(folders))

dataset_p = os.path.join(root_out, 'datasets','sordi')
dataset_imgs_train_p = os.path.join(dataset_p, 'images', 'train')
dataset_imgs_val_p = os.path.join(dataset_p, 'images', 'val')
dataset_imgs_test_p = os.path.join(dataset_p, 'images', 'test')
dataset_labels_train_p = os.path.join(dataset_p, 'labels', 'train')
dataset_labels_val_p = os.path.join(dataset_p, 'labels', 'val')
dataset_labels_test_p = os.path.join(dataset_p, 'labels', 'test')
os.makedirs(dataset_imgs_train_p, exist_ok = True)
os.makedirs(dataset_imgs_val_p, exist_ok = True)
os.makedirs(dataset_imgs_test_p, exist_ok = True)
os.makedirs(dataset_labels_train_p, exist_ok = True)
os.makedirs(dataset_labels_val_p, exist_ok = True)
os.makedirs(dataset_labels_test_p, exist_ok = True)

id2path = {}

all_classes = []
all_classes_set = []
fileindex = 0
for folder in folders:
    folder = os.path.join(root, folder)
    if not os.path.isdir(folder):
        continue
    print(os.path.join(folder, 'objectclasses.json'))
    a = time.time()
    with open(os.path.join(folder, 'objectclasses.json'), 'r') as clsf:
        classes = json.load(clsf)
    for objclass in classes:
        all_classes.append(objclass)
        objname = objclass['Name']
        if objname not in all_classes_set:
            all_classes_set.append(objname)
    files = os.listdir(os.path.join(folder, 'images'))
    for f in files:
        b = time.time()
        p_img = os.path.join(folder, 'images', f)
        p = os.path.join(folder, 'labels', 'json', f.replace('jpg', 'json'))
        fileindex += 1
        #if not os.path.exists(os.path.join(dataset_imgs_train_p, str(fileindex) + '.jpg')):
        #    os.symlink(os.path.abspath(p_img), os.path.join(dataset_imgs_train_p, str(fileindex) + '.jpg'))
        #print(p_img)
        split = p_img.split('/')
        id2path[fileindex] = split[-3] + ',' + split[-1]
        w, h = get_image_size(p_img)
        with open(p, 'r') as annof:
            annos = json.load(annof)
        dupcheck = []
        with open(os.path.join(dataset_labels_train_p, str(fileindex) + '.txt'), 'w') as txtf:
            for anno in annos:
                yolo_class_index = all_classes_set.index(anno['ObjectClassName'])
                right, left, top, bottom = anno['Right'], anno['Left'], anno['Top'], anno['Bottom']
                x_center = ((left + right) / 2) / w
                y_center = ((top + bottom) / 2) / h
                w_normalized = (right - left) / w
                h_normalized = (bottom - top) / h
                area = (right - left) * (bottom - top)
                if area < 400:
                    continue

                yololine = str(yolo_class_index) + ' ' + str(x_center) + ' ' + str(y_center) + ' ' + str(w_normalized) + ' ' + str(h_normalized)
                if yololine in dupcheck:
                    continue
                dupcheck.append(yololine)
                txtf.write(yololine)
                txtf.write('\n')
        c = time.time()
        #print('file:', (c-b))
    d = time.time()
    print('folder:', (d-a))
    #break


with open(os.path.join(dataset_p, 'id2path.json'), 'w', encoding='utf-8') as f:
    json.dump(id2path, f, ensure_ascii=False)

with open(os.path.join(dataset_p, 'sordi.json'), 'w', encoding='utf-8') as f:
    json.dump(all_classes, f, ensure_ascii=False, indent=4)

with open(os.path.join(dataset_p, 'sordi.yaml'), 'w', encoding='utf-8') as f:
    f.write('path: ./sordi\n')
    f.write('train: images/train\n')
    f.write('val: images/val\n')
    f.write('test: images/test\n')
    f.write('names:\n')
    index = 0
    for anno_class in all_classes_set:
        f.write('  ' + str(index) + ': ' + anno_class + '\n')
        index += 1

import shutil
shutil.make_archive(os.path.join('outputs', 'yolo'), 'zip', 'tmp2')