echo "Running..."
#cp -r tmp /usr/src/app
pwd
ls -lR
pwd
mkdir -p /usr/src/app
mkdir -p /usr/src/app/datasets
cp sordi.yaml /usr/src/app
cp prep.py /usr/src/app/datasets

# cp best.pt /usr/src/app
#cp id2path.json /usr/src/app
cd /usr/src/app/datasets

mkdir -p sordi/images/train
mkdir -p sordi/images/val
mkdir -p sordi/images/test
mkdir -p sordi/labels/train
mkdir -p sordi/labels/val
mkdir -p sordi/labels/test
# cd datasets
python prep.py $1 $2

cd -
cd /usr/src/app
#cat train.py
# sed -i 's/0.0, 0.0, 0.1, 0.9/0.2, 0.2, 0.5, 0.1/g' utils/metrics.py
# time python train.py --img 720 --batch 32 --epochs 10 --data sordi.yaml --weights yolov5m.pt
time yolo detect train data=sordi.yaml model=yolov8m.pt epochs=70 imgsz=720 batch=8
#ls -la runs/detect/train

#mkdir outputs
#mv -v  /usr/src/app/runs/detect/train/* ./outputs/

cd -

zip -r outputs/output.zip /usr/src/app/runs/detect/train
# cd outputs

#mv runs/train/exp/weights/best.pt outputs/best.pt