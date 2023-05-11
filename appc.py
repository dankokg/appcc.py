import os
import ezdxf
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView, FileSystemAbstract
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserListView, FileSystemAbstract

class MainWindow(Screen):
    def select_file(self, *args):
        # Creamos un file chooser para seleccionar el archivo
        self.file_chooser = FileChooserListView(
            path=FileSystemAbstract.expanduser("~"),
            filters=["*.dwg"],
            on_submit=self.on_file_selected,
            on_cancel=self.remove_file_chooser
        )
        # Agregamos el file chooser a la ventana principal
        self.add_widget(self.file_chooser)

    def remove_file_chooser(self, *args):
        # Cerramos el file chooser
        self.remove_widget(self.file_chooser)

        # Creamos un file chooser para seleccionar el archivo
        self.file_chooser = FileChooserListView(
            path=FileSystemAbstract.expanduser("~"),
            filters=["*.dwg"]
        )
        self.file_chooser.bind(on_submit=self.on_file_selected)

    def select_file(self, *args):
        # Mostramos el file chooser para seleccionar el archivo
        self.add_widget(self.file_chooser)

    def on_file_selected(self, file_chooser):
        # Cerramos el file chooser
        self.remove_widget(self.file_chooser)
        # Guardamos la ruta seleccionada en self.file_path
        self.file_path = file_chooser.selection[0]
        # Imprimimos la ruta del archivo seleccionado
        print("Archivo seleccionado:", self.file_path)

    def quantify_materials(self, *args):
        # Si no se ha seleccionado ningún archivo, mostramos un error
        if not self.file_path:
            print("Debe seleccionar un archivo DWG")
            return

        # Leemos el archivo DWG
        dwg = ezdxf.readfile(self.file_path)
        # Buscamos todos los objetos de tipo "TEXT"
        texts = dwg.modelspace().query('TEXT')
        # Inicializamos un diccionario para almacenar los materiales y sus cantidades
        materials = {}


        # Recorremos todos los textos y buscamos los que contienen "Material" y "Cantidad"
        for text in texts:
            if "Material" in text.dxf.text:
                # Extraemos el nombre del material
                material = text.dxf.text.split(":")[1].strip()
                # Buscamos el texto que indica la cantidad
                for neighbor in text.nearest(2):
                    if "Cantidad" in neighbor.dxf.text:
                        # Extraemos la cantidad y la convertimos a un número entero
                        quantity = int(neighbor.dxf.text.split(":")[1].strip())
                        # Si el material ya existe en el diccionario, sumamos la cantidad
                        if material in materials:
                            materials[material] += quantity
                        else:
                            materials[material] = quantity

        # Imprimimos los resultados
        for material, quantity in materials.items():
            print(material, quantity)

class MyApp(BoxLayout):
    def read_file(self):
        # código para leer archivo y procesar materiales
        pass

    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)

        # Widget Label
        self.add_widget(Label(text="Bienvenido a la aplicación de cuantificación de materiales"))

        # Widget Button
        self.btn = Button(text="Seleccionar archivo", size_hint_y=None, height=50)
        self.btn.bind(on_press=self.select_file)
        self.add_widget(self.btn)

        # Instanciamos la clase MainWindow
        self.main_window = MainWindow()

    def select_file(self, *args):
        # Llamamos al método select_file de la clase MainWindow
        self.main_window.select_file()

        # Removemos el botón después de haberlo presionado
        self.remove_widget(self.btn)

class MainApp(App):
    def build(self):
        return MyApp()

if __name__ == '__main__':
    MainApp().run()
