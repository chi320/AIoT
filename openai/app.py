import configparser
import datetime
import os

from flask import Flask, render_template, request, redirect, url_for
import openai

config = configparser.ConfigParser()
config.read('config.ini')
openai.api_key = config['OpenAI']['api_key']

app = Flask(__name__)

class Chat:
    def chat(prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            return "Error"


class Dalle:
    def draw(prompt):
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512",
            )
            return response.data[0].url
        except Exception as e:
            print(e)
            return "Error"




@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        try:
            chatgpt_prompt = request.form.get('chatgpt-prompt')
            dalle_prompt = request.form.get('dalle-prompt')
            if chatgpt_prompt:
                print(f"詢問ChatGPT問題: {chatgpt_prompt}")
                chatgpt_response = Chat.chat(chatgpt_prompt)
                print(f"ChatGPT回答: {chatgpt_response}")
                return render_template('index.html', chatgpt_response=chatgpt_response)
            if dalle_prompt:
                print(f"提供DALLE的敘述: {dalle_prompt}")
                dalle_response = Dalle.draw(dalle_prompt)
                print(f"圖片: {dalle_response}")
                return render_template('index.html', dalle_response_url=dalle_response)
        except:
           print("error")
    return "error", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
