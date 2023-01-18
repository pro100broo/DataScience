import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('data.csv', sep=',')

# Предобработка данных
median_income = data.groupby('income_type')['total_income'].transform('median')
data['total_income'].fillna(median_income, inplace=True)
median_income = data.groupby('income_type')['days_employed'].transform('median')
data['days_employed'].fillna(median_income, inplace=True)

# Изменение отрицательных значений на положительные
data['days_employed'] = data['days_employed'].abs()

# Выведите перечень уникальных значений столбца children.
mask = data['children'].isin([data['children'].unique().min(), data['children'].unique().max()])
data = data[~mask]

# Замените вещественный тип данных в столбце `total_income` на целочисленный с помощью метода `astype()`.
data['total_income'] = data['total_income'].astype(int)

# Обработайте неявные дубликаты в столбце education.
# В этом столбце есть одни и те же значения, но записанные по-разному: с использованием заглавных и строчных букв.
# Приведите их к нижнему регистру.
data['education'] = data['education'].str.lower()

# Выведите на экран количество строк-дубликатов в данных. Если такие строки присутствуют, удалите их
data = data.drop_duplicates()


# Категоризация данных 1
def categorize_income(income: int) -> str:
    if 0 <= income <= 30000:
        return 'E'
    elif 30001 <= income <= 50000:
        return 'D'
    elif 50001 < income <= 200000:
        return 'C'
    elif 200001 <= income <= 1000000:
        return 'B'
    elif income >= 1000001:
        return 'A'


data['total_income_category'] = data['total_income'].apply(categorize_income)


# Категоризация данных 2
def categorize_purpose(purpose: str) -> str:
    if 'авто' in purpose:
        return 'операции с автомобилем'
    elif 'недвиж' in purpose or 'жил' in purpose:
        return 'операции с недвижимостью'
    elif 'свад' in purpose:
        return 'проведение свадьбы'
    elif 'образ' in purpose:
        return 'получение образования'


data['purpose_category'] = data['purpose'].apply(categorize_purpose)


# Есть ли зависимость между количеством детей и возвратом кредита в срок?
data.groupby(['children']).agg({'debt': 'sum'}).plot(
    grid=True,  # добавление сетки на график
    figsize=(20, 10),  # установка размера окна с графиком
    title='Изменение количества задолжавших семей,\nв зависимости от числа детей',  # название графика
    ylabel='Количество должников',  # подпись оси 'y'
    xlabel='Число детей в семье',  # подпись оси 'x'
    legend=False  # отключение легенды
)


# Есть ли зависимость между семейным положением и возвратом кредита в срок?
data.groupby(['family_status']).agg({'debt': 'sum'}).sort_values('debt', ascending=False).plot(
    grid=True,
    figsize=(20, 10),
    title='Изменение количества задолжавших семей,\nв зависимости от семейного положения',
    ylabel='Количество должников',
    xlabel='Семейное положение',
    legend=False
)


# Есть ли зависимость между уровнем дохода и возвратом кредита в срок?
data.groupby(['total_income_category']).agg({'debt': 'sum'}).plot(
    grid=True,
    figsize=(20, 10),
    title='Изменение количества задолжавших семей,\nв зависимости от уровня дохода',
    ylabel='Количество должников',
    xlabel='Уровень дохода',
    legend=False
)


# Как разные цели кредита влияют на его возврат в срок?
data.groupby(['purpose_category']).agg({'debt': 'sum'}).sort_values('debt', ascending=False).plot(
    grid=True,
    figsize=(20, 10),
    title='Изменение количества задолжавших семей,\nв зависимости от цели кредита',
    ylabel='Количество должников',
    xlabel='Цель кредита',
    legend=False
)

plt.show()

# Вывод результата в виде сводной таблицы
my_pivot_table = data.pivot_table(index='children', values='debt', aggfunc=['count', 'sum', 'mean'])

my_pivot_table = my_pivot_table.sort_values(by=my_pivot_table.columns[2], ascending=False)
my_pivot_table.reset_index(inplace=True)
my_pivot_table.columns = ['Кол-во детей', 'Кол-во клиентов', 'Кол-во должников', 'Доля невозврата']
print(my_pivot_table)

