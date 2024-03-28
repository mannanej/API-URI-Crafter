##### FOR REAL USE, USE THE CRAFTER FILE #####
from subprocess import call
call("python -m ensurepip --upgrade", shell = True)
call("python -m pip install colorama", shell = True)
from colorama import Fore, Style

BASEURI = "https://localhost/MESMW/"
REQUESTURI = "api/v3/DirectAccess/?spName="
POSTDATA = ""
XMLVAR = "XML_VAR_HERE"

def main():
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
####################################################################################################################################
# This is a call to main to get the ball rolling
if __name__ == '__main__':
    print(Fore.YELLOW, "PROGRAM START", Style.RESET_ALL)
    main()
    print(Fore.YELLOW, "PROGRAM END", Style.RESET_ALL)
# END FILE
####################################################################################################################################
