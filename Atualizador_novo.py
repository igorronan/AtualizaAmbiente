import requests
import json
import os
import time
import sys
from datetime import datetime
import configparser

try:
    import credenciais
except ImportError:
    raise ImportError('Erro ao importar credenciais')

class AtualizaAmbiente:

    def __init__(self, escolha):
        config = configparser.ConfigParser()
        folder = os.path.dirname(os.path.abspath(__file__))
        config.read(folder+'\\versoes.ini')
        self.success = 0
        self.error = 0
        self.chamadas = 60
        self.start = datetime.now()
        self.id = False
        if not escolha:
            self.log("Versão não identificada",2)
            return
        else:
            if escolha:
                if config.has_section(escolha):
                    self.id = config[escolha]['id']
                else:
                    self.log('Versao nao encontrada ',2)
                    return
            else:
                self.id = config['versoes']['atual']
                return

        
        if self.id :
            self.log("Versão: "+self.retorna_versao(self.id), 1)
            self.consumo()
            
        self.resumo()

    def log(self, msg, tipo):
        if tipo == 1:
            t = '[SUCCESS]'
            self.success +=1
        else:
            t = '[ERROR]'
            self.error +=1
        print(F" - {datetime.now()} {t}: {msg}")
    
    def resumo(self):
        self.end = datetime.now()
        total = self.end-self.start
        print(f" ")
        print(f" - FIM DE PROCESSAMENTO")
        print(f" - SUCCESS: \t\t {self.success}")
        print(f" - ERROR: \t\t {self.error}")
        print(f" - DURATION: \t\t {total}")
    
    def autorizacao(self):
        self.headers = False
        self.auth = False
        self.token = False
        if not hasattr(credenciais,'username'):
            self.log("Credencial username nao encontrado",2)
            sys.exit()
        if not hasattr(credenciais,'password'):
            self.log("Credencial password nao encontrado",2)
            sys.exit()

        url = "https://totvsrestore.azurewebsites.net/api/auth"
        payload = json.dumps({
        "email": credenciais.username,
        "password": credenciais.password
        })
        self.headers = {
        'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=self.headers, data=payload)

        token = (json.loads(response.text))
        if "access_token" in token :
            self.token = token["access_token"]
            self.auth = True
            self.headers = {
            'Authorization': 'Bearer '+self.token,
            'Content-Type': 'application/json'
            }
            #self.log("Autorizacao: "+self.token,1)
        else:
            self.log("Autorização: Negada",2)

    def ambiente(self,inicio):
        self.autorizacao()
        url="https://totvsrestore.azurewebsites.net/api/user-environments"
        response = requests.request("GET", url, headers=self.headers)
        ambientes = json.loads(response.text)
        self.cls()
        for ambiente in ambientes:
            self.log(str(ambiente['id'])+ ": " +ambiente['name'],1)
            if inicio == str(ambiente['name']):
                self.id = ambiente['id']
        
        loop = True
        while loop:
            escolha = (input("Digite o ID da versao escolhida: "))
            for ambiente in ambientes:
                if escolha == str(ambiente['id']):
                    loop = False
        self.id = (escolha)
        

    def consumo(self):
        self.autorizacao()
        
        if self.auth == True:
            
            url = "https://totvsrestore.azurewebsites.net/api/user-environments/force-update/"+self.id+"/all"
            response = requests.request("POST", url, headers=self.headers)
            request = (json.loads(response.text))
            if "requestUpdateId" in request :
                self.request = request["requestUpdateId"]
                self.consulta_retorno()
                time.sleep(3)
                self.log("Liberado!",1)
            else:
                self.log(request['errorMessage'],2)
                
    def consulta_retorno(self):
        url=" https://totvsrestore.azurewebsites.net/api/user-environments/status/"+self.request
        response = requests.request("GET", url, headers=self.headers)
        request = (json.loads(response.text))
        status = True
        total = (len(request))
        chamadas = self.chamadas
        
        while status:
            installerName = ''
            status = False
            contador = 0
            
            for var in request :
                if not var["isSuccess"]:
                    status = True
                    contador += 1
                if var["isPending"]:
                    installerName = (var['installerName'])

            self.log("Restando "+str(contador) + " de: "+ str(total)+" regressiva: "+str(chamadas),1)
            response = requests.request("GET", url, headers=self.headers)
            request = (json.loads(response.text))
            chamadas = chamadas -1
            if chamadas == 0:
                return False
            
        
    def retorna_versao(self, id):
        self.autorizacao()
        url="https://totvsrestore.azurewebsites.net/api/user-environments"
        response = requests.request("GET", url, headers=self.headers)
        ambientes = json.loads(response.text)
        for ambiente in ambientes:
            if id == str(ambiente['id']):
                
                return ambiente["name"]

    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')

if __name__ == "__main__":
    if sys.argv[1:]:
        AtualizaAmbiente(str(sys.argv[1]))
    else:
        AtualizaAmbiente("atual")
        AtualizaAmbiente.log("Nenhuma versão foi passada.",2)
        AtualizaAmbiente.log("Utilize assim: python atualizador_novo.py 32",2)
        time.sleep(10)