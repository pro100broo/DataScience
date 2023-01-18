import pandas as pd
import matplotlib.pyplot as plt

excel_data = pd.ExcelFile('oilbrent.xlsx')

data_brent = excel_data.parse('нефть brent')
data_companies = excel_data.parse('companies')

# График по дням
data_brent.pivot_table(index='Дата', values='Стоимость').plot(
    grid=True,
    ylabel='Общая стоимость по дням, млн. $',
    xlabel='Дни',
    title='Изменение прибыли по месяцам',
    figsize=(20, 10)
)

plt.show()

# Добавялем новые столбцы
data_brent['Дни'] = data_brent['Дата'].dt.day
data_brent['Месяцы'] = data_brent['Дата'].dt.month

# Выводим топ 10 дней по стоимости нефти
top_days = data_brent[['Дата', 'Стоимость']].sort_values('Стоимость', ascending=False).head(10)
top_days.reset_index(inplace=True)
top_days.drop('index', inplace=True, axis=1)

print('Топ 10 дней по максимальной стоимости нефти:\n', top_days)

# Группировка по месяцам и среднему показателю стоимости
top_month = data_brent[['Месяцы', 'Стоимость']].groupby('Месяцы').agg({'Стоимость': 'mean'})
top_month.sort_values('Стоимость', ascending=False, inplace=True)
top_month.reset_index(inplace=True)
top_month.columns = (['Месяц', 'Средняя стоимость'])

print('\nТоп месяцев по среднему показателю стоимости нефти:\n', top_month)

print('\nКорреляция общей стоимости от месяца')
print(data_brent['Месяцы'].corr(data_brent['Стоимость']))
print('\nКорреляция общей стоимости от дня')
print(data_brent['Дни'].corr(data_brent['Стоимость']))

# Для общего объема добычи
# Группируем по компаниям, аггрегируем по общей стоимости, сортируем
companies_volume = data_companies.groupby('Компания').agg({'Объём добычи': 'sum'}).sort_values('Объём добычи', ascending=False)
names = companies_volume.index.to_list()
values = companies_volume['Объём добычи']
fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot()

# Вытаскиваем из отсортированной таблицы список компаний и стоимостей. Передаём их аргументами в пирог
ax.pie(companies_volume['Объём добычи'].to_list(), labels=companies_volume.index.to_list())
total = sum(data_companies['Объём добычи'])
labels = [f"{n} ({v/total:.1%})" for n, v in zip(names, values)]
ax.legend(loc='center', labels=labels)

plt.title('Объём добычи')
plt.show()

# Для общей стоимости
# companies_cost = data_companies[['Компания', 'Общая стоимость']]
companies_cost = data_companies.groupby('Компания').agg({'Общая стоимость': 'sum'}).sort_values('Общая стоимость', ascending=False)
fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot()

# Вытаскиваем из отсортированной таблицы список компаний и стоимостей. Передаём их аргументами в пирог
ax.pie(companies_cost['Общая стоимость'].to_list(), labels=companies_cost.index.to_list())

total = sum(data_companies['Объём добычи'])
labels = [f"{n} ({v/total:.1%})" for n,v in zip(data_companies['Компания'], data_companies['Общая стоимость'])]
ax.legend(loc='center', labels=labels)
plt.title('Общая стоимость')

plt.show()