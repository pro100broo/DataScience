# Функции для добавления новых столбцов по жанрам
def drama(genres):
    return True if 'Drama' in genres.split(', ') else False


def comedy(genres):
    return True if 'Comedy' in genres.split(', ') else False


def romance(genres):
    return True if 'Romance' in genres.split(', ') else False


def adventure(genres):
    return True if 'Adventure' in genres.split(', ') else False


def animation(genres):
    return True if 'Animation' in genres.split(', ') else False


def thriller(genres):
    return True if 'Thriller' in genres.split(', ') else False