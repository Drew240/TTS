import pyttsx3
import dearpygui.dearpygui as dpg
import os
import tkinter as tk
from tkinter import filedialog


engine = pyttsx3.init()


#Esto Carga el archivo con el cuadro de Windows
def load_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path,'r') as f:
            text = f.read()
            dpg.set_value("text_input", text)


#Esto es la funcion del text to speech
def speak():
    text = dpg.get_value("text_input")
    save_folder = filedialog.askdirectory()
    
   # Guardar audio
    save_path = dpg.get_value("save_path")
    if save_path:
        save_path = save_path + ".wav"
        engine.save_to_file(text, save_path)

#Esto es por error que no leia bien el texto    
    voices = engine.getProperty('voices')
    voice_map = {voice.name: i for i, voice in enumerate(voices)}
    selected_voice = dpg.get_value("voice_combo")
    voice_index = voice_map[selected_voice]
    engine.setProperty('voice', voices[voice_index].id)
    engine.setProperty('rate', dpg.get_value("rate_slider"))
    engine.setProperty('volume', dpg.get_value("volume_slider"))


    #Esto da las palabras y caractares al final
    words = len(text.split())
    chars = len(text)
    
    engine.say(text)
    engine.runAndWait()

    # Muestra el popup de confirmación
    dpg.show_item("confirmation_popup")
    dpg.set_value("stats_text", f"Palabras: {words}\nCaracteres: {chars}\nArchivo guardado: {save_path}")



 #Esto Crea la ventana con los botones
dpg.create_context()
with dpg.window(label="Conversor de Texto a Voz"):
    
    dpg.add_button(label="Cargar Archivo", callback=load_file)
    dpg.add_input_text(tag="text_input", multiline=True)

#esto seleccion la voz
    voices = engine.getProperty('voices')
    voice_names = [voice.name for voice in voices]
    dpg.add_combo(label="Seleccionar voz", items=voice_names, default_value=voice_names[0], tag="voice_combo")

    # Control de velocidad
    dpg.add_slider_int(label="Velocidad", min_value=50, max_value=250, default_value=150, tag="rate_slider")

    # Control de volumen
    dpg.add_slider_float(label="Volumen", min_value=0.0, max_value=1.0, default_value=1.0, tag="volume_slider")

    # Ruta para guardar el archivo
    dpg.add_input_text(label="Insertar nombre:", tag="save_path")
    dpg.add_button(label="Reproducir y Guardar", callback=speak)

    # ventana de confirmación
    with dpg.window(label="Resultado", modal=True, show=False, tag="confirmation_popup"):
        dpg.add_text(tag="stats_text")

    with dpg.window(label="Error", modal=True, show=False, tag="error_popup"):
     dpg.add_text(tag="error_text")


dpg.create_viewport(title='Conversor de Texto a Voz', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.start_dearpygui()   
dpg.destroy_context()