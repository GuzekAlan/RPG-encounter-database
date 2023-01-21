from django.db import connection, IntegrityError


def execute_scripts_from_file(filename):
    """Stolen from StackOverflow function. It might not be the best but it works
    Args:
        filename string: absolute path to a file
    """
    # Open and read the file as a single buffer
    cursor = connection.cursor()
    fd = open(filename, 'r')
    sql_file = fd.read()
    fd.close()
    try:
        cursor.execute(sql_file)
    except Exception as ex:
        print("Couldn't create database")
        print(ex)


def get_id_name(table_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nazwa FROM encounters." + table_name + " ORDER BY nazwa ASC;")
        return cursor.fetchall()

def get_id_name_encounter(name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nazwa FROM encounters.pokaz_potyczki(%s) ORDER BY nazwa ASC;", [name])
        return cursor.fetchall()

def get_data(table_name, columns='*'):
    with connection.cursor() as cursor:
        cursor.execute("SELECT " + ",".join(columns) + " FROM encounters." + table_name)
        return cursor.fetchall()


def save_data(table_name, **kwargs):
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
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(id) FROM encounters." + table_name)
        return cursor.fetchone()


def check_user(login, password):
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
    with connection.cursor() as cursor:
        try:
            cursor.execute("DELETE FROM encounters."+table_name+" WHERE id=(CAST(%s AS BIGINT))", [id_value])
            return True
        except IntegrityError as err:
            print(err)
            return False

def delete_encounter(id_record, username):
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT usun_potyczke(CAST(%s AS BIGINT), %s)", [id_record, username])
            print(f"Usunięto {id_record=}")
        except IntegrityError as err:
            print(err)
            return False

def get_encounter_by_creator_filter(username, min_lvl, max_lvl):
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