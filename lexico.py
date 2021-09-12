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
        self.tokensEspeciales = ['?','{', '}','[', ']',';','(',')','++','--','<<=','>>=','>>>=','&=','^|','|=','==', '>=','=>','!=','&&', '||','+=','-=','*=','/=','%=','+','*','-','^','<', '>','=','#','$','%','&','¡','!','|',':', '/','\\',',','~','`','¿']
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
            self.result = {}     
            self.tablaSimbolos = {}
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
                                self.result[palabra] = self.etiquetarToken(palabra)                    
                              #self.result.insert(i, palabra)
                    else:
                        if palabraAnalizada != '':
                            self.result[palabraAnalizada] = self.etiquetarToken(palabraAnalizada)      
                          #self.result.append(palabraAnalizada)
                else:
                    self.result[palabras[i]] = self.etiquetarToken(palabras[i])
                  #self.result.append(palabras[i])
    
           ## print(temp)   
            mensaje = "El número de palabras sin repetir del archivo es "+ str(len(self.result.keys()))
            for simbolo, descripcion in self.tablaSimbolos.items():
                self.scrolledtext1.insert("1.0", simbolo +" --> "+descripcion+"\n")
            self.scrolledtext1.insert("1.0", "----TABLA DE SIMBOLOS----\n")
            for token, descripcion in self.result.items():
                self.scrolledtext1.insert("1.0", token +" --> "+descripcion+"\n")
            self.scrolledtext1.insert("1.0", "----TOKENS----\n")
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
                self.result.append(cadena)
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
    def etiquetarToken(self, token):
        resultado = ""
        isLetra = re.compile("[a-zA-Z]")
        isIdentificador = re.compile("[_$]")
        isNumber = re.compile("[0-9]")      
        if (isLetra.fullmatch(token[0])):
            #Analizar si es una palabra reservada
            resultado = self.identificarCategoria(token, "palabrasReservadas")
            if(resultado != ""):
                #Analizar si es un identificador			
                patron = re.compile("([a-zA-Z][0-9]?)+")
                if(patron.fullmatch(token)):
                    resultado = "Identifier"
                    self.tablaSimbolos[token] = "Identifier"
        elif isIdentificador.fullmatch(token[0]):
            #Analizar si es un identificador        
            patron = re.compile("[_$]?([a-zA-Z][0-9]?)+|[_$][0-9]+")
            if(patron.fullmatch(token)):
                resultado = "Identifier"
                self.tablaSimbolos[token] = "Identifier"
            else:
                if(token == "_"):
                    resultado = "Underscore"
                elif (token == "$"):
                    resultado = "Dollar sign"
        elif isNumber.fullmatch(token[0]):
            #analizar si es un numero
            resultado = self.identificarCategoria(token, "digits")   
        elif token[0]== "\"":
            #Analizar si es un string        
            patron = re.compile('"[\w\s]*"')
            if(patron.fullmatch(token)):
                resultado = "Character string"
        else:
            #analizar si es un operador
            resultado = self.identificarCategoria(token, "operadores") 

        return resultado
    def identificarCategoria(self, token, mapa):
        resultado = ""
        for llave, valor in mapa.items():
            patron = re.compile(valor)
            if patron.fullmatch(token):
                resultado = llave
                break
        return resultado
aplicacion1 = Aplicacion()