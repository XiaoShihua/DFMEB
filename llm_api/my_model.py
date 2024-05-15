# -*- coding: utf-8 -*-
import json
import time
import requests
import logging


class MyModelAPI:
    def __init__(self, logger):
        self.logger = logger
        self.url = "http://xxx/v1/chat/completions"
        self.headers = {
                    'Content-Type': 'application/json'
                }

    def chat_generate(self, prompt, config=None):
        if config is None:
            config = {}
        temperature = config.get('temprature', 0.2)
        max_tokens = config.get('max_tokens', 2048)
        if isinstance(prompt, str):
            messages = [{"role": "user", "content": prompt}]
        else:
            messages = prompt
        payload = json.dumps({
            "model": "/home/model/Qwen1.5-14B-Chat/",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.95,
            "n": 1,
            "stream": False
        })

        for i in range(5):
            try:
                data = requests.request("POST", self.url, headers=self.headers, data=payload, timeout=180)
                # print(data.json())
                return json.loads(data.text)['choices'][0]['message']['content']
            except Exception as e:
                self.logger.info("调用接口失败，3s后重试。")
                time.sleep(3)
        self.logger.info("调用接口失败,超过重试次数。")
        return "error"


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    model_api = MyModelAPI(logger)
    content = "1+1=?"
    print(model_api.chat_generate(content))

