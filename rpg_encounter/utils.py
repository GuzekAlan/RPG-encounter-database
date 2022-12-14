from django.core.files import File

def executeScriptsFromFile(filename, cursor):
    """Stolen from StackOverflow function. It might not be the best but it works

    Args:
        filename string: absolute path to a file
        cursor: cursor for database
    """
    # Open and read the file as a single buffer
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
        except Exception:
            print("Command skipped")