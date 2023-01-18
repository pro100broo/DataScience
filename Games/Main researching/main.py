import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt

# Загрузка данных из файла в датасет
data = pd.read_csv('games.csv', sep=',')

# Приведение названий столбцов к нижнему регистру

data.columns = data.columns.str.lower()
# Вывод типа данных столбцов
print('\nТипы данных столбцов:')
for column in data.columns:
    print(column, data[column].dtype)

# Вывод пропусков
print('\nПропуски:')
for column in data.columns:
    if data[column].isna().sum() > 0:
        print(column, data[column].isna().sum())
'''
Аббревиатура TBD означает то, что игра ещё не вышла, поэтому пользовательских оценок ещё нет.
'''

'''
Строки с пропусками данных в столбцах с годом выпуска и именем платформы удаляем, т.к. нельзя
придумать достойную замену. Как вы и сказали, заглушка в данном случае неоправдана.
'''
# Обработка столбца с пользовательскими оценками
# Замена строки 'tbd' на nan, для того, чтобы перевести тип данных столбца в вещественный формат
data['user_score'] = data['user_score'].replace('tbd', np.NaN)
data['user_score'] = data['user_score'].astype(float)

'''
Пропуски с датой выхода и названием игры 
Строки с пропусками данных в столбцах с годом выпуска и именем платформы удаляем, т.к. нельзя
придумать достойную замену.
'''
data = data.dropna(subset=['year_of_release'])
data = data.dropna(subset=['name'])

# Переводим тип данных в целочисленный вид - вещественного обозначения года не может быть
data['year_of_release'] = data['year_of_release'].astype(int)

# Пустоты в столбце рейтинга не можем оставить пустыми, поэтому меняем пропуски на заглушку
data['rating'] = data['rating'].fillna('No rating')

# Подсчёт суммарных продаж по всем регионам
data['summary_sales'] = data[['na_sales', 'eu_sales', 'jp_sales', 'other_sales']].sum(axis='columns')

# Поиск дубликатов
dupl = data.duplicated(subset=['name', 'platform'])
'''
Было найдено только несколько НЕЯВНЫХ дубликатов. В данном контексте мы не имеем право их удалить, т.к.
в столбце 'name' повторяется только название серии игры. Соответственно, разные части одной серии считаем
за разные игры
'''

# Удалим игры, вышедшие в один год, но на разных платформах, для более точной статистики
unique_games = data.drop_duplicates(subset=['name', 'year_of_release'])
unique_games.groupby('year_of_release').agg({'name': 'count'}).plot(
    grid=True,
    ylabel='Проектов выпущено',
    xlabel='Год',
    legend=False,
    figsize=(20, 10)
)
plt.title('Колличество выпущенных игр в разные периоды времени')
plt.show()

'''
На графике видно постепенное увеличение выпускаемых в год проектов , начиная с 90-х. Примерно в это
время начала активно развиваться IT сфера. Появлялось множество новых платформ, выходили улучшенные версии
старых. Игровая индустрия в принципе активно развивалась, чем и обуславливается столь быстрый рост.
Ближе к 2010 году игры достигли определённой планки, после которой,
 выпускать более масштабные и качественные проекты
стало сложнее и дороже. В целом, возросла требовательность пользователей к играм. 
Поэтому число новых проектов резко пошло на спад.
'''

# Смотрим, как меняются данные по платформам.
# Фильтруем датасет по 5 платформам с самыми большими продажами
top_5_platforms = data.pivot_table(index='platform', values='summary_sales', aggfunc='sum')\
    .sort_values('summary_sales', ascending=False).index[:5].to_list()

# Строим распределние по годам
filtered = data[data['platform'].isin(top_5_platforms)]
filtered.pivot_table(index='year_of_release', columns='platform', aggfunc='size')\
    .plot(grid=True,
          figsize=(20, 10),
          ylabel='Выпущено проектов на данной платформе',
          xlabel='Год')
plt.title('Распределение популярности платформ по годам')
plt.show()
'''
На графике распределния видно, что цикл популярности именно современных платформ составляет около 10 лет.
ПОПУЛЯРНЫЕ платформы, выпущенные в более ранние периоды (до 2000-х) 'живут' немного дольше, порядка 10-12 лет
'''
# Выбираем промежуток с 2014 по 2016 год
new_data = data.loc[(data['year_of_release'] >= 2014) & (data['year_of_release'] <= 2016)]

# Строим график по глобальным продажам игр в разбивке по платформам за выбранный период
# Фильтруем датасет по нужным параметрам
sales_filtered = new_data[['platform', 'summary_sales', 'year_of_release']]

# Создаём сводную таблицу из полученного датасета
pivot = sales_filtered.pivot_table(
    index='year_of_release',
    columns='platform',
    values='summary_sales',
    aggfunc='size'
)

# Строим сам график
pivot.plot(grid=True, figsize=(20, 10), ylabel='Число проданных копий, млн.шт.', xlabel='Год', legend='left')
plt.legend(loc='upper left')
plt.title('Распределение колличества выпущенных проектов для всех платформ по годам')
plt.show()

'''
Явно лидирующая по продажам платформа: PS4
Падают по продажам: PSV, X360, 3DS, PS3, Wii, PSP, WiiU
Растут по продажам: PS4, PC, XOne
Потенциально прибыльная платформа: PS4
'''
pivot.plot.box(figsize=(20, 10))
plt.title('Диаграмма размаха\n для колличества выпущенных проектов, для всех платформ по годам')
plt.grid(axis='y')
plt.xlabel('Платформа')
plt.ylabel('Число проданных копий, млн.шт.')
plt.show()

'''
Итак, после выбора правильного временного отрезка, диаграмма размаха стала читабельной
Рассмотрим сначала платформы: PC, PSP, Wii
Данные платформы имеют короткие ящики, что говорит о том, что разброс по продажам максимально мал.
В случае с PSP и Wii, видим, что медиана средних продаж находится в пределах 20 млн. копий, что 
значительно меньше, чем у других платформ. Исходя из того, что средний разброс продаж стабильно
держиться на низком уровне, можно подтвердить, что платформы теряют популярность. В случае с PC,
Медиана лежит примерно в одной группе с популярными платформами. Исходя из того, что коробка маленькая,
можно сделать вывод о том, что эта платформа притерпевает слабый рост.
Можно выделить группу теряющих популярность платформ в правой нижней части графика: PSP, Wii, WiiU, X360
У платформы 3Ds большая часть коробки, как и нижний ус находится ниже медианы продаж, что так же говорит
о снижении популярности.
Очевидно, самая популярная платформа - PS4.

'''
# Выводим самую популярную платформу за наш период
# Фильтруем датасет по самой популярной платформе.
top_1_platform = new_data.groupby(['platform']).agg({'name': 'count'})\
      .sort_values('name', ascending=False).index[:1].to_list()
popularity_filtered = new_data.loc[new_data['platform'].isin(top_1_platform)]

# Строим диаграмму рассеяния
# Для отзывов игроков
plt.figure(figsize=(20, 10))
plt.scatter(popularity_filtered['user_score'], popularity_filtered['summary_sales'])
plt.title('Зависимость числа продаж\n от оценок игроков')
plt.xlabel('Оценки игроков')
plt.ylabel('Продано копий, млн.шт.')
plt.grid()
plt.tick_params(axis='y', which='major', labelsize=5)
plt.show()

# Для отзывов критиков
plt.figure(figsize=(20, 10))
plt.scatter(popularity_filtered['critic_score'], popularity_filtered['summary_sales'])
plt.title('Зависимость числа продаж\n от оценок критиков')
plt.xlabel('Оценки критиков')
plt.ylabel('Продано копий, млн.шт.')
plt.grid()
plt.tick_params(axis='y', which='major', labelsize=5)
plt.show()

# Расчёт корреляции
print('\nКорреляция общего числа продаж от отзывов игроков')
print(popularity_filtered['user_score'].corr(popularity_filtered['summary_sales']))
print('\nКорреляция общего числа продаж от отзывов критиков')
print(popularity_filtered['critic_score'].corr(popularity_filtered['summary_sales']))
'''
Итак, на основе коэф. корреляции можем сделать следующие выводы:
Оценки критиков демонстрируют слабую положительную корреляцию с "цифрами" продаж. 
Оценки пользователей корреляции с продажами практически не имеют
'''

# Проверим другие платформы
print('\nКорреляция для платформы: PS3')
print(new_data.loc[new_data['platform'] == 'PS3']['user_score']\
      .corr(new_data.loc[new_data['platform'] == 'PS3']['summary_sales']))
print(new_data.loc[new_data['platform'] == 'PS3']['critic_score']\
      .corr(new_data.loc[new_data['platform'] == 'PS3']['summary_sales']))
print('\nКорреляция для платформы: PC')
print(new_data.loc[new_data['platform'] == 'PC']['user_score']\
      .corr(new_data.loc[new_data['platform'] == 'PC']['summary_sales']))
print(new_data.loc[new_data['platform'] == 'PC']['critic_score']\
      .corr(new_data.loc[new_data['platform'] == 'PC']['summary_sales']))
'''
Видно, что для других популярных платформ закономерность сохраняется
'''

# Строим распределние игр по жанрам
genre_filtered = new_data.groupby('genre').agg({'summary_sales': 'mean'}).plot.bar(rot=20, figsize=(20, 10))
plt.tick_params(axis='x', which='major', labelsize=8)
plt.title('Распределение числа выпущенных игр по жаграм')
plt.xlabel('Жанр')
plt.ylabel('Продано копий, млн.шт.')
plt.grid(axis='y')
plt.show()
'''
Жанры с высокими продажами, относительно остальных: Fighting Platfirm, Sports и Shooter
Самый прибыльный жанр - Shooter
Жанры с низкими продажами: Strategy, Puzzle, Adventure
'''

# Портреты пользователей по платформам
na_platforms = new_data.groupby('platform').agg({'na_sales': 'sum'})\
    .sort_values('na_sales', ascending=False).head(5)
eu_platforms = new_data.groupby('platform').agg({'eu_sales': 'sum'})\
    .sort_values('eu_sales', ascending=False).head(5)
jp_platforms = new_data.groupby('platform').agg({'jp_sales': 'sum'})\
    .sort_values('jp_sales', ascending=False).head(5)

print(na_platforms, '\n')
print(eu_platforms, '\n')
print(jp_platforms, '\n')
'''
Различия в долях продаж обусловлены, прежде всего, курсом валюты, территорией региона и запросам пользователей.
Видно, что в штатах больше людей было готово отдать больше средств на покупку дорогого xbox.
В то же время, в Японии предпочитали игровые приставки, которые  стоили меньше,
но обладали большей портативностью.
'''

# Портреты пользователей по жанрам
na_genre = new_data.groupby('genre').agg({'na_sales': 'sum'})\
    .sort_values('na_sales', ascending=False).head(5)
eu_genre = new_data.groupby('genre').agg({'eu_sales': 'sum'})\
    .sort_values('eu_sales', ascending=False).head(5)
jp_genre = new_data.groupby('genre').agg({'jp_sales': 'sum'})\
    .sort_values('jp_sales', ascending=False).head(5)

print(na_genre, '\n')
print(eu_genre, '\n')
print(jp_genre, '\n')
'''
Видим, что популярнын жанры в штатах и Европе парктически совпадают, однако, в японском регионе наблюдается
некоторое их смешение, при отсутствии шутеров. Это показывает нам отличие восточного рынка от западного, что
может быть связанно с некоторыми особенностями. Например, менталитетом и культурой пользователей.
'''

# Влияние игрового рейтинга на продажи по регионам
# Для NA - региона
na_rating = new_data[['na_sales', 'rating']]
na_rating.groupby('rating').na_sales.nunique().to_frame('Число проданных копий, млн.шт.')\
    .plot.bar(rot=20, figsize=(20, 10))
plt.title('Продажи в NA регионе')
plt.xlabel('Игровой рейтинг')
plt.ylabel('Продано копий, млн.шт.')
plt.grid(axis='y')

# Для EU - региона
eu_rating = new_data[['eu_sales', 'rating']]
eu_rating.groupby('rating').eu_sales.nunique().to_frame('Число проданных копий, млн.шт.')\
    .plot.bar(rot=20, figsize=(20, 10))
plt.title('Продажи в EU регионе')
plt.xlabel('Игровой рейтинг')
plt.ylabel('Продано копий, млн.шт.')
plt.grid(axis='y')

# Для JP - региона
jp_rating = new_data[['jp_sales', 'rating']]
jp_rating.groupby('rating').jp_sales.nunique().to_frame('Число проданных копий, млн.шт.')\
    .plot.bar(rot=20, figsize=(20, 10))
plt.title('Продажи в JP регионе')
plt.xlabel('Игровой рейтинг')
plt.ylabel('Продано копий, млн.шт.')
plt.grid(axis='y')
plt.show()
'''
Влияние рейтинга на продажи во всех регионах примерно одинаково. 
В NA и EU - самый популярный жанр - M, средние продажи - E, M, низкие продажи E10+
В JP - T, средние продажи - E, M, низкие продажи E10+
'''

# Проверка гипотез. В обоих случаях будет выбран уровень значимости: α = 0.05
'''
Проверка гипотезы №1: 'Средние пользовательские рейтинги платформ Xbox One и PC одинаковые'
Нулевая гипотеза H0: Средние пользовательские рейтинги платформ Xbox One и PC одинаковые
Альтернативная гипотеза H1: Средние пользовательские рейтинги платформ Xbox One и PC разные
'''
without_nan = new_data.dropna()
sample_XOne = without_nan['user_score'].loc[without_nan['platform'] == 'XOne']
sample_PC = without_nan['user_score'].loc[without_nan['platform'] == 'PC']
platform_result = scipy.stats.ttest_ind(sample_XOne, sample_PC)
print('p-значение гипотезы №1:', platform_result.pvalue)
'''
Видим, что уровень значимости, полученный в результате теста, значительно меньше заданного
Следовательно, мы имеем достаточно оснований, чтобы ОПРОВЕРГНУТЬ НУЛЕВУЮ гипотезу
Итак, Средние пользовательские рейтинги платформ Xbox One и PC разные
'''
'''
Проверка гипотезы №2: 'Средние пользовательские рейтинги жанров Action и Sports разные'
Нулевая гипотеза H0: Средние пользовательские рейтинги жанров Action и Sports разные
Альтернативная гипотеза H1: Средние пользовательские рейтинги жанров Action и Sports одинаковые
'''
sample_Action = without_nan['user_score'].loc[without_nan['genre'] == 'Action']
sample_Sports = without_nan['user_score'].loc[without_nan['genre'] == 'Sports']
platform_result = scipy.stats.ttest_ind(sample_Action, sample_Sports)
print('p-значение гипотезы №2:', platform_result.pvalue)
'''
Видим, что уровень значимости, полученный в результате теста, значительно меньше заданного
Следовательно, мы имеем достаточно оснований, чтобы ОПРОВЕРГНУТЬ НУЛЕВУЮ гипотезу
Итак, Средние пользовательские рейтинги платформ Xbox One и PC разные
'''
'''
Нулевая гипотеза формируется в соответствии с тезисом, который мы должны проверить.
Альтернативная гипотеза формируется в противовес к нулевой, то есть имеет противоположное значение.
Это нужно для того, чтобы подтвердить или опровергнуть нулевую гипотезу, т.е. исходный тезис.
Для проверки гипотез был использован критерий о равенстве средних двух генеральных
совокупностей, т.к. в обоих случаях, мы имели дело с двумя большими выборками, взятыми для разных наборов
данных из одного периода (выбранного в предыдущих шагах на основе рапсределения).
'''
'''
Финальный вывод
Прогноз на 2017 год:
Большую часть бюджета на разработку игр стоит выделить на создание консольных игр для: PS4 и XOne.
Из них большее внимание уделить PS4
Оставшуюся часть бюджета выделить на разработку игр для PC, как для переспективной платформы в будущем
Стоит контролировать разработку игр на каждом этапе производства, тщательно работать над деталями проектов,
чтобы получить высокие оценки критиков
Выпус продуктов рекомендуется осуществлять следующим образом:
Для европейского и американского регионов: Shooter, Action, Sports - рейтинга 'M' 
Основное внимание сосредоточить на играх жанра Shooter
Для японского региона: Action, R-P - рейтинга 'T'
'''









