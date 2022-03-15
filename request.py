import requests
import sys

    
def valida(url):
    try:
        x = str(requests.get(url))
        if (x.find("200") < 0 ):
            print(0)
        else:
            print(1)
    except:
        print(0)
    
    
if sys.argv[1:]:
    valida(sys.argv[1])
else:
    print(0)
