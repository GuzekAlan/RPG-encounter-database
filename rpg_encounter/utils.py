from django.db import connection

def executeScriptsFromFile(filename, cursor):
    """Stolen from StackOverflow function. It might not be the best but it works
    Args:
        filename string: absolute path to a file
    """
    # Open and read the file as a single buffer
    cursor = connection.cursor()
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cursor.execute(command)
        except Exception as ex:
            print("Command skipped: ", ex)
            
def getData(table_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nazwa FROM encounters." + table_name)
        return cursor.fetchall()
    
def saveData(table_name, **kwargs):
    columns = list(kwargs.keys())
    values = list(kwargs.values())
    print(columns)
    print(values)
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO encounters." + table_name + "(" + ",".join(columns) + ") VALUES(" + ",".join(["%s" for _ in range(len(columns))]) + ")", values)
