import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

def extract_contents_from_url(source_url):
    response = requests.get(source_url)

    if response.status_code != 200:
        return None
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = soup.get_text()

        return text_content

class GPTWrapper:
    def __init__(self, model_name=None, response_format=None, system_prompt=None, seed=None, temperature=None):

        self.client = OpenAI()
        
        if model_name is None:
            model_name = "gpt-4-1106-preview"
        self.model_name = model_name

        if system_prompt is None:
            system_prompt = "You are a helpful assistant."
        self.system_prompt = system_prompt
        
        if response_format == 'json':
            response_format = {"type": 'json_object'}
        self.response_format = response_format
        
        self.seed = seed

        self.temperature = temperature

    def __call__(self, query):
        completion = self.client.chat.completions.create(
          model=self.model_name,
          response_format=self.response_format,
          seed=self.seed,
          temperature=self.temperature,
          messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": query},
            ]
        )
        return completion.choices[0].message.content