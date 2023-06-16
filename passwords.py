import sys
import re

#this area simply opens the file
try:
    f = open(sys.argv[1])
except:
    print("\nError: Please enter a file to open\n")
    exit()

print("File " + sys.argv[1] + " has been opened!")
f.close()


#this area deals with finding the user within the listing of users
user = "default value"
startCount = 0
endCount = 0
accountFound = False

#type = True for decryption, false for Encryption
def encrypt(password, type):
    global user
    shift = len(user.strip()) + 3
    chars = list(password)
    if(type):
        flipFlop = True
    else:
        flipFlop = False
    encrypted = ""
    for i in password:
        if(flipFlop):
            i = ord(i) + shift
        else:
            i = ord(i) - shift

        if(i > 126):
            i = 32 + i%126
        if(i < 33):
            i = 126 - (32-i)
            #at 25, needs to be at 119

        i = chr(i)       
        encrypted = encrypted + i
        flipFlop = not flipFlop
    return encrypted


def addLine(toStore, passw):
    global startCount
    f = open(sys.argv[1])
    lines = f.readlines()
    lines.insert(startCount+1, toStore + encrypt(passw, False) + '\n')
    f.close
    f = open(sys.argv[1], "w")
    f.writelines(lines)
    f.close()


def findPass(website):
    global startCount
    website = str(website).upper()
    f = open(sys.argv[1])
    lines = f.readlines()

    for i in range(startCount, len(lines)):
        curLine = lines[i]
        if curLine == "--END--":
            break
        if curLine.__contains__(website + "   =+|+=   "):
            curLine = curLine.replace(website + "   =+|+=   ", "")
            curLine = encrypt(curLine, True)
            curLine = curLine[:-1]
            print("\n\nFound!\n" + curLine)
            break

    f.close()
    return


def changePass(website, password):
    global startCount
    website = str(website).upper()
    f = open(sys.argv[1])
    lines = f.readlines()
    #print("OLD\n")
    #print(lines)
    toChange = -1

    for i in range(startCount, len(lines)):
        curLine = lines[i].strip()
        if curLine == "--END--":
            break
        if curLine.__contains__(website):
            toChange = i
            break
    
    if(toChange != -1):
        lines[toChange] = website + "   =+|+=   " + encrypt(password, False) + "\n"
        print("Changed!")
    else:
        print("Error: Account not Found")
    #print("NEW\n")
    #print(lines)
    f.close
    f = open(sys.argv[1], "w")
    f.writelines(lines)
    f.close()
    return


def findUser():
    global user
    global startCount
    global accountFound
    global endCount
    user = input("Please enter your account name: ")
    user = user.upper()
    f = open(sys.argv[1])


    count = 0
    for line in f:
        count+=1;
        line = line.strip()
        if(not accountFound and (user == line)):
            accountFound = True
            startCount = count
        if(accountFound and line == "--END--"):
            endCount = count
            break
        
            

    if(not accountFound):
        resolved = False
        print("\nUser Not Found")
        while(not resolved):
            create = input("Please Choose an Action:\n1. Create New Account\n2. Retry \n3. Quit\n")
            if(not create.isdigit()):
                print("\nError! Enter a valid number.")
            else:
                create = int(create)
                if(create == 1):
                    makeAccount()
                    findUser()
                    f.close()
                    resolved = True
                elif(create == 2):
                    print("\n")
                    findUser()
                    f.close()
                    resolved = True
                elif(create == 3):
                    print("\nClosing")
                    resolved = True
                    f.close()
                    exit()
                else:
                    print("\nError: Please choose a valid number")


def makeAccount():
    global user
    password = input("Please enter a password: ")
    password = encrypt(password, False)
    f = open(sys.argv[1], "a")
    f.write(user + "\n" + password + "\n--END--\n\n\n\n\n")
    f.close()
    print("Account Created\n\n")


def verifyPass(enteredPass):
    f = open(sys.argv[1])
    global startCount
    lines = f.readlines()
    storedPass = lines[startCount]
    storedPass = storedPass.strip()
    if(encrypt(enteredPass, False) == storedPass):
        f.close()
        return True
    f.close()
    return False


def actions():
    resolved = False
    while(not resolved): 
        print("\nWhat action would you like to take?")
        action = input("1. Access a Password\n2. Add a New Password\n3. Change a Password \n4. Quit\n")
        if(not action.isdigit()):
            print("\nError! Enter a valid number.")
        else:
            action = int(action)
            if(action == 1):
                website = input("What account are you looking for?\n")
                website.upper()
                findPass(website)
            elif(action == 2): 
                website = input("What website/account is this password for?\nPlease enter the account as one word\n")
                website.upper()
                webPass = input("What is your password for this account?\n")
                store = website.upper() + "   =+|+=   "
                addLine(store, webPass)
                print("Added!")
            elif(action == 3): #Not complete
                website = input("What website are you changing the password for?\n")
                webPass = input("What is your new password?\n")
                website = website.upper() + "   =+|+=   "
                changePass(website, webPass)
            elif(action == 4):
                print("\nClosing")
                resolved = True
                exit()
            else:
                print("\nError: Please choose a valid number")






findUser()
enteredPass = input("Account Found! Please enter your password: ")
passCorrect = False
while(not passCorrect):
    if(verifyPass(enteredPass)):
        passCorrect = True
        print("\nLogged in! Hello " + user);
    else:
        print("\nWrong Password. Please try again.")
        enteredPass = input("Please enter your password: ")
actions()

