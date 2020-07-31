from cryptography.fernet import Fernet
import ast

userSetting={
    "adminPass": "admin",
    "viewerPass": "guest",
    "activationKey": "KtXX1LIane85Em62ddsjUaC4bF9zNF5D7PEOWC6T",
    "apiURL": "https://epj0x952wb.execute-api.ap-south-1.amazonaws.com/default/mxnet4",
    "numberOfLambda": 2,
    "maxNumberOfCamera": 5,
}
cipher=Fernet(b'gkmrxai04WhOcWj3EGl-2Io58Q8biOWOytdQbPhNYGU=')

def putData(cipher,data):
    encrypted=cipher.encrypt(str(userSetting).encode('utf-8'))
    with open('userSetting.txt','w') as file:
        file.write(encrypted.decode('utf-8'))

def getData(cipher):
    with open('userSetting.txt','r') as file:
            data=file.read()
    userSetting=ast.literal_eval((cipher.decrypt(data.encode('utf-8'))).decode('utf-8'))
    print(userSetting)
    
putData(cipher,userSetting)
getData(cipher)


    
