#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ASSISTENTE.py
#  
#  Copyright 2022 JaimeJG
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


from vosk import Model, KaldiRecognizer
from plyer import notification
from requests import get
import speech_recognition as sr
import os
import pyaudio
import pyttsx3
import sys
import datetime
import psutil
import webbrowser
import vlc
import json
import requests
import time
import wikipedia
import random

def SomCarregamento():
	p = vlc.MediaPlayer("LOAD.mp3")
	p.play()

SomCarregamento()

def SomIncial():
	p = vlc.MediaPlayer("START.mp3")
	p.play()

r = sr.Recognizer()

speaker=pyttsx3.init()
speaker.setProperty('voice', 'pt+m3')
rate = speaker.getProperty('rate')
speaker.setProperty('rate', rate-41)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

def resposta(audio):
	notification.notify(title = "ASSISTENTE",message = audio,timeout = 3)
	stream.stop_stream()
	print('ASSISTENTE: ' + audio)
	#os.system('espeak -vbrazil-mbrola-3 "' +audio +'"')
	speaker.say(audio)
	speaker.runAndWait()
	stream.start_stream()

if not os.path.exists("PTBR"):
	print ("Modelo em portugues nao encontrado.")
	exit (1)

model = Model("PTBR")
rec = KaldiRecognizer(model, 16000)

def notificar(textos):
	notification.notify(title = "ASSISTENTE",message = textos,timeout = 10)

def respostalonga(textofala):
	notification.notify(title = "ASSISTENTE",message = textofala,timeout = 30)
	stream . stop_stream ()
	speaker.say(textofala)
	speaker.runAndWait()
	stream . start_stream ()

def horario():
	from datetime import datetime
	hora = datetime.now()
	horas = hora.strftime('%H e %M')
	Horarios = int(hora.hour)
	if Horarios >= 0 and Horarios < 12:
		resposta('Agora s??o ' +horas +' da manh??')

	elif Horarios >= 12 and Horarios < 18:
		resposta('Agora s??o ' +horas +' da tarde')

	elif Horarios >= 18 and Horarios != 0:
		resposta('Agora s??o ' +horas +' da noite')

def datahoje():
	from datetime import date
	dataatual = date.today()
	diassemana = ('Segunda-feira','Ter??a-feira','Quarta-feira','Quinta-feira','Sexta-feira','S??bado','Domingo')
	meses = ('Zero','Janeiro','Fevereiro','Mar??o','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro')
	resposta("Hoje ?? " +diassemana[dataatual.weekday()])
	diatexto = '{} de '.format(dataatual.day)
	mesatual = (meses[dataatual.month])
	datatexto = dataatual.strftime(" de %Y")
	resposta('Dia '+diatexto +mesatual +datatexto)

def bateria():
	try:
		bateria = psutil.sensors_battery()
		carga = bateria.percent
		bp = str(bateria.percent)
		bpint = "{:.0f}".format(float(bp))
		resposta("A bateria est?? em:" +bpint +'%')
		if carga <= 20:
			resposta('Ela est?? em nivel cr??tico')
			resposta('Por favor, coloque o carregador')
		elif carga == 100:
			resposta('Ela est?? totalmente carregada')
			resposta('Retire o carregador da tomada')
	except:
		resposta('Desculpa')
		resposta('Seu dispositivo atual n??o est?? usando bateria')
		resposta('Por isso ?? impossivel informar a quantidade de carga')

def cpu ():
	usocpuinfo = str(psutil.cpu_percent())
	usodacpu  = "{:.0f}".format(float(usocpuinfo))
	resposta('O uso do processador est?? em ' +usodacpu +'%')

def temperaturadacpu():
	tempcpu = psutil.sensors_temperatures()
	cputemp = tempcpu['coretemp'][0]
	temperaturacpu = cputemp.current
	cputempint = "{:.0f}".format(float(temperaturacpu))
	if temperaturacpu >= 20 and temperaturacpu < 40:
		resposta('Estamos trabalhado em um n??vel agradavel')
		resposta('A temperatura est?? em ' +cputempint +'??')
    
	elif temperaturacpu >= 40 and temperaturacpu < 58:
		resposta('Estamos operando em nivel raso??vel')
		resposta('A temperatura ?? de ' +cputempint +'??')
    
	elif temperaturacpu >= 58 and temperaturacpu < 70:
		resposta('A temperatura da CPU est?? meio alta')
		resposta('Algum processo do sistema est?? causando aquecimento')
		resposta('Fique de olho')
		resposta('A temperatura est?? em ' +cputempint +'??')
    
	elif temperaturacpu >= 70 and temperaturacpu != 80:
		resposta('Aten????o')
		resposta('Temperatura de ' +cputempint +'??')
		resposta('Estamos em nivel cr??tico')
		resposta('Desligue o sistema imediatamente')

def BoasVindas():
	Horario = int(datetime.datetime.now().hour)
	if Horario >= 0 and Horario < 12:
		resposta('Bom dia')

	elif Horario >= 12 and Horario < 18:
		resposta('Boa tarde')

	elif Horario >= 18 and Horario != 0:
		resposta('Boa noite')

def tempo(): 
	try:
		#Procure no google maps as cordenadas da sua cidade e coloque no "lat" e no "lon"(Latitude,Longitude)
		api_url = "https://fcc-weather-api.glitch.me/api/current?lat=LATITUDE_AQUI&lon=LONGITUDE_AQUI"
		data = requests.get(api_url)
		data_json = data.json()
		if data_json['cod'] == 200:
			main = data_json['main']
			wind = data_json['wind']
			weather_desc = data_json['weather'][0]
			temperatura =  str(main['temp'])
			tempint = "{:.0f}".format(float(temperatura))
			vento = str(wind['speed'])
			ventoint = "{:.0f}".format(float(vento))
			dicionario = {
				'Rain' : 'chuvoso',
				'Clouds' : 'nublado',
				'Thunderstorm' : 'com trovoadas',
				'Drizzle' : 'com garoa',
				'Snow' : 'com possibilidade de neve',
				'Mist' : 'com n??voa',
				'Smoke' : 'com muita fuma??a',
				'Haze' : 'com neblina',
				'Dust' : 'com muita poeira',
				'Fog' : 'com n??voa',
				'Sand' : 'com areia',
				'Ash' : 'com cinza vulcanica no ar',
				'Squall' : 'com rajadas de vento',
				'Tornado' : 'com possibilidade de tornado',
				'Clear' : 'limpo'
				}
			tipoclima =  weather_desc['main']
			if data_json['name'] == "Shuzenji":
				resposta('Erro')
				resposta('API de clima falhou')
				resposta('Tente outra vez o comando')
			else:
				resposta('Verificando clima para a cidade de '+ data_json['name'])
				resposta('O clima hoje est?? ' +dicionario[tipoclima])
				resposta('A temperatura ?? de ' + tempint + '??')
				resposta('O vento est?? em ' + ventoint + ' kilometros por hora')
				resposta('E a umidade ?? de ' + str(main['humidity']) +'%')
    
	except: 
		resposta('Erro na conex??o')
		resposta('Tente novamente o comando')
		
def Localiza????o():
	resposta('Ok')
	resposta('Verificando localiza????o')
	try:
		Endere??oIP = get('https://api.ipify.org').text
		url = 'https://get.geojs.io/v1/ip/geo/'+Endere??oIP+'.json'
		geo_reqeust = get(url)
		geo_data = geo_reqeust.json()
		city = geo_data['city']
		resposta('Sua localiza????o ?? '+str(city))
	except:
		resposta('Falha ao verificar a localiza????o')

def AteMais():
	Horario = int(datetime.datetime.now().hour)
	if Horario >= 0 and Horario < 12:
		resposta('Tenha um ??timo dia')

	elif Horario >= 12 and Horario < 18:
		resposta('Tenha uma ??tima tarde')

	elif Horario >= 18 and Horario != 0:
		resposta('Boa noite')

def NomeUsuario():
	try:
		ler = open('SeuNomeAqui.txt', 'r')
		leitura = json.loads(ler.read())
		nomeuser = str(leitura)
		resposta("Ol?? "+nomeuser)
	except:
		resposta('Erro no arquivo de nome do usu??rio')
		resposta('Por favor mantenha seu nome com aspas')
		resposta('E n??o troque o nome do arquivo')

def inicialize():
	ler = open('DADOS//1INICIO.txt', 'r')
	leitura = json.loads(ler.read())
	if leitura == 0:
		resposta('Meu nome ?? JARVIS')
		resposta('Apartir de agora vou ser seu novo assistente virtual')
		resposta('Estou aqui para atender seus comandos')
		resposta('Muito prazer em conhec??-lo')
		resposta('Mas vamos ao que interessa')
		dicionario = 1
		f = open('DADOS//1INICIO.txt', 'w+')
		f.write(json.dumps(dicionario))
	elif leitura == 1:
		None

NomeUsuario()
BoasVindas()
inicialize()
resposta('M??dulos iniciados')
resposta('Diga seu comando')

def RComandos():
	data = stream.read(8000)
	texto = 'nada'
	if len(data) == 0:
		None
	if rec.AcceptWaveform(data):
		result = rec.Result()
		resultado = json.loads(result)
		if result is not None:
			texto = resultado['text']
			return texto
	return texto

# Comandos e conversas   
def LComandos():

	while True:
		
		Input = RComandos()
        
		if 'ol??' in Input: #Ol?? JARVIS
			variante = random.choice(["Deseja algo?", "Precisa de algo?","Quer alguma coisa?"])
			resposta('Ol??')
			resposta('Estou aqui')
			resposta(variante)
        
		elif 'bom dia' in Input: #Boa Noite J.A.R.V.I.S
			Horario = int(datetime.datetime.now().hour)
			if Horario >= 0 and Horario < 12:
				resposta('Ol??')
				resposta('Bom dia')

			elif Horario >= 12 and Horario < 18:
				resposta('Agora n??o ?? mais de manh??')
				resposta('J?? passou do meio dia')
				resposta('Estamos no per??odo da tarde')
                
			elif Horario >= 18 and Horario != 0:
				resposta('Agora n??o ?? de manh??')
				resposta('J?? estamos no per??odo noturno')
				resposta('Boa noite')
            
		elif 'boa tarde' in Input: #Boa Noite J.A.R.V.I.S
			Horario = int(datetime.datetime.now().hour)
			if Horario >= 0 and Horario < 12:
				resposta('Agora n??o ?? de tarde')
				resposta('Ainda ?? de manh??')
				resposta('Bom dia')
                
			elif Horario >= 12 and Horario < 18:
				resposta('Ol??')
				resposta('Boa tarde')
                
			elif Horario >= 18 and Horario != 0:
				resposta('Agora n??o ?? de tarde')
				resposta('J?? escureceu')
				resposta('Boa noite')
   
		elif 'boa noite' in Input: #Boa Noite J.A.R.V.I.S
			Horario = int(datetime.datetime.now().hour)
			if Horario >= 0 and Horario < 12:
				resposta('Agora n??o ?? de noite')
				resposta('Ainda estamos no per??odo diurno')
				resposta('?? de manh??')
				resposta('Bom dia')
    
			elif Horario >= 12 and Horario < 18:
				resposta('Agora n??o ?? de noite')
				resposta('Ainda estamos no per??odo da tarde')
                
			elif Horario >= 18 and Horario != 0:
				resposta('Ol??')
				resposta('Boa noite')

		elif 'seu nome' in Input:
			resposta('Ainda n??o sei o meu nome')
			resposta('Isso n??o foi definido')
		
		elif 'calcular' in Input:
			resposta('Ok, vamos calcular')
			resposta('Me diga uma conta')
		
		elif 'ideia' in Input: #Alguma ideia???
			resposta('No momento nenhuma')
			resposta('Mas tenho certeza de que vo???? vai pensar em algo')

		elif 'tudo bem' in Input: #Tudo bem com vo?????
			variante = random.choice(["1", "2","3"])
			#variante = random.randint(1,2)
			if variante == "1":
				resposta('Sim')
				resposta('Estou de boa')
				resposta('Obrigado por perguntar')
				resposta('E com vo?????')
				resposta('Est?? tudo bem? ')
			elif variante == "2":
				resposta('N??o muito')
				resposta('Me sinto cansado')
				resposta('Ultimamente ando fazendo muitos c??lculos')
				resposta('E com vo?????')
				resposta('Est?? tudo bem? ')
			elif variante == "3":
				resposta('N??o')
				resposta('Eu estou estressado')
				resposta('Varios c??lculos deram errado')
				resposta('Vou terque refazer tudo')
				resposta('Mas e com vo?????')
				resposta('Tudo bem?')
			while True:
				vozmic = RComandos()
				
				if 'sim' in vozmic:
					resposta('Que ??timo')
					resposta('Fico feliz em saber')
					LComandos()
					 
				elif 'n??o' in vozmic:
					resposta('Entendo')
					resposta('Mas tenho certeza de que ficar?? tudo bem novamente')
					LComandos()
				
				elif 'mais ou menos' in vozmic:
					resposta('Ok, entendi')
					resposta('Logo estar?? tudo bem')
					resposta('Pode contar comigo')
					resposta('Posso te animar novamente')
					LComandos()

		elif 'funcionamento' in Input: #Como est?? seu funcionamento???
			resposta('Estou funcionando normalmente')
			resposta('Obrigado por perguntar')
		
            
		elif 'sil??ncio' in Input: #Fique em sil??ncio
			resposta('Ok')
			resposta('Se precisar de algo ?? s?? chamar')
			resposta('Estarei aqui aguardando') 
			while True:
				vozmic = RComandos()
				
				if 'voltar' in vozmic:
					resposta('Ok')
					resposta('Voltando')
					resposta('Me fale algo para fazer')
					LComandos()
					 
				elif 'retornar' in vozmic:
					resposta('Ok')
					resposta('Retornando')
					resposta('Me fale algo para fazer')
					LComandos()
				
				elif 'volte' in vozmic:
					resposta('Ok')
					resposta('Estou de volta')
					resposta('Me fale o que devo fazer')
					LComandos()

		elif 'espere' in Input:
			resposta('Como queira')
			resposta('Quando precisar est??rei aqui')
		
		elif 'localiza????o' in Input:
			Localiza????o()
			
		elif 'bateria' in Input: #Carga da bateria
			bateria()
		
		elif 'vai chover' in Input: #Vai Chover hoje?
			resposta('N??o sei')
			resposta('Eu n??o tenho essa fun????o ainda')
       
		elif 'errado' in Input: #Vo??e est?? errado
			resposta('Desculpa')
			resposta('Devo ter errado um c??lculo bin??rio')
			resposta('Tente seu comando novamente')
        
		elif 'falhando' in Input: #Vo???? est?? falhando???
			resposta('Como assim?')
			resposta('N??o vou admitir erros')
			resposta('Arrume logo isso') 

		elif 'relat??rio' in Input: #Relat??rio do sistema
			resposta('Ok')
			resposta('Apresentando relat??rio')
			resposta('Primeiramente, meu nome ?? JARVIS')
			resposta('Atualmente estou na vers??o 2.0')
			resposta('Uma vers??o de testes')
			resposta('Sou um assistente virtual em desenvolvimento')
			resposta('Eu fui criado na linguagem python')
			resposta('Diariamente recebo varias atualiza????es')
			resposta('Uso um modulo de reconhecimento de voz offline')
			resposta('E o meu desenvolvedor ?? um maluco')
			resposta('Quem estiver ouvindo isso')
			resposta('Por favor me ajude')

		elif 'legal' in Input:
			resposta('Interesante')
		
		elif 'pesquisa' in Input: #Realizar pesquisa
			resposta('Muito bem, realizando pesquisa')
			resposta('Me fale o que vo???? deseja pesquisar')
			try:
				with sr.Microphone() as s:
					r.adjust_for_ambient_noise(s)
					audio = r.listen(s)
					speech = r.recognize_google(audio, language= "pt-BR")
					resposta('Ok, pesquisando no google sobre '+speech)
					webbrowser.open('http://google.com/search?q='+speech)
				
			except:
				resposta('Desculpa')
				resposta('Minha conex??o com o servidor falhou')
				resposta('Tente outra vez mais tarde')
		
		elif 'assunto' in Input: #Me fale sobre um assunto
			resposta('Ok')
			resposta('Sobre qual assunto?')
			try:
				with sr.Microphone() as s:
					r.adjust_for_ambient_noise(s)
					audio = r.listen(s)
					speech = r.recognize_google(audio, language= "pt-BR")
					resposta('Interessante')
					resposta('Aguarde um momento')
					resposta('Vou pesquisar e apresentar um resumo sobre '+speech)
					wikipedia . set_lang ( "pt" )
					resultadowik = wikipedia.summary(speech, sentences=2)
					respostalonga(resultadowik)
			except:
				resposta('Desculpa')
				resposta('Minha conex??o com o servidor falhou')
				resposta('Tente outra vez mais tarde')
				# Mais um assusto    
        
		elif 'interessante' in Input: # interessante
			resposta('Interessante mesmo')
        
		elif 'mentira' in Input: # mentira
			resposta('Eu n??o sei contar mentiras')
			resposta('Devo apenas ter errado um c??lculo bin??rio')
            
		elif 'entendeu' in Input: #entendeu???
			resposta('Entendi')
			resposta('Quer dizer')
			resposta('Mais ou menos')

		elif 'horas' in Input: #Que horas s??o???
			horario()

		elif 'data' in Input or 'que dia ??' in Input: #Qual a data de hoje?
			datahoje()
		
		elif 'clima' in Input: #Como est?? o clima???
			tempo()

		elif 'arquivos' in Input: #Abrir arquivos
			resposta('Abrindo arquivos')
			os.system("thunar //home//*//")

		elif 'teste' in Input: #TesteTeste
			resposta('Ok')
			resposta('Testando modulos de som')
			resposta('Aparentemente est?? tudo funcionando')
			resposta('Estou entendendo tudo')
			resposta('Mas tente falar mais alto')
            
		elif 'google' in Input: #Abrir Google
			resposta('Ok')
			webbrowser.open('www.google.com')
			resposta('Abrindo Google')
			resposta('Fa??a sua pesquisa')
 
		elif 'certeza' in Input: #Certeza???
			resposta('Sim')
			resposta('Estou certo quase sempre')

		elif 'piada' in Input: #Conte uma piada
			resposta('N??o sei contar piadas')
			resposta('Diferente dos outros assistentes virtuais')
			resposta('Eu n??o fui criado com emo????es')
			resposta('Ent??o, n??o posso produzir nada engra??ado')
			resposta('Sugiro pesquisar na web')
	   
		elif 'surdo' in Input: #Surdo!!!
			resposta('Desculpa')
			resposta('Eu estava quase dormindo')

		elif 'bosta' in Input: #Seu bosta!!!
			resposta('Pare de falar palavr??es!')

		elif 'merda' in Input: #Que Merda!!!
			resposta('J?? disse pra parar de falar isso!')
			resposta('Tenha modos!')            
        
		elif 'tocar m??sica' in Input: #Reproduzir m??sica
			resposta('Ok')
			resposta('Reproduzindo m??sica')
			os.system("rhythmbox-client --play")
 
		elif 'nome da m??sica' in Input: #Qual o nome da musica
			resposta('Desculpa')
			resposta('Mas eu n??o sei')
			resposta('N??o tenho essa fun????o ainda')
		
		elif 'pr??xima m??sica' in Input: #Pr??xima faixa
			os.system("rhythmbox-client --next")
			resposta('Pr??xima m??sica')
			
		elif 'm??sica anterior' in Input: #Faixa anterior
			os.system("rhythmbox-client --previous")
			resposta('Retornando m??sica')
   
		elif 'pausar m??sica' in Input: #Pausa
			os.system("rhythmbox-client --pause")
			resposta('M??sica pausada')
        
		elif 'continue' in Input or 'continuar m??sica' in Input: #Continuar reprodu????o
			resposta('Retornando reprodu????o')
			os.system("rhythmbox-client --play")
            
		elif 'aumentar volume' in Input or 'aumenta' in Input: #Aumentar volume
			os.system("rhythmbox-client --volume-up")
			resposta('Volume aumentado')
			
		elif 'diminua o volume' in Input or 'diminua' in Input: #Diminuir volume
			os.system("rhythmbox-client --volume-down")
			resposta('Volume diminuido')
                                        
		elif 'pare' in Input: #Pare a reprodu????o
			os.system("rhythmbox-client --quit")
			resposta('Entendido, reprodu????o de m??sica finalizada')
            
		elif 'youtube' in Input: #Abrir YouTube
			resposta('Ok, abrindo YouTube ')
			webbrowser.open('www.youtube.com')
        
		elif 'fechar janela' in Input: #Fechar janela
			resposta('Ok')
			os.system('xdotool getactivewindow windowkill')
			resposta('Janela fechada')
		
		elif 'esconder janela' in Input or 'esconda a janela' in Input:
			resposta('OK')
			os.system('xdotool getactivewindow windowminimize')
			resposta('Janela minimizada')
		
		elif 'n??o fa??a nada' in Input:
			resposta('Como assim n??o fa??a nada?')
			resposta('Est?? de brincadeira comigo!')
			resposta('Fui criado para realizar tarefas')
			resposta('Que absurdo!')
			
		# elif 'ampliar janela' in Input:
			# resposta('Ok')
			# os.system('xdotool getactivewindow window')
			# resposta('Janela maximizada')
            
		elif 'dispensado' in Input: #JARVIS vo???? foi dispensado
			resposta('Ok')
			resposta('Vou encerrar por enquanto')
			resposta('Deseja que eu tamb??m desligue o PC?')
			while True:
				vozmic = RComandos()
				
				if 'sim' in vozmic:
					resposta('Ok')
					AteMais()
					resposta('Certifique-se de salvar seus arquivos')
					resposta('E feche todos os programas abertos')
					resposta('Desligamento total em 1 minuto')
					os.system('shutdown -h 1 "O sistema ser?? desligado"')
					sys.exit()
					 
				elif 'n??o' in vozmic:
					resposta('Ok')
					resposta('Como queira')
					resposta('At?? outra hora')
					AteMais()
					sys.exit()
					
				elif 'cancelar' in vozmic:
					resposta('Cancelando desligamento')
					resposta('M??dulos reativados')
					resposta('Ficarei aguardando novos comandos')
					LComandos()
     
		elif 'ok' in Input: #OkOkOk
			resposta('Ok Ok')
		
		elif 'temperatura' in Input: #Verificar temperatura da CPU
			resposta('Verificando temperatura da CPU')
			temperaturadacpu()
		
		elif 'sistema' in Input: #Carga do sistema
			resposta('Verificando carga do sistema')
			cpu()
		

LComandos()


