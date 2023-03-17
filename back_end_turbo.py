import requests
from googletrans import Translator
from flask import Flask,request,jsonify
from wsgiref.simple_server import make_server
from flask_cors import CORS
import yaml
import time



SV = Flask(__name__)
CORS(SV) # allow cross-domain

using_model = "text-davinci-003"
using_model = "gpt-3.5-turbo"

url = 'https://api.openai.com/v1/completions'
proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
translator = Translator()
req_retry_num = 3
get_data_failed_num = 5

with open('config.yaml', 'r',encoding='utf-8') as f:
    config = yaml.safe_load(f)
api_key = config['api_key']
sensitive_words = config['sensitive_words']
sensitive_words_list = sensitive_words.split(",")
default_prompt = config['default_prompt']
simplifier_prompt = config['simplifier_prompt']
weekly_report_prompt = config['weekly_report_prompt']
summaries_prompt = config['summaries_prompt']


def calculator_exec_time(run_time):
    hour = run_time // 3600
    minute = (run_time - 3600 * hour) // 60
    second = run_time - 3600 * hour - 60 * minute
    return f'time-consuming: {hour}h{minute}m{second}s'

def count_use():
    try:
        with open("count_use.txt", "r+") as file:
            count = int(file.readline().strip())
            count += 1
            file.seek(0)
            file.write(str(count))
            file.truncate()
    except FileNotFoundError:
        with open("count_use.txt", "w") as file:
            file.write("1")


def translate_languages(translate_messages,dest='en') :
    try:
        tranlated = translator.translate(translate_messages, dest=dest)
        # print(tranlated.text)
        return tranlated.text
    except Exception as E:
        # print("translate error: ", E)
        return "translate error"


def openai_chat(prompt, history):

    if not prompt:
        return gr.update(value='', visible=len(history) < 10), [(history[i]['content'], history[i+1]['content']) for i in range(0, len(history)-1, 2)], history

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    prompt_msg = {
                "role": "user",
                "content": prompt
            }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": history + [prompt_msg]
    }

    response = requests.post(url, headers=headers, json=data)
    json_data = json.loads(response.text)

    response = json_data["choices"][0]["message"]

    history.append(prompt_msg)
    history.append(response)

    return gr.update(value='', visible=len(history) < 10), [(history[i]['content'], history[i+1]['content']) for i in range(0, len(history)-1, 2)], history

def send_message(message,api_key=api_key):
    ## message = request.form["message"]
    local_message = message
    global req_retry_num
    global get_data_failed_num
    try:
        response = requests.post(url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + api_key
            },
            json={
            "model": using_model,
            "messages": [{"role": "user", "content": message}]
            }

        )

        if response.json()["choices"]:
            req_retry_num = 3 # init because success
            get_data_failed_num = 10
            response_text = response.json()["choices"][0]["message"]["content"]
            # print(response_text)
            return response_text  
        else:
            get_data_failed_num -= 1
            if get_data_failed_num != 0:
                send_message(local_message)
    except Exception as E:
        # print("requests_error",E)
        req_retry_num -= 1
        if req_retry_num != 0 :
            send_message(local_message)
            return "Oops, Data acquisition failed and is being repaired"
answer = ''
def choose_prompt(google_translated,using_func,external_api_key):
    global answer
    '''
    chatgpt-input_D = default
    chat-gpt-input_C = default_eng
    chat-gpt-input_W = weekly
    chat-gpt-input_S = summaries
    chat-gpt-input_Si = simplifier
    chatgpt-response_P = practice
    '''
    if len(external_api_key) == len(api_key):
        print(external_api_key)
        if using_func == 'chatgpt-input_D':
            answer = send_message(google_translated + default_prompt,external_api_key)
        elif using_func == 'chatgpt-input_C':
            answer = send_message(google_translated + default_prompt,external_api_key)
        elif using_func == 'chatgpt-input_W':
            answer = send_message(weekly_report_prompt + google_translated,external_api_key)
        elif using_func == 'chatgpt-input_S':
            answer = send_message(summaries_prompt + google_translated,external_api_key)
        elif using_func == 'chatgpt-input_Si':
            answer = send_message(simplifier_prompt + google_translated,external_api_key)
    else:
        if using_func == 'chatgpt-input_D':
            answer = send_message(google_translated + default_prompt)
        elif using_func == 'chatgpt-input_C':
            answer = send_message(google_translated + default_prompt)
        elif using_func == 'chatgpt-input_W':
            answer = send_message(weekly_report_prompt + google_translated)
        elif using_func == 'chatgpt-input_S':
            answer = send_message(summaries_prompt + google_translated )
        elif using_func == 'chatgpt-input_Si':
            answer = send_message(simplifier_prompt + google_translated)
            
    print("google_translated,using_func: ",using_func,external_api_key,google_translated)
    return answer
        
@SV.route("/GetContent", methods=["POST"])
def index():
    Referer = request.headers.get("Referer")
    try:
        if "artclass.eu.org" in Referer :
            try:
                message = request.json["prompt"] # "" if not prompt key: return "",not KeyError
                if message.strip() == "":
                    time.sleep(1)
                    return jsonify({"text": "so short"}),200
                if any(x in message for x in sensitive_words_list): # check for sensitive word 
                    return jsonify({"text": '请不要涉zheng'}),200
                language_type = request.json["language_type"]
                using_func = request.json["using_func"]
                external_api_key = request.json["api_key"]
                # print(message)
                google_translated = translate_languages(message,"en")
                chat_answer = choose_prompt(google_translated,using_func,external_api_key)
                if language_type != 'en':
                    answer_for_customer = translate_languages(chat_answer, "zh-cn")
                    print("resp:" ,jsonify({"text": answer_for_customer}))
                    return jsonify({"text": answer_for_customer}),200 
                print("resp:" ,jsonify({"text": answer_for_customer}))
                return jsonify({"text": answer_for_customer}),200 
            except:
                return  jsonify({"text": 'request error'}),200
    except:
        return jsonify({"text": "Authentication failed"}),200




if __name__ == '__main__':
    SV.config['JSON_AS_ASCII'] = False
    server = make_server('0.0.0.0', 18081, SV)
    server.serve_forever()


