
from os import error
import tkinter as tk
from tkinter import scrolledtext as st
import sys
import re
import time
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.constants import HORIZONTAL, N

class Token:
    def setValues(self,token,descripcion):
        self.token = token
        self.descripcion = descripcion
    def mostrar(self):
         return (str(self.token) +" \t--> "+ self.descripcion + "\n")
class Aplicacion:
    
    def __init__(self):
        self.ventana1 = tk.Tk()
        F_font = ('bold', 15)
        self.ventana1.title("Analizador lexico")
        self.agregar_menu()          
        self.scrolledtext1= st.ScrolledText(self.ventana1,width=100, height=30, font=F_font)
        self.scrolledtext1.grid(column=0, row=0, padx=10,pady=10)
        self.scrolledtext1.insert("1.0", "Seleccione un archivo en la pestaña ARCHIVO")
        self.abrir()
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
        #nombrearch = fd.askopenfilename(initialdir="c:", title="Seleccione archivo", filetypes=(("txt files", "*.txt"),("todos los archivos", "*.*")))    
        nombrearch="C:\\Users\\crist\\Documents\\Noveno\\Compiladores\\T1\\compilador\\proyecto2\\codiguito.txt"  
        if nombrearch!='':
            archi1 = open(nombrearch,"r", encoding="utf-8")
            self.contenido = archi1.read()
            archi1.close()
            self.result = []
            self.tablaSimbolos = {}
            self.scrolledtext1.delete("1.0", tk.END)        
            #CODIGO PARA SEPARAR TOKENS Y ETIQUETARLOS
            indice = 0    
            lineaActual = 1;
            self.scope = 1
            inicio = time.time()
            numRegex = re.compile("[0-9]");
            letraRegex = re.compile("[a-zA-Z]");
            leyendoCadena = False
            leyendoChar=False
            leyendoIdentificador = False
            leyendoComentario = False
            leyendoComentarioMul = False
            token = ""
            numSimbols = 0
            while indice < len(self.contenido):
                actual = self.contenido[indice]
                if(indice < len(self.contenido)-1):
                    siguiente = self.contenido[indice+1]
                else:
                    siguiente = "\n"

                if leyendoIdentificador:       
                    if letraRegex.fullmatch(actual) or numRegex.fullmatch(actual) or actual == '_':
                        token += actual
                        indice+=1
                    else:
                        self.agregarALista(token)
                        leyendoIdentificador= False
                        token = ""                                             
                elif leyendoCadena:
                    charEspecial = ""
                    leyendoCharEspecial = False
                    token+=actual
                    if actual == "\n":
                        self.error(lineaActual, indice, "Se esperaba \"")
                    elif actual == '\"' and token[len(token)-2] != "\\":                   
                        leyendoCadena=False                           
                        indice+=1
                        self.agregarALista(token)
                        token=""
                    else:                       
                        indice+=1
                    #Codigo para analizar caracteres especiales dentro de un string
                    if actual == "\\":
                        if siguiente == "t" or siguiente == "n" or siguiente == "\\" or siguiente == "r" or siguiente == "\"" or siguiente == "\'":
                            print("Hola encontre un caracter especial en un string")
                        if siguiente == "u":
                            charEspecial = "\\u"
                            leyendoCharEspecial = True
                    if leyendoCharEspecial:
                        if len(charEspecial) < 6:
                            charEspecial+= actual
                            
                        else:
                            print("Encontre  un caracter de UNICODE")
                            leyendoCharEspecial = False
                    #_____________________________________
                elif leyendoChar:            
                    token+=actual
                    if actual == "\n":
                        self.error(lineaActual, indice, "Se esperaba \'")
                    elif actual == '\'' and token[len(token)-2] != "\\":                   
                        leyendoChar=False                           
                        indice+=1
                        self.agregarALista(token)
                        token=""
                    else:                       
                        indice+=1                    
                elif leyendoComentario:
                    if actual == '\n':
                        leyendoComentario=False                            
                        indice+=1 
                        print("encontre un comentario:", token)   
                        token=""
                    else:
                        token+=actual
                        indice+=1
                elif leyendoComentarioMul:
                    if actual == '*' and siguiente == ')':
                        leyendoComentarioMul=False                            
                        indice+=2
                        print("encontre un comentario multiple:", token)   
                        token=""
                    else:
                        token+=actual
                        indice+=1
                elif actual != ' ' and actual !="\n"  and actual != "\t":
                    token += actual
                    # print("token ", token)
                    # print("actual ", actual)
                    # print("siguiente ", siguiente)                    
                    if (actual == '-' and siguiente != '-') or numRegex.fullmatch(actual):
                        #print("entre al else de numero")
                        if numRegex.fullmatch(siguiente):
                            indice+=1                      
                        else:
                            #print("token final ",token)
                            self.agregarALista(token)                        
                            token = ""
                            indice+=1
                    
                    elif actual=='\"':
                        #print("entre al else de cadena")
                        indice+=1
                        leyendoCadena=True
                    elif actual=='\'':
                        #print("entre al else de cadena")
                        indice+=1
                        leyendoChar=True
                    elif(actual=='-' and siguiente == '-'):
                        print("entre al else de comentario")
                        indice+=1
                        leyendoComentario=True
                    elif(actual=='(' and siguiente == '*'):
                        #print("entre al else de comentario multiple")
                        indice+=1
                        leyendoComentarioMul=True
                        
                    elif(letraRegex.fullmatch(actual) and siguiente=='\n'):
                        
                        self.agregarALista(token)
                        token = ""
                        indice+=1    
                        
                    elif(letraRegex.fullmatch(actual)):
                        #print("entre al else de identificador")                         
                        indice+=1
                        leyendoIdentificador = True
                   

                    # elif (actual == "@" and letraRegex.fullmatch(siguiente)):

                    else:                     
                    
                        if(actual == "{"): self.scope+=1
                        if(actual == "}"): self.scope-=1
                        #print("token en simbolos ", token)
                        if numSimbols ==1 or letraRegex.fullmatch(siguiente) or actual==";" or siguiente== '_' or numRegex.fullmatch(siguiente) or siguiente == '\"' or siguiente == ' ' or siguiente == '\n' or siguiente == ';' or actual == ")" or actual == "}" or actual == "]" or (actual == '>' and siguiente == '('):
                            #print("token final ",token)
                            self.agregarALista(token)
                            token = ""
                            numSimbols=0
                            indice+=1
                        else:
                            numSimbols+=1
                            indice+=1            
                else:
                    if actual == "\n": 
                        lineaActual+=1
                    indice+=1
            



            fin = time.time()
            
            #IMPRIMIR EN PANTALLA EL RESULTADO
            self.scrolledtext1.insert("1.0", str((fin-inicio)))
            self.scrolledtext1.insert("1.0", "\n----TIEMPO CONSUMIDO----\n", 'tiempo')
            for simbolo, descripcion in reversed(self.tablaSimbolos.items()):
                self.scrolledtext1.insert("1.0", simbolo +" \t--> "+str(descripcion)+"\n")
            self.scrolledtext1.insert("1.0", "\n----TABLA DE SIMBOLOS----\n",'simbolos')
            for objeto in reversed(self.result):
                self.scrolledtext1.insert("1.0", objeto.mostrar())
                #print(objeto.token,"\t\t-->",objeto.descripcion,"\n")
            self.scrolledtext1.insert("1.0", "\n----TOKENS----\n",'tokens')
            self.scrolledtext1.tag_config('tokens',background="lightblue", foreground='blue', justify="center")           
            self.scrolledtext1.tag_config('simbolos', background="lightblue", foreground='blue', justify="center") 
            self.scrolledtext1.tag_config('tiempo', background="lightblue", foreground='blue', justify="center") 
    def agregarALista(self,token):
        #print("token en metodo ", token)
   
        descripcion = self.etiquetarToken(token)
        objectoToken = Token()
        objectoToken.token = token;
        objectoToken.descripcion = descripcion
        self.result.append(objectoToken)
    
    def etiquetarToken(self, token):

        palabrasReservadas= {'lit-bool': 'true|false','keyword': 'var|and|break|dec|do|elif|else|if|inc|not|or|return|while'}
        operadores={'parethesis open':'[(]',
                    'parethesis close':'[)]',
                    'bracket open':'[\[]',
                    'bracket close':'[\]]',
                    'brackets':'\[\]',
                    'parethesis':'\(\)',
                    'curly brackets':'{}',
                    'end instruction':';',            
                    'coma':',',            
                    'curly bracket open':'[{]',
                    'curly bracket close':'[}]',
                    "op-comp": '==|<>',
                    "op-rel": '>=|<=|<|>',
                    "op-assig": '=',
                    "op-add": '\+|-',
                    "op-mul" : '\*|\/|%',
                    "op-unary": 'not'
                    }
        digitos={'lit-int': '[-]?[0-9]+'}
        literals ={ 'lit-char':'\\u[0-9a-fA-F]{6}|\\n|\\r|\\t|\\|\'|\"'}
        resultado = ""
        isLetra = re.compile("[a-zA-Z]")
        isNumber = re.compile("[0-9]")      
        if (isLetra.fullmatch(token[0])):
            #Analizar si es una palabra reservada
            resultado = self.identificarCategoria(token, palabrasReservadas)
            if(resultado == ""):
                #Analizar si es un identificador			
                patron = re.compile("^[a-zA-Z](\w)*")
                if(patron.fullmatch(token)):
                    resultado = "identifier"
                    info = {'type ':resultado, 'scope ':self.scope}
                    if self.tablaSimbolos.get(token) is None:
                        self.tablaSimbolos[token] = info
        elif isNumber.fullmatch(token[0]) or token[0] == '-':
            #analizar si es un numero
            #print("cadena ", token)             
           patron = re.compile('[-]?[0-9]+')
           if token == "-":
               resultado = 'op-add'
           if patron.fullmatch(token):
               resultado = 'lit-int';
               
        elif token[0]== "\"":
            #Analizar si es un string                    
            patron = re.compile('[\"][\w\s\W]*[\"]')
            if(patron.fullmatch(token)):
                resultado = "lit-str"
        elif token[0]== "\'": #'\t'
            #Analizar si es un lt-char
            print("HOLA SOY UN  CHAR ", token)
            print("HOLA SOY UN  CHAR LEN ", len(token))
            if(len(token) == 3):
                print("entre")
                patron = re.compile('[\'].[\']')
                if(patron.fullmatch(token)):
                    print("entre")
                    resultado = "lit-char"
            elif len(token) > 3:                
                if token[1] == "\\":
                    if token[2] == "t" or token[2] == "n" or token[2] == "\\" or token[2] == "r" or token[2] == "\"" or token[2] == "\'":
                        resultado = "lit-char"
                    if token[2] == "u":
                        patron = re.compile('[\'][\\\\][u]([0-9a-fA-F]){6}[\']')
                        
                        if(patron.fullmatch(token)):
                            resultado = "lit-char"                                                      
        else:
            #analizar si es un operador
            resultado = self.identificarCategoria(token, operadores) 

        if(resultado ==""):
            resultado = "No encontrado"
        return resultado
        
    def identificarCategoria(self, token, mapa):
        resultado = ""
        for llave, valor in mapa.items():
            patron = re.compile(valor)
            if patron.fullmatch(token):
                resultado = llave
                break
        return resultado
    def error(self, linea, posicion, mensaje):
        print("Se encontró un error en la linea ", linea, ", posicion ", posicion, ".\nMensaje: ", mensaje)

aplicacion1 = Aplicacion()