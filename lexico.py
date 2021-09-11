import tkinter as tk
from tkinter import scrolledtext as st
import sys
import re
from tkinter import filedialog as fd
from tkinter import messagebox as mb

class Aplicacion:
    
    def __init__(self):
        self.ventana1 = tk.Tk()
        self.ventana1.title("Contador de palabras")
        self.agregar_menu()          
        self.patronNumeros = re.compile("[+-]?([0-9]*[.])?[0-9]+")
        self.patronCadenas = re.compile('"[\w\s]*"')                
        self.patronComentarios = re.compile("\/\*[\w\s]*\*\/|\/\/[\w\s]*")
        self.tokensEspeciales = ['¿', '?','@','°','^','~','`','{', '}', ';',':', '/',',', '+','*', '-','(',')', '¡','!','==', '>=','=>','!=','&&', '||','<', '>','=','+=','-=','*=','/=','#','$','%','&','|','[', ']','.']
        self.scrolledtext1= st.ScrolledText(self.ventana1,width=80, height=20)
        self.scrolledtext1.grid(column=0, row=0, padx=10,pady=10)
        self.scrolledtext1.insert("1.0", "Seleccione un archivo en la pestaña ARCHIVO")
        self.ventana1.mainloop()
    
    def agregar_menu(self):
        menubar1 = tk.Menu(self.ventana1)
        self.ventana1.config(menu=menubar1)
        opciones1 = tk.Menu(menubar1, tearoff=0)
        opciones1.add_command(label="Abrir archivo", command=self.abrir)
        opciones1.add_separator()
        opciones1.add_command(label="Salir", command=self.salir)
        menubar1.add_cascade(label="Archivo", menu=opciones1)
    
    def salir(self):
        sys.exit(0)

    def abrir(self):
        nombrearch = fd.askopenfilename(initialdir="c:", title="Seleccione archivo", filetypes=(("txt files", "*.txt"),("todos los archivos", "*.*")))    
        index = 0        
        if nombrearch!='':
            archi1 = open(nombrearch,"r", encoding="utf-8")
            self.contenido = archi1.read()
            archi1.close()
            self.temp = []     
            self.scrolledtext1.delete("1.0", tk.END)
            self.ignorarCadenas()
            self.ignorarComentarios()
            palabras = self.contenido.split()
            longitud = len(palabras)
                   
            for i in range(longitud):
                if len(palabras[i]) >0:
                    palabraAnalizada = self.analizarPalabra(palabras[i])
                    if isinstance(palabraAnalizada, list):                      
                        for palabra in reversed(palabraAnalizada):
                            if palabra != "":
                                self.temp.insert(i, palabra)
                    else:
                        if palabraAnalizada != '':
                            self.temp.append(palabraAnalizada)
                else:
                    self.temp.append(palabras[i])
    
           ## print(temp)   
            mensaje = "El número de palabras sin repetir del archivo es "+ str(len(self.temp))
            for palabra in self.temp:
                self.scrolledtext1.insert("1.0", palabra +"\n")
            self.scrolledtext1.insert("1.0", "----PALABRAS----\n")
            self.scrolledtext1.insert("1.0", mensaje + "\n\n")
            
    def ignorarComentarios(self):
        comentario = "x"
        try:
            while comentario != "":                    
                comentario = re.search(self.patronComentarios, self.contenido).group(0)                 
                print(comentario)
                comentario = comentario.replace("/*", "\/\*")
                comentario = comentario.replace("*/", "\*\/")
                print(comentario)
                a = re.split(comentario, self.contenido)
                self.contenido = " ".join(a)                 
        except AttributeError:
            pass
    
    def ignorarCadenas(self):
        cadena = "x"
        try:
            while cadena != "":
                cadena = re.search(self.patronCadenas, self.contenido).group(0)                    
                self.temp.append(cadena)
                a = re.split(cadena, self.contenido)                   
                self.contenido = " ".join(a)                    
        except AttributeError:
            pass

    def analizarPalabra (self, palabra):                
        res=[]  
        for token in self.tokensEspeciales:                    
            ocurrencias = palabra.count(token)
            if ocurrencias > 0:    
                for i in range(ocurrencias):                                                           
                    res.append(token)
                palabraDividida = palabra.split(token)    
                for subPalabra in palabraDividida:
                    if len(subPalabra)>1:    
                        if isinstance(subPalabra, str):
                            isNumber = self.patronNumeros.fullmatch(subPalabra)                                                                     
                        if not isNumber:
                            palabraAnalizada =self.analizarPalabra(subPalabra)
                            if isinstance(palabraAnalizada,list):
                                for item in palabraAnalizada:
                                    res.append(item)
                            elif palabraAnalizada != "":
                                res.append(palabraAnalizada)
                        else:
                            res.append(subPalabra)
                    else:
                        res.append(subPalabra)
                break

        if len(res) >0:        
            return res
        else:     
            return palabra

aplicacion1 = Aplicacion()

