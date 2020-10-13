import sqlite3
import os
from errorHandler import *
from sqlite3 import Error
# constants that define all our tables
# here we define the general structure for our table for file
FILE_TABLE_NAME = "file"
FILE_TABLE_STRUC = f'''{FILE_TABLE_NAME}(
filename TEXT PRIMARY KEY, 
path TEXT, 
moved INTEGER, 
mimetype TEXT
)'''

# server's general structure
SERVER_TABLE_NAME = "server"
SERVER_TABLE_STRUC = f'''{SERVER_TABLE_NAME}(
hostname TEXT PRIMARY KEY, 
root_path TEXT
)'''

# relationship between file and server
MAIN_RELATIONSHIP = "server_stores"
MRS_TABLE_STRUC = f'''{MAIN_RELATIONSHIP}(
file_filename TEXT,
server_hostname TEXT,
FOREIGN KEY(file_filename) REFERENCES file(filename),
FOREIGN KEY(server_hostname) REFERENCES server(hostname))'''

# index default filename
INDEX_FILENAME = "index.html"
# and its aliases are listed here
INDEX_ALIASES = ["/index.htm", "/index", "/", "/.", ""]

# response object
class ResponseFile():
    def __init__(self, message, mime, body, length):
        self.message = message
        self.mime = mime
        self.body = body
        self.length = length

# directory structure html
directory_structure = '''
<!DOCTYPE html>
<html>
<head><title>{:}</title></head>
<body>
<br>
<h1>Directory listing for {:}</h1>
<ui>
{:}
</ui>
</body>
</html>'''
def initServerInformation(hostname, root_path, cursor):
    cursor.execute(f'''INSERT OR IGNORE INTO server VALUES(\'{hostname}\', \'{root_path}\')''')
    
def stablishConnection(database_name):
    try:
        return sqlite3.connect(database_name + ".db")
    except Error:
        print(Error)
        # maybe raise something here
def initDatabase(database_name):
    checkRoot(database_name)
    connection = stablishConnection(database_name)
    cursor = connection.cursor()
    initTables(cursor)
    initServerInformation(database_name, database_name + "/", cursor )
    connection.commit()
    connection.close()
    
def manageDatabase(database_name):
    if not os.path.isfile(database_name + ".db"):
        initDatabase(database_name)


def initTables(maindb_cursor):
    try:
        maindb_cursor.execute("CREATE TABLE IF NOT EXISTS {}".format(FILE_TABLE_STRUC))
        maindb_cursor.execute("CREATE TABLE IF NOT EXISTS {}".format(SERVER_TABLE_STRUC))
        maindb_cursor.execute("CREATE TABLE IF NOT EXISTS {}".format(MRS_TABLE_STRUC))
    except Error as err:
        print(err.args)
        print(err.__class__)
        
def createFile(file_to_create, file_data=None, cursor=None):
    pass

def openFile(request):
    try:
        with open(request , "rb") as file_to_return:
            body =  file_to_return.read()
            body_length = file_to_return.seek(0, os.SEEK_END)
        return body, body_length
    except FileNotFoundError:
        raise NotFound
    
def searchFile(requested_path, hostname):
    if requested_path in INDEX_ALIASES:
        body_index, body_length = openFile(INDEX_FILENAME)
        return ResponseFile("200 OK",
                            "text/html ; charset=utf-8",
                            body_index,
                            body_length)
    
    # if it's a folder (that is not our root) that we are requesting 
    elif requested_path[-1] == "/":
        if not os.path.isdir(hostname + requested_path):
            raise NotFound
        else:
            directory_list = os.listdir(hostname + requested_path)
            body_directory = ""
            for files in directory_list:
                body_directory += "<li>{}</li>\n".format(files)
                
            directory_formatted_string_to_bytes = bytes(directory_structure.format(
                requested_path,
                hostname + requested_path,
                body_directory), "UTF-8")
            
            return ResponseFile("200 OK",
                                "text/html ; charset=utf-8",
                                directory_formatted_string_to_bytes,
                                len(directory_formatted_string_to_bytes))
    else:
        connection = stablishConnection(hostname)
        cursor = connection.cursor()
        requested_filename = requested_path.split("/")[-1]
        cursor.execute(f'''SELECT * FROM file WHERE filename = \'{requested_filename}\' ''')
        try:
            name, file_path, was_moved, mimetype = cursor.fetchall()[0]
        except IndexError:
               raise NotFound
        finally:
            connection.close()
        if was_moved == "1":
            raise MovedPerm(file_path)
        
        data, data_length = openFile(file_path)
        return ResponseFile("200 OK",
                            mimetype,
                            data,
                            data_length)
                
        
def deleteFile(requested_deletion):
    pass
def moveFile(requested_moving):
    pass
def scanDirectory():
    pass

# if there isn`t a root directory, create one
# raise an exception if that's impossible to do
def checkRoot(root):
    if not os.path.isdir(root):
        os.mkdir(root)


