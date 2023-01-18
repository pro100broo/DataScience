import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# Загрузка данных из файла в датафрейм
data = pd.read_csv('data.csv', sep='\t')

# Вывод общей информации о датафрейме
print(data.info())

# Построение общей гистограммы, включающей данные каждого столбца
data.hist(figsize=(15, 20))
plt.show()

# Вывод столбцов с пропусками пропусков
for column in data.columns:
    if data[column].isna().sum() > 0:
        print(f'В столбце "{column}" обнаружено {data[column].isna().sum()} пропусков')

# Заполнение пропусков в некоторых столбцах на необходимые значения
data[['balcony', 'parks_around3000', 'ponds_around3000']] = \
    data[['balcony', 'parks_around3000', 'ponds_around3000']].fillna(0)
data['is_apartment'] = data['is_apartment'].fillna(False)
data['ceiling_height'] = data['ceiling_height'].fillna(data['ceiling_height'].mean())

'''
Самая распространённая причина пропусков в данных - человеческий фактор. Пользователь может умышленно
или случайно не указывать определённые данные. Алгоритм, формирующий датасет, по вине программиста 
может использовать, к примеру, непрафильный формат данных, что приведёт к некорректной обработке информации.
'''

# Вывод типа данных столбцов
for column in data.columns:
    print(f'Тип данных столбца "{column}": {data[column].dtype}.')

# Изменение типа данных некоторых столбцов
data['is_apartment'] = data['is_apartment'].astype(bool)
data['balcony'] = data['balcony'].astype(int)
data[['total_images', 'rooms', 'floor']] = data[['total_images', 'rooms', 'floor']].astype(float)
data['first_day_exposition'] = pd.to_datetime(data['first_day_exposition'])

# Изменение названия ячеек столбца, содержащих неявные дубликаты
for index in data.index:
    if type(data['locality_name'][index]) == str:
        data.loc[index, 'locality_name'] = \
            ' '.join([word for word in data['locality_name'][index].split() if not word.islower()])

'''
Тип данных столбца должен соответствовать находящейся в нём информации. Превентивное изменение типа 
упрощает дальнейшее взаимодействие с датасетом.
'''

# Удаление редких и выбивающихся значений
# Уменьшение точности чисел столбцов до сотых, десятых долей
data[['living_area', 'days_exposition']] = data[['living_area', 'days_exposition']].round(2)
data['ceiling_height'] = data['ceiling_height'].round(1)

# Приводим значения высот потолков к нормальному виду
for index in data.index:
    name = data['ceiling_height'][index]
    if type(name) == np.float64 and name > 10.0:
        while name > 10:
            name /= 10
        data.loc[index, 'ceiling_height'] = name

# Удаляем строки с аномально большой площадью кухни, большим (либо нулевым) числом комнат, большой высотой потолков
data = data.loc[
        (data['total_area'] < 200) & (data['rooms'].isin([1, 2, 3, 4, 5, 6])) & \
        (data['ceiling_height'] > 2) & (data['ceiling_height'] < 3.5) & \
        (data['last_price'] < 100000000) & (data['last_price'] > 1000000)
    ]
print(data)

'''
Особенности:
1. Числа с большой точностью там, где это не нужно
2. Аномально большая высота потолков
3. Аномально большое число комнат
4. Аномально большая площадь кухни
'''

# Добавляем новые столбцы в датафрейм
# Цена одного квадратного метра, с последующим округлением до сотых долей
data['price_per_meter'] = data['last_price'] / data['total_area']
data['price_per_meter'] = data['price_per_meter'].round(2)


# Функция возвращает численное представление дня недели, на основе datetime объекта
def format_days(date: datetime) -> int:
    return date.weekday()


# Столбцы с годом, месяцем и днём недели:
data['day_of_publication'] = data['first_day_exposition'].apply(format_days)
data['month_of_publication'] = data['first_day_exposition'].dt.month
data['year_of_publication'] = data['first_day_exposition'].dt.year

# Создание данных для столбца с характеристикой этажей
values_list = []
for index in data.index:
    if data['floors_total'][index] - data['floor'][index] == data['floors_total'][index] - 1:
        values_list.append('первый')
    elif data['floors_total'][index] - data['floor'][index] == 0:
        values_list.append('последний')
    else:
        values_list.append('другой')

# Столбец с типом этажа
data['floor_type'] = values_list

# Столбец расстояние до центра города (в km)
data['cityCenters_nearest_km'] = data['cityCenters_nearest'] // 1000

# Построение всех необходимых гистограмм
data['total_area'].hist(figsize=(20, 10))
plt.title('total_area')
plt.show()
data['living_area'].hist(figsize=(20, 10))
plt.title('living_area')
plt.show()
data['kitchen_area'].hist(figsize=(20, 10))
plt.title('kitchen_area')
plt.show()
data['last_price'].hist(figsize=(20, 10))
plt.title('last_price')
plt.show()
data['rooms'].hist(figsize=(20, 10))
plt.title('rooms')
plt.show()
data['ceiling_height'].hist(figsize=(20, 10))
plt.title('ceiling_height')
plt.show()
data['floor'].hist(figsize=(20, 10))
plt.title('floor')
plt.show()
data['floor_type'].hist(figsize=(20, 10))
plt.title('floor_type')
plt.show()
data['floors_total'].hist(figsize=(20, 10))
plt.title('floors_total')
plt.show()
data['cityCenters_nearest'].hist(figsize=(20, 10))
plt.title('cityCenters_nearest')
plt.show()
data['airports_nearest'].hist(figsize=(20, 10))
plt.title('airports_nearest')
plt.show()
data['parks_nearest'].hist(figsize=(20, 10))
plt.title('parks_nearest')
plt.show()
data['day_of_publication'].hist(figsize=(20, 10))
plt.title('day_of_publication')
plt.show()
data['month_of_publication'].hist(figsize=(20, 10))
plt.title('month_of_publication')
plt.show()

'''
Особенности:
1. Общая площадь:  Наибольшее число предложений в пределах 25-75 м^2
2. Жилая площадь: Кол-во практически совпадает с общей площадью. 
                  Делаем вывод, что чаще всего продают именно жилые помещения среднего сегмента
3. Площадь кухни: Самая распространённая площадь 4-13 м^2 
4. Общая стоимость: Самая распространённая цена в пределах 6 млн.руб.
5. Кол-во комнат: Самая распротсранённая планировка включает в себя 1, 2 или 3 команты
6. Высота потолков: Самая распространённая высота потолков 2,4-2,5 метра
7. Этаж: Чаще всего продают жильё на 1-4 этажах, что говорит о преимущественно малоэтажной застройке населённых пунктов
8. Тип этажа: Предложений по продаже жилья на первом и последнем этажах значительно меньше, чем на остальных
9. Тип этажа: Предложений по продаже жилья на первом и последнем этажах значительно меньше, чем на остальных
10.Расстояние до центра города: Наибольшее число предложений в пределах 8-20км до городского центра
11.Расстояние до аэропорта: Наибольшее число предложений в пределах 10-50км до ближайшего аэропорта
12.Расстояние до парка: Наибольшее число предложений в пределах 600м до парка
'''

data['days_exposition'].hist(figsize=(20, 10))
plt.title('days_exposition')
plt.show()

# Вывод среднего и медианного значения
print(f'Медиана: {data["days_exposition"].median()}, Среднее: {data["days_exposition"].mean()}')

'''
Средний срок продажи жилья - 3 месяца. Отсюда делаем вывод, что продажа считается быстрой, попадая в этот срок.
Долгим сроком продажи назовём период в несколько лет.
'''

# Строим графики зависимостей цены от указанных выличин
data.pivot_table(index='total_area', values='last_price').plot(
    grid=True,
    figsize=(20, 10),
    ylabel='Стоимость, млн.р',
    xlabel='Общая площадь, м^2',
    title='Зависимость цены жилья от общей площади'
)

data.pivot_table(index='living_area', values='last_price').plot(
    grid=True,
    figsize=(20, 10),
    ylabel='Стоимость, млн.р',
    xlabel='Жилая площадь, м^2',
    title='Зависимость цены жилья от жилой площади'
)

data.pivot_table(index='kitchen_area', values='last_price').plot(
    grid=True,
    figsize=(20, 10),
    ylabel='Стоимость, млн.р',
    xlabel='Площадь кухни, м^2',
    title='Зависимость цены жилья от площади кухни'
)

data.pivot_table(index='rooms', values='last_price').plot(
    grid=True,
    figsize=(20, 10),
    ylabel='Стоимость, млн.р',
    xlabel='Число комнат',
    title='Зависимость цены жилья от числа комнат'
)

data.groupby(['floor_type']).agg({'last_price': ['mean']}).sort_values('floor_type').plot(
    grid=True,
    figsize=(20, 10),
    ylabel='Стоимость, млн.р',
    xlabel='Расположение этажа',
    title='Зависимость цены жилья от типа этажа',
    legend=False
)

data.groupby(['day_of_publication']).agg({'last_price': ['mean']}).plot(
    grid=True,
    figsize=(20, 10),
    ylabel='Стоимость, млн.р',
    xlabel='День недели',
    title='Зависимость цены жилья от дня публикации',
    legend=False
)

data.groupby(['month_of_publication']).agg({'last_price': ['mean']}).plot(
    grid=True,
    figsize=(20, 10),
    ylabel='Стоимость, млн.р',
    xlabel='Месяц',
    title='Зависимость цены жилья от месяца публикации',
    legend=False
)

data.groupby(['year_of_publication']).agg({'last_price': ['mean']}).plot(
    grid=True,
    figsize=(20, 10),
    ylabel='Стоимость, млн.р',
    xlabel='Год',
    title='Зависимость цены жилья от года публикации',
    legend=False
)

plt.show()

print('\nКорреляция общей стоимости жилья от общей площади: ', data['last_price'].corr(data['total_area']))
print('Корреляция общей стоимости жилья от жилой площади: ', data['last_price'].corr(data['living_area']))
print('Корреляция общей стоимости жилья от площади кухни: ', data['last_price'].corr(data['kitchen_area']))
print('Корреляция общей стоимости жилья от количества комннат: ', data['last_price'].corr(data['rooms']))

'''
На общую стоимость жилья больше всего является параметр площади (общая, жилая, площадь кухни)
Также, влияет расположение квартиры в доме. Меньше всего платят за этажи, близкие к первому, либо последнему
'''

# Находим среднюю цену одного квадратного метра в 10 населённых пунктах с наибольшим числом объявлений
grouped_per_meter = data.groupby(['locality_name']).agg({'first_day_exposition': 'count', 'price_per_meter': 'mean'})
sorted_data = grouped_per_meter.sort_values('first_day_exposition', ascending=False).head(10)

# Вывод общей статистики по 10 городам
print('\nЦена одного квадратного метра в населённых пунктах с наибольшим числом объявлений:\n', sorted_data)

# Вывод максимума и минимума
print('\nНаибольшая стоимость жилья в городе Санкт-Петербург:\n', sorted_data.sort_values("price_per_meter", ascending=False))
print('\nНаименьшая стоимость жилья в городе Выборг:\n', sorted_data.sort_values("price_per_meter"))

# Находим среднюю цену каждого километра
grouped_per_distance = data[['last_price', 'cityCenters_nearest_km']].loc[data['locality_name'] == 'Санкт-Петербург']
grouped_average_distance = grouped_per_distance.groupby(['cityCenters_nearest_km']).agg({'last_price': 'mean'})
sorted_average_distance = grouped_average_distance.sort_values('cityCenters_nearest_km')
print('Средняя цена каждого километра по удалённости от центра млн.р:\n', sorted_average_distance)

'''
Чем дальше от центра города расположено жилье, тем оно дешевле
'''



