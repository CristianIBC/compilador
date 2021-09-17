import tkinter as tk
from tkinter import scrolledtext as st
import sys
import re
import time
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.constants import N

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
           
        if nombrearch!='':
            archi1 = open(nombrearch,"r", encoding="utf-8")
            self.contenido = archi1.read()
            archi1.close()
            self.result = []
            self.tablaSimbolos = {}
            self.scrolledtext1.delete("1.0", tk.END)        
            #CODIGO PARA SEPARAR TOKENS Y ETIQUETARLOS
            indice = 0    
            self.scope = 1
            inicio = time.time()
            numRegex = re.compile("[0-9]");
            letraRegex = re.compile("[a-zA-Z]");
            leyendoCadena = False
            leyendoIdentificador = False
            leyendoComentario = False
            leyendoComentarioMul = False
            token = ""
            while indice < len(self.contenido):
                actual = self.contenido[indice]
                if(indice < len(self.contenido)-1):
                    siguiente = self.contenido[indice+1]
                else:
                    siguiente = "\n"  

                if leyendoIdentificador:              
                    if letraRegex.fullmatch(actual) or numRegex.fullmatch(actual) or actual == '_':                                
                        token+=actual
                        indice+=1
                    if not letraRegex.fullmatch(siguiente) and not numRegex.fullmatch(siguiente) and not siguiente == '_':
                        self.agregarALista(token)
                        leyendoIdentificador= False
                        token = ""               
                elif leyendoCadena:
                        if actual == '\"' or actual =='\'':
                            token+=actual
                            leyendoCadena=False                            
                            indice+=1
                            self.agregarALista(token)
                            token=""
                        else:
                            token+=actual
                            indice+=1
                elif leyendoComentario:
                    if actual == '\n':
                        leyendoComentario=False                            
                        indice+=1 
                        #print("encontre un comentario:", token)   
                        token=""
                    else:
                        token+=actual
                        indice+=1
                elif leyendoComentarioMul:
                    if actual == '*' and siguiente == '/':
                        leyendoComentarioMul=False                            
                        indice+=2
                        #print("encontre un comentario multiple:", token)   
                        token=""
                    else:
                        token+=actual
                        indice+=1
                elif actual != ' ' and actual !="\n"  and actual != "\t":
                    token += actual
                    #print("token ", token)
                    if (actual == '.' or numRegex.fullmatch(actual) or actual == "+" or actual == "-"): #(actual == '+' or actual == '-' and numRegex.fullmatch(siguiente)) or numRegex.fullmatch(siguiente) or (actual == '.' and numRegex.fullmatch(siguiente)):
                        #print("entre al else de numero")
                        if siguiente == '.' or numRegex.fullmatch(siguiente) or siguiente == "f":
                            indice+=1
                        elif actual == '-' and siguiente == '>':
                            indice+=1                        
                        else:
                            #print("token final ",token)
                            self.agregarALista(token)
                            token = ""
                            indice+=1
                    
                    elif(actual=='\"' or actual =='\''):
                        #print("entre al else de cadena")
                        indice+=1
                        leyendoCadena=True
                    elif(actual=='/' and siguiente == '/'):
                        #print("entre al else de comentario")
                        indice+=1
                        leyendoComentario=True
                    elif(actual=='/' and siguiente == '*'):
                        #print("entre al else de comentario multiple")
                        indice+=1
                        leyendoComentarioMul=True
                    elif(letraRegex.fullmatch(actual) or actual=='_' or actual=='$'):
                            #print("entre al else de identificador")                         
                        indice+=1
                        leyendoIdentificador = True
                    # elif (actual == "@" and letraRegex.fullmatch(siguiente)):

                    else:
                        if(actual == "{"): self.scope+=1;
                        if(actual == "}"): self.scope-=1;
                        if letraRegex.fullmatch(siguiente) or siguiente== '_' or numRegex.fullmatch(siguiente) or siguiente == '\"' or siguiente == ' ' or siguiente == '\n' or siguiente == ';' or actual == ")" or actual == "}" or actual == "]" or (actual == '>' and (siguiente != '=' and siguiente != '>')) or (actual == "<" and (siguiente != "=" and siguiente != "<")):
                            #print("token final ",token)
                            self.agregarALista(token)
                            token = ""
                            indice+=1
                        else:
                            indice+=1
                
                
                else:
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
        objectoToken = Token()
        objectoToken.token = token;
        objectoToken.descripcion = self.etiquetarToken(token);
        self.result.append(objectoToken)
    
    def etiquetarToken(self, token):
        palabrasReservadas= {'modifier': 'public|protected|private|abstract|static|final|transit|volatile',
                             'result type':'void',
                             'integral type':'byte|short|int|long|char',
                             'primitive type':'boolean',
                             'floating-point type':'float|double',
                             'string class':'String',                             
                             'reserved word':'throw|catch|return|break|finally|try|continue|default|super|this|new|byte|class|interface|package|const|goto|implements|extends|import|instanceof|native|synchronized|throws',
                             'iteratives label':'while|for|do',
                             'null literal':'NULL|null',
                             'conditional label':'if|switch|case|else'
                             }
        operadores={'parethesis open':'[(]',
                    'parethesis close':'[)]',
                    'bracket open':'[\[]',
                    'bracket close':'[\]]',
                    'brackets':'\[\]',
                    'parethesis':'\(\)',
                    'curly brackets':'{}',
                    'end instruction':';',
                    'dot':'\.',
                    'coma':',',
                    'colon':':',
                    'curly bracket open':'[{]',
                    'curly bracket close':'[}]',
                    'arithmetic operator':'[+]|[-]|[*]|[\/]|[%]|[\^]',
                    'lambda operator': '->',
                    'unary operator':'[-][-]|[+][+]|[!]',
                    'equality operator':'[=][=]|[!][=]',
                    'relational operator': '[>][=]|[<][=]|[>]|[<]',
                    'conditional operator':'[&][&]|[|][|]',
                    'assignment operator':'[=]|[*][=]|[\/][=]|[%][=]|[+][=]|[-][=]|[<][<][=]|[>][>][=]|[>][>][>][=]|[&][=]|[\^][=]|[|][=]',
                    'bitwise operator':'[&]|[|][~]',
                    'bit shift operator':'[<][<]|[>]{2,3}'}
        digitos={'digit':'[0-9]','number':'[+-]?[0-9]+'}
        
        floatingPointLiteral={'floatingPointLiteral':'[+-]?[0-9]*\.[0-9]+[E]?[f]?'}
        resultado = ""
        isLetra = re.compile("[a-zA-Z]")
        isIdentificador = re.compile("[_$]")
        isNumber = re.compile("[0-9]")      
        if (isLetra.fullmatch(token[0])):
            #Analizar si es una palabra reservada
            resultado = self.identificarCategoria(token, palabrasReservadas)
            if(resultado == ""):
                #Analizar si es un identificador			
                patron = re.compile("(\w)+")
                if(patron.fullmatch(token)):
                    resultado = "identifier"
                    info = {'type ':resultado, 'scope ':self.scope}
                    if self.tablaSimbolos.get(token) is None:
                        self.tablaSimbolos[token] = info
        elif isIdentificador.fullmatch(token[0]):
            #Analizar si es un identificador   
            print("cadena ", token)     
            patron = re.compile("[_$]?(\w)+")
            if(patron.fullmatch(token)):
                resultado = "identifier"
                info = {'type ':resultado, 'scope ':self.scope}
                if self.tablaSimbolos.get(token) is None:
                    self.tablaSimbolos[token] = info
            else:
                if(token == "_"):
                    resultado = "underscore"
                elif (token == "$"):
                    resultado = "dollar sign"

        elif isNumber.fullmatch(token[0]) or ((token[0] == '+' or token[0] == '-' or token[0] == '.')) :
            #analizar si es un numero
            resultado = self.identificarCategoria(token, digitos)  
            if(resultado == ""):
                resultado = self.identificarCategoria(token,floatingPointLiteral)
            if(resultado == ""):
                resultado = self.identificarCategoria(token,operadores)
        elif token[0]== "\"" or token[0] =='\'':
            #Analizar si es un string                    
            patron = re.compile('[\'\"][\w\s\W]*[\'\"]')
            if(patron.fullmatch(token)):
                resultado = "character string"
        else:
            #analizar si es un operador
            resultado = self.identificarCategoria(token, operadores) 

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