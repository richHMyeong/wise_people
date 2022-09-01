
# 포트를 열고

# html은 조건반복문 등 사용x 진쟈투를 써서 사용할 수 있따.
from flask import Flask, request


app = Flask(__name__) # flask 서버를 app이라는 변수에 담음
@app.route('/', methods = ['GET', 'POST'])
def index():
    json_data = request.get_json()
    # tmp = json_data["angle1"]
    # tmp = str(json_data)
    # print(tmp)
    # print('받았다!')
    angle1 = json_data["angle1"]
    distance = json_data["distance"]
    updown = json_data["updown"]
    time = json_data["time"]
    #data = str(angle1)+', '+str(distance)+','+str(updown)+','+str(time)
    # str만 전달이 가능하다
    return 'index'

@app.route('/hand', methods = ['GET','POST'])
def go():
    json_data = request.get_json()
    #tmp = json_data["angle1"]
    tmp = str(json_data)
    print(tmp)
    # angle1 = json_data["angle1"]
    # distance = json_data["distance"]
    # updown = json_data["updown"]
    # time = json_data["time"]
    # print(angle1)
    return 'adsfdf'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 5000, debug=True)
