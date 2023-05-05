from flask import Flask,render_template,request
import openai
# url의 해당정보 가져오기
from urllib.request import urlopen
# beautifulSoup 이용하기, 정보를 쉽게 가져오도록 beautiful soup 이용
from bs4 import BeautifulSoup

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

app = Flask(__name__,template_folder="templates") # flask name 선언

@app.route("/") #flask 웹 페이지 경로
@app.route("/main")
def main(): # 경로에서 실행될 기능 선언
#    temperature,weath,windy = get_weather()
    temperature,weath,windy=("0도","흐림","바람 붐")
    return render_template('index.html',
                           temperature=temperature,
                           weath=weath,
                           windy=windy) # 날씨값 전달

@app.route('/post', methods=['GET','POST']) 
def post():
    if request.method == 'POST': # post형식으로 값을 받아왔을 때
        value = request.form['id_name'] # value에 받아온 값 저장
        value = str(value)
#    values=openAi(value)
    values = []
    for i in range(1,6):
        values.append(value+str(i))
    return render_template('post.html', values = values) # post.html로 값 전달

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)


