from django.db import connection, IntegrityError

def executeScriptsFromFile(filename):
    """Stolen from StackOverflow function. It might not be the best but it works
    Args:
        filename string: absolute path to a file
    """
    # Open and read the file as a single buffer
    cursor = connection.cursor()
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    try:
        cursor.execute(sqlFile)
    except Exception as ex:
        print("Command skipped: ", ex)
            
def getIdName(table_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nazwa FROM encounters." + table_name)
        return cursor.fetchall()
    
def getData(table_name, columns='*'):
    with connection.cursor() as cursor:
        cursor.execute("SELECT " + ",".join(columns) + " FROM encounters." + table_name)
        return cursor.fetchall()
    
def saveData(table_name, **kwargs):
    columns = list(kwargs.keys())
    values = list(kwargs.values())
    with connection.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO encounters." + table_name + "(" + ",".join(columns) + ") VALUES(" + ",".join(["%s" for _ in range(len(columns))]) + ")", values)
            return 0
        except IntegrityError as err:
            print(err)
            return -1

def connectManyToMany(table_name, idsLeft, idsRight):
    idLeftName = 'id_' + table_name.split('_')[0]
    idRightName = 'id_' + table_name.split('_')[1]
    with connection.cursor() as cursor:
        for idLeft in idsLeft:
            for idRight in idsRight:
                try:
                    cursor.execute(f'INSERT INTO encounters.{table_name} ({idLeftName}, {idRightName})' +  "VALUES (%s, %s)", [idLeft, idRight])
                except IntegrityError as err:
                    print(err)
                    return -1

def getMaxIndex(table_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(id) FROM encounters." + table_name)
        return cursor.fetchone()
