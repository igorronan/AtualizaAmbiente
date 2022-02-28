Configurações;
Utilizar o restore já configurado pela totvs;
Pegar os ID´s dos ambientes criados no Totvs Restore e modificar a linha destinada a eles;
    
    Atualizador_novo.py
    self.versoes = {"32":"1195","33":"491","34":"1705", "35":"2154"}

Deve-se criar aplicativos no IIS de acordo com cada versão desejada.
    Ex: http://localhost/32

Pra o ambinte atual deve criar o aplicativo na seguinte configuração
    Ex: http://localhost/Atual
