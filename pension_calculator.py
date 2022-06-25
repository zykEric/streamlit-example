import pandas as pd
import numpy as np

average_salary = pd.read_excel('平均工资.xlsx')
average_salary.index=average_salary['省份']
dict2 = {65:101, 60:139, 55:170, 50:195}

def pension_calculator(age,workingyear,retire_age,cum_account,city_avgsal,salary,salary_growth,average_salary_growth,average_percent):
    basic_pension = round(float(city_avgsal) * pow(1 + average_salary_growth, retire_age - age - 1) * (
                1 + average_percent) / 2 * (retire_age - age + workingyear) * 0.01, 2)
    salary_list = []
    for i in range(0, retire_age - age):
        salary_then = salary * pow(1 + salary_growth, i)
        salary_list.append(salary_then * 0.08 * 12)
    personal_pension = round((cum_account + np.array(salary_list).sum()) / dict2[retire_age],2)
    additional_pension = round(float(city_avgsal) * pow(1 + average_salary_growth, retire_age - age - 1) * average_percent * (
                retire_age - age + workingyear) * 0.001,2)
    pension_total= basic_pension + personal_pension + additional_pension
    return pension_total, basic_pension, personal_pension, additional_pension