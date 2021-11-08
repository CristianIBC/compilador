from os import error
import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as ScrolledTex
import sys
from anytree import Node, RenderTree
import re
import time
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.constants import HORIZONTAL, N

class Token:
    def setValues(self,token,descripcion, num, linea, posicion):
        self.token = token
        self.descripcion = descripcion
        self.num = num
        self.linea = linea
        self.posicion = posicion
    def mostrar(self):
         return (str(self.token) +" \t "+ self.descripcion +"\t\t\t\t"+ str(self.num) + "\n")
class Aplicacion:    
    ID = 0
    VAR = 1
    AND = 2
    BREAK = 3
    DEC = 4
    DO = 5
    ELIF = 6
    ELSE = 7
    IF = 8
    INC = 9
    NOT = 10
    OR = 11
    RETURN = 12
    WHILE = 13
    PAR_IZQ = 14
    PAR_DER = 15
    CORCH_IZQ = 16
    CORCH_DER = 17
    LLAVE_IZQ = 18
    LLAVE_DER = 19
    PUNTOYCOMA = 20
    COMA = 21
    OP_COMP = 22
    OP_REL = 23
    OP_ASSIGN = 24
    OP_ADD = 25
    OP_MUL = 26
    OP_UNARY = 27
    LIT_INT = 28
    LIT_CHAR = 29
    LIT_STR = 30
    LIT_BOOL = 31
    PESO = 32
    

    def __init__(self):    

        self.ventana1 = tk.Tk()
        F_font = ('bold', 15)
        self.ventana1.title("Analizador lexico")
        self.agregar_menu()          
        self.scrolledtext1= ScrolledTex.ScrolledText(self.ventana1,width=100, height=30, font=F_font)
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
        nombrearch = fd.askopenfilename(initialdir="c:", title="Seleccione archivo", filetypes=(("txt files", "*.txt"),("todos los archivos", "*.*")))    
      #  nombrearch="C:\\Users\\crist\\Documents\\Noveno\\Compiladores\\T1\\compilador\\proyecto2\\codiguito.txt"  
        if nombrearch!='':
            archi1 = open(nombrearch,"r", encoding="utf-8")
            self.contenido = archi1.read()
            archi1.close()
            self.result = []
            self.tablaSimbolos = {}
            self.scrolledtext1.delete("1.0", tk.END)        
            inicio = time.time()
            #SE EJECUTA EL ANALISIS LEXICO
            self.lexico()
            #SE EJECUTA EL ANALISIS SINTACTICO
            self.parser(self.result)
            fin = time.time()

            #IMPRIMIR EN PANTALLA EL RESULTADO
            self.scrolledtext1.insert("1.0", str((fin-inicio))+"\n")
            self.scrolledtext1.insert("1.0", "\n----TIEMPO CONSUMIDO----\n", 'tiempo')
            for simbolo, descripcion in reversed(self.tablaSimbolos.items()):
                self.scrolledtext1.insert("1.0", simbolo +" \t--> "+str(descripcion)+"\n")
            self.scrolledtext1.insert("1.0", "\n----TABLA DE SIMBOLOS----\n",'simbolos')
            for objeto in reversed(self.result):
                self.scrolledtext1.insert("1.0", objeto.mostrar())               
            self.scrolledtext1.insert("1.0", "Token\tDescripcion\t\t\tNumero asociado\n","titulos")
            self.scrolledtext1.insert("1.0", "\n----TOKENS----\n",'tokens')
            self.scrolledtext1.tag_config('titulos',background="lightgray", foreground='blue')           
            self.scrolledtext1.tag_config('tokens',background="lightblue", foreground='blue', justify="center")           
            self.scrolledtext1.tag_config('simbolos', background="lightblue", foreground='blue', justify="center") 
            self.scrolledtext1.tag_config('tiempo', background="lightblue", foreground='blue', justify="center") 

     

    def lexico(self):
        #CODIGO PARA SEPARAR TOKENS Y ETIQUETARLOS
        indice = 0    
        self.lineaActual = 1;
        self.scope = 1
   
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
                    self.agregarALista(token, self.lineaActual, indice+len(token))
                    leyendoIdentificador= False
                    token = ""                                             
            elif leyendoCadena:
                charEspecial = ""
                leyendoCharEspecial = False
                token+=actual
                if actual == "\n":
                    self.error(self.lineaActual, indice, "Se esperaba \"")
                elif actual == '\"' and token[len(token)-2] != "\\":                   
                    leyendoCadena=False                           
                    indice+=1
                    self.agregarALista(token, self.lineaActual, indice+len(token))
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
                    self.error(self.lineaActual, indice, "Se esperaba \'")
                elif actual == '\'' and token[len(token)-2] != "\\":
                                        
                    leyendoChar=False                           
                    indice+=1
                    self.agregarALista(token, self.lineaActual, indice+len(token))
                    token=""
                else:
                    if len(token)>3:
                        if token[len(token)-3] == "\\" and token[len(token)-2]!="u":                        
                            
                            leyendoChar=False                           
                            indice+=1
                            self.agregarALista(token, self.lineaActual, indice+len(token))
                            token=""
                        else:
                            indice+=1
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
                        self.agregarALista(token, self.lineaActual, indice+len(token))                        
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
                    
                    self.agregarALista(token, self.lineaActual, indice+len(token))
                    token = ""
                    indice+=1    
                    
                elif(letraRegex.fullmatch(actual)):
                    #print("entre al else de identificador")                         
                    indice+=1
                    leyendoIdentificador = True
                

                # elif (actual == "@" and letraRegex.fullmatch(siguiente)):

                else:                     
                
                    if(actual == "{"): self.scope+=1
                    
                    #print("token en simbolos ", token)
                    if numSimbols ==1 or letraRegex.fullmatch(siguiente) or actual==";" or siguiente== '_' or numRegex.fullmatch(siguiente) or siguiente=='\'' or siguiente=='-' or siguiente == '\"' or siguiente == ' ' or siguiente == '\n' or siguiente == ';' or actual == '('  or actual == '{'  or actual == '['  or actual == ")" or actual == "}" or actual == "]" or siguiente == ')'or siguiente == ']'or siguiente == '}' or (actual == '>' and siguiente == '('):
                        #print("token final ",token)
                        self.agregarALista(token, self.lineaActual, indice+len(token))
                        token = ""
                        numSimbols=0
                        indice+=1
                    else:
                        numSimbols+=1
                        indice+=1            
            else:
                if actual == "\n": 
                    self.lineaActual+=1
                indice+=1
        
    def agregarALista(self,token, linea, posicion):
        #print("token en metodo ", token)
   
        descripcion, num = self.etiquetarToken(token)
        objectoToken = Token()
        objectoToken.token = token;
        objectoToken.descripcion = descripcion
        objectoToken.num = num
        objectoToken.posicion = posicion
        objectoToken.linea = linea
        print(token)
        self.result.append(objectoToken)

    def etiquetarToken(self, token):

        palabrasReservadas= {'lit-bool': ['true|false', self.LIT_BOOL],'keyword': ['var|and|break|dec|do|elif|else|if|inc|not|or|return|while', -1]}
        operadores={'parethesis open':['[(]', self.PAR_IZQ],
                    'parethesis close':['[)]', self.PAR_DER],
                    'bracket open':['[\[]', self.CORCH_IZQ],
                    'bracket close':['[\]]', self.CORCH_DER],
                    'brackets':['\[\]', -1],
                    'parethesis':['\(\)', -1],
                    'curly brackets':['{}', -1],
                    'end instruction':[';', self.PUNTOYCOMA],            
                    'coma':[',', self.COMA],            
                    'curly bracket open':['[{]', self.LLAVE_IZQ],
                    'curly bracket close':['[}]', self.LLAVE_DER],
                    "op-comp": ['==|<>', self.OP_COMP],
                    "op-rel": ['>=|<=|<|>', self.OP_REL],
                    "op-assig": ['=', self.OP_ASSIGN],
                    "op-add": ['\+|-', self.OP_ADD],
                    "op-mul" : ['\*|\/|%', self.OP_MUL],
                    "op-unary": ['not', self.OP_UNARY]
                    }
        digitos={'lit-int': '[-]?[0-9]+'}
        literals ={ 'lit-char':'\\u[0-9a-fA-F]{6}|\\n|\\r|\\t|\\|\'|\"'}
        resultado = ""
        num = -1
        isLetra = re.compile("[a-zA-Z]")
        isNumber = re.compile("[0-9]")      
        if (isLetra.fullmatch(token[0])):
            #Analizar si es una palabra reservada
            resultado, num = self.identificarCategoria(token, palabrasReservadas)
            if resultado == "keyword" and num == -1:      
                if token == "var": num = self.VAR
                elif token == "and": num = self.AND
                elif token == "break": num = self.BREAK
                elif token == "dec": num = self.DEC
                elif token == "do": num = self.DO
                elif token == "elif": num = self.ELIF
                elif token == "else": num = self.ELSE
                elif token == "if": num = self.IF
                elif token == "inc": num = self.INC
                elif token == "not": num = self.NOT
                elif token == "or": num = self.OR
                elif token == "return": num = self.RETURN
                elif token == "while": num = self.WHILE
            if(resultado == "" and num == -1):
                #Analizar si es un identificador			
                patron = re.compile("^[a-zA-Z](\w)*")
                if(patron.fullmatch(token)):
                    resultado = "identifier"
                    num = self.ID
                    info = {'type ':resultado, 'scope ':self.scope}
                    if self.tablaSimbolos.get(token) is None:
                        self.tablaSimbolos[token] = info
        elif isNumber.fullmatch(token[0]) or token[0] == '-':           
           patron = re.compile('[-]?[0-9]+')
           if token == "-":
               resultado = 'op-add'
               num = self.OP_ADD
           if patron.fullmatch(token):
               resultado = 'lit-int';
               num = self.LIT_INT
               
        elif token[0]== "\"":
            #Analizar si es un string                    
            patron = re.compile('[\"][\w\s\W]*[\"]')
            if(patron.fullmatch(token)):
                resultado = "lit-str"
                num = self.LIT_STR
        elif token[0]== "\'": #'\t'
            #Analizar si es un lt-char

            if(len(token) == 3):
                patron = re.compile('[\'].[\']')
                if(patron.fullmatch(token)):
                    resultado = "lit-char"
                    num = self.LIT_CHAR
            elif len(token) > 3:                
                if token[1] == "\\":
                    if token[2] == "t" or token[2] == "n" or token[2] == "\\" or token[2] == "r" or token[2] == "\"" or token[2] == "\'":
                        resultado = "lit-char"
                        num = self.LIT_CHAR
                    if token[2] == "u":
                        patron = re.compile('[\'][\\\\][u]([0-9a-fA-F]){6}[\']')
                        
                        if(patron.fullmatch(token)):
                            resultado = "lit-char"                                                      
                            num = self.LIT_CHAR
        else:
            #analizar si es un operador
            resultado,num = self.identificarCategoria(token, operadores) 

        if(resultado ==""):
            resultado = "No encontrado"
        return resultado,num
        
    def identificarCategoria(self, token, mapa):
        resultado = ""
        num = -1
        for llave, valor in mapa.items():
            patron = re.compile(valor[0])
            if patron.fullmatch(token):
                resultado = llave
                num = valor[1]
                break
        return resultado, num
    
    def parser(self, tokens):
       # print("holi")
       self.tokensParser = tokens
       self.indexToken = -1    
       root = Node("Program")  
       self.move()
       self.Program(root)
       self.scrolledtext1.insert("1.0", "\n----ARBOL SINTACTICO----\n", 'arbol')
       for pre, fill, node in RenderTree(root):
           print("%s%s" % (pre, node.name))
           self.scrolledtext1.insert(END, "%s%s" % (pre, node.name) +"\n")
       self.scrolledtext1.tag_config('arbol', background="lightblue", foreground='blue', justify="center") 
    def move(self):
        self.indexToken+=1
        self.tokenActual = self.tokensParser[self.indexToken] if self.indexToken < len(self.tokensParser) else self.PESO
        if self.tokenActual == self.PESO:
            print("Se termino de leer la cadena")        
       
    def consume(self, token, parent):
        if token == self.tokenActual.num:
            print("token consumido ",  self.tokenActual.token)
            Node("token: "+str( self.tokenActual.token) + "   ("+ self.tokenActual.descripcion+ ")" , parent= parent)
            self.move()
        else:
            self.errorParser([token], 4)
            
    def error(self, linea, posicion, mensaje):
        print("Se encontró un error en la linea ", linea, ", posicion ", posicion, ".\nMensaje: ", mensaje)


    def errorParser(self, tokensEsperados):
        elementos = "";
        for i in range(len(tokensEsperados)):
            if i == 0:
                elementos +=str(tokensEsperados[i])
            else:    
                elementos+= ","+str(tokensEsperados[i])
        print("Error en la linea ", self.tokenActual.linea, "posicion", self.tokenActual.posicion)
        print("Se esperaba alugno de los siguientes elementos", elementos)
        exit(0)

    def Program(self, parent):
        if self.tokenActual.num == self.VAR:            
            self.DefList(parent)
        elif self.tokenActual.num == self.ID:
            self.DefList(parent)
        elif self.tokenActual == self.PESO:
            self.DefList(parent)
        else:
            self.errorParser([self.VAR, self.ID, self.PESO])
            
    def DefList(self, parent):
        parent = Node("DefList", parent = parent)

        if self.tokenActual.num == self.VAR:            
            self.DefListP(parent)
        elif self.tokenActual.num == self.ID:
            self.DefListP(parent)
        elif self.tokenActual == self.PESO:
            self.DefListP(parent)
        else:
            self.errorParser([self.VAR, self.ID, self.PESO])
    
    def DefListP(self,parent):
        parent = Node("DefListP", parent = parent)
        if self.tokenActual == self.PESO:   
            Node("ε", parent)         
            return
        elif self.tokenActual.num == self.ID:
            self.Def(parent)
            self.DefListP(parent)
        elif self.tokenActual.num == self.VAR:
            self.Def(parent)
            self.DefListP(parent)
        else:
            self.errorParser([self.VAR, self.ID, self.PESO])
    def Def(self,parent):
        parent = Node("Def", parent = parent)
        if self.tokenActual.num == self.VAR:
            self.VarDef(parent)
        elif self.tokenActual.num == self.ID:
            self.FunDef(parent)
        else:
            self.errorParser([self.VAR, self.ID])
    def VarDef(self,parent):
        parent = Node("VarDef", parent = parent)
        if self.tokenActual.num == self.VAR:
            self.consume(self.VAR, parent)
            self.VarList(parent)
            self.consume(self.PUNTOYCOMA,parent)

        else:
            self.errorParser([self.VAR])
    def FunDef(self, parent):
        parent = Node("FunDef", parent = parent)
        if self.tokenActual.num == self.ID:
            self.consume(self.ID, parent)
            self.consume(self.PAR_IZQ, parent)
            self.ParamList(parent)
            self.consume(self.PAR_DER, parent)
            self.consume(self.LLAVE_IZQ, parent)
            self.VarDefList(parent)
            self.StmtList(parent)
            self.consume(self.LLAVE_DER, parent)
        else:
            self.errorParser([self.ID])
    def VarList(self, parent):
        parent = Node("VarList", parent = parent)
        if self.tokenActual.num == self.ID:
            self.IdList(parent)
        else:
            self.errorParser([self.ID])
    def IdList(self, parent):
        parent = Node("IdList", parent = parent)
        if self.tokenActual.num == self.ID:
            self.consume(self.ID, parent)
            self.IdListCount(parent)
        else:
            self.errorParser([self.ID])
    def IdListCount(self, parent):
        parent = Node("IdListCont", parent = parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
            Node("ε", parent)   
            return
        elif self.tokenActual.num == self.COMA:
            self.consume(self.COMA, parent)
            self.consume(self.ID, parent)
            self.IdListCount(parent)
        elif self.tokenActual.num == self.PAR_DER:
            Node("ε", parent)   
            return
        else:
            self.errorParser([self.PUNTOYCOMA, self.COMA, self.PAR_DER])

    def ParamList(self, parent):
        parent = Node("ParamList", parent = parent)
        if self.tokenActual.num == self.ID:
            self.IdList(parent)
        elif self.tokenActual.num == self.PAR_DER:
            Node("ε", parent)   
            return
        else:
            self.errorParser([self.ID, self.PAR_DER])
    def VarDefList(self, parent):
        parent = Node("VarDefList", parent = parent)
        if self.tokenActual.num == self.VAR:
            self.VarDefListP(parent)
        elif self.tokenActual.num == self.PUNTOYCOMA:
            self.VarDefListP(parent)
        elif self.tokenActual.num == self.ID:
            self.VarDefListP(parent)
        elif self.tokenActual.num == self.LLAVE_DER:
            self.VarDefListP(parent)
        elif self.tokenActual.num == self.INC:
            self.VarDefListP(parent)
        elif self.tokenActual.num == self.DEC:
            self.VarDefListP(parent)
        elif self.tokenActual.num == self.IF:
            self.VarDefListP(parent)
        elif self.tokenActual.num == self.WHILE:
            self.VarDefListP(parent)
        elif self.tokenActual.num == self.DO:
            self.VarDefListP(parent)
        elif self.tokenActual.num == self.BREAK:
            self.VarDefListP(parent)
        elif self.tokenActual.num == self.RETURN:
            self.VarDefListP(parent)
        elif self.tokenActual.num == self.PESO:
            self.VarDefListP(parent)
        else:
            self.errorParser([self.ID, self.LLAVE_DER, self.VAR,self.INC,self.DEC,self.IF,self.WHILE,self.DO,self.BREAK, self.RETURN, self.PESO, self.PUNTOYCOMA])
    def VarDefListP(self, parent):
        parent = Node("VarDefListP", parent = parent)
        if self.tokenActual.num == self.VAR:
            self.VarDef(parent)
            self.VarDefListP(parent)
        elif self.tokenActual.num == self.PUNTOYCOMA:
            Node("ε", parent)   
            return        
        elif self.tokenActual.num == self.ID:
            Node("ε", parent)   
            return
        elif self.tokenActual.num == self.LLAVE_DER:
            Node("ε", parent)   
            return
        elif self.tokenActual.num == self.INC:
            Node("ε", parent)   
            return
        elif self.tokenActual.num == self.DEC:
            Node("ε", parent)   
            return
        elif self.tokenActual.num == self.IF:
            Node("ε", parent)   
            return
        elif self.tokenActual.num == self.WHILE:
            Node("ε", parent)   
            return
        elif self.tokenActual.num == self.DO:
            Node("ε", parent)   
            return
        elif self.tokenActual.num == self.BREAK:
            Node("ε", parent)   
            return
        elif self.tokenActual.num == self.RETURN:
            Node("ε", parent)   
            return
        elif self.tokenActual.num == self.PESO:
            Node("ε", parent)   
            return
        else:
            self.errorParser([self.ID, self.LLAVE_DER, self.VAR,self.INC,self.DEC,self.IF,self.WHILE,self.DO,self.BREAK, self.RETURN, self.PESO, self.PUNTOYCOMA])
    def StmtList(self, parent):
        parent = Node("StmtList", parent = parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
            self.StmtListP(parent)
        elif self.tokenActual.num == self.ID:
            self.StmtListP(parent)
        elif self.tokenActual.num == self.LLAVE_DER:
            self.StmtListP(parent)
        elif self.tokenActual.num == self.INC:
            self.StmtListP(parent)
        elif self.tokenActual.num == self.DEC:
            self.StmtListP(parent)
        elif self.tokenActual.num == self.IF:
            self.StmtListP(parent)
        elif self.tokenActual.num == self.WHILE:
            self.StmtListP(parent)
        elif self.tokenActual.num == self.DO:
            self.StmtListP(parent)
        elif self.tokenActual.num == self.BREAK:
            self.StmtListP(parent)
        elif self.tokenActual.num == self.RETURN:
            self.StmtListP(parent)
        else:
            self.errorParser([self.ID, self.LLAVE_DER,self.INC,self.DEC,self.IF,self.WHILE,self.DO,self.BREAK, self.RETURN, self.PUNTOYCOMA])
    
    def StmtListP(self, parent):
        parent = Node("StmtListP", parent = parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
            self.Stmt(parent)
            self.StmtListP(parent)
        elif self.tokenActual.num == self.ID:
            self.Stmt(parent)
            self.StmtListP(parent)
        elif self.tokenActual.num == self.LLAVE_DER:
            Node("ε", parent)   
            return
        elif self.tokenActual.num == self.INC:
            self.Stmt(parent)
            self.StmtListP(parent)
        elif self.tokenActual.num == self.DEC:
            self.Stmt(parent)
            self.StmtListP(parent)
        elif self.tokenActual.num == self.IF:
            self.Stmt(parent)
            self.StmtListP(parent)
        elif self.tokenActual.num == self.WHILE:
            self.Stmt(parent)
            self.StmtListP(parent)
        elif self.tokenActual.num == self.DO:
            self.Stmt(parent)
            self.StmtListP(parent)
        elif self.tokenActual.num == self.BREAK:
            self.Stmt(parent)
            self.StmtListP(parent)
        elif self.tokenActual.num == self.RETURN:
            self.Stmt(parent)
            self.StmtListP(parent)
        else:
            self.errorParser([self.ID, self.LLAVE_DER,self.INC,self.DEC,self.IF,self.WHILE,self.DO,self.BREAK, self.RETURN, self.PUNTOYCOMA])
        
    def Stmt(self, parent):
        return
aplicacion1 = Aplicacion()
