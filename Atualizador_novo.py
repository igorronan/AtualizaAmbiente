import requests
import json
import random
import time
import sys
import credenciais

class AtualizaAmbiente:

    def __init__(self, escolha):
        self.versoes = {"32":"1195","33":"491","34":"1705", "35":"2154"}
        
        if not escolha:
            self.id = json.loads(self.versoes["35"])
        else:
            if escolha in self.versoes:
                self.id = self.versoes[escolha]
            else:
                self.id = 0

        print("Versão: "+str(escolha))
        if self.id :
            self.consumo()

    def autorizacao(self):
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
            print("Autorização: Liberada")
            self.token = token["access_token"]
            self.auth = True
            self.headers = {
            'Authorization': 'Bearer '+self.token,
            'Content-Type': 'application/json'
            }
        else:
            print("Autorização: Negada")
            self.token = False
            self.auth = False

    
    def ambiente(self):
        self.autorizacao()
        url="https://totvsrestore.azurewebsites.net/api/user-environments"
        response = requests.request("GET", url, headers=self.headers)
        print(response.text)


    def consumo(self):
        self.autorizacao()
        if self.auth:
            url = "https://totvsrestore.azurewebsites.net/api/user-environments/force-update/"+self.id+"/all"
            response = requests.request("POST", url, headers=self.headers)
            request = (json.loads(response.text))
            if "requestUpdateId" in request :
                self.request = request["requestUpdateId"]
                self.consulta_retorno()
                time.sleep(5)
                print("Liberado!")
                

    
    def consulta_retorno(self):
        url=" https://totvsrestore.azurewebsites.net/api/user-environments/status/"+self.request
        response = requests.request("GET", url, headers=self.headers)
        request = (json.loads(response.text))
        status = True
        total = (len(request))
        while status:
            status = False
            contador = 0
            for var in request :
                if not var["isSuccess"]:
                    status = True
                    contador += 1

            print("Restando "+str(contador) + " de: "+ str(total))
            response = requests.request("GET", url, headers=self.headers)
            request = (json.loads(response.text))
        
if __name__ == "__main__":
    if sys.argv[1:]:
        AtualizaAmbiente(str(sys.argv[1]))
    else:
        print("Nenhuma versão foi passada.")
        print("Utilize assim: python atualizador_novo.py 32")
        time.sleep(10)