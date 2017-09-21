#!/bin/sh
source  ~/.bashrc

copy_data=1
if [ $# -ge 1 ]; then
    copy_data=$1
fi

TFRecord_path_test="/user/h_miui_ad/develop/wangpeng9/micontest/TFRecord_base_test"

cur_path=`pwd`
test_data_path="/home/work/wangpeng9/micontest/data/test"

#copy test data
if [ ! -d ${test_data_path} ]; then
    mkdir -p ${test_data_path}
fi
if [ ${copy_data} -eq 1 ]; then
    rm -rf ${test_data_path}/*
    cd ${test_data_path}
    hadoop --cluster c3prc-hadoop fs -get ${TFRecord_path_test}
fi

#back to work path
cd ${cur_path}

test_dir=${test_data_path}

log_dir=dnn_log
if [ ! -d ${log_dir} ]; then
    mkdir -p ${log_dir}
fi
log_name="dnn_wide_deep.log"

model_dir=dnn_model
if [ ! -d ${model_dir} ]; then
    mkdir -p ${model_dir}
fi
model_name="dnn"

predict_out=predict_result.csv
sorted_predict_out=sorted_predict_result.csv

CUDA_VISIBLE_DEVICES="0"  python model/predict.py \
    --batch_size=128 \
    --test_dir=${test_dir} \
    --model_dir=${model_dir} \
    --model_name=${model_name} \
    --log_dir=${log_dir} \
    --log_name=${log_name} \
    --predict_out=${predict_out} \
    > log.test 2>&1

python model/sort_predict_result.py ${predict_out} ${sorted_predict_out}