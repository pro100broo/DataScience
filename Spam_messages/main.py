import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import numpy as np

# Подготовка данных
data = pd.read_csv('spam.csv', sep=',')
data.columns = data.columns.str.lower()
data['message'] = data['message'].str.lower()
data = data.replace(to_replace="[*.!?',@#&/‘;:#№$%^()-_=+]", value='', regex=True)

# Построение модели логистической регрессии
tfidf = TfidfVectorizer(stop_words='english')

tfidf_matrix = tfidf.fit_transform(data.message)  # X
names = tfidf.get_feature_names_out()  # Y

# Матрица весов (модель линейной регрессии)
tfidf_matrix = pd.DataFrame(tfidf_matrix.toarray(), columns=names)

# Train test
tfidf_matrix = tfidf_matrix.transpose()
x_train, x_test, y_train, y_test = train_test_split(tfidf_matrix, names, train_size=0.7, random_state=42)

# Ручной поиск стоп-слов
X = tfidf.fit_transform(data.message)
y = data.category

N = 20
# индексы топ 10 столбцов с максимальной суммой элементов (в столбцах)
idx = np.ravel(X.sum(axis=0).argsort(axis=1))[::-1][:N]
top_10_words = np.array(tfidf.get_feature_names_out())[idx].tolist()
print(top_10_words)

