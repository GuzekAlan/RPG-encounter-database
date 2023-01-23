"""Funkcje do komunikowania się z bazą danych"""
from django.db import connection, IntegrityError

def execute_scripts_from_file(filename):
    """Funkcja do wykonania skryptu SQL z pliku
    :filename: ścieżka do pliku, z którego należy wziąć skrypt
    """
    cursor = connection.cursor()
    fd = open(filename, 'r')
    sql_file = fd.read()
    fd.close()
    try:
        cursor.execute(sql_file)
    except Exception as ex:
        print(f"Error occured while reading {filename=}")
        print(ex)


def get_id_name(table_name):
    """Funkcja zwraca id oraz nazwę z podanej tabeli
    :table_name: nazwa tabeli (bez przedrostka SCHEMA)
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nazwa FROM encounters." + table_name + " ORDER BY nazwa ASC;")
        return cursor.fetchall()

def get_id_name_encounter(name):
    """Funkcja zwraca id oraz nazwę z tabeli `potyczki` użytkownika o podanej nazwie
    :name: nazwa użytkownika, którego potyczki należy zwróci, w przypadku nazwy ADMIN zwróci wszystkie
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nazwa FROM encounters.pokaz_potyczki(%s) ORDER BY nazwa ASC;", [name])
        return cursor.fetchall()

def get_data(table_name, columns='*'):
    """Funkcja zwraca wszystkie rekordy z określonych kolumn z podanej tablicy
    :table_name: nazwa tablicy z której pobierane są dane
    :columns: lista column, z których pobierane są dane (zapisana jako string)
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT " + ",".join(columns) + " FROM encounters." + table_name)
        return cursor.fetchall()


def save_data(table_name, **kwargs):
    """Funkcja zapisuje w podanej tablicy rekord o podanych atrybutach.
    :table_name: nazwa tablicy do której jest dodawany rekord
    :kwargs: słownik którego klucze są nazwami atrybutów tablicy, a wartości tym, co należy tam zapisać
    Zwraca 0 jeśli wszystko się powiedzie, lub liczbę inną niż 0 jeśli wystąpią błędy
    """
    columns = list(kwargs.keys())
    values = list(kwargs.values())
    with connection.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO encounters." + table_name + "(" + ",".join(columns) + ") VALUES(" + ",".join(["%s" for _ in range(len(columns))]) + ")", values)
            return 0
        except IntegrityError as err:
            print(err)
            return -1


def connect_many_to_many(table_name, ids_left, ids_right):
    """Funkcja dodaje do tablicy asocjacyjnej wszystkie kombinacje rekordów
    :table_name: nazwa tablicy asocjacyjnej
    :ids_left: lista id lewej tablicy
    :ids_right: lista id prawej tablicy
    """
    ids_left_name = 'id_' + table_name.split('_')[0]
    ids_right_name = 'id_' + table_name.split('_')[1]
    with connection.cursor() as cursor:
        for idLeft in ids_left:
            for idRight in ids_right:
                try:
                    cursor.execute(f'INSERT INTO encounters.{table_name} ({ids_left_name}, {ids_right_name})' + "VALUES (%s, %s)", [idLeft, idRight])
                    return 0
                except IntegrityError as err:
                    print(err)
                    return -1


def get_max_index(table_name):
    """Funkcja zwraca maksymalny indeks z podanej tablicy
    :table_name: nazwa tablicy
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(id) FROM encounters." + table_name)
        return cursor.fetchone()


def check_user(login, password):
    """Funkcja porównuje hasło z bazy danych z podanym na podstawie loginu
    :login: login użytkownika, którego hasło należy zwrócić z bazy danych
    :password: hasło do porównania
    Zwraca nazwę użytkownika lub None
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT nazwa, haslo FROM encounters.osoby WHERE login=%s", [login])
            data = cursor.fetchone()
            if not data:
                return None
            if data[1] == password:
                return data[0]
            return None
        except IntegrityError as err:
            print(err)
            return None


def get_user_id(username):
    """Funkcja zwraca id użutkownika o podanej nazwie lub None
    :username: nazwa użytkownika
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT id FROM encounters.osoby WHERE nazwa=%s", [username])
            data = cursor.fetchone()
            if data:
                return data[0]
        except IntegrityError as err:
            print(err)
            return None


def get_encounter_by_creator(username):
    """Funkcja zwraca potyczki danego użytkownika (jeśli ADMIN to wszystkie)
    :username: nazwa użytkownika
    Jeśli nie ma takiego użytkownika to zwraca None
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM encounters.pokaz_potyczki(%s)", [username])
            data = cursor.fetchall()
            if data:
                return data
        except IntegrityError as err:
            print(err)
            return None

def delete_from_table(table_name, id_value):
    """Funkcja usuwa rekord o podanym id z tabeli
    :table_name: nazwa tabeli
    :id_value: id rekordu
    Zwraca True jeśli się udało usunąć lub False jeśli się nie udało
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("DELETE FROM encounters."+table_name+" WHERE id=(CAST(%s AS BIGINT))", [id_value])
            return True
        except IntegrityError as err:
            print(err)
            return False

def delete_encounter(id_record, username):
    """Funkcja usuwa potyczkę o podanym rekordzie, jeśli należy ona do użytkownika
    :id_record: numer id potyczki
    :username: nazwa użytkownika
    Zwraca True jeśli się udało usunąć lub False jeśli się nie udało
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT usun_potyczke(CAST(%s AS BIGINT), %s)", [id_record, username])
            print(f"Usunięto {id_record=}")
        except IntegrityError as err:
            print(err)
            return False

def get_encounter_by_creator_filter(username, min_lvl, max_lvl):
    """Funkcja zwraca listę potyczek danego użytkownika, których poziom trudności mieści się w zadanym rozmiarze
    :username: nazwa użytkownika
    :min_lvl: minimalny poziom trudności
    :max_lvl: maksymalny poziom trudności
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM encounters.filtruj_potyczki_po_poziomie_trudnosci(%s, CAST(%s AS BIGINT), CAST(%s AS BIGINT))", [username, min_lvl, max_lvl])
            data = cursor.fetchall()
            if data:
                return data
            return None
        except IntegrityError as err:
            print(err)
            return None