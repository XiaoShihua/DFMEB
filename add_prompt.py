# -*- coding: utf-8 -*-
"""
将prompt添加到数据中
"""
from copy import deepcopy
from prompt_template import prompt_dict


class PromptCreate:
    def __init__(self):
        self.keys = prompt_dict.keys()

    def create(self, key, **kwargs):
        if key in self.keys:
            eval_messages = deepcopy(prompt_dict[key])
            return eval_messages.format(**kwargs)
        else:
            raise KeyError(f"任务：{key} 无法匹配到对应模板，请检查后重试！")


if __name__ == '__main__':
    PC = PromptCreate()
    a = {"id": 1, "question": "11", "A": "11", "B": "22", "C": "33", "D": "44"}
    print(PC.create("经济学知识", **a))
