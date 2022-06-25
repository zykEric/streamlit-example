import streamlit as st
import pandas as pd
import numpy as np


st.title('养老金计算器')
name_text = st.sidebar.text_input(
    '姓名',
    value='李明'
)
gender_text = st.sidebar.selectbox(
    '性别',
    ('男','女')
)
age_text = st.sidebar.text_input(
    '年龄(岁)',
    value=24
)
workingyear_text = st.sidebar.text_input(
    '工作年限(年)',
    value=2
)
cum_account_text = st.sidebar.text_input(
    '个人账户累积养老金(元)',
    value=20000
)
province_box = st.sidebar.selectbox(
    "所在省份",
    ('北京', '天津', '河北', '山西', '内蒙古', '辽宁',
     '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽',
     '福建', '江西', '山东', '河南', '湖北', '湖南',
     '广东', '广西', '海南', '重庆', '四川', '贵州',
     '云南', '西藏', '陕西', '甘肃', '青海', '宁夏',
     '新疆')
)
retire_age_box = st.sidebar.selectbox(
    '预计退休年龄(岁)',
    (65, 60, 55, 50)
)


salary_text = st.sidebar.text_input(
    '月薪(元)',
    value=10000
)
salary_growth_text = st.sidebar.text_input(
    '预计月薪年增长率(%)',
    value=10
)
average_percent_text = st.sidebar.text_input(
    '平均缴费比例(%,按社平工资 60%-300%)',
    value=100
)

average_salary_growth_text = st.sidebar.text_input(
    '预计社会平均工资年增长率(%)',
    value=3
)

def pension_calculator(age,workingyear,retire_age,cum_account,province,salary,salary_growth,average_salary_growth,average_percent):
    dict1 = {'北京': 9407.166667, '天津': 6777.0, '河北': 5409.166667, '山西': 5392.333333, '内蒙古': 6344.0, '辽宁': 5709.0,
             '吉林': 6004.75,'黑龙江': 4718.291667, '上海': 10338.0, '江苏': 6977.125, '浙江': 6594.416667, '安徽': 5975.14,
             '福建': 6126.416667,'江西': 5548.0, '山东': 6242.166667, '河南': 5328.0,'湖北': 5925.833333, '湖南': 5460.0,
             '广东': 7647.0, '广西': 5819.333333, '海南': 6543.0, '重庆': 6164.833333,'四川': 6210.0, '贵州': 6378.916667,
             '云南': 6284.0, '西藏': 8839.0, '陕西': 6053.0, '甘肃': 6053.0, '青海': 7023.166667, '宁夏': 6110.0, '新疆': 6028.615385}
    dict2 = {65: 101, 60: 139, 55: 170, 50: 195}
    basic_pension = round(float(dict1[province]) * pow(1 + average_salary_growth, retire_age - age - 1) * (
                1 + average_percent) / 2 * (retire_age - age + workingyear) * 0.01, 2)
    salary_list = []
    for i in range(0, retire_age - age):
        salary_then = salary * pow(1 + salary_growth, i)
        salary_list.append(salary_then * 0.08 * 12)
    personal_pension = round((cum_account + np.array(salary_list).sum()) / dict2[retire_age],2)
    additional_pension = round(float(dict1[province]) * pow(1 + average_salary_growth, retire_age - age - 1) * average_percent * (
                retire_age - age + workingyear) * 0.001,2)
    pension_total = basic_pension + personal_pension + additional_pension
    inflation_rate = 0.03
    inflation = pow(1 + inflation_rate, retire_age - age - 1)

    return pension_total, basic_pension, personal_pension, additional_pension, inflation
age = int(age_text)
workingyear = int(workingyear_text)
retire_age = int(retire_age_box)
cum_account = float(cum_account_text)
province = str(province_box)
salary = float(salary_text)
salary_growth = float(salary_growth_text)/100
average_salary_growth = float(average_salary_growth_text)/100
average_percent = float(average_percent_text)/100
pension_total, basic_pension, personal_pension, additional_pension , inflation = pension_calculator(age,workingyear,retire_age,cum_account,province,salary,salary_growth,average_salary_growth,average_percent)

pension_pd = pd.DataFrame(
    columns=['金额(元)','相当于现在(元）'],index=['预估养老金(总)','预估基础养老金','预估个人养老金','预估增发养老金']
)
value=np.array([pension_total,basic_pension,personal_pension,additional_pension]).round(2)
pv=np.array([pension_total/inflation,basic_pension/inflation,personal_pension/inflation,additional_pension/inflation]).round(2)
pension_pd['金额(元)'] = value
pension_pd['相当于现在(元）']=pv

# st.table(pension_pd)

if gender_text =='男':
    title = '先生'
else :
    title = '女士'

st.markdown(f'##### {name_text}{title},您的养老金计算结果如下:')
st.write('预估养老金(总)：', round(pension_total,2), '元,','相当于现在的',round(pension_total/inflation,2), '元')
st.write('预估基础养老金：', round(basic_pension,2), '元,','相当于现在的',round(basic_pension/inflation,2), '元')
st.write('预估个人养老金：', round(personal_pension,2), '元,','相当于现在的',round(personal_pension/inflation,2), '元')
st.write('预估增发养老金：', round(additional_pension,2), '元,','相当于现在的',round(additional_pension/inflation,2), '元')
bar1, bar2 = st.columns(2)
with bar1:
    st.bar_chart(pension_pd.iloc[:,0])
with bar2:
    st.bar_chart(pension_pd.iloc[:, 1])
st.markdown('-------')
st.markdown('##### 为您推荐养老产品——财通资管鑫管家B')
st.image('财通资管鑫管家B.png')

