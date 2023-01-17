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
        print("Command skipped: ", ex)


def get_id_name(table_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nazwa FROM encounters." + table_name)
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
            print(data)
            if data[1] == password:
                return data[0]
            return None
        except IntegrityError as err:
            print(err)
            return None
