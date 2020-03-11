import tushare as ts
import numpy as np
import matplotlib.pyplot as mp
import pandas as pd
import json
from scipy import stats

class CalculateModel():
    def last_date_per_month(self,df_all,date_name):
        recent_month = pd.datetime.now().month
        recent_year = pd.datetime.now().year
        df_all[date_name] = pd.to_datetime(df_all[date_name])
        df_all['month'] = df_all[date_name].dt.month
        df_all['year'] = df_all[date_name].dt.year
        df_all = df_all[~((df_all['month']==recent_month)&(df_all['year']==recent_year))] # 去除本月数据
        df_all = df_all[~((df_all['month']<=(recent_month-1))&(df_all['year']<=(recent_year-1)))] # 去除一年以前的数据
        df_all = df_all[~(df_all['year']<(recent_year-1))]
        months = df_all['month'].unique()
        df = pd.DataFrame()
        for item in months:
            max = df_all[df_all['month']==item].iloc[0]
            df = df.append(max)
        # df.pop('month')
        df.pop('year')
        df.reset_index(drop=True, inplace=True)
        return df

    def get_last_day(self,fid):
        ts.set_token('776d9779a8461c8f84056e01d4208a718e6154ac59e5c0b76829286e')
        pro = ts.pro_api()

        # 近一年每月上证指数最后一天指标
        df_sz = ts.pro_bar(ts_code='000001.SH', asset='I',start_date='20190101')
        df_sz = df_sz.loc[:,['trade_date','close']]
        df_sz = self.last_date_per_month(df_sz,'trade_date')
        # print(df_sz)

        # 近一年每月基金最后一天指标
        df_fund = pro.fund_nav(ts_code=fid+'.OF')
        df_fund = df_fund.loc[:,['end_date','unit_nav','accum_nav']]
        df_fund = self.last_date_per_month(df_fund,'end_date')
        # print(df_fund)

        # 合并表格
        df_ana = pd.merge(df_sz,df_fund)
        return df_ana

    def cal(self,df_ana):
        # 计算收益率
        s1 = (df_ana['accum_nav']/df_ana['accum_nav'].shift(-1))-1
        s2 = (df_ana['close']/df_ana['close'].shift(-1))-1
        df_ana['fund_return'] = s1 #　基金 - RP
        df_ana['sz_return'] = s2 # 上证指数 - RM
        df_ana['cny_year_ins']=pd.Series(1.5/100/12,index=df_ana.index) # 无风险收益率 -- 一年期活期收益率 -- RF

        # 计算 rp-rf 和 rm-rf
        df_ana = df_ana.iloc[:-1]
        rp_rf = df_ana['fund_return']-df_ana['cny_year_ins']
        rm_rf = df_ana['sz_return']-df_ana['cny_year_ins']

        # 计算beta、alpha
        x = np.column_stack((rm_rf.values,np.ones_like(rm_rf.values)))
        y = rp_rf.values
        result = np.linalg.lstsq(x,y,rcond=None)[0]
        beta=result[0]
        alpha=result[1]
        # print('beta:',beta,'alpha:',alpha)

        # 计算平均收益率
        pr_plus_1 = df_ana['fund_return']+1
        avg_return = stats.gmean(pr_plus_1)-1
        # print(avg_return)

        # 计算accum标准差
        accum_std = np.std(df_ana['accum_nav'].iloc[:-1])
        # print(accum_std)

        # 计算sharpe
        sharpe = (avg_return-np.mean(df_ana['cny_year_ins'].iloc[:-1]))/accum_std
        # print(sharpe)

        # 计算Treynor
        Treynor = (avg_return-np.mean(df_ana['cny_year_ins'].iloc[:-1]))/beta
        # print(Treynor)

        # 计算Jeason
        Jeason = (avg_return-np.mean(df_ana['cny_year_ins'].iloc[:-1]))/(avg_return-np.mean(df_ana['cny_year_ins'].iloc[:-1]))*beta
        # print(round(Jeason*100,3))

        cal_dict = {}
        cal_dict['beta'] = round(beta,6)
        cal_dict['alpha'] = round(alpha,6)
        cal_dict['avg_return'] = round(avg_return,6)
        cal_dict['accum_std'] = round(accum_std,6)
        cal_dict['Treynor'] = round(Treynor,6)
        cal_dict['sharpe'] = round(sharpe,6)
        cal_dict['Jeason'] = round(Jeason,6)

        return cal_dict
    
    def run(self,fid):
        return self.cal(self.get_last_day(fid))

# if __name__ == '__main__':
#     s = CalculateModel()
#     s.run('002930')

