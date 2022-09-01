# 보통 flask는 app.py로 만듦.
# flask run해서 실행하는 방법..app.py를 가장먼저 인식해서 app.py로 함

# 1. 플라스크 생성
# 2. 주소 생성 (중요!!!!)
# 3. 플라스크 서버 실행 방법: 파이썬 app.py로 실행, 플라스크 run 명령어로 실행,
# python app.py로 실행하려면

from flask import Flask

def create_app(): # 모두 감싸는 함수 하나 만들고 return app함

    app = Flask(__name__) # flask 서버를 app이라는 변수에 담음

    # rest api는 주소기반. com/이후부터 uri. 뒤에 붙을수록 뎁스가 깊다고하고 깊을수록 복잡해짐.

    # app.route있으면 url을 자동으로 찾아서 분기해줌. 내가 지정한 '/' 이후 uri부분과 맞우면..함수 적용
    # 슬래시 붙은 걸 자동으로 찾은 후 라우트 바로 밑 함수가 호출 됨. 어떤 웹이나 앱에 return한느 거.
    @app.route('/')
    def index():
        return {'result': '안녕 반가워.'}


    @app.route('/chatbot') #슬래시 있어야 함
    def catbot():
        return {'result': '나는 챗봇이야'}

    return app
# python app.py명령어로 실행하려면!!
#if __name__ == '__main__':
#    app.run(host='127.0.0.1', port=5000, debug = True) #app.run으로만 해도 됨(자동으로 디폴트값 들어감(
    # 여러 서버돌릴 때 포트번호 매우 중요. 포트번호 바꿔줘도 됨. 반드시 겹치지 않도록 하자.
    # 외부에서 같은 포트번호로 들어오 ㄹ대.. 어디로 가야할지 모름. 디폴트는 5000번
    # debug=true는 지금 개발중이다~라는 뜻

# 우와 신기~!~!
# 나중에 기능 필요할 때마다 /chatbot처럼 주소 붙여서 ㅁ나들면 됨.
# 터미널에서 python app.py로 수정 가능
# debug=True로 되어 있으면 코드 수정 시 자동으로 서버 껐다가 다ㅣㅅ 켜짐.

# 서버 실행하는 두 번째 방법(대부분 이 방법 사용) : terminal에서 falsk run 입력
# debug mode가 off임.
# 한 번만 하면 됨. set FLASK_DEBUG=true 하면 디버그 모드가 온으로 바ㅜ김

# 파일 이름 바꾼 후 flask run하면 app.py없어서 오류 뜸
# 이럴 때는 set FLASK_APP=chatbot 적으면 됨. (실행할 파일 지정)

# 아마존 등 서버에 올릴 때는 터미널의 flask run 명령어로 올림.

# 플라스크는 애플맄[이션 어쩌구 타입을 사용. 프로젝트 아래에 템플릿 폴더만ㄷ름. 그후 그 아래에 챗폿py를 실행
# 실행하는 그 내부 파일들오 크리에이트앱 안에 집어넣음
# 플라스크 런하면 자동으로 이 폴더 ㅣㄹ행하고...므ㅓ..