import tkinter as tk
from tkinter import scrolledtext as st
import sys
import re
from tkinter import filedialog as fd
from tkinter import messagebox as mb

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
        #self.patronNumeros = re.compile("[+-]?([0-9]*[.])?[0-9]+")
        #self.patronCadenas = re.compile('"[\w\s]*"')                
        self.patronComentarios = re.compile("\/\*[\w\s]*\*\/|\/\/[\w\s]*")
        #self.tokensEspeciales = ['?','{', '}','[', ']',';','(',')','++','--','<<=','>>=','>>>=','<<','>>>','>>','&=','^|','|=','==', '>=','=>','!=','&&', '||','+=','-=','*=','/=','%=','+','*','-','^','<', '>','=','#','$','%','&','¡','!','|',':', '/','\\',',','~','`','¿']
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
            self.ignorarComentarios()
            #CODIGO PARA SEPARAR TOKENS Y ETIQUETARLOS
            indice = 0    
            
            numRegex = re.compile("[0-9]");
            letraRegex = re.compile("[a-zA-Z]");
            leyendoCadena = False
            token = ""
            while indice < len(self.contenido):
                actual = self.contenido[indice]
                if(indice < len(self.contenido)-1):
                    siguiente = self.contenido[indice+1]
                else:
                    siguiente = "\n"
                print("actual ",actual)
                print("siguiente ",siguiente)
                if actual != ' ' and not leyendoCadena:
                    token += actual
                    print("token ", token)
                    if (actual == '+' or actual == '-' and numRegex.fullmatch(siguiente)) or numRegex.fullmatch(siguiente) or (actual == '.' and numRegex.fullmatch(siguiente)):
                        if siguiente == '.' or numRegex.fullmatch(siguiente):
                            indice+=1
                        else:
                            print("token final ",token)
                            self.agregarALista(token)
                            token = ""
                            indice+=1;
                    else:
                        if letraRegex.fullmatch(siguiente) or siguiente== '_' or numRegex.fullmatch(siguiente) or siguiente == '\"' or siguiente == ' ' or siguiente == '\n':
                            print("token final ",token)
                            self.agregarALista(token)
                            token = ""
                            indice+=1;
                        else:
                            indice+=1
                            
                




                
            #IMPRIMIR EN PANTALLA EL RESULTADO
            for simbolo, descripcion in self.tablaSimbolos.items():
                self.scrolledtext1.insert("1.0", simbolo +" \t--> "+descripcion+"\n")
            self.scrolledtext1.insert("1.0", "\n----TABLA DE SIMBOLOS----\n")
            for objeto in reversed(self.result):
                self.scrolledtext1.insert("1.0", objeto.mostrar())
                #print(objeto.token,"\t\t-->",objeto.descripcion,"\n")
            self.scrolledtext1.insert("1.0", "----TOKENS----\n")           
    def agregarALista(self,token):
        print("token en metodo ", token)
        objectoToken = Token()
        objectoToken.token = token;
        objectoToken.descripcion = self.etiquetarToken(token);
        self.result.append(objectoToken)
    def ignorarComentarios(self):
        comentario = "x"
        try:
            while comentario != "":                    
                comentario = re.search(self.patronComentarios, self.contenido).group(0)                                
                comentario = comentario.replace("/*", "\/\*")
                comentario = comentario.replace("*/", "\*\/")           
                a = re.split(comentario, self.contenido)
                self.contenido = " ".join(a)                 
        except AttributeError:
            pass
    
    def etiquetarToken(self, token):
        palabrasReservadas= {'modifier': 'public|protected|private|abstract|static|final|transit|volatile',
                             'result type':'void',
                             'integral type':'byte|short|int|long|char',
                             'primitive type':'boolean',
                             'floating-point type':'float|double',
                             'String type':'String',                             
                             'reserved word':'throw|catch|return|break|finally|try|continue|default|super|this|new|byte|class|interface|package|const|goto|implements|extends|import|instanceof|native|synchronized|throws',
                             'iteratives label':'while|for|do',
                             'null literal':'NULL|null',
                             'conditional label':'if|switch|case|else'}
        operadores={'parethesis open':'[(]',
                    'parethesis close':'[)]',
                    'bracket open':'[\[]',
                    'bracket close':'[\]]',
                    'end instruction':';',
                    'curly bracket open':'[{]',
                    'curly bracket close':'[}]',
                    'arithmetic operator':'[+]|[-]|[*]|[\/]|[%]|[\^]',
                    'unary operator':'[-][-]|[+][+]|[!]',
                    'equality operator':'[=][=]|[!][=]',
                    'relational operator': '[>][=]|[<][=]|[>]|[<]',
                    'conditional operator':'[&][&]|[|][|]',
                    'assignment operator':'[=]|[*][=]|[\/][=]|[%][=]|[+][=]|[-][=]|[<][<][=]|[>][>][=]|[>][>][>][=]|[&][=]|[\^][=]|[|][=]',
                    'bitwise operator':'[&]|[|][~]',
                    'bit shift operator':'[<][<]|[>]{2,3}'}
        digitos={'digit':'[0-9]','number':'[+-]?[0-9]+'}
        
        floatingPointLiteral={'floatingPointLiteral':'[+-]?[0-9]*[.][0-9]+[E]?[f]?'}
        resultado = ""
        isLetra = re.compile("[a-zA-Z]")
        isIdentificador = re.compile("[_$]")
        isNumber = re.compile("[0-9]")      
        if (isLetra.fullmatch(token[0])):
            #Analizar si es una palabra reservada
            resultado = self.identificarCategoria(token, palabrasReservadas)
            if(resultado == ""):
                #Analizar si es un identificador			
                patron = re.compile("([a-zA-Z][0-9]?_?)+")
                if(patron.fullmatch(token)):
                    resultado = "Identifier"
                    self.tablaSimbolos[token] = "Identifier"
        elif isIdentificador.fullmatch(token[0]):
            #Analizar si es un identificador        
            patron = re.compile("[_$]?([a-zA-Z][0-9]?_?)+|[_$][0-9]+")
            if(patron.fullmatch(token)):
                resultado = "Identifier"
                self.tablaSimbolos[token] = "Identifier"
            else:
                if(token == "_"):
                    resultado = "Underscore"
                elif (token == "$"):
                    resultado = "Dollar sign"
        elif isNumber.fullmatch(token[0]) or ((token[0] == '+' or token[0] == '-') and isNumber.fullmatch(token[1])) :
            #analizar si es un numero
            resultado = self.identificarCategoria(token, digitos)  
            if(resultado == ""):
                resultado = self.identificarCategoria(token,floatingPointLiteral)
        elif token[0]== "\"":
            #Analizar si es un string        
            patron = re.compile('"[\w\s]*"')
            if(patron.fullmatch(token)):
                resultado = "Character string"
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