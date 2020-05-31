from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from lib.KivyCalendar import DatePicker
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
import music_creator
from kivy.uix.popup import Popup
import wave
import pyaudio
from threading import Thread
import pygame
import time
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import random
import sys
import time
import threading
import datetime


class Read(threading.Thread):

	"""Thread chargé simplement d'afficher une lettre dans la console."""

	def __init__(self,list_chunk,screen):
		Thread.__init__(self)
		self.list_chunk=list_chunk
		self.screen=screen
		app=App.get_running_app()
		app.enable=True


	def run(self):
		"""Code à exécuter pendant l'exécution du thread."""
		
		
		waveFile = wave.open(music_creator.path_data_out+'out.wav', 'r')
		#open a wav format music  
		f = wave.open(music_creator.path_data_out+'out.wav',"rb")  
		#instantiate PyAudio  
		p = pyaudio.PyAudio()  
		#open stream  
		stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
					channels = f.getnchannels(),  
					rate = f.getframerate(),  
					output = True)  
		#read data  
		data = f.readframes(self.list_chunk[0][1])
		self.screen.list_color_bx[0].update([0, 1, 0, self.list_chunk[0][0]])
		self.screen.legend_current.text=(datetime.datetime.strptime(
							self.screen.legend_current.text,
							'%Y-%m-%d')+datetime.timedelta(days=int(self.screen.granule.text))).strftime('%Y-%m-%d')
		count=1
		p = pyaudio.PyAudio()
		stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
					channels = f.getnchannels(),  
					rate = f.getframerate(),  
					output = True)
		#play stream  
		while data: 
			stream.write(data) 
			try:			
				data = f.readframes(self.list_chunk[count][1])
				app=App.get_running_app()
				if app.enable:
					self.screen.list_color_bx[count].update([0, 1, 0, self.list_chunk[count][0]])
					self.screen.legend_current.text=(datetime.datetime.strptime(
						self.screen.legend_current.text,
						'%Y-%m-%d')+datetime.timedelta(days=int(self.screen.granule.text))).strftime('%Y-%m-%d')
					count=count+1
				else:
					break
			except:
				break
		#stop stream  
		stream.stop_stream()  
		stream.close()  
		#close PyAudio  
		p.terminate()
		



class BackButton(Button):
	def __init__(self,screen,**kwargs):
		super().__init__(**kwargs)
		self.screen=screen
	
	def on_release(self):
		self.screen.popup.dismiss()
		app=App.get_running_app()
		app.enable=False
	

	
Window.clearcolor=(0.5,0.5,0.5,1)



class LabelColored(Label):
	def update(self,color):
		self.canvas.before.clear()
		with self.canvas.before:
			Color(color[0], color[1], color[2], color[3])
			Rectangle(pos=self.pos, size=self.size)


class PlayButton(Button):
	def __init__(self,list_chunk,screen,**kwargs):
		super().__init__(**kwargs)
		self.list_chunk=list_chunk
		self.screen=screen

	def on_release(self):
		if self.text=='Stop':
			app=App.get_running_app()
			app.enable=False
			self.text='Read'
			self.screen.legend_current.text=self.screen.legend_start.text
			print(len(self.screen.list_color_bx))
			for i in self.screen.list_color_bx:
				i.update([0,0,0,0])
			print('y')
		else:
			self.screen.thread_lect=Read(self.list_chunk,self.screen)
			self.screen.thread_lect.start()
			self.text='Stop'
		


		

class CustomDatePicker(DatePicker):
    def update_value(self, inst):
        """ Update textinput value on popup close """
        self.text = "%s.%s.%s" % tuple(self.cal.active_date)
        self.focus = False
        App.get_running_app().root.ids.ti.text = self.text


class Screen1(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
	 
	def stop_thread(self,instance):
		app=App.get_running_app()
		app.enable=False

	def on_press(self):
		start_date=self.start_date.text.split('.')[-1]+'-'+(self.start_date.text.split('.')[1]).zfill(2)+'-'+(self.start_date.text.split('.')[0]).zfill(2)
		end_date=self.end_date.text.split('.')[-1]+'-'+(self.end_date.text.split('.')[1]).zfill(2)+'-'+(self.end_date.text.split('.')[0]).zfill(2)
		self.music=music_creator.MusicCreator(self.spinner[0].text,
									self.spinner[1].text.split(' ')[-1],
									start_date,
									end_date,
									int(self.granule.text))
		self.box=BoxLayout(orientation='vertical')
		self.boxcontent=BoxLayout(orientation='vertical')
		self.boxtime=BoxLayout(size_hint=(1, 0.1))
		self.legend_start=LabelColored(text=start_date,font_size=15,color=(1,1,1,0.5))
		self.legend_current=LabelColored(text=start_date,font_size=30,size_hint=(0.9,1))
		self.legend_end=LabelColored(text=end_date,font_size=15,color=(1,1,1,0.5))
		self.boxtime.add_widget(self.legend_start)
		self.boxtime.add_widget(self.legend_current)
		self.boxtime.add_widget(self.legend_end)
		self.boxcontent.add_widget(self.boxtime)
		self.boxcolor=BoxLayout(size_hint=(1, 0.7))
		self.list_color_bx=[]
		for i in range(len(self.music.list_chunk)):
			self.labelcolor=LabelColored()
			self.boxcolor.add_widget(self.labelcolor)
			self.list_color_bx.append(self.labelcolor)
		self.boxcontent.add_widget(self.boxcolor)
		self.box.add_widget(self.boxcontent)
		self.boxbtn=BoxLayout(size_hint=(1, 0.2))
		self.boxbtn.add_widget(PlayButton(self.music.list_chunk,self))
		self.boxbtn.add_widget(BackButton(self,text='back',pos_hint={'x':0.1,'y':0.2},size_hint=(0.3, 0.5)))
		self.box.add_widget(self.boxbtn)
		self.popup=Popup(title='Your Space Song from '+self.spinner[0].text+' on '+self.spinner[1].text+' between '+start_date+' and '+end_date,title_color=(1,1,1,1),
		content = self.box,
		size_hint=(0.9,0.9)
		)
		self.popup.bind(on_dismiss=self.stop_thread)
		self.popup.open()
	
	def limit_spinner(self, *args):
		max=5
		for i in self.spinner:
			i.dropdown_cls.max_height= max *dp(30)

class Interface(App):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		#Load kivy template
		self.builder=Builder.load_file('./KivyTemplate/interface.kv')
		enable=True

	def stop(self):
		self.enable=False
	
	def build(self):
		self.title = "The Space Song"
		return self.builder

if __name__=='__main__':
	
	Interface().run()
	


