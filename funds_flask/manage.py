from flask import Flask
from funds import funds
from comments import comments

# 主app
app = Flask(__name__)

# 注册蓝图
app.register_blueprint(funds)
app.register_blueprint(comments)

@app.route('/')
def index():
    return 'index'

@app.route('/list')
def list():
    return 'list'

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)