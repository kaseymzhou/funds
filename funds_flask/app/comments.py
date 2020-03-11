from flask import Blueprint

# 蓝图必须指定俩参数，前者为蓝图名称，后者为蓝图所在模块
comments = Blueprint('comments',__name__)

@comments.route('/comments/hello')
def hello():
    return '/comments/hello'

@comments.route('/comments/new')
def new():
    return '/comments/new'

@comments.route('/comments/edit')
def edit():
    return '/comments/edit'