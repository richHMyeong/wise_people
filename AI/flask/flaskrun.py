# orm->클래스개념.더 직관적으로 테이블에 데이터 삽입
# 플라스크 마이그레이트: 플라스크의 테이블구조와 sql의 테이블 구조가 같은지 확ㅇ니. 다르면 자동으로 맞춤.
# 점프투플라스크 추천 https://wikidocs.net/book/4542

# 플라스크 서버 만들 때 이 구조로 만들어야 한다.
# 실행: set FLASK_APP=chatbot 하면 chatbot폴더가 실행됨
from flask import Flask
from flask import render_template



# html은 조건반복문 등 사용x 진쟈투를 써서 사용할 수 있따.

app = Flask(__name__) # flask 서버를 app이라는 변수에 담음
@app.route('/')
def index():
    return 'dfsf'

@app.route('/chatbot') #슬래시 있어야 함
def catbot():
    return {'result': '나는 챗봇이야'}

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 5000)
# 터미널 : set FLASK_APP = 패키지폴더명  set FLASK_DEBUG=true 해주기

# 플라스크 서버는 항상 실행되어 있어야. 원래는 terminal켜서 거기서 적어야 함.flask run
