from subprocess import call
# Get imports installed
cmds = ["python -m ensurepip --upgrade", "py -m ensurepip --upgrade",
        "python -m pip install colorama", "py -m pip install colorama",
        "python -m pip install pyodbc", "py -m pip install pyodbc",
        "python -m pip install pandas", "py -m pip install pandas"]
for i in range(0, len(cmds), 2):
    cmd = call(cmds[i], shell = True)
    if cmd == 0:
        print("Python Success")
    else:
        cmd = call(cmds[i+1], shell = True)
        print("Py Success")
import os
import pyodbc
import pandas as pd
from colorama import Fore, Style

BASEURI = "https://localhost/MESMW/"
REQUESTURI = "api/v3/DirectAccess/?spName="
POSTDATA = ""
XMLVAR = "XML_VAR_HERE"

def BuildYourOwn():
    # Make the special variables editable
    global REQUESTURI
    global POSTDATA
    # Get the name of the stored procedure
    storedProcedure = input("Stored Procedure Name: ")
    REQUESTURI += storedProcedure
    # Get a list of variable names, split them into array
    variables = input("Provide A Comma Seperated List Of Variable Names: ")
    variables = variables.replace(" ", "")
    variables = variables.split(",")
    # Get a list of variable types, split them into array
    types = input("Provide The Variable Types In Order(str,int): ")
    types = types.replace(" ", "")
    types = types.split(",")
    # Go through and create the returned string
    POSTDATA = """ "{ """
    for i in range(0, len(variables)):
        if "string" in types[i] or "str" in types[i] or "s" in types[i]:
            POSTDATA += """ \\" """ + variables[i] + """ \\":\\""+ """ + XMLVAR + """ +"\\", """
        elif "integer" in types[i] or "int" in types[i] or "i" in types[i]:
            POSTDATA += """ \\" """ + variables[i] + """ \\":"+ """ + XMLVAR + """ +", """
    # Remove the final comma, add a cap, and remove spaces
    POSTDATA = POSTDATA.replace(" ", "")
    POSTDATA = POSTDATA[:-1]
    POSTDATA += """ }" """
    POSTDATA = POSTDATA.replace(" ", "")
    #####
    print("----------------------------------------")
    print("The Base URI Is: ", BASEURI)
    print("The Request URI Is: ", REQUESTURI)
    print("The POST Data Is: ", Fore.BLUE, POSTDATA, Style.RESET_ALL)
    return

def Query():
    # Make the special variables editable
    global REQUESTURI
    global POSTDATA
    # Get the name of the DRIVER
    driver = input("Driver Name(Probably SQL Server): ")
    # Get the name of the SERVER
    server = input("Server Name: ")
    # Get the name of the DATABASE
    database = input("DataBase Name(Probably MESDB): ")
    cnxn_str = ("Driver={"+driver+"};"
            "Server="+server+";"
            "Database="+database+";"
            "Trusted_Connection=yes;")
    # Get the name of the STORED PROCEDURE
    storedProcedure = input("Stored Procedure Name: ")
    REQUESTURI += storedProcedure
    # Build the query
    query = ("SELECT SP.name, ST.name FROM sys.parameters SP JOIN sys.types ST ON ST.user_type_id = SP.user_type_id WHERE object_id = object_id('dbo." + storedProcedure + "')")
    # query = ("SELECT Definition FROM SKEGridConfigurations")
    # Init database connection
    cnxn = pyodbc.connect(cnxn_str)
    # Execute the Query and save it
    data = pd.read_sql(query, cnxn)
    # Build a string of names and types
    values = []
    for i in range(0, data.index.size):
        for j in range(0, data.columns.size):
            values.append(data.iloc[i, j])
    # Print the SQL Table
    print("")
    print("Returned Table:")
    print(data)
    # Go through and create the returned string
    POSTDATA = """ "{ """
    for i in range(0, len(values), 2):
        if values[i + 1] == "nvarchar":
            POSTDATA += """ \\" """ + values[i][1:] + """ \\":\\""+ """ + XMLVAR + """ +"\\", """
        elif values[i + 1] == "int":
            POSTDATA += """ \\" """ + values[i][1:] + """ \\":"+ """ + XMLVAR + """ +", """
    # Remove the final comma, add a cap, and remove spaces
    POSTDATA = POSTDATA.replace(" ", "")
    POSTDATA = POSTDATA[:-1]
    POSTDATA += """ }" """
    POSTDATA = POSTDATA.replace(" ", "")
    #####
    print("----------------------------------------")
    print("The Base URI Is: ", BASEURI)
    print("The Request URI Is: ", REQUESTURI)
    print("The POST Data Is: ", Fore.BLUE, POSTDATA, Style.RESET_ALL)
    # Close the DB Connection
    del cnxn
    return
####################################################################################################################################
# This is a call to main to get the ball rolling
if __name__ == '__main__':
    os.system("cls")
    print(Fore.YELLOW, "PROGRAM START", Style.RESET_ALL)
    version = input("Build Your Own(B) OR Query(Q): ")
    if version == "B":
        BuildYourOwn()
    elif version == "Q":
        Query()
    print(Fore.YELLOW, "PROGRAM END", Style.RESET_ALL)
# END FILE
####################################################################################################################################