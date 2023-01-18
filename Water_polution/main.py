import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Загрузка датасета
data = pd.read_csv('water.csv', sep=',')

# Удаление столбца с id
data = data.drop('Unnamed: 0', axis=1)

# Статистический анализ северных и южных городов
print('\n----------------------------------------------------------'
      '\n|Статистический анализ данных по северным и южным городам|'
      '\n----------------------------------------------------------')
# Построение точечного графика
data.pivot_table(index='hardness', values='mortality').plot(grid=True,
                                                               figsize=(20, 10))
plt.title('Изменение кол-ва смертей в зависимости от коэф. жёсткости воды\nДля северных и южных городов')
plt.xlabel('Коэф. жёсткости воды')
plt.ylabel('Средняя годовая смертность')
plt.show()

# Расчёт корреляции Пирсона
print('\nКорреляция жёсткости воды и средней годовой смертностью:')
print(f"\nКоэффициент корреляции Пирсона: {data['mortality'].corr(data['hardness'])}")

# Расчёт корреляции Спирмена
cof, _ = st.spearmanr(data['mortality'], data['hardness'])
print(f'Коэффициент корреляции Спирмена: {cof}')

print('\nНа основе анализа коэф. корреляции можем сделать следующие выводы:'
      '\nОценки коэф. жёсткости воды демонстрируют слабую отрицательную корреляцию со средней годовой смертностью. ')

# Построение модели линейной регрессии
# https://www.codecamp.ru/blog/linear-regression-python/

model = ols('hardness ~ mortality', data=data).fit()

print('\nМодель линейной регрессии: ')
print(model.summary())

# Расчёт коэффициента детерминации
print(f'\nКоэффициент детерминации: {model.rsquared * 100}')
print('Итак, {res:.1f}% смертей обусловлено жёсткостью воды.\n'.format(res=model.rsquared * 100))

# Вывод графика остатков
fig = plt.figure(figsize=(15, 7))
fig = sm.graphics.plot_regress_exog(model, 'mortality', fig=fig)

plt.show()

# Статистический анализ северных городов
print('\n--------------------------------------------------'
      '\n|Статистический анализ данных по северным городам|'
      '\n--------------------------------------------------')
north_data = data.loc[data['location'] == 'North']

# Построение точечного графика
north_data.pivot_table(index='hardness', values='mortality').plot(grid=True,
                                                               figsize=(20, 10))
plt.title('Изменение кол-ва смертей в зависимости от коэф. жёсткости воды\nДля северных городов')
plt.xlabel('Коэф. жёсткости воды')
plt.ylabel('Средняя годовая смертность')
plt.show()

# Расчёт корреляции Пирсона
print('\nКорреляция жёсткости воды и средней годовой смертностью:')
print(f"\nКоэффициент корреляции Пирсона: {north_data['mortality'].corr(north_data['hardness'])}")

# Расчёт корреляции Спирмена
cof, _ = st.spearmanr(north_data['mortality'], north_data['hardness'])
print(f'Коэффициент корреляции Спирмена: {cof}')

print('\nНа основе анализа коэф. корреляции можем сделать следующие выводы:'
      '\nОценки коэф. жёсткости воды демонстрируют слабую отрицательную корреляцию со средней годовой смертностью. ')

# Построение модели линейной регрессии
# https://www.codecamp.ru/blog/linear-regression-python/

model = ols('hardness ~ mortality', data=north_data).fit()

print('\nМодель линейной регрессии: ')
print(model.summary())

# Расчёт коэффициента детерминации
print(f'\nКоэффициент детерминации: {model.rsquared * 100}')
print('Итак, {res:.1f}% смертей обусловлено жёсткостью воды.\n'.format(res=model.rsquared * 100))

# Вывод графика остатков
fig = plt.figure(figsize=(15, 7))
fig = sm.graphics.plot_regress_exog(model, 'mortality', fig=fig)

plt.show()

# Статистический анализ южных городов
print('\n--------------------------------------------------'
      '\n|Статистический анализ данных по южным городам|'
      '\n--------------------------------------------------')
south_data = data.loc[data['location'] == 'South']

# Построение точечного графика
south_data.pivot_table(index='hardness', values='mortality').plot(grid=True,
                                                               figsize=(20, 10))
plt.title('Изменение кол-ва смертей в зависимости от коэф. жёсткости воды\nДля южных городов')
plt.xlabel('Коэф. жёсткости воды')
plt.ylabel('Средняя годовая смертность')
plt.show()

# Расчёт корреляции Пирсона
print('\nКорреляция жёсткости воды и средней годовой смертностью:')
print(f"\nКоэффициент корреляции Пирсона: {south_data['mortality'].corr(south_data['hardness'])}")

# Расчёт корреляции Спирмена
cof, _ = st.spearmanr(south_data['mortality'], south_data['hardness'])
print(f'Коэффициент корреляции Спирмена: {cof}')

print('\nНа основе анализа коэф. корреляции можем сделать следующие выводы:'
      '\nОценки коэф. жёсткости воды демонстрируют слабую отрицательную корреляцию со средней годовой смертностью. ')

# Построение модели линейной регрессии
# https://www.codecamp.ru/blog/linear-regression-python/

model = ols('hardness ~ mortality', data=south_data).fit()

print('\nМодель линейной регрессии: ')
print(model.summary())

# Расчёт коэффициента детерминации
print(f'\nКоэффициент детерминации: {model.rsquared * 100}')
print('Итак, {res:.1f}% смертей обусловлено жёсткостью воды.\n'.format(res=model.rsquared * 100))

# Вывод графика остатков
fig = plt.figure(figsize=(15, 7))
fig = sm.graphics.plot_regress_exog(model, 'mortality', fig=fig)

plt.show()
