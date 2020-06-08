import datetime # Biblioteca de data e hora 
import os
import glob 
import time # Biblioteca utilizada pelo 'time.sleep'
import json  # biblioteca de tratamento json
import urllib  # tratamento de url
import sys
import RPi.GPIO as GPIO # Biblioteca utilizada pelos LEDs e BIP 
import socket 
from time import *

GPIO.setmode(GPIO.BCM) # ativando os pinos utilizados pelos LEDs e BIP
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT) # AMARELO
GPIO.setup(23, GPIO.OUT) # AZUL/VERDE 
GPIO.setup(24, GPIO.OUT) # VERMELHO
Buzzer_PIN = 25          #Bip
GPIO.setup(Buzzer_PIN, GPIO.OUT, initial= GPIO.LOW)#bip

os.system('modprobe w1-gpio') # Configuracao para  aivar o pino utilizado pelo sensor de temperatura
os.system('modprobe w1-therm') # Configuracao para  aivar o pino utilizado pelo sensor de temperatura

# Configuracao do sensor de temperatura DS18B20
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
device_id = device_folder + '/name'
nome = open(device_id, 'r')
id = nome.readline()

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
    
def read_temp():
    lines = read_temp_raw()
    
    while lines[0].strip()[-3:] != 'YES':
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    
while True:
    dt=datetime.datetime.now().date() # variavel que traz a data 
    h=datetime.datetime.now().time()
    dh= h.strftime("%H:%M:%S") # variavel que traz a hora
    temper= round(read_temp(),1) # variavel que traz a temperatura, apenas com um algarismo depois da virgula, ja devidamente arredondado
    filename= device_file
    l= open(filename, 'r') # Abrir arquio para leitura
    
    if temper == 0.000: # Se o sensor estiver marcando 0.000 indica que o sensor esta danificado 
        print ('Sensor danificado!','\n', '\n', '\n')
        GPIO.output(18, GPIO.HIGH) # Como forma de alerta o LED amarelo ascende 
        GPIO.output(23, GPIO.HIGH) # VERDE

    else:
        if temper == 85.000: # Se o sensor estiver marcando 0.000 indica que o sensor esta danificado 
            print ('Sensor danificado!','\n', '\n', '\n')
            GPIO.output(18, GPIO.HIGH) # Como forma de alerta o LED amarelo ascende 
            GPIO.output(23, GPIO.HIGH) # VERDE

        else:
            for line in l:
                if 'NO' in line:
                    print ('Sensor danificado!','\n', '\n', '\n')
                    GPIO.output(18, GPIO.HIGH) # Como forma de alerta o LED amarelo ascende 
                    GPIO.output(23, GPIO.HIGH) # VERDE
                else:
                    print("ID=",id,"Temperatura=",temper,"°C","Data=",dt,"Hora=", dh)
                    GPIO.output(18, GPIO.LOW) # Quando o sensor voltar a funcionar o LED amarelo apaga
                    GPIO.output(23, GPIO.HIGH)
        
    if 28 < temper != 85.000 : # Quando osensor identifica que a temperatura esta mais alta que o esperado ele assendo o lede vermelho
        print('TEMPERATURA ALTA!') 
        GPIO.output(24, GPIO.HIGH) # VERMELHO
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(Buzzer_PIN,GPIO.HIGH) # Bip
        
    else:
        GPIO.output(24, GPIO.LOW) # Caso o sensor volte a temperatura normal o LED vermelho
        GPIO.output(23, GPIO.HIGH) # AZUL/VERDE
        GPIO.output(Buzzer_PIN,GPIO.LOW) # Bip

    temper=(str(round(read_temp(),1))) # Variavel que traz a temperatura
    abrir= open('sensor1.txt','a') # Abre o arquivo, e o 'a' refere-se a appende, ou seja, esse metdo deve ser utilizado quando o arquivo ja foi aberto outra vez
    ler= open('sensor1.txt', 'r') # Abrir arquio para leitura
    cat= ler.readline() # Le aqrquivo
  
    if cat == temper: #Compara o valor registrado no arquirquivo com a variavel atual
        print('Igual =', cat,'\n\n') # Caso seja igual, retorna 'igual'
    else:
        open('sensor1.txt','w') # Apagando o que esta escrito no arquivo 
        abrir.write(str(temper)) # Tramnsforma o valor da variavel em string e escreve no arquivo
        print('Mudou para ->', temper, '\n\n') # Printa o arquivo com a nova variavel
        
        #dados= '{"id":id,"temperatura":temper,"datas":dt,"hora":dh}'
        #url= "http://10.73.1.246/sensor/sensor/setData/"+ dados
        #abrir= urlopen(url)
        #envio= abrir.read()
        #print ('\n', abrir,'\n',envio)
        
    abrir.close() #Fecha o arquivo aberto para escrita 
    ler.close() # Fecha aruivo aberto para leitura
    
else: # Caso nada especificado acima estejaa funcionado ele executa ais acoes
    print("Path '%s' does not exists or is inaccessible" %device_file) 
    sys.exit()
        
    print("Falha na leitura dos sensores")
    time.sleep(1)
       
    GPIO.output(23, GPIO.LOW) 
    GPIO.output(24, GPIO.LOW) # Caso o sensor volte a temperatura normal o LED vermelho
    GPIO.output(23, GPIO.LOW)
    
# Envio dos dados do sensor para o coletor  
dados = {"ID":id,"Temperatura":temper,"Data":dt,"Hora":dh}
    
url = "https://-----.com.br/-/" + dados + "/json/"
response = urllib.urlopen(url)  # consulta a url inserida
    
urllib.request.urlopen
    
    
    