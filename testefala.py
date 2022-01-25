#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  testefala.py
#  
#  Copyright 2021 DARK <dark@DARK-PC>
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
import pyaudio
import json
import os

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

if not os.path.exists("PTBR"):
	print ("Modelo em portugues nao encontrado.")
	exit (1)

model = Model("PTBR")
rec = KaldiRecognizer(model, 16000)

# def RComandos():
	# rec.pause_threshold = 1
	# data = stream.read(20000)
	# rec.AcceptWaveform(data)
	# res = json.loads(rec.Result())
	# saida = str(res['text'])
	# return saida

def RComandos():
	data = stream.read(8000)
	if len(data) == 0:
		None
	if rec.AcceptWaveform(data):
		result = rec.Result()
		resultado = json.loads(result)
		if result is not None:
			texto = resultado['text']
			print(texto)
		


while True:
	RComandos()



