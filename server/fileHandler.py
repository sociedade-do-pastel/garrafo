import sqlite3
import os
from errorHandler import *
from sqlite3 import Error
from mimeTypes import mime_types 
# constants that define all our tables
# here we define the general structure for our table for file
FILE_TABLE_NAME = "file"
FILE_TABLE_STRUC = f'''CREATE TABLE {FILE_TABLE_NAME}(
filename TEXT PRIMARY KEY, 
path TEXT, 
moved INTEGER, 
mimetype TEXT
)\n'''

# server's general structure
SERVER_TABLE_NAME = "server"
SERVER_TABLE_STRUC = f'''CREATE TABLE {SERVER_TABLE_NAME}(
hostname TEXT PRIMARY KEY, 
root_path TEXT
)\n'''

# relationship between file and server
MAIN_RELATIONSHIP = "server_stores"
MRS_TABLE_STRUC = f'''CREATE TABLE  {MAIN_RELATIONSHIP}(
file_filename TEXT,
server_hostname TEXT,
FOREIGN KEY(file_filename) REFERENCES file(filename),
FOREIGN KEY(server_hostname) REFERENCES server(hostname))\n'''

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
    cursor.execute("INSERT OR IGNORE INTO server VALUES(?,?)",
                   (hostname, root_path))
    
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
        maindb_cursor.execute(FILE_TABLE_STRUC)
        maindb_cursor.execute(SERVER_TABLE_STRUC)
        maindb_cursor.execute(MRS_TABLE_STRUC)
    except Error as err:
        print(err.args)
        print(err.__class__)
        exit()
        
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
        cursor.execute("SELECT * FROM file WHERE filename=?",
                       (requested_filename,))
        try:
            name, file_path, was_moved, mimetype = cursor.fetchall()[0]
        except IndexError:
               raise NotFound
        finally:
            connection.close()
        if was_moved == 1:
            raise MovedPerm(file_path)
        
        data, data_length = openFile(file_path)
        return ResponseFile("200 OK",
                            mimetype,
                            data,
                            data_length)
                
        
def deleteFile(requested_deletion):
    try:
        os.remove(requested_deletion)
    except IOError:
        raise ServerError

def deleteFileFromDatabase(filename, cursor):
    succ = cursor.execute("DELETE FROM file WHERE filename=?", (filename,))
    if succ is None:
        raise ServerError
    
def moveFile(requested_moving):
    pass
def scanDirectory():
    pass
def insertIntoDatabase(filename, path, moved, mimetype, cursor):
    cursor.execute("INSERT OR IGNORE INTO file VALUES (?, ?, ?, ?)",
                   (filename, path, moved, mimetype))

    
def createFolders(passed_folders):
    path_string = ""
    for path in passed_folders:
        path_string += f"{path}/"
        if os.path.isfile(path_string):
            raise ServerError
        elif not os.path.isdir(path_string):
            os.mkdir(path_string)
        else:
            continue
        
def createFile(filename_and_path_to_create, file_to_create, hostname, cursor=None):
    filename_plus_root = hostname + filename_and_path_to_create
    divided_path = filename_plus_root.split("/")
    moved = 0
    # first, check if the requested filename already exists within the server
    connection = stablishConnection(hostname)
    cursor = connection.cursor()
    cursor.execute("SELECT path FROM file WHERE filename=?", (divided_path[-1], ))
    found_files = cursor.fetchone()
    print(found_files)
    # already exists within our server and is in a different path
    if found_files is not None and found_files[0] != filename_and_path_to_create:
        deleteFile(found_files[0]) # see if this is right
        deleteFileFromDatabase(divided_path[-1], cursor)
        moved = 1
        
    # have to make sure, though, that at least the requested folders exist
    if not len(divided_path) == 0:
        folders_to_create = divided_path[:-1]
        createFolders(folders_to_create)
    try:
    # if we choose to create/update a file, wb could work well here
        with open(filename_plus_root, "wb") as new_file:
            new_file.write(file_to_create)
    except IOError:
        raise ServerError

    
    # now that our file is created, update the database
    insertIntoDatabase(divided_path[-1],
                       filename_plus_root,
                       moved,
                       mime_types.get(divided_path[-1].split(".")[-1], "text/html ; charset=utf-8"),
                       cursor)
    
    connection.commit()
    connection.close()
    return moved

# if there isn`t a root directory, create one
# raise an exception if that's impossible to do
def checkRoot(root):
    if not os.path.isdir(root):
        os.mkdir(root)


