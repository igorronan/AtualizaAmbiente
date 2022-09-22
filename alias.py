import configparser
import os
import sys

config = configparser.ConfigParser()
origin = os.path.dirname(os.path.abspath(__file__))
config.read(origin+'\\versoes.ini')

banco = 'sql'
DbType = 'SqlServer'
DbProvider = 'SqlClient'


if sys.argv[1:]:
    versao = sys.argv[1]
else:
    print('Informar a versao desejada')
    exit()

if not config.has_section(versao):
    print('Versao nao encontrada no arquivo')
    exit()

chaves={"id","sqlhost","sqlbanco","oraclehost","oraclebanco"}

for chave in chaves:
    if not config.has_option(versao, chave):
        print("Arquivo de configuração deve conter a tag '"+chave+"'")
        exit()

if versao == 'atual':
    folder = "C:\\RM\\Atual\\Release\\Bin"
else:
    folder = "C:\\RM\\Legado\\12.1."+str(versao)+"\\Bin"


DbServer = config[versao]['sqlhost']
DbName='<DbName>'+config[versao]['sqlbanco']+'</DbName>' 

if sys.argv[2:]:
    if sys.argv[2] == "2":
        banco = 'oracle'
        DbType = 'Oracle'
        DbProvider = 'OracleClient'
        DbServer = config[versao]['oraclehost']+'/'+config[versao]['oraclebanco']
        DbName='<DbName />'


f = open(folder+'\\alias.dat', "w")
f.write('<?xml version="1.0" standalone="yes"?>\n')
f.write('<RMSAliasData xmlns="http://tempuri.org/RMSAliasData.xsd">\n')
f.write('<DbConfig>\n')
f.write('<Alias>CorporeRM</Alias>\n')
f.write('<DbType>'+str(DbType)+'</DbType>\n')
f.write('<DbProvider>'+str(DbProvider)+'</DbProvider>\n')
f.write('<DbServer>'+str(DbServer)+'</DbServer>\n')
f.write(DbName+'\n')
f.write('<UserName>SYSDBA</UserName>\n')
f.write('<Password>masterkey</Password>\n')
f.write('<RunService>false</RunService>\n')
f.write('<JobServerEnabled>false</JobServerEnabled>\n')
f.write('<JobServerMaxThreads>3</JobServerMaxThreads>\n')
f.write('<JobServerLocalOnly>false</JobServerLocalOnly>\n')
f.write('<JobServerPollingInterval>10</JobServerPollingInterval>\n')
f.write('<ChartAlertEnabled>false</ChartAlertEnabled>\n')
f.write('<ChartAlertPollingInterval>20</ChartAlertPollingInterval>\n')
f.write('<ChartHistoryEnabled>false</ChartHistoryEnabled>\n')
f.write('<ChartHistoryPollingInterval>20</ChartHistoryPollingInterval>\n')
f.write('<RSSReaderMailEnabled>false</RSSReaderMailEnabled>\n')
f.write('<RSSReaderMailPollingInterval>10</RSSReaderMailPollingInterval>\n')
f.write('<JobServerProcessPoolEnabled>true</JobServerProcessPoolEnabled>\n')
f.write('</DbConfig>\n')
f.write('</RMSAliasData>\n')
f.close()