from flask import Blueprint

# 蓝图必须指定俩参数，前者为蓝图名称，后者为蓝图所在模块
funds = Blueprint('funds',__name__)

@funds.route('/funds/hello')
def hello():
    return '/funds/hello'

@funds.route('/funds/new')
def new():
    return '/funds/new'

@funds.route('/funds/edit')
def edit():
    return '/funds/edit'