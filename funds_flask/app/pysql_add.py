import pymysql
import pandas as pd

# 请先在mysql中创建库 create database ffunds charset utf8;

db=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='123456',database='ffunds',charset='utf8')
cursor=db.cursor()

# 总类表
# sql_createTb_catalog = """CREATE TABLE `%s`(id INT NOT NULL AUTO_INCREMENT,NAME VARCHAR(30),PRIMARY KEY(id))"""%('catalog')
# cursor.execute(sql_createTb_catalog)

try:
    sql1 = "INSERT INTO `catalog` VALUES (%s, %s)"
    cursor.executemany(sql1,[(1,'按投资类别'),(2,'按风险程度'),(3,'按基金管理人'),(4,'其他')])
    db.commit()
except Exception as e:
    db.rollback()
    print(e)

# 分类表 -- 1
# sql_createTb_subclass_investment = """CREATE TABLE `%s`(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#                                             cid INT NOT NULL, name VARCHAR(30), constraint cid_i foreign key(cid) references catalog(id));
#                                             """%('subclass_investment')
# cursor.execute(sql_createTb_subclass_investment)

try:
    sql2 = "INSERT INTO `subclass_investment` VALUES (%s, %s, %s)"
    cursor.executemany(sql2,[(1,1,'债券型'),(2,1,'债券指数'),(3,1,'股票型'),
                            (4,1,'QDII'),(5,1,'混合-FOF'),(6,1,'混合型'),(7,1,'其他')])
    db.commit()
except Exception as e:
    db.rollback()
    print(e)

# 分类表 -- 2
# sql_createTb_subclass_risk = """CREATE TABLE `%s`(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#                                             cid INT NOT NULL, name VARCHAR(30), constraint cid_r foreign key(cid) references catalog(id));
#                                             """%('subclass_risk')
# cursor.execute(sql_createTb_subclass_risk)

try:
    sql3 = "INSERT INTO `subclass_risk` VALUES (%s, %s, %s)"
    cursor.executemany(sql3,[(1,2,'高风险'),(2,2,'中高风险'),(3,2,'中风险'),(4,2,'中低风险'),(5,2,'低风险'),(6,2,'其他')])
    db.commit()
except Exception as e:
    db.rollback()
    print(e)

# 分类表 -- 3
# sql_createTb_subclass_management = """CREATE TABLE `%s`(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#                                             cid INT NOT NULL, name VARCHAR(30), constraint cid_m foreign key(cid) references catalog(id));
#                                             """%('subclass_management')
# cursor.execute(sql_createTb_subclass_management)

try:
    sql4 = "INSERT INTO `subclass_management` VALUES (%s, %s, %s)"
    cursor.executemany(sql4,[(1,3,'博时基金'),(2,3,'广发基金'),(3,3,'中信保诚公司'),(4,3,'南方基金'),
                            (5,3,'华夏基金'),(6,3,'工银瑞信基金'),(7,3,'招商基金'),
                            (8,3,'万家基金'),(9,3,'嘉实基金'),(10,3,'易方达基金'),(11,3,'其他')
    ])
    db.commit()
except Exception as e:
    db.rollback()
    print(e)

# 基金详细表
# sql_createTb_funds_details = """CREATE TABLE `%s`(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#                                             name VARCHAR(30),
#                                             fid VARCHAR(10),
#                                             risk INT NOT NULL,
#                                             class INT NOT NULL,
#                                             management INT NOT NULL);
#                                             """%('funds_details')
# cursor.execute(sql_createTb_funds_details)


risk_dict= [('高风险',1),('中高风险',2),('中风险',3),('中低风险',4),('低风险',5)]
class_dict = [('债券型',1),('债券指数',2),('股票型',3),('QDII',4),('混合FOF',5),('混合型',6)]
management_dict = [('博时基金',1),('广发基金',2),('中信保诚公司',3),('南方基金',4),('华夏基金',5),('工银瑞信基金',6),('招商基金',7),('万家基金',8),('嘉实基金',9),('易方达基金',10)]

df_recommend = pd.DataFrame(pd.read_csv('../../similarities_train/funds_sorted.csv'))
funds_list = []
for index,row in df_recommend.iterrows():
    for item1 in risk_dict:
        if row['risk']==item1[0]:
            row['risk']=item1[1]
    for item2 in class_dict:
        if row['class']==item2[0]:
            row['class']=item2[1]
    for item3 in management_dict:
        if row['management']==item3[0]:
            row['management']=item3[1]
    if row['risk'] not in range(1,6):
        row['risk'] = 6
    if row['class'] not in range(1,7):
        row['class'] = 7
    if row['management'] not in range(1,11):
        row['management'] = 11
    funds_list.append((index+1,row['fname'],row['fnum'],row['risk'],row['class'],row['management']))

# print(funds_list)

try:
    sql5 = "INSERT INTO `funds_details` VALUES (%s, %s, %s, %s,%s, %s)"
    cursor.executemany(sql5,funds_list)
    db.commit()
except Exception as e:
    db.rollback()
    print(e)


db.close()
cursor.close()
