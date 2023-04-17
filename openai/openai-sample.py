import configparser
import openai

config = configparser.ConfigParser()
config.read('config.ini')
openai.api_key = config['OpenAI']['api_key']


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


if __name__ == "__main__":

    prompt = input("輸入詢問ChatGPT問題: ")
    response = Chat.chat(prompt)
    print(f"Response: {response}")

    prompt = input("輸入DALLE產生圖片的敘述: ")
    response = Dalle.draw(prompt)
    print(f"Response: {response}")
