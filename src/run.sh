echo "Running..."
#cp -r tmp /usr/src/app
cp sordi.yaml /usr/src/app
cp prep.py /usr/src/app

cp best.pt /usr/src/app
#cp id2path.json /usr/src/app
cd /usr/src/app
mkdir -p sordi/images/train
mkdir -p sordi/images/val
mkdir -p sordi/images/test
mkdir -p sordi/labels/train
mkdir -p sordi/labels/val
mkdir -p sordi/labels/test
python prep.py $1 $2
#cat train.py
sed -i 's/0.0, 0.0, 0.1, 0.9/0.2, 0.2, 0.5, 0.1/g' utils/metrics.py
time python train.py --img 720 --batch 16 --epochs 50 --data sordi.yaml --weights yolov5m.pt
#ls -lR runs
cd -
zip -r outputs/output.zip /usr/src/app/runs/train/exp
#mv runs/train/exp/weights/best.pt outputs/best.pt