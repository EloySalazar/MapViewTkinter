import tkinter as tk

import customtkinter as ctk
import requests
import tkintermapview as tkm

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green") 

class App(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("MapView")
        self.geometry("800x800")
        self.initialize_gui()

    def search_address(self,event):

        self.map_view.set_address(self.address_entry.get())

    def add_marker_event(self,coords):

        print("Add marker:", coords)
        new_marker = self.map_view.set_marker(coords[0], coords[1], text="new marker")
        adr = tkm.convert_coordinates_to_address(coords[0],coords[1])
   

        url = f'http://api.openweathermap.org/data/2.5/weather?q={adr.state}&appid=ff22dd7e138d3aaf14c5cb5cac4a52ee&units=metric'
    
        res = requests.get(url)
        data = res.json()
        temp = data['main']['temp']

        self.temperature.configure(text = str(temp) + " °C ")
        self.country.configure(text = adr.state + " " + adr.country)

    def change_map(self):
        
        if self.var_radio_buton.get() == 1:

            self.map_view.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=100)
        
        else:

            self.map_view.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=1000) 

    def initialize_gui(self):

        self.map_frame = ctk.CTkFrame(self,width= 900,height= 1600)
        self.map_frame.pack(padx = 0,pady = 0,side = tk.RIGHT)

        self.address_entry = ctk.CTkEntry(self.map_frame,font = ("Arial",18),placeholder_text= "Address",width= 300)
        self.address_entry.pack(padx = 50,pady = 30)
        self.address_entry.bind('<Return>', self.search_address)

        self.search_buton = ctk.CTkButton(self.map_frame,font = ("Arial",19),text = "Search",command= lambda:self.search_address(None))
        self.search_buton.pack(padx = 0,pady = 0)

        self.var_radio_buton = tk.IntVar(value=0)

        self.google_radio_buton = ctk.CTkRadioButton(self.map_frame,font = ("Arial",20),text = "Google",variable=self.var_radio_buton,value= 1,command= self.change_map)
        self.google_radio_buton.pack(padx = 30,pady = 0)

        self.google_satelite_radio_buton = ctk.CTkRadioButton(self.map_frame,font = ("Arial",20),text = "Google Satelite",variable= self.var_radio_buton,value= 2,command= self.change_map)
        self.google_satelite_radio_buton.pack(padx = 80,pady = 0)

        self.temperature_label = ctk.CTkLabel(self,font = ("Arial",28),text= "Temperature:")
        self.temperature_label.pack(padx = 0,pady = 0)

        self.country = ctk.CTkLabel(self,font = ("Arial",22),text= "")
        self.country.pack(padx = 0,pady = 30)

        self.temperature = ctk.CTkLabel(self,font = ("Arial",22),text= "")
        self.temperature.pack(padx = 0,pady = 0)

        self.map_view = tkm.TkinterMapView(self.map_frame,width=800, height=600, corner_radius=0)
        self.map_view.pack(padx = 30,pady = 40)
        self.map_view.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=100)
        self.map_view.add_right_click_menu_command(label="Add Marker",
                                        command=self.add_marker_event,
                                        pass_coords=True)
        self.map_view.set_zoom(0)




app = App()
app.mainloop()