import pandas as pd

# Импортируйте библиотеку pandas и откройте с её помощью файл data_1_7.csv. Изучите названия признаков.
data = pd.read_csv('data.csv', sep=',')

# Выведите на экран количество строк и столбцов в полученной таблице
print(f'Число строк: {len(data.index)}, число столбцов: {len(data.columns)}')

# Изучите типы данных, используемые в таблицы и узнайте, где данные отсутствуют
for column in data.columns:
    print(f'Тип данных в столбце {column}: {data[column].dtype}')

# Пропуски
for column in data.columns:
    print(f'Тип пропусков в столбце {column}: {data[column].isna().sum()}')

# Выведите первые 10 строк таблицы
print(data.head(10))

# Выведите последние 5 строк таблицы
print(data.tail())

# Создайте новый столбец "Name Award" в котором будут находиться название и статус награды фильма разделенные пробелом.

# Для фильма с названием "FilmName" и статусом "Winner" должно выйти "FilmName Winner"
data['Name Award'] = data['Film'] + ' ' + data['Award']

# Узнайте, сколько различных (уникальных) значений содержится столбце "Award"
print(len(data['Award'].unique()))

# Выясните, сколько фильмов было выпущено в 1992 году?
print(data['Year of Release'].loc[data['Year of Release'] == 1992].count())

# Среди этих фильмов оставьте те, у которых рейтинг не меньше 8
print(data['Year of Release'].loc[(data['Year of Release'] == 1992) & (data['Audience Rating'] >= 8)].count())

# Среди оставшихся фильмов найдите тот, который не выигрывал премию Оскар
print(
    data['Year of Release'].loc[
        (data['Year of Release'] == 1992) &
        (data['Audience Rating'] >= 8) &
        (data['Award'] == 'Winner')
    ].count()
)

# Среди всех фильмов выведите те, которые были сняты в период между 1992 и 2000 годом
print(data['Year of Release'].loc[(data['Year of Release'] > 1922) & (data['Year of Release'] > 2000)].count())

# В отдельную переменную сохраните часть таблицы, для которой отсутствует информация в столбце "Movie Info"
filtered = data[data.index.isin([index for index, note in enumerate(data['Movie Info']) if type(note) != str])]

# Получите новый датасет, который получается из старого путём выбрасывания всех строк, в которых значение "Movie Info" отсутствует
data = data.loc[data['Movie Info'] != 'No info']

# Отсортируйте полученный датасет по значению столбца Audience Rating
data = data.sort_values('Audience Rating', ascending=False)
print(data['Audience Rating'])

# Выберите фильм, которого нет в списке. Добавьте в таблицу строку, описывающую ваш фильм. Не обязательно писать точные значения параметров. Может выдумать их
print('Фильм уже есть в списке' if 'укпаафдтваф' in data['Film'].unique() else 'Фильма нет в списке')

# Создайте две таблицы, в первую поместите 5 фильмов с лучшим пользовательским рейтингом, а во вторую 5 с худшим. Объедините эти две таблицы в одну.
best_rating = data.head()
worst_rating = data.tail()
new_data = pd.concat([best_rating, worst_rating])

# С помощью функции groupby() вычислите средние рейтинги фильмов, которые получали награду оскар и тех, которые нет
print(data.groupby('Award').agg({'Audience Rating': 'mean'}))

# С помощью функции groupby вычислите максимальные и минимальные рейтинги среди фильмов с оскаром и без
print(data.groupby('Award').agg({'Audience Rating': 'max'}))
print(data.groupby('Award').agg({'Audience Rating': 'min'}))

# Вычислите, сколько всего фильмов выиграли Оскар и какая у них доля в датасете
print(len(data.loc[data['Award'] == 'Winner']) / len(data))

# Выведите корреляцию между числовыми признаками в таблице
print(data[[
          'Year of Release',
          'Movie Time',
          'IMDB Rating',
          'Tomatometer Rating',
          'Tomatometer Count',
          'Audience Rating',
          'Audience Count',
          'Tomatometer Top Critics Count',
          'Tomatometer Fresh Critics Count',
          'Tomatometer Rotten Critics Count'
      ]].corr())

# Выясните, для каких фильмов в таблице есть сразу несколько строк
print(data[data.duplicated('Film')])

# Выясните, у каких фильмов парный год номинации, например, 1927/28. Уберите вторую дату. Для примера получится 1927
for index, text in enumerate(data['Oscar Year']):
    data.loc[index, 'Oscar Year'] = text[0:4]

# В датасете есть столбец года проведения церемонии Оскар. Добавьте к году дату - 25 апреля. Итоговый столбец должен иметь календарный тип данных.
for index, text in enumerate(data['Oscar Year']):
    data.loc[index, 'Oscar Year'] += '-04-25'

print(data['Oscar Year'].dtype)
data['Oscar Year'] = pd.to_datetime(data['Oscar Year'])
print(data['Oscar Year'].dtype)
print(data['Oscar Year'].dt.weekday)

# Выведите три компании (столбец Production Company), фильмы которых завоевали самое большое количество наград
filtered_data = data.loc[data['Award'] == 'Winner']
filtered_data = filtered_data.groupby('Production Company').agg({'Award': 'count'}).sort_values('Award', ascending=False)
print(filtered_data.head(3))






