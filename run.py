# -*- coding: utf-8 -*-
import json
import os
import time
import logging
import argparse
from tqdm import tqdm
from add_prompt import PromptCreate
from llm_api.my_model import MyModelAPI

parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default="A_data/test", type=str, help="data_path")
parser.add_argument('--output_file', default="xx_A_result_14B.jsonl", type=str, help="output_path")
args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
model = MyModelAPI(logger)
pc = PromptCreate()


def run(model_api, in_file, out_file):
    questions = []
    with open(in_file, "r", encoding="utf-8") as f:
        for line in f:
            questions.append(json.loads(line))
    fd = open("error.txt", "w", encoding="utf-8")
    with open(out_file, "a+", encoding="utf-8") as fw:
        for question in tqdm(questions):
            # 添加prompt模板
            try:
                prompt = pc.create(key=question["task"], **question)
                # print(prompt)
                content = model_api.chat_generate(prompt)
                question["answer"] = content
                logger.info(question)
                fw.writelines(json.dumps(question, ensure_ascii=False))
                fw.writelines("\n")
                fw.flush()
                # break
            except:
                fd.write("{}, {}".format(in_file, question["task"]))
                continue
    fd.close()


if __name__ == "__main__":
    if os.path.exists(args.output_file):
        os.remove(args.output_file)
    start = time.time()
    for src, dirs, files in os.walk(args.data_path):
        for file in files:
            if file.endswith(".jsonl"):
                in_path = os.path.join(src, file)
                run(model, in_path, args.output_file)
    print(f"总计耗时：{(time.time()-start)/3600} h")
