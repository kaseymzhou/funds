# FFUNDS 基金信息平台

### 1. 板块

#### 1.1 基金模块：

- 基金基本信息展示（基金网站爬取、tushare接口）

- 基金推荐（基于商品的协同过滤）
- 基金业绩指标计算（Pandas、Numpy、Scipy）
- 基金数据可视化（Echarts）

#### 1.2 用户模块（待完善）：

- 登录注册
- 用户对基金的评价
- 用户留言

### 2. 主要环境

- Windows7（开发环境）
- Python 3.7
- Anaconda 4.7.12
- Flask 1.1.1
- MySQL 8.0.19
- Tushare 1.2.51
- SQLAlchemy 1.3.9
- Pymysql 0.9.3
- Flask-SQLAlchemy 2.4.1
- Flask-MySQLdb 0.2.0

### 3. 使用方法

- MySQL创建库：create database ffunds default charset utf8;
- 进入funds_flask/app/中进入`__init__.py`，把数据库用户名和密码修改为与本机一致的信息
- 执行funds_flask中执行create_db.py，创建数据表
- 进入app文件夹执行pysql_add.py，创建表记录
- 执行manage.py文件
- 打开funds_flask/web/templates的funds-index.html

#### TO BE NOTICES

- 本项目重心在服务端以及数据处理部分，因此前端套用了付费静态页面模版，但ajax的数据传输以及Echarts图表绘制为本人添加的。再次提醒，本项目只为本人编程学习所用，没有任何商业用途。
- 因时间原因，部分模板尚待完善，可能部分页面会有bug，后续会更新修正的。
- 如果点击导航栏，查看每个基金分类下的基金数量后，发现显示no data available，或者点进具体基金详情页面时发现展示异常，只是数据在传输中，稍等一会就好。
- 部分QDII信息异常，是由于本人tushare积分不够，无法调用QDII信息获取借口。以后会努力提高积分哒~

