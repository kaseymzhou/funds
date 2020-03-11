from flask import Blueprint, render_template,request
from flask_paginate import Pagination, get_page_parameter
import tushare as ts
import numpy as np
import matplotlib.pyplot as mp
import pandas as pd
import json
from .calculate_model import CalculateModel
import pymysql
from app import db
from .models import Funddetails,Catalog,Sbi,Sbr,Sbm


# 蓝图必须指定俩参数，前者为蓝图名称，后者为蓝图所在模块
funds = Blueprint('funds',__name__)

# tushare token
ts.set_token('776d9779a8461c8f84056e01d4208a718e6154ac59e5c0b76829286e')
pro = ts.pro_api()

# 读取基金基本信息csv
df_funds_basic = pd.read_csv('../similarities_train/funds_details.csv')
df_funds_basic = pd.DataFrame(df_funds_basic)

@funds.route('/trend/<fid>')
def trend(fid):
    df_dtxf = pro.fund_nav(ts_code=fid+'.OF').iloc[:60]
    df_dtxf = df_dtxf.loc[:,['end_date','unit_nav','accum_nav','adj_nav']]
    fund_name = df_funds_basic[df_funds_basic['fnum']==fid].fname.iloc[0]
    print(fund_name)
    line_info = {}
    line_info['date'] = df_dtxf['end_date'].tolist()
    line_info['unit_nav'] = df_dtxf['unit_nav'].tolist()
    line_info['accum_nav'] = df_dtxf['accum_nav'].tolist()
    line_info['adj_nav'] = df_dtxf['adj_nav'].tolist()
    line_info['fund_name'] = fund_name
    result = json.dumps(line_info)
    return request.args.get("callback")+'('+result+')'

@funds.route('/recommend/<fid>')
def recommend(fid):
    df_recommend = pd.DataFrame(pd.read_csv('../score16.csv'))
    per_recommend = df_recommend[df_recommend.fnum==fid].iloc[:,1:]
    s_index = per_recommend.index[0]
    per_recommend = per_recommend.sort_values(by=s_index,ascending=False,axis=1).iloc[:,0:6].columns.tolist()
    recommend_list = []
    for item in per_recommend:
        per_rec_dict = {}
        series_fund = df_funds_basic[df_funds_basic['fnum']==item]
        per_rec_dict['name'] = series_fund['fname'].values[0]
        per_rec_dict['management'] = series_fund['management'].values[0]
        per_rec_dict['min'] = series_fund['mmin_amount'].values[0]
        per_rec_dict['fid'] = series_fund['fnum'].values[0]
        recommend_list.append(per_rec_dict)
    recom = {}
    recom['list'] = recommend_list
    # print(recom)
    result = json.dumps(recom)
    return request.args.get("callback")+'('+result+')'

@funds.route('/describe/<fid>')
def describe(fid):
    series_fund = df_funds_basic[df_funds_basic['fnum']==fid]
    per_rec_dict = {}
    per_rec_dict['manager'] = series_fund['manager'].values[0]
    per_rec_dict['management'] = series_fund['management'].values[0]
    per_rec_dict['class'] = series_fund['class'].values[0]
    per_rec_dict['risk'] = series_fund['risk'].values[0]
    per_rec_dict['founded_date'] = series_fund['founded_date'].values[0]
    per_rec_dict['rank'] = series_fund['rank_1y'].values[0]
    result = json.dumps(per_rec_dict)
    return request.args.get("callback")+'('+result+')'

@funds.route('/cal/<fid>')
def cal(fid):
    c = CalculateModel()
    indicator_fund = c.run(fid)
    result = json.dumps(indicator_fund)
    # print(type(result))
    return request.args.get("callback")+'('+result+')'

@funds.route('/catalog_view/<int:cid>/<int:sid>/<int:page>')
def catalog_view(cid,sid,page):
    # cid = request.args.get('cid')
    # sid = request.args.get('sid')
    # request.query_string
    df_funds_basic = pd.read_csv('../similarities_train/funds_details.csv')
    df_funds_basic = pd.DataFrame(df_funds_basic)
    if cid == 1:
        subclass_obj = Sbi.query.filter(Sbi.id==sid).all()
        fund_info_db = subclass_obj[0].funds_fk
    elif cid == 2:
        subclass_obj = Sbr.query.filter(Sbr.id==sid).all()
        fund_info_db = subclass_obj[0].funds_fk_r
    elif cid == 3:
        subclass_obj = Sbm.query.filter(Sbm.id==sid).all()
        fund_info_db = subclass_obj[0].funds_fk_m
    else:
        fund_info_db = 'no data'
    per_fund_preview_list = []
    for item in fund_info_db:
        per_fund_preview_dict = {}
        per_fund_preview_dict['name'] = item.name
        per_fund_preview_dict['fid'] = item.fid
        per_fund_preview_dict['management'] = df_funds_basic[df_funds_basic['fnum']==item.fid]['management'].values[0]
        per_fund_preview_dict['manager'] = df_funds_basic[df_funds_basic['fnum']==item.fid]['manager'].values[0]
        per_fund_preview_dict['unit_nv'] = df_funds_basic[df_funds_basic['fnum']==item.fid]['unit_nv'].values[0]
        per_fund_preview_dict['cnv_change_6m'] = df_funds_basic[df_funds_basic['fnum']==item.fid]['cnv_change_6m'].values[0]
        per_fund_preview_list.append(per_fund_preview_dict)
    # per_page = 5
    # page = int(page)
    # per_fund_preview_result = per_fund_preview_list[(page-1)*per_page:page*per_page]
    per_fund_preview_result = per_fund_preview_list
    result = json.dumps({'content':per_fund_preview_result,'sname':subclass_obj[0].name})
    return request.args.get("callback")+'('+result+')'

@funds.route('/index')
def index():
    df_funds_basic = pd.read_csv('../similarities_train/funds_details.csv')
    df_funds_basic = pd.DataFrame(df_funds_basic)
    man_choice_list = ['广发基金', '博时基金', '南方基金','华夏基金', '工银瑞信基金', '招商基金']
    type_choice_list = ['债券指数', '债券型','股票型', '混合FOF','混合型']
    score_list = []
    for i in man_choice_list:
        for j in type_choice_list:
            total_scale = df_funds_basic[(df_funds_basic['management']==i)&(df_funds_basic['class']==j)]['scale']
            total_scale = total_scale.str.split('亿').str[0]
            total_scale = total_scale.astype('float').sum()
            score = [type_choice_list.index(j),man_choice_list.index(i),total_scale]
            # print(j,i,score)
            score_list.append(score)
    # print(score_list)
    result = json.dumps({'score_list':score_list})
    return request.args.get("callback")+'('+result+')'