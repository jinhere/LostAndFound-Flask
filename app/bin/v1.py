from flask import Blueprint
from flask import render_template
app = Blueprint('v1', __name__, url_prefix='/v1')
# v1은 url_for에서 쓰임. 두번째는 정적파일과 템플렛 위치를 추적시 사용
# url_prefix는 저걸로 시작하고 밑에 route 인자값이 뒤에 붙는 거임
@app.route('/users')
def users():
#    return 'v1'
    return render_template('hello.html',name='kim')
@app.route('/users/<int:user_id>')
def get_user(user_id):
    return 'good morning Quinn {}'.format(str(user_id))