import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as st
import warnings

from categorize import vine_to_color, country_to_continent

# Шаг1: Предобработка данных

warnings.simplefilter(action='ignore', category=FutureWarning)

# Загружаем датасет
not_filtered_data = pd.read_csv('wine_data.csv', sep=',')
# Выводим общую информацию
not_filtered_data.info()

# Проверяем датасет на наличие пропусков в данных
colours = ['#993366', '#FFFF00']
plt.figure(figsize=(20, 10))
sns.heatmap(not_filtered_data.isnull(), cmap=sns.color_palette(colours))

# Настраиваем график
plt.title('Матрица пропущенных значений набора данных', fontsize=14)
plt.xticks(fontsize=8, rotation=45)
plt.yticks(fontsize=8)
plt.figtext(0.5, -0.2, "Рисунок 1. - Матрица пропущенных значений набора данных")
plt.show()

# Удаляем столбец, содержащий номера строк
not_filtered_data = not_filtered_data.drop(columns=['Unnamed: 0'], axis=1)

# Названия столбцов не  трогаем, т.к. они уже нижнего регистра
# Типы данных тоже менять не будем, т.к. наполнение кажждого столбца соответствует текущему типу данных в нём
# Выводим конкретные цифры по пропускам в столбцах
print('\nПропуски:')
for column in not_filtered_data.columns:
    if not_filtered_data[column].isna().sum() > 0:
        print(column, not_filtered_data[column].isna().sum())

# Видим по 5 пропусков в столбцах country и province. Находятся они в одинаковых строках.
# Видим приличное число пропусков в столбце price. В дальнейшем nan может помешать. К примеру при проверке гипотез
# или при построении линейной регрессии
# Так как мы можем удалить до 10% строк от объема датасета, можем удалить строки, описанные выше.
# Создаём новый датасет, в котором будет произведено удаление/фильтрация информации, чтобы всегда иметь доступ
# к начальному датасету
# Удаляем явные дубликаты:
data = not_filtered_data.drop_duplicates(keep=False)
# Удаляем пропуски
data = data.dropna(subset=['country', 'price'])
# В столбце price видим несколько аномально больших значений. От них тоже избавимся, т.к. в дальнейшем
# столь большие числа помешают нам сделать правильные статистические выводы.
data = data.loc[data['price'] < 300]
# Контролируем общий объём удалённой информации:
print(f'\nБыло удалено: {round(100 - (data.shape[0] / not_filtered_data.shape[0]) * 100)}% данных')
# Заполним пропуски в столбцах со строковым типом данных 'заглушкой'
data[['region_2', 'region_1', 'designation']] = data[['region_2', 'region_1', 'designation']].fillna('No info')

# Добавляем столбец с регионами
data['region'] = data['country'].map(country_to_continent)

# Шаг2: Исследовательский анализ данных

# Выводим 5 самых популярных сортов в каждом регионе.
print('\nСамые популярные сорта вин по регионам: ')
for region in data['region'].unique().tolist():
    print('\n', data[data['region'] == region].groupby(['region', 'variety']).agg({'points': 'max'}) \
          .sort_values('points', ascending=False).head(5))

# Находим 5 самых дорогих сортов вина.
max_price_filtered = data.groupby('variety').agg({'price': 'max'}).sort_values('price', ascending=False)
top_5_price = max_price_filtered.index[:5].to_list()
# Выводим среднюю цену вин по регионам:
print('\nСредняя цена самых дорогих сортов вина по регионам: ')
for region in data['region'].unique().tolist():
    print('\nРегион: ', region)
    filtered_top_5 = data[(data['region'] == region) & data['variety'].isin(top_5_price)]
    print(filtered_top_5.groupby('variety').agg({'price': 'mean'}).sort_values('price', ascending=False))

# Потолком бюджетной ценовой категории был выбран порог в 10$
budget_filtered = data[data['price'] < 10]
print('\nСамые популяные сорта вин в бюджетном сегменте: ')
print(budget_filtered.groupby('variety').agg({'points': 'max'}).sort_values('points', ascending=False).head(10))

# Выводим лидирующие сорта вин по рейтингу
print('\nЛидирующие сорта вин по рейтингу: ')
print(data.groupby('variety').agg({'points': 'max'}).sort_values('points', ascending=False).head(5))

# Строим диаграмму размаха (график ящик с усами) по странам
data.plot.box(by='country', column='points', figsize=(20, 10))
plt.title('Диаграмма размаха\n для рейтинга вина по странам')
plt.grid(axis='y')
plt.xlabel('Страна')
plt.ylabel('Рейтинг журнала Wine Enthusiast')
plt.tick_params(axis='x', labelrotation=20, labelsize=5)
plt.show()

# Строим диаграмму размаха (график ящик с усами) по сортам винограда
top10_variety = data.groupby('variety').agg({'points': 'max'}).sort_values('points', ascending=False).head(10)
top10_variety = top10_variety.index.to_list()
variety_sorted = data[data['variety'].isin(top10_variety)]
variety_sorted.plot.box(by='variety', column='points', figsize=(20, 12))
plt.title('Диаграмма размаха\n для рейтинга вина по сортам винограда')
plt.grid(axis='y')
plt.xlabel('Сорт винограда')
plt.ylabel('Рейтинг журнала Wine Enthusiast')
plt.tick_params(axis='x', labelrotation=20, labelsize=8)
plt.show()

# Выявляем закономерность влияния рейтинга вина на его цену
# Строим диаграмму рассеяния
fig = plt.figure(figsize=(20, 10))
ax = fig.add_subplot()
plt.scatter(data['points'], data['price'])
ax.xaxis.set_major_locator(ticker.FixedLocator([x for x in range(80, 101, 1)]))
plt.title('Зависимость общей стоимости вина\n от рейтинга')
plt.xlabel('Рейтинг журнала Wine Enthusiast')
plt.ylabel('Общая стоимость вина')
plt.grid()
plt.tick_params(axis='y', which='major')
plt.show()
# Считаем корреляцию
print('\nКорреляция общей стоимости вина от рейтинга')
print(data['price'].corr(data['points']))

'''
Выводы раздела 2:
1. Список популярных вин незначительно меняется в зависимости от региона.
Это может быть связано с разными климатическими условиями, в которых произрастает виноград разных сортов. 
Видим, что в Латинской Америке, Азии и Африке максимальные оценки ниже, 
чем в остальных регионах, а в Европе, Океании и Северной Америке средний показатель практически равен 99.
Эти данные могу сказать, к примеру, что лучшее вино производят в Европе, Америке и Океании.
2. Средняя цена самых дорогих вин в регионах варьируется в пределах 15-65$. 
В независимости от региона, марка вин 'Bordeaux-style Red Blend' держиться в топе цен.
3. Самые популярные марки вин в бюджетном сегменте:
Sauvignon Blanc, Fumé Blanc, Riesling, Portuguese Red , Tempranillo
Можно отметить, что рейтнг топовых бюджетных вин не привышает 91 балла, что может сказать о их среднем качестве
4. Лидирующие по рейтингам вина:
Cabernet Sauvigno , Pinot Noir , Sangiovese, Red Blend, Nebbiolo 
5. При категоризации по странам:
   Средний размер ящика составляет порядка 4-5 баллов рейтинга.
   В целом, среднее значение у большинства ящиков сбалансированно.
   Большая часть ящиков группируется в пределах 82-90 баллов.
   У ящиков, преимущественно, европейских стран наблюдается большое число аномальных выбросов.
   Самый большой рейтинг у вин наблюдается в Аглии и Австрии.
   Самый низкий рейтинг - в Украине и Азиатских странах (Китай, Северная Корея)
6. Оценки журнала Wine Enthusiast демонстрируют слабую положительную корреляцию с общей стоимостью вина. 
Коэф. корреляции: 0.5234145575309755
'''
# Шаг3: Составление структуры развития рынка вина по регионам
# Находим самые популярные сорта по регионам
# Вычислим корреляцию рейтинга с общей стоимостью вина для каждого региона
print('\nСамые популярные сорта вин по регионам: ')
for region in data['region'].unique().tolist():
    print('\n', data[data['region'] == region].groupby(['region', 'variety']).agg({'points': 'max'}) \
          .sort_values('points', ascending=False).head(5))
    filtered_region = data[data['region'] == region]
    print(f'Корреляция для региона: {region}: ', filtered_region['price'].corr(filtered_region['points']))

'''
Вывод раздела 3:
В каждом регионе, оценки журнала Wine Enthusiast демонстрируют слабую положительную корреляцию с общей стоимостью вина.
Если сравнивать регионы между собой, то в Европе наблюдается наибольший коэф. корреляции, а в Азиатском наименьший.
Отсюда можно сделать вывод, что именно в Европе наибольшее влияние на цену оказывают оценки критиков.
'''
# Шаг4: Исследование статистических показателей зависимости цены вина от рейтинга в регионе.
# Строим линейную регрессию зависимости между ценой продукта и его рейтингом.
for region in data['region'].unique().tolist():
    # Наборы наших значений для построение диаграммы рассеяния
    x = data['points'].loc[data['region'] == region]
    y = data['price'].loc[(data['region'] == region)]

    # Получаем необхожимые значения для построения линии линейной регресии
    (slope, intercept, rvalue, pvalue, stderr) = st.linregress(x, y)

    # Построение диаграммы рассеяния
    plt.figure(figsize=(20, 10))
    plt.scatter(x, y, color="red", marker="o", label="Original data")

    # Построение линии линейной регрессии
    regr_line_points = [intercept + slope * point for point in x]
    plt.plot(x, regr_line_points, color="green", label="Fitted line")

    plt.title(f'Линейная регрессия для региона: {region}')
    plt.xlabel('Рейтинг журнала Wine Enthusias')
    plt.ylabel('Общая стоимость вина')
    plt.show()
'''
Вывод раздела 4:

Во всех регионах наблюдаем сильное отклонение стоимости от предполагаемой нормы. Это подтверждает то, что
общая стоимость вина слабо коррелирует с рейтингом
'''
# Шаг5: Проверка гипотез. В обоих случаях будет выбран уровень значимости: α = 0.05
# Для проерки гипотезы №1, создадим новый столбец с фильтрацией по цвету вина
data['color'] = data['variety'].map(vine_to_color)
p_value = 0.05

print('\nНулевая гипотеза формируется в соответствии с тезисом, который мы должны проверить.'
      '\nАльтернативная гипотеза формируется в противовес к нулевой, то есть имеет противоположное значение.'
      '\nЭто нужно для того, чтобы подтвердить или опровергнуть нулевую гипотезу, т.е. исходный тезис.'
      '\nДля проверки гипотез был использован критерий о равенстве средних двух генеральных'
      '\nсовокупностей, т.к. в обоих случаях, мы имели дело с двумя большими выборками, взятыми для разных наборов'
      '\nданных из одного временного периода.')


print('\nПроверка гипотезы №1: Средние пользовательские рейтинги красного и белого вина одинаковые'
      '\nНулевая гипотеза H0: Средние пользовательские рейтинги красного и белого вина одинаковые'
      '\nАльтернативная гипотеза H1: Средние пользовательские рейтинги красного и белого вина разные')

without_nan = data.dropna()
sample_points_white = without_nan['points'].loc[without_nan['color'] == 'white']
sample_points_red = without_nan['points'].loc[without_nan['color'] == 'red']
result = st.ttest_ind(sample_points_white, sample_points_red)
print('p-значение гипотезы №1:', result.pvalue)
if result.pvalue > p_value:
    print('\nВидим, что уровень значимости, полученный в результате теста, выше заданного'
          '\nСледовательно, мы имеем достаточно оснований, чтобы ПОДТВЕРДИТЬ НУЛЕВУЮ гипотезу'
          '\nИтак, cредние пользовательские рейтинги красного и белого вина одинаковые')
else:
    print('\nВидим, что уровень значимости, полученный в результате теста, меньше заданного'
          '\nСледовательно, мы имеем достаточно оснований, чтобы ОПРОВЕРГНУТЬ НУЛЕВУЮ гипотезу'
          '\nИтак, cредние пользовательские рейтинги красного и белого вина разные')

print('\nПроверка гипотезы №2: Средние цены двух популярных сортов вина одинаковые'
      '\nНулевая гипотеза H0: Средние цены двух популярных сортов вина одинаковые'
      '\nАльтернативная гипотеза H1: Средние цены двух популярных сортов вина разные')

vines = data.groupby('variety').agg({'points': 'max'}).sort_values('points', ascending=False).index[:2].to_list()

sample_first_vine = data['price'].loc[data['variety'] == vines[0]]
sample_second_vine = data['price'].loc[data['variety'] == vines[1]]
result = st.ttest_ind(sample_first_vine, sample_second_vine)
print('p-значение гипотезы №2:', result.pvalue)
if result.pvalue > p_value:
    print('\nВидим, что уровень значимости, полученный в результате теста, выше заданного'
          '\nСледовательно, мы имеем достаточно оснований, чтобы ПОДТВЕРДИТЬ НУЛЕВУЮ гипотезу'
          '\nИтак, средние цены двух популярных сортов вина одинаковые')
else:
    print('\nВидим, что уровень значимости, полученный в результате теста, меньше заданного'
          '\nСледовательно, мы имеем достаточно оснований, чтобы ОПРОВЕРГНУТЬ НУЛЕВУЮ гипотезу'
          '\nИтак, средние цены двух популярных сортов вина разные')

'''
Финальный вывод:
Цель данного проекта — выявить, какие признаки имеют наибольшее влияние на рейтинг вина.
Итак, наибольшее влияние на рейтинг вина имеет сорт винограда и регион.
'''

