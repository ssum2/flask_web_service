from flask import Flask, render_template, request
from flask_restful import reqparse, abort, Api, Resource
from werkzeug import secure_filename

#Flask 인스턴스 생성
app = Flask(__name__)
api = Api(app)


@app.route("/")
def template_test():
    return render_template(
                'index.html',                      #렌더링 html 파일명
                title="Flask Template Test",       #title 텍스트 바인딩1
                my_str="Hello Flask!",             #my_str 텍스트 바인딩2
                my_list=[x + 1 for x in range(30)] #30개 리스트 선언(1~30)
            )


#할일 정의
TODOS = {
    'todo1': {'task': 'Make Money'},
    'todo2': {'task': 'Play PS4'},
    'todo3': {'task': 'Study!'},
}

#예외 처리
def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')

# 할일(Todo)
# Get, Delete, Put 정의
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# 할일 리스트(Todos)
# Get, POST 정의
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = 'todo%d' % (len(TODOS) + 1)
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## URL Router에 맵핑한다.(Rest URL정의)
##
api.add_resource(TodoList, '/todos/')
api.add_resource(Todo, '/todos/<string:todo_id>')



#업로드 HTML 렌더링
@app.route('/upload')
def render_file():
   return render_template('upload.html')

#파일 업로드 처리
@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      #저장할 경로 + 파일명
      f.save(secure_filename(f.filename))
      return 'uploads 디렉토리 -> 파일 업로드 성공!'


#서버 실행
if __name__ == '__main__':
    app.run(debug=True)
