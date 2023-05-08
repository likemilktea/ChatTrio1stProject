from flask import Flask,render_template,request
import openai
# url의 해당정보 가져오기
from urllib.request import urlopen
# beautifulSoup 이용하기, 정보를 쉽게 가져오도록 beautiful soup 이용
from bs4 import BeautifulSoup
import pandas as pd
from time import localtime
from time import time



## 네이버 날씨에서 정보 가져오기
def get_weather():
    url = "https://weather.naver.com"
    page = urlopen(url)
    soup = BeautifulSoup(page,'lxml')
    # 날씨 # 온도 # 바람 # 목적 # 습도 # 미세먼지
    temp = soup.find("strong",class_="current").text
#    print(temp[6:])
    # 온도
    temperature = temp[6:]
    # 날씨
    weath = soup.find("span",class_="weather").text
    #print(weath)
    # 바람
    windy = soup.find("ul",class_="weather_table list")
    #print(windy)
    return (temperature,weath,windy)

# openAi
def openAi(question):

    key1 = "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"
    openai.api_key = key1

    text1 = question
    msg = text1

    msg_input = [ ]
    msg_input.append( {"role":"user", "content":msg})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msg_input
    )

    answers=response.choices[0].message.content.split("\n\n")
    return answers

def save_csv(columns, path):
    my_dict = {"month":[columns[0]],"temperature": [columns[1]], "wether": [columns[2]]} # DataFrame으로 만들어 csv로
    df1=pd.DataFrame(my_dict)
    df1.to_csv(path,mode='a',header=False,index=False)

app = Flask(__name__,template_folder="templates") # flask name 선언

@app.route("/") #flask 웹 페이지 경로
@app.route("/main")
def main(): # 경로에서 실행될 기능 선언
    temperature,weath,windy = get_weather()

    return render_template('index.html',
                           temperature=temperature,
                           weath=weath,
                           windy=windy) # 날씨값 전달

@app.route('/post', methods=['GET','POST']) # post형식으로 값을 받아왔을 때
def post():
    temperature,weath,windy = get_weather()
    
    month=localtime(time()).tm_mon # 검색한 월
    
    save_path="db/sample.csv"
    save_csv([month,temperature[:-2],weath],save_path) #검색한 월,기온,날씨,저장 위치   
    
    if request.method == 'POST':
        value = request.form['id_name'] # value에 받아온 값 저장
        value = temperature + ' ' + weath + ' ' +str(month) + ' ' + str(value)
    values=openAi(value)
    
    return render_template('post.html', values = values) # post.html로 값 전달
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)