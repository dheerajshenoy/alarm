import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

import kivy 
from kivymd.app import MDApp
#from android.storage import primary_external_storage_path
#from android.permissions import request_permissions, Permission
#request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
from kivy.clock import Clock 
from kivymd.uix.dialog import MDDialog
from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivymd.uix.button import MDFlatButton as Button
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty
from plyer import accelerometer, tts, notification, filechooser
#from kivy.clock import mainthread
from os import path
from kivy.logger import Logger
from kivymd.uix.label import MDLabel as Label
from kivymd.uix.picker import MDDatePicker
from os.path import join
#import configparser
#from kivy.lang import Builder
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDFlatButton
from kivy.uix.gridlayout import GridLayout
import time 



class alarm(MDApp):
    def build(self):
        #self.theme_cls.theme_style="Dark"
        
        global store 
        global KEYS
        KEYS = []
        store = JsonStore(join(self.user_data_dir,"alarms.json"))
        sm = ScreenManager()
        sm.add_widget(mainWindow(name='mainwindow'))
        sm.add_widget(alarmWindow(name='alarmwindow'))
        
        for keys in store:
            for ele in store[keys]:
                KEYS.append(store[keys][ele])
        return sm
    
    @classmethod 
    def fire_alarm(cls):
                




class alarmCard(MDCard):
    global store

    def on_delete(self, instance):
        #if(self.show_dialog()):
            ID = instance.id
            ID = ID.replace("delete_key",'')
            print(ID)
            store.delete(ID)
            alarmWindow.refresh()

        

    def show_dialog(self):
        confirm_dialog = MDDialog(text="Are You Sure?",buttons=[MDFlatButton(text="Cancel",on_press=lambda x: confirm_dialog.dismiss()),MDFlatButton(text="Yes")])
        confirm_dialog.open()
        return True

class mainWindow(Screen):
    global store
    tree = ObjectProperty()
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        

        if(len(store) != 0):
            for keys in store:
                card = alarmCard()
                lb = Label(text=keys,font_style="H4")
                sw = MDSwitch(id="aa"+keys,pos_hint={"right":0.96})
                dsw = MDRaisedButton(text="Delete",pos_hint={"right":1},md_bg_color=(1,0,0,1),id="delete_key"+keys)
                card.add_widget(lb)
                card.add_widget(sw)
                card.add_widget(dsw)
                dsw.bind(on_release=card.on_delete)
                self.ids.tree.add_widget(card)
    
    def update_alarm(self):
        self.ids.tree.clear_widgets()
        for keys in store:
            card = alarmCard()
            lb = Label(text=keys,font_style="H4")
            sw = MDSwitch(id="aa"+keys,pos_hint={"right":0.96})
            dsw = MDRaisedButton(text="Delete",pos_hint={"right":1},md_bg_color=(1,0,0,1),id="delete_key"+keys)
            card.add_widget(lb)
            card.add_widget(sw)
            card.add_widget(dsw)
            dsw.bind(on_release=card.on_delete)
            self.ids.tree.add_widget(card)
         
    def changeScreen(self):
        self.parent.current = 'alarmwindow'
        self.parent.transition.direction = 'left'

class alarmWindow(Screen):
    date = ObjectProperty()
    repeat = ObjectProperty()
    time = ObjectProperty()
    ringtone_file_name = ObjectProperty()
    label = ObjectProperty()
    ok_button = ObjectProperty()

        

    def getinfo(self):
        global Date
        global Time
        global Repeat
        global Name
        global Ringtone_file_name
        global store 
         

        #try:
            
        #store.put(str(len(store)),label=str(Name),date=str(Date),time=str(Time),ringtone=str(Ringtone_file_name),repeat=bool(Repeat))
        try:
            store[str(len(store))] = {'label':str(Name),'date':str(Date),'time':str(Time),'ringtone':str(Ringtone_file_name),'repeat':bool(Repeat)}
        except NameError:
            Repeat = False
            store[str(len(store))] = {'label':str(Name),'date':str(Date),'time':str(Time),'ringtone':str(Ringtone_file_name),'repeat':bool(Repeat)}

    def get_label(self):
        self.ids.ok_button.disabled = True
        global Name
        Name = self.ids.label.text
        self.check_empty()
    
        alarm().fire_alarm()

    def update_ringtone(self,selection):
        self.ids.display_file_name.text = str(selection) 
    
    def check_empty(self):
        global Date
        global Time
        global Repeat
        global Name
        global Ringtone_file_name
        Name = self.ids.label.text

        if(Name!= ""):
            try:
                print(Name)
                print(Time)
                print(Name)
                print(Ringtone_file_name)
                self.ids.ok_button.disabled = False

            except NameError:
                pass
        else:
            self.ids.ok_button.disabled = True

    def get_date(self, date):
        global Date
        Date = date
        self.check_empty()

    def show_date_picker(self):
        date_dialog = MDDatePicker(callback=self.get_date)
        date_dialog.open()
    
    def get_time(self, instance, time):
        global Time
        Time = time
        self.check_empty()

    
    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()
    

    def get_repeat(self,checkbox,value):
        global Repeat
        Repeat = bool(value)
        self.check_empty()

    def show_file_manager(self):
        path='/'
        #path = app_storage_path()
        self.file_manager = MDFileManager(select_path = self.select_path,ext=['mp3','ogg','flac'])
        self.file_manager.show(path)

    def select_path(self,path):
        global Ringtone_file_name
        Ringtone_file_name = path
        self.file_manager.close()
        self.check_empty()
    
    def clear_data(self):
        global Repeat
        global Ringtone_file_name
        global Name
        global Time
        global Date

        Repeat = ""
        Ringtone_file_name = ""
        Name  = ""
        Time = ""
        Date = ""

        self.ids.repeat.active = False
        self.ids.ringtone_file_name.text = ""
        self.ids.label.text = "" 

    @classmethod
    def refresh(cls):
        #popup = Popup(title="Refresh",
        #content=Label(text="Please Refresh the page to view the currently added alarm",font_style="H5",halign="center",theme_text_color="Custom",text_color=(1,1,1,1)),
        #size_hint=(None,None),
        #size=(400,400))
        #popup.open()
        dialog = MDDialog(text="Please refresh the page", size_hint=(None,None),size=(400,400),buttons=[ MDFlatButton(text="OK",on_press= lambda x: dialog.dismiss())])
        dialog.open()
if __name__ == "__main__":
    alarm().run()

