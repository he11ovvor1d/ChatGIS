# -*- coding: utf-8 -*-
# author:mxq2003 time:2023/5/30

"""
    本次训练仅仅完成了查询河流长度的SQL语句
    请保证至少8GB运行内存(我之前没注意，内存溢出过一次)和3GB磁盘空间
    请修改输入数据在硬盘上的位置，我已经使用TODO标识了
    所有我修改过的参数都使用TODO标识了
    大约需要五个半个小时
"""

from multiprocessing import freeze_support

import pandas as pd
from sklearn.model_selection import train_test_split  # 用于分割测试集和训练集
from datasets import Dataset
from transformers import AutoTokenizer, T5ForConditionalGeneration

from transformers import Seq2SeqTrainer
from transformers import Seq2SeqTrainingArguments

from datasets import load_metric

import warnings

warnings.filterwarnings('ignore')


# map article and summary len to dict as well as if sample is longer than 512 tokens
def map_to_length(x):
    x["input_len"] = len(tokenizer(x["input"]).input_ids)
    x["input_longer_256"] = int(x["input_len"] > 256)
    x["input_longer_128"] = int(x["input_len"] > 128)
    x["input_longer_64"] = int(x["input_len"] > 64)
    # TODO 调整输出层的大小
    x["out_len"] = len(tokenizer(x["target"]).input_ids)
    x["out_longer_256"] = int(x["out_len"] > 256)
    x["out_longer_128"] = int(x["out_len"] > 128)
    x["out_longer_64"] = int(x["out_len"] > 64)
    return x


def compute_and_print_stats(x):
    if len(x["input_len"]) == sample_size:
        print(
            "Input Mean: {}, %-Input > 256:{},  %-Input > 128:{}, %-Input > 64:{} Output Mean:{}, %-Output > 256:{}, %-Output > 128:{}, %-Output > 64:{}".format(
                sum(x["input_len"]) / sample_size,
                sum(x["input_longer_256"]) / sample_size,
                sum(x["input_longer_128"]) / sample_size,
                sum(x["input_longer_64"]) / sample_size,
                sum(x["out_len"]) / sample_size,
                sum(x["out_longer_256"]) / sample_size,
                sum(x["out_longer_128"]) / sample_size,
                sum(x["out_longer_64"]) / sample_size,
            )
        )


# tokenize the examples
def convert_to_features(example_batch):
    input_encodings = tokenizer.batch_encode_plus(
        ["translate English to SQL: " + example for example in example_batch['input']],
        padding='max_length', truncation=True, max_length=64
    )
    target_encodings = tokenizer.batch_encode_plus(
        ["translate English to SQL: " + example for example in example_batch['target']],
        padding='max_length', truncation=True, max_length=128
    )
    encodings = {
        'input_ids': input_encodings['input_ids'],
        'attention_mask': input_encodings['attention_mask'],
        'labels': target_encodings['input_ids'],
        'decoder_attention_mask': target_encodings['attention_mask']
    }

    return encodings


def compute_metrics(pred):
    labels_ids = pred.label_ids
    pred_ids = pred.predictions

    # all unnecessary tokens are removed
    pred_str = tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    labels_ids[labels_ids == -100] = tokenizer.pad_token_id
    label_str = tokenizer.batch_decode(labels_ids, skip_special_tokens=True)

    rouge_output = rouge.compute(predictions=pred_str, references=label_str, rouge_types=["rouge2"])["rouge2"].mid

    return {
        "rouge2_precision": round(rouge_output.precision, 4),
        "rouge2_recall": round(rouge_output.recall, 4),
        "rouge2_fmeasure": round(rouge_output.fmeasure, 4),
    }


tokenizer = AutoTokenizer.from_pretrained("t5-small",local_files_only=True)
model = T5ForConditionalGeneration.from_pretrained("t5-small",local_files_only=True)
tokenizer.model_max_length = 512
model.config.max_length = 512
rouge = load_metric("rouge")
if __name__ == '__main__':
    freeze_support()

    df_dataset = pd.read_csv('./data/newDataSet.csv', sep='#') # TODO 数据集输入位置（使用井号分割问题和SQL语句）
    train_df, test_df = train_test_split(df_dataset, test_size=0.4, random_state=42)
    print(train_df)
    train_data = Dataset.from_pandas(train_df)
    test_data = Dataset.from_pandas(test_df)
    sample_size = 40  # TODO changed orginal = 10000
    #data_stats = test_data.select(range(sample_size)).map(map_to_length, num_proc=14)
    #output = data_stats.map(
    #     compute_and_print_stats,
    #     batched=True,
    #     batch_size=-1,
    # )
    train_data = train_data.map(convert_to_features, batched=True, remove_columns=train_data.column_names)
    test_data = test_data.map(convert_to_features, batched=True, remove_columns=test_data.column_names)

    columns = ['input_ids', 'attention_mask', 'labels', 'decoder_attention_mask']

    train_data.set_format(type='torch', columns=columns)
    test_data.set_format(type='torch', columns=columns)

    # set training arguments - Feel free to adapt it
    training_args = Seq2SeqTrainingArguments(
        output_dir="./output/t5-small-finetuned-wikisql2",
        per_device_train_batch_size=16,  # TODO origin =16,reduce to 8
        num_train_epochs=5,  # TODO orgin =5,reduce to 3
        per_device_eval_batch_size=16,  # TODO origin =16,reduce to 8
        predict_with_generate=True,
        evaluation_strategy="no",
        do_train=True,
        do_eval=False,
        # logging_steps=500,
        save_strategy="no",
        # save_steps=1000,
        # eval_steps=1000,
        overwrite_output_dir=True,
        #save_total_limit=9,   TODO origin =3,increase to 9
        load_best_model_at_end=True,
        # fp16=True,
        # push_to_hub=True
        # fp16=True,
    )

    # instantiate trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        compute_metrics=compute_metrics,
        train_dataset=train_data,
        eval_dataset=test_data
        # tokenizer=tokenizer,
    )
    trainer.evaluate()
    print('done')
    trainer.train()
    trainer.save_model()
    tokenizer.save_pretrained('./output/t5-small-finetuned-wikisql2') #  TODO 保存文件的目录 在win10环境下，会保存到python所在环境的磁盘下
    # 我的python环境在D盘，模型被保存在D://content/t5-small-finetuned-wikisql
    trainer.create_model_card()
