from os import error, fsdecode
import os
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
    def setValues(self,token,descripcion, num, linea, posicion, scope):
        self.token = token
        self.descripcion = descripcion
        self.num = num
        self.linea = linea
        self.posicion = posicion
        self.scope = scope
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
    LIT_INT = 27
    LIT_CHAR = 28
    LIT_STR = 29
    LIT_BOOL = 30
    PESO = 31
    
    terminales ={
        '0': 'id',
        '1':'var',
        '2':'and',
        '3':'break',
        '4':'dec',
        '5':'do',
        '6':'elif',
        '7':'else',
        '8':'if',
        '9':'inc',
        '10':'not',
        '11':'or',
        '12':'return',
        '13':'while',
        '14':'(',
        '15':')',
        '16':'[',
        '17':']',
        '18':'{',
        '19':'}',
        '20':';',
        '21':',',
        '22':'<>, ==',
        '23':'>, <, >=, <=',
        '24':'=',
        '25':'+, -, not',
        '26':'*, /, %',
        '27':'lit-int',
        '28':'lit-char',
        '29':'lit-str',
        '30':'lit-bool',
        '31':'$'
    }
    def __init__(self):    

        self.ventana1 = tk.Tk()
        F_font = ('bold', 12)
        self.ventana1.title("Analizador lexico")
        self.agregar_menu()          
        self.scrolledtext1= ScrolledTex.ScrolledText(self.ventana1,width=145, height=40, font=F_font)
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
        #nombrearch="C:\\Users\\crist\\Documents\\Noveno\\Compiladores\\T1\\compilador\\proyecto2\\codiguito.txt"  
        if nombrearch!='':
            archi1 = open(nombrearch,"r", encoding="utf-8")
            self.contenido = archi1.read()
            archi1.close()
            self.result = []
            self.tablaVariables = []
            self.tablaFunciones = []
            self.scrolledtext1.delete("1.0", tk.END)        
            inicio = time.time()
            #SE EJECUTA EL ANALISIS LEXICO
            self.lexico()
            #SE EJECUTA EL ANALISIS SINTACTICO
            print("\nEmpieza sintactico")
            self.parser(self.result)
            fin = time.time()

            #IMPRIMIR EN PANTALLA EL RESULTADO
            self.scrolledtext1.insert("1.0", str((fin-inicio))+"\n")
            self.scrolledtext1.insert("1.0", "\n----TIEMPO CONSUMIDO----\n", 'tiempo')
            for simbolo in self.tablaFunciones:
                self.scrolledtext1.insert("1.0", str(simbolo)+"\n")
            self.scrolledtext1.insert("1.0", "\nFunciones\n")
            for simbolo in self.tablaVariables:
                self.scrolledtext1.insert("1.0", str(simbolo)+"\n")
            self.scrolledtext1.insert("1.0", "\nVariables\n")
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
        posicion = 0
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
                    
                    self.agregarALista(token, self.lineaActual,  (indice+1)-len(token)-posicion, self.scope)
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
                    self.agregarALista(token, self.lineaActual,  posicion, self.scope)
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
                    self.agregarALista(token, self.lineaActual,  posicion, self.scope)
                    token=""
                else:
                    if len(token)>3:
                        if token[len(token)-3] == "\\" and token[len(token)-2]!="u":                        
                            
                            leyendoChar=False                           
                            indice+=1
                            self.agregarALista(token, self.lineaActual,  (indice+1)-len(token)-posicion, self.scope)
                            
                            token=""
                        else:
                            indice+=1
                    else:
                        indice+=1                    
                                                
            elif leyendoComentario:
                if actual == '\n':
                    leyendoComentario=False
                    self.lineaActual += 1                           
                    indice+=1                        
                    token=""
                else:
                    token+=actual
                    indice+=1
            elif leyendoComentarioMul:
                if actual == '*' and siguiente == ')':
                    leyendoComentarioMul=False    
                    #self.lineaActual-=1                        
                    indice+=2                    
                    token=""
                else:
                    if(actual == '\n'):
                        self.lineaActual+=1 
                    token+=actual
                    indice+=1
            elif actual != ' ' and actual !="\n"  and actual != "\t":
                token += actual
                # 5("token ", token)
                # print("actual ", actual)
                # print("siguiente ", siguiente)                    
                if (actual == '-' and siguiente != '-') or numRegex.fullmatch(actual):
                    #print("entre al else de numero")
                    if numRegex.fullmatch(siguiente):
                        indice+=1                      
                    else:
                        #print("token final ",token)
                        indice+=1
                        self.agregarALista(token, self.lineaActual,  (indice+1)-len(token)-posicion, self.scope)                        
                        token = ""
                        
                
                elif actual=='\"':
                    #print("entre al else de cadena")
                    indice+=1
                    leyendoCadena=True
                elif actual=='\'':
                    #print("entre al else de cadena")
                    indice+=1
                    leyendoChar=True
                elif(actual=='-' and siguiente == '-'):                    
                    indice+=1
                    leyendoComentario=True
                elif(actual=='(' and siguiente == '*'):
                    #print("entre al else de comentario multiple")
                    indice+=1
                    leyendoComentarioMul=True
                    
                elif(letraRegex.fullmatch(actual) and siguiente=='\n'):                    
                    indice+=1    
                    self.agregarALista(token, self.lineaActual,  (indice+1)-len(token)-posicion, self.scope)
                    token = ""
                   
                    
                elif(letraRegex.fullmatch(actual)):
                    #print("entre al else de identificador")                         
                    indice+=1
                    leyendoIdentificador = True
                

                # elif (actual == "@" and letraRegex.fullmatch(siguiente)):

                else:                     
                
                    if(actual == "{"): self.scope+=1
                    if(actual == "}"): self.scope+=1
                    #print("token en simbolos ", token)
                    if numSimbols ==1 or letraRegex.fullmatch(siguiente) or actual==";" or siguiente== '_' or numRegex.fullmatch(siguiente) or siguiente=='\'' or siguiente=='-' or siguiente == '\"' or siguiente == ' ' or siguiente == '\n' or siguiente == ';' or actual == '('  or actual == '{'  or actual == '['  or actual == ")" or actual == "}" or actual == "]" or siguiente == ')'or siguiente == ']'or siguiente == '}' or (actual == '>' and siguiente == '('):
                        #print("token final ",token)
                        indice+=1
                        self.agregarALista(token, self.lineaActual,(indice+1)-len(token)-posicion, self.scope)
                        token = ""
                        numSimbols=0
                        
                    else:
                        numSimbols+=1
                        indice+=1            
            else:
                if actual == "\n": 
                    self.lineaActual+=1 
                    
                    posicion = indice+1
                    #print("posicion",posicion)                   
                indice+=1
        
    def agregarALista(self,token, linea, posicion, scope):
        #print("token en metodo ", token)
   
        descripcion, num = self.etiquetarToken(token)
        print("token ",token, "descripcion ",descripcion)
        if descripcion == "No encontrado":
            self.error(linea, posicion, mensaje="Token" +str(token.token)+"no encontrado")           
        objectoToken = Token()
        objectoToken.token = token;
        objectoToken.descripcion = descripcion
        objectoToken.num = num       
        objectoToken.posicion = posicion 
        objectoToken.linea = linea
        objectoToken.scope = scope

        self.result.append(objectoToken)

    def etiquetarToken(self, token):

        palabrasReservadas= {'lit-bool': ['true|false', self.LIT_BOOL],'keyword': ['var|and|break|dec|do|elif|not|else|if|inc|or|return|while', -1]}
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
                    "op-add": ['\+|-|not', self.OP_ADD],
                    "op-mul" : ['\*|\/|%', self.OP_MUL],                  
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
                elif token == "not": num = self.OP_ADD
                elif token == "or": num = self.OR
                elif token == "return": num = self.RETURN
                elif token == "while": num = self.WHILE
            if(resultado == "" and num == -1):
                #Analizar si es un identificador			
                patron = re.compile("^[a-zA-Z](\w)*")
                if(patron.fullmatch(token)):
                    resultado = "identifier"
                    num = self.ID                    
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
       self.tokensParser = tokens
       self.indexToken = -1    
       self.root = Node("Program")  
       self.move()
       self.Program(self.root)
       self.scrolledtext1.insert("1.0", "\n----ARBOL SINTACTICO----\n", 'arbol')
       for pre, fill, node in RenderTree(self.root):
           #print("%s%s" % (pre, node.name))
           self.scrolledtext1.insert(END, "%s%s" % (pre, node.name) +"\n")
       self.scrolledtext1.tag_config('arbol', background="lightblue", foreground='blue', justify="center") 
    def move(self):
        self.indexToken+=1
        if(self.indexToken >= len(self.tokensParser)):
            toke = Token()
            toke.token = "$"
            toke.descripcion ="Fin"
            toke.num =31
            toke.linea =self.tokenActual.linea
            toke.posicion = self.tokenActual.posicion
            toke.scope = self.tokenActual.scope

        self.tokenActual = self.tokensParser[self.indexToken] if self.indexToken < len(self.tokensParser) else toke
        if self.tokenActual.num == self.PESO:
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
        exit(0)

    def errorParser(self, tokensEsperados, mensaje = ""):
        elementos = "";
        for i in range(len(tokensEsperados)):
            if i == 0:
                elementos +=self.terminales[str(tokensEsperados[i])]
            else:    
                elementos+= ","+self.terminales[str(tokensEsperados[i])]     
        print("Error en la linea "+str(self.tokenActual.linea)+ " posicion "+ str(self.tokenActual.posicion ))
        print("Se esperaba alguno de los siguientes elementos \'"+ elementos+ "\'")    
        for pre, fill, node in RenderTree(self.root):
            print("%s%s" % (pre, node.name))        

        exit(0)


    def errorVariable(self, token,linea, posicion, declarada):
        if declarada:
            print("Error en la linea "+ str(linea)+", posicion "+str(posicion-1)+": variable "+str(token)+ " ya declarada")
        else:
            print("Error en la linea "+ str(linea)+", posicion "+str(posicion-1)+": variable "+str(token)+ " no declarada")
        exit(0)
    
    def asignarTipoVar(self, token, tipo):
        for i in range(len(self.tablaVariables)):
            if self.tablaVariables[i]['id'] == token:
                self.tablaVariables[i]['type'] = tipo
    def asignarTipoFun(self, token, tipo):
         for i in range(len(self.tablaFunciones)):
                if self.tablaFunciones[i]['id'] == token:
                    self.tablaFunciones[i]['return'] = tipo

    def variableDeclarada(self, token):        
        id = None
        print("token ",token.token)
        print("token ",token.scope)
        for simbolo in self.tablaVariables:            
            if simbolo['id'] == token.token:
                id = simbolo
                break
        print(id)
        if id is None:
            return False
        else:

            if id['inFunction'] == True and id['scope'] == token.scope:
                return True            
            elif  id['inFunction'] == False and token.scope >= id['scope']:
                return True
            else:                
                return False
    def funcionDeclarada(self, token):
        id = None
        for simbolo in self.tablaFunciones:
            print(simbolo)
            if simbolo['id'] == token.token:
                id = simbolo
                break     
        if id is None:         
            if token.token == 'printi'or token.token == 'printc'or token.token == 'prints'or token.token == 'println'or token.token == 'readi'or token.token == 'reads'or token.token == 'new'or token.token == 'size' or token.token == 'add'or token.token == 'get' or token.token == 'set':
                return True
            return False
        else:
            return True

    def Program(self, parent):
        if self.tokenActual.num == self.VAR:            
            self.DefList(parent)
        elif self.tokenActual.num == self.ID:
            self.DefList(parent)
        elif self.tokenActual.num == self.PESO:
            self.DefList(parent)
        else:
            self.errorParser([self.VAR, self.ID, self.PESO])
            
    def DefList(self, parent):
        parent = Node("DefList", parent = parent)

        if self.tokenActual.num == self.VAR:            
            self.DefListP(parent)
        elif self.tokenActual.num == self.ID:
            self.DefListP(parent)
        elif self.tokenActual.num == self.PESO:
            self.DefListP(parent)
        else:
            self.errorParser([self.VAR, self.ID, self.PESO])
    
    def DefListP(self,parent):
        parent = Node("DefListP", parent = parent)
        if self.tokenActual.num == self.PESO:   
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
    def VarDef(self,parent, isParam=False, inFuncion = False):
        parent = Node("VarDef", parent = parent)
        if self.tokenActual.num == self.VAR:
            self.consume(self.VAR, parent)
            self.VarList(parent,isParam, inFuncion)
            self.consume(self.PUNTOYCOMA,parent)

        else:
            self.errorParser([self.VAR])
    def FunDef(self, parent):
        parent = Node("FunDef", parent = parent)
        if self.tokenActual.num == self.ID:
            id = self.tokenActual
            self.consume(self.ID, parent)
            self.consume(self.PAR_IZQ, parent)
            numIds=self.ParamList(parent)            
            self.consume(self.PAR_DER, parent)
            self.consume(self.LLAVE_IZQ, parent)
            info = {'id':id.token,'numParam':numIds,'return':None, 'scope':id.scope}
            self.tablaFunciones.append(info)
            # if not self.funcionDeclarada(id):
            #     self.tablaFunciones.append(info)
            # else:                
            #     self.errorVariable(id.token, id.linea, id.posicion, declarada=True)
            self.VarDefList(parent)
            tipo = self.StmtList(parent)   
            if tipo is None:
                tipo = 'lit-int'         
            self.asignarTipoFun(id.token,tipo)
            #self.eliminarVariables(self.tokenActual.scope)
            self.consume(self.LLAVE_DER, parent)
            

        else:
            self.errorParser([self.ID])
    def VarList(self, parent, isParam=False, inFuncion = False):
        parent = Node("VarList", parent = parent)
        if self.tokenActual.num == self.ID:
            self.IdList(parent,isParam, inFuncion)
        else:
            self.errorParser([self.ID])
    def IdList(self, parent,  isParam=False, inFuncion = False):
        parent = Node("IdList", parent = parent)
        if self.tokenActual.num == self.ID:
            scope=self.tokenActual.scope
            if isParam:
                scope+=1                        
            info = {'id':self.tokenActual.token,'type':'None','scope':scope, 'inFunction':inFuncion}
            self.tablaVariables.append(info)
            # if not self.variableDeclarada(self.tokenActual):          
            #     self.tablaVariables.append(info)
            # else:                
            #     self.errorVariable(self.tokenActual.token,self.tokenActual.linea, self.tokenActual.posicion, declarada=True)
            self.consume(self.ID, parent)                
            numIds= self.IdListCount(parent, 1, isParam, inFuncion)
            
            return numIds
        else:
            self.errorParser([self.ID])
    def IdListCount(self, parent, numIds, isParam=False, inFuncion = False):
        parent = Node("IdListCont", parent = parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
            Node("ε", parent)               
            return numIds
        elif self.tokenActual.num == self.COMA:
            self.consume(self.COMA, parent)
            scope=self.tokenActual.scope
            if isParam:
                scope+=1                         
            info = {'id':self.tokenActual.token,'type':'None','scope':scope, 'inFunction':inFuncion}     
            self.tablaVariables.append(info)
            # if not self.variableDeclarada(self.tokenActual):
            #     self.tablaVariables.append(info)
            # else:                
            #     self.errorVariable(self.tokenActual.token,self.tokenActual.linea, self.tokenActual.posicion, declarada=True)
            self.consume(self.ID, parent)
            numIds+=1
            return self.IdListCount(parent, numIds, isParam,inFuncion)
        elif self.tokenActual.num == self.PAR_DER:
            Node("ε", parent)               
            return numIds
        else:
            self.errorParser([self.PUNTOYCOMA, self.COMA, self.PAR_DER])

    def ParamList(self, parent):
        parent = Node("ParamList", parent = parent)
        if self.tokenActual.num == self.ID:
            numIds= self.IdList(parent, isParam=True) #regresa el numero de ids que se declararon            
            return numIds
        elif self.tokenActual.num == self.PAR_DER:
            Node("ε", parent)           
            return 0
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
            self.VarDef(parent,inFuncion=True )
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
            return self.StmtListP(parent)
        elif self.tokenActual.num == self.ID:
            return self.StmtListP(parent)
        elif self.tokenActual.num == self.LLAVE_DER:
            return self.StmtListP(parent)
        elif self.tokenActual.num == self.INC:
            return self.StmtListP(parent)
        elif self.tokenActual.num == self.DEC:
            return self.StmtListP(parent)
        elif self.tokenActual.num == self.IF:
            return self.StmtListP(parent)
        elif self.tokenActual.num == self.WHILE:
            return self.StmtListP(parent)
        elif self.tokenActual.num == self.DO:
            return self.StmtListP(parent)
        elif self.tokenActual.num == self.BREAK:
            return self.StmtListP(parent)
        elif self.tokenActual.num == self.RETURN:    
            return self.StmtListP(parent)    
        else:
            self.errorParser([self.ID, self.LLAVE_DER,self.INC,self.DEC,self.IF,self.WHILE,self.DO,self.BREAK, self.RETURN, self.PUNTOYCOMA])
    
    def StmtListP(self, parent,):        
        parent = Node("StmtListP", parent = parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
            tipo = self.Stmt(parent)
            tipo2 = self.StmtListP(parent)
            if tipo is not None:
                return tipo
            else: return tipo2
        elif self.tokenActual.num == self.ID:
            tipo = self.Stmt(parent)
            tipo2 = self.StmtListP(parent)
            if tipo is not None:
                return tipo
            else: return tipo2
        elif self.tokenActual.num == self.LLAVE_DER:
            Node("ε", parent)   
            return 
        elif self.tokenActual.num == self.INC:
            tipo = self.Stmt(parent)
            tipo2 = self.StmtListP(parent)
            if tipo is not None:
                return tipo
            else: return tipo2
        elif self.tokenActual.num == self.DEC:
            tipo = self.Stmt(parent)
            tipo2 = self.StmtListP(parent)
            if tipo is not None:
                return tipo
            else: return tipo2
        elif self.tokenActual.num == self.IF:
            tipo = self.Stmt(parent)
            tipo2 = self.StmtListP(parent)
            if tipo is not None:
                return tipo
            else: return tipo2
        elif self.tokenActual.num == self.WHILE:
            tipo = self.Stmt(parent)
            tipo2 = self.StmtListP(parent)
            if tipo is not None:
                return tipo
            else: return tipo2
        elif self.tokenActual.num == self.DO:
            tipo = self.Stmt(parent)
            tipo2 = self.StmtListP(parent)
            if tipo is not None:
                return tipo
            else: return tipo2
        elif self.tokenActual.num == self.BREAK:
            tipo = self.Stmt(parent)
            tipo2 = self.StmtListP(parent)
            if tipo is not None:
                return tipo
            else: return tipo2
        elif self.tokenActual.num == self.RETURN:            
            tipo = self.Stmt(parent)
            tipo2 = self.StmtListP(parent)
            if tipo is not None:
                return tipo
            else: return tipo2
        else:
            self.errorParser([self.ID, self.LLAVE_DER,self.INC,self.DEC,self.IF,self.WHILE,self.DO,self.BREAK, self.RETURN, self.PUNTOYCOMA])
        
    def Stmt(self, parent):
        parent = Node("Stmt", parent = parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
            self.StmtEmpty(parent)
        elif self.tokenActual.num == self.ID:
            id = self.tokenActual;
            self.consume(self.ID, parent)
            self.StmtFactorizado(parent, id)
        elif self.tokenActual.num == self.INC:
            self.StmtIncr(parent)
        elif self.tokenActual.num == self.DEC:
            self.StmtDecr(parent)
        elif self.tokenActual.num == self.IF:
            self.StmtIf(parent)
        elif self.tokenActual.num == self.WHILE:
            self.StmtWhile(parent)
        elif self.tokenActual.num == self.DO:
            self.StmtDoWhile(parent)
        elif self.tokenActual.num == self.BREAK:
            self.StmtBreak(parent)
        elif self.tokenActual.num == self.RETURN:
            tipo = self.StmtReturn(parent)
            print("stmt ", tipo)           
            return tipo

            
        else:
            self.errorParser([self.PUNTOYCOMA, self.ID, self.INC,self.DEC, self.IF,self.WHILE, self.DO, self.BREAK, self.RETURN])
            
    def StmtEmpty(self,parent):
        parent = Node("StmtEmpty",parent=parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
            self.consume(self.PUNTOYCOMA, parent)
        else:
            self.errorParser([self.PUNTOYCOMA])
    
    def StmtFactorizado(self, parent, id ):        
        parent = Node("StmtFactorizado", parent=parent)
        if self.tokenActual.num == self.PAR_IZQ:
            # if not self.funcionDeclarada(id):
            #     self.errorVariable(id.token, id.linea, id.posicion, False)
            self.consume(self.PAR_IZQ,parent)
            self.ExprList(parent)
            self.consume(self.PAR_DER,parent)
            self.consume(self.PUNTOYCOMA,parent)
            
        elif self.tokenActual.num == self.OP_ASSIGN:
            # if not self.variableDeclarada(id):
            #     self.errorVariable(id.token, id.linea, id.posicion, False)
            self.consume(self.OP_ASSIGN,parent)
            tipo = self.Expr(parent)
            self.asignarTipoVar(id.token, tipo)
            self.consume(self.PUNTOYCOMA,parent)
        else:
            self.errorParser([self.PAR_IZQ,self.OP_ASSIGN])
    
    def StmtIncr(self,parent):
        parent = Node("StmtIncr", parent=parent)
        if self.tokenActual.num == self.INC:
            self.consume(self.INC,parent)
            if self.tokenActual.num == self.ID:
                self.consume(self.ID,parent)
                # if self.variableDeclarada(self.tokenActual):
                # 
                # else: 
                #     self.errorVariable(self.tokenActual.token, self.tokenActual.linea, self.tokenActual.posicion, False)
                self.consume(self.PUNTOYCOMA,parent)
            else:
                self.errorParser([self.ID])
        else:
            self.errorParser([self.INC])
    
    def StmtDecr(self,parent):
        parent = Node("StmtDecr", parent=parent)
        if self.tokenActual.num == self.DEC:
            self.consume(self.DEC,parent)
            if self.tokenActual.num != self.ID:
                self.errorParser([self.ID])
            self.consume(self.ID,parent)
            # if self.variableDeclarada(self.tokenActual):
            # 
            # else: 
            #     self.errorVariable(self.tokenActual.token, self.tokenActual.linea, self.tokenActual.posicion, False)        
            self.consume(self.PUNTOYCOMA,parent)
        else:
            self.errorParser([self.DEC])
    
    def StmtIf(self,parent):
        parent = Node("StmtIf", parent=parent)
        if self.tokenActual.num == self.IF:
            self.consume(self.IF,parent)
            self.consume(self.PAR_IZQ,parent)
            self.Expr(parent)
            self.consume(self.PAR_DER,parent)
            self.consume(self.LLAVE_IZQ,parent)
            self.StmtList(parent)
            self.consume(self.LLAVE_DER,parent)
            self.ElseIfList(parent)
            self.Else(parent)
        else:
            self.errorParser([self.IF])
    
    def StmtWhile(self,parent):
        parent = Node("StmtWhile", parent=parent)
        if self.tokenActual.num == self.WHILE:
            self.consume(self.WHILE,parent)
            self.consume(self.PAR_IZQ,parent)
            self.Expr(parent)
            self.consume(self.PAR_DER,parent)
            self.consume(self.LLAVE_IZQ,parent)
            self.StmtList(parent)
            self.consume(self.LLAVE_DER,parent)
        else:
            self.errorParser([self.WHILE])
    
    def StmtDoWhile(self,parent):
        parent= Node("StmtDoWhile",parent=parent)
        if self.tokenActual.num == self.DO:
            self.consume(self.DO,parent)
            self.consume(self.LLAVE_IZQ,parent)
            self.StmtList(parent)
            self.consume(self.LLAVE_DER,parent)
            self.consume(self.WHILE, parent)
            self.consume(self.PAR_IZQ,parent)
            self.Expr(parent)
            self.consume(self.PAR_DER,parent)
            self.consume(self.PUNTOYCOMA,parent)
        else:
            self.errorParser([self.DO])
    
    def StmtBreak(self,parent):
         parent= Node("StmtBreak",parent=parent)
         if self.tokenActual.num == self.BREAK:
             self.consume(self.BREAK,parent)
             self.consume(self.PUNTOYCOMA,parent)
         else:
             self.errorParser([self.BREAK])
    
    def StmtReturn(self,parent):
        parent= Node("StmtReturn",parent=parent)
        if self.tokenActual.num == self.RETURN:
             self.consume(self.RETURN,parent)
             tipo = self.Expr(parent)             
             self.consume(self.PUNTOYCOMA,parent)             
             return tipo
        else:
             self.errorParser([self.RETURN])
             
    def ExprList(self,parent):
        parent= Node("ExprList",parent=parent)
        if self.tokenActual.num == self.ID:
             self.Expr(parent)
             self.ExprListCont(parent)
        elif self.tokenActual.num == self.PAR_IZQ:
            self.Expr(parent)
            self.ExprListCont(parent)
        elif self.tokenActual.num == self.PAR_DER:
            Node("ε", parent)   
            return
        elif self.tokenActual.num == self.OP_ADD:
            self.Expr(parent)
            self.ExprListCont(parent)
        elif self.tokenActual.num == self.CORCH_IZQ:
            a = self.Expr(parent)
            self.ExprListCont(parent)
            return a
        elif self.tokenActual.num == self.CORCH_DER:
            Node("ε", parent)   
            return
        elif self.tokenActual.num == self.LIT_BOOL:
            self.Expr(parent)
            self.ExprListCont(parent)
        elif self.tokenActual.num == self.LIT_INT:
            self.Expr(parent)
            self.ExprListCont(parent)
        elif self.tokenActual.num == self.LIT_CHAR:
            self.Expr(parent)
            self.ExprListCont(parent)
        elif self.tokenActual.num == self.LIT_STR:
            self.Expr(parent)
            self.ExprListCont(parent)
     
        else:
             self.errorParser([self.ID,self.PAR_IZQ,self.PAR_DER,self.OP_ADD,self.CORCH_IZQ,self.CORCH_DER,self.LIT_BOOL,self.LIT_INT,self.LIT_CHAR,self.LIT_STR])
    
    def Expr(self,parent):
        parent= Node("Expr",parent=parent)        
        if self.tokenActual.num == self.ID:
             self.ExprOr(parent)
        elif self.tokenActual.num == self.PAR_IZQ:
            self.ExprOr(parent)
        elif self.tokenActual.num == self.OP_ADD:
            self.ExprOr(parent)
        elif self.tokenActual.num == self.CORCH_IZQ:
            return self.ExprOr(parent)
        elif self.tokenActual.num == self.LIT_BOOL:
            return self.ExprOr(parent)
        elif self.tokenActual.num == self.LIT_INT:
            return self.ExprOr(parent)
        elif self.tokenActual.num == self.LIT_CHAR:
            return self.ExprOr(parent)
        elif self.tokenActual.num == self.LIT_STR:
            return self.ExprOr(parent)
        else:
            self.errorParser([self.ID,self.PAR_IZQ,self.OP_ADD,self.CORCH_IZQ,self.LIT_BOOL,self.LIT_INT,self.LIT_CHAR,self.LIT_STR])
        
    def ElseIfList(self,parent):
        parent= Node("ElseIfList",parent=parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
             self.ElseIfListP(parent)
        elif self.tokenActual.num == self.ID:
            self.ElseIfListP(parent)
        elif self.tokenActual.num == self.LLAVE_DER:
            self.ElseIfListP(parent)
        elif self.tokenActual.num == self.INC:
            self.ElseIfListP(parent)
        elif self.tokenActual.num == self.DEC:
            self.ElseIfListP(parent)
        elif self.tokenActual.num == self.IF:
            self.ElseIfListP(parent)
        elif self.tokenActual.num == self.ELIF:
            self.ElseIfListP(parent)
        elif self.tokenActual.num == self.ELSE:
            self.ElseIfListP(parent)
        elif self.tokenActual.num == self.WHILE:
            self.ElseIfListP(parent)
        elif self.tokenActual.num == self.DO:
            self.ElseIfListP(parent)
        elif self.tokenActual.num == self.BREAK:
            self.ElseIfListP(parent)
        elif self.tokenActual.num == self.RETURN:
            self.ElseIfListP(parent)
        else:
            self.errorParser([self.PUNTOYCOMA,self.ID,self.LLAVE_DER,self.INC,self.DEC,self.IF,self.ELIF, self.ELSE, self.WHILE, self.DO, self.BREAK, self.RETURN])
        
    def Else(self,parent):
         parent= Node("Else",parent=parent)
         if self.tokenActual.num == self.PUNTOYCOMA:
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
         elif self.tokenActual.num == self.ELSE:
             self.consume(self.ELSE,parent)
             self.consume(self.LLAVE_IZQ,parent)
             self.StmtList(parent)
             self.consume(self.LLAVE_DER,parent)
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
         else:
             self.errorParser([self.PUNTOYCOMA, self.ID, self.LLAVE_DER, self.INC, self.DEC, self.IF, self.ELSE, self.WHILE, self.DO, self.BREAK, self.RETURN])
        
    def ExprListCont(self,parent):
        parent= Node("ExprListCont",parent=parent)
        if self.tokenActual.num == self.COMA:
             self.consume(self.COMA,parent)
             self.Expr(parent)
             self.ExprListCont(parent)
        elif self.tokenActual.num == self.PAR_DER:
             Node("ε", parent)
             return
        elif self.tokenActual.num == self.CORCH_DER:
             Node("ε", parent)
             return
        else:
            self.errorParser([self.COMA,self.PAR_DER,self.CORCH_DER])
    
    def ExprOr(self,parent):
        parent= Node("ExprOr",parent=parent)
        if self.tokenActual.num == self.ID:
             self.ExprAnd(parent)
             self.ExprOrP(parent)
        elif self.tokenActual.num == self.PAR_IZQ:
             self.ExprAnd(parent)
             self.ExprOrP(parent)
        elif self.tokenActual.num == self.OP_ADD:
             self.ExprAnd(parent)
             self.ExprOrP(parent)
        elif self.tokenActual.num == self.CORCH_IZQ:
             a = self.ExprAnd(parent)
             self.ExprOrP(parent)
             return a
        elif self.tokenActual.num == self.LIT_BOOL:
            a = self.ExprAnd(parent)
            self.ExprOrP(parent)
            return a
        elif self.tokenActual.num == self.LIT_INT:
            a = self.ExprAnd(parent)
            self.ExprOrP(parent)
            return a
        elif self.tokenActual.num == self.LIT_CHAR:
            a = self.ExprAnd(parent)
            self.ExprOrP(parent)
            return a
        elif self.tokenActual.num == self.LIT_STR:
            a = self.ExprAnd(parent)
            self.ExprOrP(parent)
            return a
        else:
            self.errorParser([self.ID,self.PAR_IZQ,self.OP_ADD,self.CORCH_IZQ,self.LIT_BOOL,self.LIT_INT,self.LIT_CHAR,self.LIT_STR])
    
    def ElseIfListP(self,parent):
        parent= Node("ElseIfListP",parent=parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
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
        elif self.tokenActual.num == self.ELIF:
             self.consume(self.ELIF,parent)
             self.consume(self.PAR_IZQ,parent)
             self.Expr(parent)
             self.consume(self.PAR_DER,parent)
             self.consume(self.LLAVE_IZQ,parent)
             self.StmtList(parent)
             self.consume(self.LLAVE_DER,parent)
             self.ElseIfListP(parent)
        elif self.tokenActual.num == self.ELSE:
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
        else:
             self.errorParser([self.PUNTOYCOMA, self.ID, self.LLAVE_DER, self.INC, self.DEC, self.IF, self.ELIF,self.ELSE, self.WHILE, self.DO, self.BREAK, self.RETURN])
    
    def ExprAnd(self,parent):
        parent= Node("ExprAnd",parent=parent)
        if self.tokenActual.num == self.ID:
            self.ExprComp(parent)
            self.ExprAndP(parent)     
        elif self.tokenActual.num == self.PAR_IZQ:
            self.ExprComp(parent)
            self.ExprAndP(parent)
        elif self.tokenActual.num == self.OP_ADD:
            self.ExprComp(parent)
            self.ExprAndP(parent)
        elif self.tokenActual.num == self.CORCH_IZQ:
            a = self.ExprComp(parent)
            self.ExprAndP(parent)
            return a
        elif self.tokenActual.num == self.LIT_BOOL:
            a = self.ExprComp(parent)
            self.ExprAndP(parent)
            return a
        elif self.tokenActual.num == self.LIT_INT:
            a = self.ExprComp(parent)
            self.ExprAndP(parent)
            return a
        elif self.tokenActual.num == self.LIT_CHAR:
            a = self.ExprComp(parent)
            self.ExprAndP(parent)
            return a
        elif self.tokenActual.num == self.LIT_STR:
            a = self.ExprComp(parent)
            self.ExprAndP(parent)
            return a
        else:
            self.errorParser([self.ID,self.PAR_IZQ,self.OP_ADD,self.CORCH_IZQ,self.LIT_BOOL,self.LIT_INT,self.LIT_CHAR,self.LIT_STR])
    
    def ExprOrP(self,parent):
        parent= Node("ExprOrP",parent=parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
             Node("ε", parent)
             return    
        elif self.tokenActual.num == self.COMA:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.PAR_DER:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OR:
            self.consume(self.OR,parent)
            self.ExprAnd(parent)
            self.ExprOrP(parent)
        elif self.tokenActual.num == self.CORCH_DER:
            Node("ε", parent)
            return
        else:
            self.errorParser([self.PUNTOYCOMA,self.COMA,self.PAR_DER,self.OR,self.CORCH_DER])
    
    def ExprComp(self,parent):
        parent= Node("ExprComp",parent=parent)
        if self.tokenActual.num == self.ID:
             self.ExprRel(parent)
             self.ExprCompP(parent)  
        elif self.tokenActual.num == self.PAR_IZQ:
            self.ExprRel(parent)
            self.ExprCompP(parent)
        elif self.tokenActual.num == self.OP_ADD:
            self.ExprRel(parent)
            self.ExprCompP(parent)
        elif self.tokenActual.num == self.CORCH_IZQ:
            a = self.ExprRel(parent)
            self.ExprCompP(parent)
            return a
        elif self.tokenActual.num == self.LIT_BOOL:
            a = self.ExprRel(parent)
            self.ExprCompP(parent)
            return a
        elif self.tokenActual.num == self.LIT_INT:
            a = self.ExprRel(parent)
            self.ExprCompP(parent)
            return a
        elif self.tokenActual.num == self.LIT_CHAR:
            a = self.ExprRel(parent)
            self.ExprCompP(parent)
            return a
        elif self.tokenActual.num == self.LIT_STR:
            a = self.ExprRel(parent)
            self.ExprCompP(parent)
            return a
        else:
            self.errorParser([self.ID,self.PAR_IZQ,self.OP_ADD,self.CORCH_IZQ,self.LIT_BOOL,self.LIT_INT,self.LIT_CHAR,self.LIT_STR])
            
    def ExprAndP(self,parent):
        parent= Node("ExprAndP",parent=parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
             Node("ε", parent)
             return    
        elif self.tokenActual.num == self.COMA:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.PAR_DER:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OR:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.AND:
              self.consume(self.AND,parent)
              self.ExprComp(parent)
              self.ExprAndP(parent)
        elif self.tokenActual.num == self.CORCH_DER:
            Node("ε", parent)
            return
        else:
            self.errorParser([self.PUNTOYCOMA,self.COMA,self.PAR_DER,self.OR,self.AND,self.CORCH_DER])
        
    def ExprRel(self,parent):
        parent= Node("ExprRel",parent=parent)
        if self.tokenActual.num == self.ID:
             self.ExprAdd(parent)
             self.ExprRelP(parent) 
        elif self.tokenActual.num == self.PAR_IZQ:
            self.ExprAdd(parent)
            self.ExprRelP(parent)
        elif self.tokenActual.num == self.OP_ADD:
            self.ExprAdd(parent)
            self.ExprRelP(parent)
        elif self.tokenActual.num == self.CORCH_IZQ:
            a = self.ExprAdd(parent)
            self.ExprRelP(parent)
            return a
        elif self.tokenActual.num == self.LIT_BOOL:
            a = self.ExprAdd(parent)
            self.ExprRelP(parent)
            return a
        elif self.tokenActual.num == self.LIT_INT:
            a = self.ExprAdd(parent)
            self.ExprRelP(parent)
            return a
        elif self.tokenActual.num == self.LIT_CHAR:
            a = self.ExprAdd(parent)
            self.ExprRelP(parent)
            return a
        elif self.tokenActual.num == self.LIT_STR:
            a = self.ExprAdd(parent)
            self.ExprRelP(parent)
            return a
        else:
            self.errorParser([self.ID,self.PAR_IZQ,self.OP_ADD,self.CORCH_IZQ,self.LIT_BOOL,self.LIT_INT,self.LIT_CHAR,self.LIT_STR])
    
    def ExprCompP(self,parent):
        parent= Node("ExprCompP",parent=parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
             Node("ε", parent)
             return    
        elif self.tokenActual.num == self.COMA:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.PAR_DER:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OR:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.AND:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OP_COMP:
            self.OpComp(parent)
            self.ExprRel(parent)
            self.ExprCompP(parent)
        elif self.tokenActual.num == self.CORCH_DER:
            Node("ε", parent)
            return
        else:
            self.errorParser([self.PUNTOYCOMA,self.COMA,self.PAR_DER,self.OR,self.AND,self.OP_COMP,self.CORCH_DER])
        
    def ExprAdd(self,parent):
        parent= Node("ExprAdd",parent=parent)        
        if self.tokenActual.num == self.ID:
             self.ExprMul(parent)
             self.ExprAddP(parent)   
        elif self.tokenActual.num == self.PAR_IZQ:
            self.ExprMul(parent)
            self.ExprAddP(parent)
        elif self.tokenActual.num == self.OP_ADD:
            self.ExprMul(parent)
            self.ExprAddP(parent)
 
        elif self.tokenActual.num == self.CORCH_IZQ:
            a = self.ExprMul(parent)
            self.ExprAddP(parent)
            return a
        elif self.tokenActual.num == self.LIT_BOOL:
            a = self.ExprMul(parent)
            self.ExprAddP(parent)
            return a
        elif self.tokenActual.num == self.LIT_INT:
            a = self.ExprMul(parent)
            self.ExprAddP(parent)
            return a
        elif self.tokenActual.num == self.LIT_CHAR:
            a = self.ExprMul(parent)
            self.ExprAddP(parent)
            return a
        elif self.tokenActual.num == self.LIT_STR:
            a = self.ExprMul(parent)
            self.ExprAddP(parent)
            return a
        else:
            self.errorParser([self.ID,self.PAR_IZQ,self.OP_ADD,self.CORCH_IZQ,self.LIT_BOOL,self.LIT_INT,self.LIT_CHAR,self.LIT_STR])
            
    def ExprRelP(self,parent):
        parent= Node("ExprRelP",parent=parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
             Node("ε", parent)
             return    
        elif self.tokenActual.num == self.COMA:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.PAR_DER:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OR:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.AND:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OP_COMP:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OP_REL:
            self.OpRel(parent)
            self.ExprAdd(parent)
            self.ExprRelP(parent)
        elif self.tokenActual.num == self.CORCH_DER:
            Node("ε", parent)
            return
        else:
            self.errorParser([self.PUNTOYCOMA,self.COMA,self.PAR_DER,self.OR,self.AND,self.OP_COMP,self.OP_REL,self.CORCH_DER])
    
    def ExprMul(self,parent):
        parent= Node("ExprMul",parent=parent)
        if self.tokenActual.num == self.ID:
             self.ExprUnary(parent)
             self.ExprMulP(parent)
        elif self.tokenActual.num == self.PAR_IZQ:
            self.ExprUnary(parent)
            self.ExprMulP(parent)
        elif self.tokenActual.num == self.OP_ADD:
            self.ExprUnary(parent)
            self.ExprMulP(parent)
        elif self.tokenActual.num == self.CORCH_IZQ:
            a = self.ExprUnary(parent)
            self.ExprMulP(parent)
            return a
        elif self.tokenActual.num == self.LIT_BOOL:
            a = self.ExprUnary(parent)
            self.ExprMulP(parent)
            return a
        elif self.tokenActual.num == self.LIT_INT:
            a = self.ExprUnary(parent)
            self.ExprMulP(parent)
            return a
        elif self.tokenActual.num == self.LIT_CHAR:
            a = self.ExprUnary(parent)
            self.ExprMulP(parent)
            return a
        elif self.tokenActual.num == self.LIT_STR:
            a = self.ExprUnary(parent)
            self.ExprMulP(parent)
            return a
        else:
            self.errorParser([self.ID,self.PAR_IZQ,self.OP_ADD,self.CORCH_IZQ,self.LIT_BOOL,self.LIT_INT,self.LIT_CHAR,self.LIT_STR])
    
    def OpComp(self,parent):
        parent= Node("OpComp",parent=parent)
        if self.tokenActual.num == self.OP_COMP:
             self.consume(self.OP_COMP,parent)
        else:
            self.errorParser([self.OP_COMP])
            
    def ExprAddP(self,parent):
        parent= Node("ExprAddP",parent=parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
             Node("ε", parent)
             return    
        elif self.tokenActual.num == self.COMA:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.PAR_DER:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OR:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.AND:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OP_COMP:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OP_REL:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OP_ADD and self.tokenActual.token != "not":
            self.OpAdd(parent)
            self.ExprMul(parent)
            self.ExprAddP(parent)
        elif self.tokenActual.num == self.CORCH_DER:
            Node("ε", parent)
            return
        else:
            self.errorParser([self.PUNTOYCOMA,self.COMA,self.PAR_DER,self.OR,self.AND,self.OP_COMP,self.OP_REL,self.OP_ADD,self.CORCH_DER])
    
    def OpRel(self,parent):
        parent= Node("OpRel",parent=parent)
        if self.tokenActual.num == self.OP_REL:
             self.consume(self.OP_REL,parent)
        else:
            self.errorParser([self.OP_REL])
    
    def ExprUnary(self,parent):
        parent= Node("ExprUnary",parent=parent)
        if self.tokenActual.num == self.ID:
             self.ExprPrimary(parent) 
        elif self.tokenActual.num == self.PAR_IZQ:
            self.ExprPrimary(parent)
        elif self.tokenActual.num == self.OP_ADD:
            self.OpAdd(parent)
            self.ExprUnary(parent)
        elif self.tokenActual.num == self.CORCH_IZQ:
            return self.ExprPrimary(parent)
        elif self.tokenActual.num == self.LIT_BOOL:
            return self.ExprPrimary(parent)
        elif self.tokenActual.num == self.LIT_INT:
            return self.ExprPrimary(parent)
        elif self.tokenActual.num == self.LIT_CHAR:
            return self.ExprPrimary(parent)
        elif self.tokenActual.num == self.LIT_STR:
            return self.ExprPrimary(parent)
        else:
            self.errorParser([self.ID,self.PAR_IZQ,self.OP_ADD,self.CORCH_IZQ,self.LIT_BOOL,self.LIT_INT,self.LIT_CHAR,self.LIT_STR])
    
    def ExprMulP(self,parent):
        parent= Node("ExprMulP",parent=parent)
        if self.tokenActual.num == self.PUNTOYCOMA:
             Node("ε", parent)
             return    
        elif self.tokenActual.num == self.COMA:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.PAR_DER:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OR:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.AND:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OP_COMP:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OP_REL:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OP_ADD:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OP_MUL:
            self.OpMul(parent)
            self.ExprUnary(parent)
            self.ExprMulP(parent)
        elif self.tokenActual.num == self.CORCH_DER:
            Node("ε", parent)
            return
        else:
            self.errorParser([self.PUNTOYCOMA,self.COMA,self.PAR_DER,self.OR,self.AND,self.OP_COMP,self.OP_REL,self.OP_ADD,self.OP_MUL,self.CORCH_DER])
    
    def OpAdd(self,parent):
        parent= Node("OpAdd",parent=parent)
        if self.tokenActual.num == self.OP_ADD:
             self.consume(self.OP_ADD,parent)  
        else:
            self.errorParser([self.OP_ADD])
    
    def ExprPrimary(self,parent):        
        parent= Node("ExprPrimary",parent=parent)
        if self.tokenActual.num == self.ID:
             self.consume(self.ID,parent)
             self.ExprPrimaryFact(parent)
        elif self.tokenActual.num == self.PAR_IZQ:
            self.consume(self.PAR_IZQ,parent)
            self.Expr(parent)
            self.consume(self.PAR_DER,parent)
        elif self.tokenActual.num == self.CORCH_IZQ:
             return self.Array(parent)
        elif self.tokenActual.num == self.LIT_BOOL:
             return self.Lit(parent)
        elif self.tokenActual.num == self.LIT_INT:
             return self.Lit(parent)
        elif self.tokenActual.num == self.LIT_CHAR:
             return self.Lit(parent)
        elif self.tokenActual.num == self.LIT_STR:
             return self.Lit(parent)
        else:
            self.errorParser([self.ID,self.PAR_IZQ,self.CORCH_IZQ,self.LIT_BOOL,self.LIT_INT,self.LIT_CHAR,self.LIT_STR])

    def OpMul(self,parent):
        parent= Node("OpMul",parent=parent)
        if self.tokenActual.num == self.OP_MUL:
             self.consume(self.OP_MUL,parent)
        else:
            self.errorParser([self.OP_MUL])
    
    def ExprPrimaryFact(self,parent):
        parent= Node("ExprPrimaryFact",parent=parent)        
        if self.tokenActual.num == self.PUNTOYCOMA:
             Node("ε", parent)
             return    
        elif self.tokenActual.num == self.COMA:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.PAR_IZQ:
            self.consume(self.PAR_IZQ,parent)
            self.ExprList(parent)
            self.consume(self.PAR_DER,parent)
        elif self.tokenActual.num == self.PAR_DER:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OR:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.AND:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OP_COMP:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OP_REL:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OP_ADD:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.OP_MUL:
            Node("ε", parent)
            return
        elif self.tokenActual.num == self.CORCH_DER:
            Node("ε", parent)
            return
        else:
            self.errorParser([self.PUNTOYCOMA,self.COMA,self.PAR_IZQ,self.PAR_DER,self.OR,self.AND,self.OP_COMP,self.OP_REL,self.OP_ADD,self.OP_MUL,self.CORCH_DER])
        
    def Array(self,parent):
        parent= Node("Array",parent=parent)
        if self.tokenActual.num == self.CORCH_IZQ:
             self.consume(self.CORCH_IZQ,parent)
             self.ExprList(parent)
             self.consume(self.CORCH_DER,parent)
             return "array"
        else:
            self.errorParser([self.CORCH_IZQ])
    
    def Lit(self,parent):
        parent= Node("Lit",parent=parent)
        if self.tokenActual.num == self.LIT_BOOL:
             self.consume(self.LIT_BOOL,parent)
             return 'lit-bool'
        elif self.tokenActual.num == self.LIT_INT:
            if int(self.tokenActual.token) <= 2147483647 and int(self.tokenActual.token) >= -2147483648:
                self.consume(self.LIT_INT,parent)
                return 'lit-int'
            else:
                self.error(self.tokenActual.linea,self.tokenActual.posicion,"Integer Overflow")
        elif self.tokenActual.num == self.LIT_CHAR:
             self.consume(self.LIT_CHAR,parent)
             return 'lit-char'
        elif self.tokenActual.num == self.LIT_STR:
             self.consume(self.LIT_STR,parent)
             return 'lit-str'
        else:
            self.errorParser([self.LIT_BOOL,self.LIT_INT,self.LIT_CHAR,self.LIT_STR])

aplicacion1 = Aplicacion()
