# ==========================================================
# Inteligencia Artificial. Tercer curso. Grupo 2.
# Grado en Ingeniería Informática - Tecnologías Informáticas
# Curso 2018-19
# Universidad de Sevilla
# Trabajo práctico
# Profesor: José Luis Ruiz Reina
# ===========================================================

# --------------------------------------------------------------------------
# Primer componente del grupo (o único autor): 
#
# APELLIDOS: Ramos Miró
# NOMBRE: Enrique
# 
# Segundo componente (si se trata de un grupo):
#
# APELLIDOS
# NOMBRE:
# ----------------------------------------------------------------------------

# *****************************************************************************
# HONESTIDAD ACADÉMICA Y COPIAS: un trabajo práctico es un examen, por lo que
# debe realizarse exclusivamente por cada estudiante o grupo. La discusión y
# el intercambio de información de carácter general con los compañeros se
# permite (e incluso se recomienda), pero NO AL NIVEL DE CÓDIGO. Igualmente el
# remitir código de terceros, obtenido a través de la red o cualquier otro
# medio, se considerará plagio.

# Cualquier plagio o compartición de código que se detecte significará
# automáticamente la calificación de CERO EN LA ASIGNATURA para TODOS los
# alumnos involucrados. Por tanto a estos alumnos NO se les conservará, para
# futuras convocatorias, ninguna nota que hubiesen obtenido hasta el
# momento. Sin perjuicio de OTRAS MEDIDAS DE CARÁCTER DISCIPLINARIO. 
# *****************************************************************************


# IMPORTANTE: NO CAMBIAR EL NOMBRE NI A ESTE ARCHIVO NI A LAS FUNCIONES QUE SE
# PIDEN 





# ---------------------------------------------------------------------------
# PARTE 0: Conjuntos de datos 
# ---------------------------------------------------------------------------

# EN ESTA PARTE NO SE PIDE NADA, PERO ES NECESARIO LEERLA PARA ENTENDER LA
# ESTRUCTURA DE LOS CONJUNTOS DE DATOS QUE SE PROPORCIONAN 
#
# Los archivos jugar_tenis.py, lentes.py, votos.py y credito.py (que se pueden
# descargar desde la página del trabajo) contienen los conjuntos de datos que
# vamos a usar para probar los algoritmos implementados.

# Cada archivo contiene la definición correspondiente de las siguientes
# variables:

# * atributos: es una lista de pares (Atributo,Valores) para cada atributo o
#   característica del conjunto de datos. Atributo es el nombre del atributo y
#   Valores es la lista de sus posibles valores.

# * atributo_clasificación: nombre del atributo de clasificación

# * clases: posibles valores (o clases) del atributo de clasificación

# * entr: conjunto de entrenamiento, una lista de ejemplos en los que cada
#   ejemplo es una lista de valores (cada valor indica el valor del atributo
#   correspondiente, en el mismo orden en el que aparecen en la lista de
#   atributos). El último valor del ejemplo es su clase.

# Además, votos.py y credito.py contienen las siguientes variables adicionales:

# * valid: conjunto de validación, una lista de ejemplos con el mismo formato
#     que la de entrenamiento. Este conjunto de ejemplo se usará para
#     generalizar el modelo aprendido con el de entrenamiento (en nuestro
#     caso, para hacer la poda). 

# * test: conjunto de test, una lista de ejemplos con el mismo formato
#     que la de entrenamiento. Este conjunto de ejemplo se usará para
#     medir el rendimiento final del clasificador aprendido. 

# Cargamos los cuatro conjuntos de datos:

import jugar_tenis
import lentes
import votos
import credito
import copy


# ---------------------------------------------------------------------------
# PARTE 1: Aprendizaje de reglas mediante cobertura
# ---------------------------------------------------------------------------

# En esta parte se trata de implementar el algoritmo de aprendizaje de reglas
# mediante cobertura, tal y como se explica en las diapositivas de la Sección 3 
# del tema 3.


# Representación de reglas:
# =========================

# Para implementar el algoritmo de cobertura, lo primero que hay que decidir
# es cómo se va a repesentar una regla en python. En lo que sigue
# describirimos una representación que NO ES OBLIGATORIA, pero que será la que
# usemos en nuestros ejemplos de ejecución. 

# Puesto que el algoritmo aprende todas las reglas a la vez para cada clase,
# no será necesario que representemos la conclusión de una regla (ya que para una
# clase dada será siempre la misma), sino que sólo necesitamos representar las
# condiciones de la regla.

# Si tenemos una regla 

#     Si Atr1=v1 y Atr2=v2 y ... y Atrn=vn Entonces Clase=c

# representaremos la regla mediante la lista de pares:

#  [(i1,v1),(i2,v2),...,(in,vn)]

# donde i1,i2,..,in son las posiciones de los atributos Atr1,...,Atrn
# en la lista atributos que aparece en el archivo de datos.

# Ejemplos:
# ---------

# Por ejemplo, en el ejemplo de las lentes de contacto, las condiciones de la regla:

# Si (Astigmatismo = +) y (Lagrima = Normal) y (Diagnóstico = Miope) Entonces [Lente = Rígida]

# se representan por la lista:

# [(2, '+'), (3, 'Normal'), (1, 'Miope')]

# ya que en la lista lentes.atributos, "Astigmatismo" está en la posición 2,
# "Lagrima" en la posición 3, y "Diagnóstico" en la posición 1. 

# Otro ejemplo. En jugar_tenis, las condiciones de la regla:

# Si (Humedad = Normal) y (Viento = Débil) Entonces [Jugar Tenis = si]

# se representan por la lista:

# [(2, 'Normal'), (3, 'Débil')]

# ya que en jugar_tenis.atributos, "Humedad" está en la posición 2 y "Viento"
# en la posición 3.
# -------------

# Función que se pide
# ===================

# Implementar una función "cobertura(entr,atributos,clase)" que recibiendo
# como entrada un conjunto de entrenamiento (en forma de lista de ejemplos),
# la lista de los atributos del problema (tal y como se representa en los
# archivos ded datos) y un valor de clasificación, devuelve la lista de las
# condiciones de la reglas aprendidas por el algoritmo de cobertura, tal y como
# se describe en la diapositiva 43 del tema 7.


    # Ejemplos:
# ---------

# >>> cobertura(lentes.entr,lentes.atributos,"Rígida")
# [[(2, '+'), (3, 'Normal'), (1, 'Miope')],
#  [(0, 'Joven'), (2, '+'), (3, 'Normal')]] 


# >>> cobertura(lentes.entr,lentes.atributos,"Blanda")
# [[(2, '-'), (3, 'Normal'), (1, 'Hipermétrope')],
#  [(2, '-'), (3, 'Normal'), (0, 'Joven')],
#  [(0, 'Prepresbicia'), (2, '-'), (3, 'Normal')]]

# >>> cobertura(jugar_tenis.entr,jugar_tenis.atributos,"no")
# [[(0, 'Soleado'), (2, 'Alta')], 
#  [(0, 'Lluvia'), (3, 'Fuerte')]]

# >>> cobertura(credito.entr,credito.atributos,"conceder") 
# [[(0, 'funcionario'), (5, 'altos')],
#  [(2, 'dos o más'), (5, 'medios')],
#  [(0, 'laboral'), (5, 'altos'), (1, 'ninguno')],
#  [(2, 'dos o más'), (0, 'funcionario'), (4, 'soltero')],
#  [(2, 'dos o más'), (0, 'funcionario'), (1, 'uno')],
#  [(0, 'laboral'), (5, 'altos'), (2, 'dos o más')],
#  [(0, 'laboral'), (5, 'altos'), (3, 'dos o más')],
#  [(2, 'dos o más'), (0, 'funcionario'), (3, 'uno')],
#  [(0, 'laboral'), (5, 'altos'), (4, 'viudo')],
#  [(2, 'dos o más'), (0, 'funcionario'), (4, 'divorciado')],
#  [(2, 'dos o más'), (0, 'funcionario'), (1, 'dos o más'), (3, 'dos o más')],
#  [(5, 'altos'), (0, 'laboral'), (4, 'casado')],
#  [(2, 'dos o más'), (0, 'parado'), (3, 'dos o más'), (4, 'divorciado')],
#  [(0, 'laboral'), (5, 'altos'), (2, 'una'), (3, 'uno')],
#  [(3, 'ninguno'), (2, 'dos o más'), (4, 'casado'), (1, 'uno'), (5, 'bajos')],
#  [(3, 'ninguno'), (0, 'parado'), (4, 'viudo'), (1, 'ninguno')],
#  [(2, 'dos o más'), (0, 'parado'), (1, 'dos o más'), (3, 'ninguno')],
#  [(3, 'ninguno'), (2, 'ninguna'), (4, 'viudo'), (0, 'parado')],
#  [(1, 'uno'),(2, 'dos o más'),(3, 'dos o más'),(0, 'parado'),(4, 'soltero')],
#  [(0, 'laboral'), (4, 'divorciado'), (2, 'ninguna'), (3, 'ninguno')]]
# ---------

def cobertura(entr,atributos,clase):
    
    reglas_aprendidas = []
    reglas = []
    frecuencia_relativa = 0
    mapa = {}
    mapa1 = {}
    ind = 0
    ind1 = 0
    entrenamiento = entr
    guarda_reglas = []
    frecuencia_valor = 0
    frecuencia_contador = 0
    cont_entr = 0
    lista_valores = []
    lista_claves = []
    
    while(cont_entr < len(entr)): #voy contando las veces que aparece en el conj de entr el valor del atributo. 
        if(entr[cont_entr][-1] == clase):
            frecuencia_valor +=1
        cont_entr += 1
    
    for a in atributos: #hago dos mapas idénticos para después usar uno y copiar el otro en ese, cuando necesite el mapa inicial.
        for i in a:
            mapa[ind] = i 
        ind = ind+1
    
    for a in atributos:
        for i in a:
            mapa1[ind1] = i 
        ind1 = ind1+1
     
    for k,v in mapa.items(): #guardo en dos listas diferentes las claves y valores del mapa
        lista_claves.append(k)
        lista_valores.append(v)

    while(frecuencia_contador != frecuencia_valor): #mientras la frec del contador que inicializo arriba a 0, sea distinta a la fre
                                                    #frecuencia del valor voy a permanecer dentro del 'while'
        while(frecuencia_relativa != 1): #hago como nos dice en el algoritmo de cobertura, que mientras sea distinta la frec relativa a 1, sigo iterando.
            tuplas_atributos = []
            n = 0
            cont_fr = 0
            max_num = 0
            for c,v in zip(lista_claves, lista_valores): #voy iterando por cada clave,valor en el mapa y a su vez por todos los valores de esa clave para ver posteriormente, si el valor es igual a al valor que hay en la posicion de la fila que me marca la clave (fila[k]). 
                for valor in v:
                    den = sum([1 for fila in entr if valor == fila[c]]) #calculo el denominador en una lista por comprensión, que me da 1 cuando se cumple la condición que quiero y luego lo sumo.
                    num = sum([1 for fila in entr if valor == fila[c] and clase == fila[-1]]) #idem, pero para el numerador.
                    
                    if(num == 0 and den == 0):#controlo si el numerador y el denominador son 0 para evitar la excepción de división por 0.
                        pass
                    else:
                        frec = num/den
                    
                    if(frec > cont_fr): #si la frec es mayor que el contador que voy a llevar para quedarme con la mayor frecuencia, también me quedo con el numerador para después comparar cuando haya dos frec relativas iguales quedarme con la que coja mas elementos.
                        cont_fr = frec   
                        max_num = num
                        n = c 
                        atributo_actual = valor 
                    
                    elif(frec == cont_fr): #cuando llego a una frec de 1, significa que voy a tener dos frec relativas iguales 2/2 o 3/3 por ejemplo, por eso me quedaré con 3/3 que cubre a más ejemlos 
                        if(frec==1 and num > max_num):
                                cont_fr = frec     
                                max_num = num
                                n = c
                                atributo_actual = valor      
                    
            tuplas_atributos.append(n) #voy guardando clave,valor en la tupla que va a ser una condición de una regla.
            tuplas_atributos.append(atributo_actual)
            tuplas_atributos = tuple(tuplas_atributos)
            
            frecuencia_relativa = cont_fr #actualizo la frecuencia, por si es 1, ya no entraría dentro del segundo while.
        
            #actualizo el conjunto de entrenamiento, quedandome con todos los ejemplos que cumplen el valor que he selecionado antes.
            cont_conj_entr = 0 
            conjunto_entr_nuevo = []
    
            while(cont_conj_entr < len(entr)):
                if(atributo_actual == entr[cont_conj_entr][n]):
                    conjunto_entr_nuevo.append(entr[cont_conj_entr])
                    
                cont_conj_entr += 1
            
            entr = conjunto_entr_nuevo    
            #print("conjunto de entrenamiento----->", entr)
            #print(mapa)
            del mapa[n] #borro del mapa la fila que he cogido del valor anterior, para que no pueda cogerlo más ni a el ni a ninguno de los que tienen ese atributo.
    
            reglas.append(tuplas_atributos) #voy añaniendo a la lista 'reglas' la tupla o condición de antes
        
        reglas_aprendidas.append(reglas) #guardo todas las reglas en la lista final de reglas.
        reglas = []
        frecuencia_relativa = 0
        frecuencia_contador += max_num #aumento la frecuencia del contador con el número de veces que aparece el valor en el conj de entrenamiento, para ver si me falta todavía alguno para volver al primer while y tratarlo en una iteración más.
        mapa = mapa1.copy() #copio el mapa1 en el mapa para que me vuelva a aparecer todo el mapa.
        for _ in entr: #por cada fila del conj de entr que me he quedado anteriormente, del entrenamiento(que tengo el conjunto sin modificar) lo elimino para no coger más esas filas del conj de entr.
            entrenamiento.remove(_)
            guarda_reglas.append(_) #a su vez voy guardandola en la variable 'guarda_reglas' para después, cuando se termine el algoritmo tenga todo el conjunto de entrenamiento al completo.
            
        entr = entrenamiento
        
    entr += guarda_reglas
    #print("Regla o reglas aprendidas para {}: ".format(clase), reglas_aprendidas)
    return reglas_aprendidas 

#print("***********************RÍGIDA*******************************************")  
#print(cobertura(lentes.entr,lentes.atributos,"Rígida"))
#print("**********************BLANDA********************************************")
#print(cobertura(lentes.entr,lentes.atributos,"Blanda"))
#print("**********************TENIS********************************************")
#print(cobertura(jugar_tenis.entr,jugar_tenis.atributos,"no"))
#print("**********************CREDITO********************************************")
#print(cobertura(credito.entr,credito.atributos,"conceder"))

# ---------------------------
# PARTE 2: Reglas de decisión
# ---------------------------

# El algoritmo de aprendizaje de reglas por cobertura nos permite aprender un
# conjunto de reglas por cada valor de clasificación. Si a partir de estas
# reglas queremos tener un clasificador para nuevos ejemplos, de los cuales no
# conocemos su clasificación, lo natural sería buscar una regla de las
# aprendididas que cubra al ejemplo (es decir, tal que el ejemplo cumple las
# condiciones de la regla), y entonces clasificar el ejemplo según el valor de
# clasificación que aparece en la conclusión de esa regla.

# Sin embargo, esta manera natural de clasificar usando reglas, a veces
# presenta algunos problemas:
# (1) Un mismo ejemplo podría ser cubierto con varias reglas distintas, 
#     con distintos valores de clasificación en sus conclusiones 
# (2) O por el contrario, puede que ninguna regla cubra al ejemplo. 

# En ambas situaciones, debemos decidir qué valor de clasificación le damos al
# ejemplo. Existen varias maneras de tratar esto, pero nosotros en este
# trabajo veremos la manera más simple, que pasamos a describir.  

# Para evitar el problema (1), el conjunto de reglas lo daremos ORDENADO, y
# consideraremos sólo la PRIMERA regla, en ese orden, que cubra al ejemplo que
# se quiere clasificar. Para ordenar el conjunto de reglas, colocaremos en
# primer lugar las reglas aprendidas para el valor de clasificación menos
# frecuente en el conjunto de entrenamiento, a continuación las reglas
# apendidas para la segunda clase menos frecuente, etc. La idea intuitiva es
# que las clases menos frecuentes se tratan primero, ya que son más
# específicas.  Además, para evitar el problema (2), en último lugar no
# incluiremos las reglas de la clase más frecuente, sino que colocaremos al
# final una sola regla para dicha clase, sin condiciones (es decir,
# devolveríamos el valor de clasificación más frecuente en ejemplos que no
# cumplen las condiciones de ninguna de las reglas de las restantes clases).

# Los conjuntos de reglas ordenados que clasifican los ejemplos como se han
# descrito, los llamaremos REGLAS DE DECISIÓN. Por ejemplo, lo que sigue es un
# conjunto de reglas de decisión para el ejemplo de las lentes:

# Ejemplo:
# --------

# * Si (Astigmatismo = +) y (Lagrima = Normal) y (Diagnóstico = Miope) Entonces [Lente = Rígida]
# * Si (Edad = Joven) y (Astigmatismo = +) y (Lagrima = Normal) Entonces [Lente = Rígida]
# * Si (Astigmatismo = -) y (Lagrima = Normal) y (Diagnóstico = Hipermétrope) Entonces [Lente = Blanda]
# * Si (Astigmatismo = -) y (Lagrima = Normal) y (Edad = Joven) Entonces [Lente = Blanda]
# * Si (Edad = Prepresbicia) y (Astigmatismo = -) y (Lagrima = Normal) Entonces [Lente = Blanda]
# * En caso contrario, [Lente = Ninguna]

# Con estas reglas de decisión, si queremos clasificar el ejemplo 
#   ["Joven","Hipermétrope","-","Normal"]
# lo clasificaríamos como "Blanda", ya que la primera regla que cubre al
# ejemplo es la tercera. 
# Si queremos clasificar el ejemplo 
# ["Joven","Hipermétrope","-","Reducida"]
# entonces lo calificaríamos como "Ninguna", ya que no lo cubre ninguna de las
# reglas, excepto la última.
# ---------

# En python, los conjuntos de reglas de decisión se pueden representar de la
# siguiente manera (no es obligatorio representarlo así, es sólo una posible
# manera):

# [[Clase_1,[R11,R12, ...]],
#  [Clase_2,[R21,R22,....]] 
#  .....
#  [Clase_n,[[]]]

# Donde [Ri1,Ri2,...] a su vez son la lista de reglas (en realidad, sólo sus
# condiciones) de la clase i. 

# Ejemplo:
# --------

# Por ejemplo, lo que sigue es la representación en python del conjunto de
# reglas de decisión anterior:

# [['Rígida',
#    [[(2, '+'), (3, 'Normal'), (1, 'Miope')],
#   [(0, 'Joven'), (2, '+'), (3, 'Normal')]]],
# ['Blanda',
#  [[(2, '-'), (3, 'Normal'), (1, 'Hipermétrope')],
#   [(2, '-'), (3, 'Normal'), (0, 'Joven')],
#   [(0, 'Prepresbicia'), (2, '-'), (3, 'Normal')]]],
# ('Ninguna', [[]])]

# Un conjunto de reglas de decisión para el problema de jugar al tenis: 

# [['no', [[(0, 'Soleado'), (2, 'Alta')], 
#          [(0, 'Lluvia'), (3, 'Fuerte')]]],
#  ['si', [[]]]]
# ---------

# Funciones que se piden:
# -----------------------

# - Una función "reglas_decision_cobertura(entr,atributos,clases)", que
#   recibiendo como entrada un conjunto de entrenamiento (en forma de lista de
#   ejemplos), la lista de los atributos del problema (tal y como se representa
#   en los archivos ded datos) y la lista de valores de clasificación del
#   problema, aprende un conjunto de reglas de decisión mediante el algoritmo de
#   cobertura. En concreto, esta función debe ordenar las clases de menor a
#   mayor frencuencia en el conjunto de entrenamiento, y en ese orden, para cada
#   clase aprender el correspondiente conjunto de reglas (llamando a la función
#   "cobertura" anteriormente implementada). Para la última clase (la más
#   frecuente en el conjunto de entrenamiento), no se aprenden reglas, sino que
#   se coloca una única regla sin condiciones.

# - Una función "imprime_RD(reglas_decision,atributos,atributo_clasificacion)"
#   que recibe un conjunto de reglas de clasificación, la lista de los atributos
#   del problema (tal y como se representa en los archivos de datos) y el nombre
#   del atributo de clasificación, e imprime las reglas de una manera más
#   legible, tal y como por ejemplo se muestra arriba. 

# - Una función "clasifica_RD(ej,reglas_decision)" que recibe un ejemplo ej y
#   un conjunto de reglas de decisión, y devuelve la clasificación que el
#   conjunto de reglas de decisión da para ese ejemplo.

# - Una función "rendimiento_RD(reglas_decision,ejemplos)" que devuelve el
#   rendimiento del conjunto de reglas de decisión sobre un conjunto de
#   ejemplos de los que ya se conoce su valor de clasificación. El rendimiento se
#   define como la proporción de ejemplos que se clasifican correctamente. 


# Ejemplos:
# ---------

# Jugar al tenis:
# ______________

# >>> jt_rd=reglas_decision_cobertura(jugar_tenis.entr,jugar_tenis.atributos,jugar_tenis.clases)
# >>> imprime_RD(jt_rd,jugar_tenis.atributos,jugar_tenis.atributo_clasificación)

# * Si (Cielo = Soleado) y (Humedad = Alta) Entonces [Jugar Tenis = no]
# * Si (Cielo = Lluvia) y (Viento = Fuerte) Entonces [Jugar Tenis = no]
# * En caso contrario, [Jugar Tenis = si]

# >>> clasifica_RD(['Soleado' ,'Suave','Alta','Fuerte'],jt_rd)
# 'no'
# >>> rendimiento_RD(jt_rd,jugar_tenis.entr)
# 1.0


# Lentes de contacto:
# ___________________

# >>> lentes_rd=reglas_decision_cobertura(lentes.entr,lentes.atributos,lentes.clases)
# >>> imprime_RD(lentes_rd,lentes.atributos,lentes.atributo_clasificación)

# * Si (Astigmatismo = +) y (Lagrima = Normal) y (Diagnóstico = Miope) Entonces [Lente = Rígida]
# * Si (Edad = Joven) y (Astigmatismo = +) y (Lagrima = Normal) Entonces [Lente = Rígida]
# * Si (Astigmatismo = -) y (Lagrima = Normal) y (Diagnóstico = Hipermétrope) Entonces [Lente = Blanda]
# * Si (Astigmatismo = -) y (Lagrima = Normal) y (Edad = Joven) Entonces [Lente = Blanda]
# * Si (Edad = Prepresbicia) y (Astigmatismo = -) y (Lagrima = Normal) Entonces [Lente = Blanda]
# * En caso contrario, [Lente = Ninguna]

# >>> clasifica_RD(["Joven","Hipermétrope","-","Normal"],lentes_rd)
# 'Blanda'
# >>> clasifica_RD(["Joven","Hipermétrope","-","Reducida"],lentes_rd)
# 'Ninguna'
# >>> rendimiento_RD(lentes_rd,lentes.entr)
# 1.0

# Votos:
# ______


# >>> votos_rd=reglas_decision_cobertura(votos.entr,votos.atributos,votos.clases)
# >>> imprime_RD(votos_rd,votos.atributos,votos.atributo_clasificación)

# * Si (voto4 = s) y (voto7 = s) Entonces [Partido = republicano]
# * Si (voto4 = s) y (voto2 = ?) Entonces [Partido = republicano]
# * Si (voto4 = s) y (voto13 = n) Entonces [Partido = republicano]
# * Si (voto4 = s) y (voto6 = n) Entonces [Partido = republicano]
# * Si (voto4 = s) y (voto8 = ?) Entonces [Partido = republicano]
# * Si (voto4 = s) y (voto14 = ?) Entonces [Partido = republicano]
# * Si (voto4 = s) y (voto11 = ?) Entonces [Partido = republicano]
# * Si (voto4 = s) y (voto15 = ?) Entonces [Partido = republicano]
# * Si (voto4 = s) y (voto7 = ?) Entonces [Partido = republicano]
# * Si (voto4 = s) y (voto14 = n) Entonces [Partido = republicano]
# * Si (voto4 = s) y (voto3 = n) y (voto13 = s) Entonces [Partido = republicano]
# * Si (voto4 = ?) y (voto9 = ?) Entonces [Partido = republicano]
# * Si (voto3 = n) y (voto12 = ?) Entonces [Partido = republicano]
# * Si (voto3 = n) y (voto6 = n) y (voto15 = n) Entonces [Partido = republicano]
# * En caso contrario, [Partido = demócrata]

# >>> clasifica_RD(votos.test[23],votos_rd)
# 'demócrata'
# >>> rendimiento_RD(votos_rd,votos.entr)
# 1.0
# >>> rendimiento_RD(votos_rd,votos.valid)
# 0.9565217391304348
# >>> rendimiento_RD(votos_rd,votos.test)
# 0.9195402298850575


# Concesión de crédito:
# _____________________

# >>> credito_rd=reglas_decision_cobertura(credito.entr,credito.atributos,credito.clases)
# >>> imprime_RD(credito_rd,credito.atributos,credito.atributo_clasificación)

# * Si (Empleo = funcionario) y (Ingresos = altos) Entonces [Crédito = conceder]
# * Si (Propiedades = dos o más) y (Ingresos = medios) Entonces [Crédito = conceder]
# * Si (Empleo = laboral) y (Ingresos = altos) y (Productos = ninguno) Entonces [Crédito = conceder]
# * Si (Propiedades = dos o más) y (Empleo = funcionario) y (Estado civil = soltero) Entonces [Crédito = conceder]
# * Si (Propiedades = dos o más) y (Empleo = funcionario) y (Productos = uno) Entonces [Crédito = conceder]
# * Si (Empleo = laboral) y (Ingresos = altos) y (Propiedades = dos o más) Entonces [Crédito = conceder]
# * Si (Empleo = laboral) y (Ingresos = altos) y (Hijos = dos o más) Entonces [Crédito = conceder]
# * Si (Propiedades = dos o más) y (Empleo = funcionario) y (Hijos = uno) Entonces [Crédito = conceder]
# * Si (Empleo = laboral) y (Ingresos = altos) y (Estado civil = viudo) Entonces [Crédito = conceder]
# * Si (Propiedades = dos o más) y (Empleo = funcionario) y (Estado civil = divorciado) Entonces [Crédito = conceder]
# * Si (Propiedades = dos o más) y (Empleo = funcionario) y (Productos = dos o más) y (Hijos = dos o más) Entonces [Crédito = conceder]
# * Si (Ingresos = altos) y (Empleo = laboral) y (Estado civil = casado) Entonces [Crédito = conceder]
# * Si (Propiedades = dos o más) y (Empleo = parado) y (Hijos = dos o más) y (Estado civil = divorciado) Entonces [Crédito = conceder]
# * Si (Empleo = laboral) y (Ingresos = altos) y (Propiedades = una) y (Hijos = uno) Entonces [Crédito = conceder]
# * Si (Hijos = ninguno) y (Propiedades = dos o más) y (Estado civil = casado) y (Productos = uno) y (Ingresos = bajos) Entonces [Crédito = conceder]
# * Si (Hijos = ninguno) y (Empleo = parado) y (Estado civil = viudo) y (Productos = ninguno) Entonces [Crédito = conceder]
# * Si (Propiedades = dos o más) y (Empleo = parado) y (Productos = dos o más) y (Hijos = ninguno) Entonces [Crédito = conceder]
# * Si (Hijos = ninguno) y (Propiedades = ninguna) y (Estado civil = viudo) y (Empleo = parado) Entonces [Crédito = conceder]
# * Si (Productos = uno) y (Propiedades = dos o más) y (Hijos = dos o más) y (Empleo = parado) y (Estado civil = soltero) Entonces [Crédito = conceder]
# * Si (Empleo = laboral) y (Estado civil = divorciado) y (Propiedades = ninguna) y (Hijos = ninguno) Entonces [Crédito = conceder]
# * Si (Ingresos = bajos) y (Empleo = parado) y (Propiedades = una) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = jubilado) y (Propiedades = ninguna) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Propiedades = ninguna) y (Empleo = funcionario) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = parado) y (Productos = ninguno) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = jubilado) y (Productos = dos o más) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = parado) y (Hijos = ninguno) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = laboral) y (Productos = uno) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = parado) y (Estado civil = viudo) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = jubilado) y (Propiedades = una) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Propiedades = ninguna) y (Productos = ninguno) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = parado) y (Productos = uno) y (Propiedades = ninguna) Entonces [Crédito = no conceder]
# * Si (Ingresos = medios) y (Propiedades = ninguna) y (Empleo = jubilado) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = jubilado) y (Hijos = uno) Entonces [Crédito = no conceder]
# * Si (Empleo = parado) y (Ingresos = medios) y (Propiedades = ninguna) y (Productos = dos o más) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Estado civil = divorciado) y (Propiedades = ninguna) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Estado civil = divorciado) y (Empleo = laboral) y (Productos = ninguno) Entonces [Crédito = no conceder]
# * Si (Ingresos = medios) y (Empleo = parado) y (Propiedades = ninguna) y (Productos = uno) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = jubilado) y (Estado civil = soltero) Entonces [Crédito = no conceder]
# * Si (Ingresos = medios) y (Productos = ninguno) y (Propiedades = una) y (Estado civil = soltero) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = jubilado) y (Estado civil = divorciado) y (Productos = ninguno) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = laboral) y (Productos = ninguno) Entonces [Crédito = no conceder]
# * Si (Ingresos = medios) y (Empleo = parado) y (Propiedades = ninguna) y (Hijos = uno) Entonces [Crédito = no conceder]
# * Si (Ingresos = medios) y (Hijos = dos o más) y (Propiedades = una) y (Productos = dos o más) Entonces [Crédito = no conceder]
# * Si (Empleo = parado) y (Ingresos = bajos) y (Productos = uno) y (Hijos = uno) Entonces [Crédito = no conceder]
# * Si (Empleo = parado) y (Ingresos = medios) y (Productos = ninguno) y (Hijos = uno) Entonces [Crédito = no conceder]
# * Si (Ingresos = medios) y (Empleo = parado) y (Productos = ninguno) y (Estado civil = soltero) Entonces [Crédito = no conceder]
# * Si (Ingresos = medios) y (Hijos = dos o más) y (Propiedades = una) y (Empleo = parado) Entonces [Crédito = no conceder]
# * Si (Empleo = jubilado) y (Ingresos = bajos) y (Estado civil = divorciado) y (Hijos = ninguno) Entonces [Crédito = no conceder]
# * Si (Ingresos = medios) y (Propiedades = ninguna) y (Empleo = parado) y (Estado civil = divorciado) Entonces [Crédito = no conceder]
# * Si (Ingresos = medios) y (Empleo = jubilado) y (Productos = dos o más) y (Propiedades = una) Entonces [Crédito = no conceder]
# * Si (Empleo = laboral) y (Hijos = dos o más) y (Propiedades = ninguna) y (Ingresos = medios) y (Productos = uno) Entonces [Crédito = no conceder]
# * En caso contrario, [Crédito = estudiar]

# >>> clasifica_RD(credito.test[44],credito_rd)
# 'estudiar'
# >>> clasifica_RD(credito.test[11],credito_rd)
# 'conceder'

# >>> rendimiento_RD(credito_rd,credito.entr)
# 1.0
# >>> rendimiento_RD(credito_rd,credito.valid)
# 0.8950617283950617
# >>> rendimiento_RD(credito_rd,credito.test)
# 0.8895705521472392

#PRIMERA FUNCIÓN
def reglas_decision_cobertura(entr,atributos,clases):
    
    dicc = {}
    for clase in clases: #itero sobre las clases 
        frecuencia_atributos = 0
        for lin in entr:
            if(lin[-1] == clase): #si la clase es igual al último elemento de cada final en el conjunto de entrenamiento, que es la clase de esa fila.
                frecuencia_atributos +=1
        dicc[frecuencia_atributos] = clase #creo un diccionaria con clave la frecuencia del atributo y el valor la clase con la que aparece en el conj de entr.
    
    
    reglas_decision = list(dicc.items()) #paso el diccionario a una lista.
    reglas_decision.sort() #ordeno la lista, para que las clases aparezcan de menor a mayor frencuencia en el conjunto de entrenamiento como nos dice en el enunciado.
    
    dicc2 = {}
    lista_reglas_decision = []
    lista = []
    ls = []
    for regla in reglas_decision:
        if(regla != reglas_decision[-1]): #evito que me coja la última regla.
            var = regla[1]
            dicc2[var] = cobertura(entr, atributos, var) #creo un dicc2 en el que llamo a la función cobertura anterior, para que me calcule todas las reglas.
            lista = list(dicc2.items())
            for tupla in lista:
                ls = list(tupla)
                if(ls in lista_reglas_decision): #evito que haya reglas repetidas.
                    pass
                else:
                    lista_reglas_decision.append(ls)#mi variable final en la que voy a guardar todas las reglas de decisión.
        else:
            
            var1 = regla[1]
            lista_atr_final = []
            lista_atr_final.append(var1)
            lista_atr_final.append([[]]) #añado al último atributo una lista vacía.
            lista_reglas_decision.append(lista_atr_final)
            
    #print("Reglas de decisión aprendidas: ", lista_reglas_decision)  
    return lista_reglas_decision

#print("********LENTES*****")
lentes_rd = reglas_decision_cobertura(lentes.entr, lentes.atributos, lentes.clases)
lentes_rd
#print(lentes_rd)
#print("*******JUGAR_TENIS*****")
jt_rd = reglas_decision_cobertura(jugar_tenis.entr,jugar_tenis.atributos,jugar_tenis.clases)
jt_rd
#print(jt_rd)
#print("*********VOTOS*****")
votos_rd = reglas_decision_cobertura(votos.entr,votos.atributos,votos.clases)
votos_rd
#print(votos_rd)
#print("********CREDITO*****")
credito_rd = reglas_decision_cobertura(credito.entr,credito.atributos,credito.clases)
credito_rd
#print(credito_rd)

#SEGUNDA FUNCIÓN
# * Si (Astigmatismo = +) y (Lagrima = Normal) y (Diagnóstico = Miope) Entonces [Lente = Rígida]
# * Si (Edad = Joven) y (Astigmatismo = +) y (Lagrima = Normal) Entonces [Lente = Rígida]
# * Si (Astigmatismo = -) y (Lagrima = Normal) y (Diagnóstico = Hipermétrope) Entonces [Lente = Blanda]
# * Si (Astigmatismo = -) y (Lagrima = Normal) y (Edad = Joven) Entonces [Lente = Blanda]
# * Si (Edad = Prepresbicia) y (Astigmatismo = -) y (Lagrima = Normal) Entonces [Lente = Blanda]
# * En caso contrario, [Lente = Ninguna]

# * Si (Cielo = Soleado) y (Humedad = Alta) Entonces [Jugar Tenis = no]
# * Si (Cielo = Lluvia) y (Viento = Fuerte) Entonces [Jugar Tenis = no]
# * En caso contrario, [Jugar Tenis = si]

def imprime_RD(reglas_decision,atributos,atributo_clasificacion):
    
    cont_final = 0
    for regla in reglas_decision:
    
        valor_clasificacion = regla[0]
        valor_reglas = regla[1]
        for r in valor_reglas:
            if(cont_final == 1): #este contador es para que si vale 1, rompa el for, porque significa que ya no queda más reglas que tratar por eso imprimimos mas abajo "Si ({} = {}) Entonces [{} = {}] \n"
                break
            else:
                cont = 1
                a = ""
                b = ""
                c = ""
            for j in r:
                valor = j[1] #me quedo con el valor del atributo
                num_atr = j[0]#me quedo con el número del atributo
                atributo = atributos[num_atr][0]#veo el numero del atributo a que nombre se refiere en la lista de atributos, por ejemplo, para tenis 0->cielo.
                if(cont < len(r)): #controlo que el contador inicializado a 1 arriba sea menor que la longitudo de la regla.
                    if(cont == 1):
                        a = ("Si ({} = {}) y ".format(atributo, valor))
                        
                    else:
                        b += ("({} = {}) y ".format(atributo, valor))
                        
                    cont += 1
                else:
                    if(cont == 1):
                        c = ("Si ({} = {}) Entonces [{} = {}] \n".format(atributo, valor, atributo_clasificacion, valor_clasificacion))
                        print(c)
                        cont_final += 1 
                        break
                        
                    else:
                        c = ("({} = {}) Entonces [{} = {}] \n".format(atributo, valor, atributo_clasificacion, valor_clasificacion))
                        print(a + b + c)
                        
                    
    print("En caso contrario, [{} = {}]".format(atributo_clasificacion, valor_clasificacion))       
                
#imprime_RD(lentes_rd,lentes.atributos,lentes.atributo_clasificación)
#imprime_RD(jt_rd,jugar_tenis.atributos,jugar_tenis.atributo_clasificación)
#imprime_RD(votos_rd,votos.atributos,votos.atributo_clasificación)
#imprime_RD(credito_rd,credito.atributos,credito.atributo_clasificación)


#TERCERA FUNCIÓN
# - Una función "clasifica_RD(ej,reglas_decision)" que recibe un ejemplo ej y
#   un conjunto de reglas de decisión, y devuelve la clasificación que el
#   conjunto de reglas de decisión da para ese ejemplo.
# * Si (Cielo = Soleado) y (Humedad = Alta) Entonces [Jugar Tenis = no]
# * Si (Cielo = Lluvia) y (Viento = Fuerte) Entonces [Jugar Tenis = no]
# * En caso contrario, [Jugar Tenis = si]
# >>> clasifica_RD(['Soleado' ,'Suave','Alta','Fuerte'],jt_rd)
# 'no'

def clasifica_RD(ej,reglas_decision):
    
    lista_un_elemento = []
    for i in reglas_decision:
        
        valor_clasificacion = i[0] #valor_clasificacion, va a tomar por ejemplo para el ejemplo de lentes Rígida y valor_reglas '+'
        valor_reglas = i[1]
        for r in valor_reglas:
            cont = 0
            for j in r:
                valor = j[1]
                numero = j[0]
                
                if(valor == ej[numero]): #veo sin en el conjunto que me pasan por parámetros en la posición que me diga el valor j[0] es igual que el valor que seleciono con valor.
                    cont += 1 #si es así, voy contando.
                else:
                    pass
            
            if(cont == len(r)): #si cont es igual que la longitud de la regla, significará que en esa línea del conjunto de entrenamiento coinciden los dos valores.
                lista_un_elemento.append(valor_clasificacion)#añado a la lista la clase. si o no, en el ejemplo del tenis.
            
            else:
                pass
    
    if(lista_un_elemento != []):
        return lista_un_elemento[0]
        #print("Clasificación que el conjunto de reglas de decisión da para este ejemplo: ","'",lista_un_elemento[0],"'")
    else:
        return valor_clasificacion
        #print("Clasificación que el conjunto de reglas de decisión da para este ejemplo: ","'",valor_clasif,"'")         


#RESULTADOS QUE DEBEN DE SALIR
#print(clasifica_RD(['Soleado' ,'Suave','Alta','Fuerte'],jt_rd))
# 'no'
#print(clasifica_RD(["Joven","Hipermétrope","-","Normal"],lentes_rd))
# 'Blanda'
#print(clasifica_RD(["Joven","Hipermétrope","-","Reducida"],lentes_rd))
# 'Ninguna'
#print(clasifica_RD(votos.test[23],votos_rd))
# 'demócrata'
#print(clasifica_RD(credito.test[44],credito_rd))
# 'estudiar'
#print(clasifica_RD(credito.test[11],credito_rd))
# 'conceder'


#CUARTA FUNCIÓN   
# - Una función "rendimiento_RD(reglas_decision,ejemplos)" que devuelve el
#   rendimiento del conjunto de reglas de decisión sobre un conjunto de
#   ejemplos de los que ya se conoce su valor de clasificación. El rendimiento se
#   define como la proporción de ejemplos que se clasifican correctamente. 


def rendimiento_RD(reglas_decision,ejemplos):
  
    num = 0
    den = len(ejemplos) #denominador va a ser la longitud de conjunto de ejemplos que se pasa por parámetros.
    for i in ejemplos:
        valor_clasif = i[-1] #me quedo con el último elemento.
        valor_clasif_RD = clasifica_RD(i, reglas_decision) #llamo al método clasifica de antes para obtener la clase en el 'valor_clasif_RD'.
        if(valor_clasif == valor_clasif_RD): #simplemente comparo si el valor de clasf es igual que el que me da la función Clasifica_RD.
            num += 1 # si es así numerador le voy sumando 1.
    
    rendimiento_final = num/den
    
    #print("El rendimiento final del conjunto de reglas de decisión sobre un conjunto de ejemplos es: ", rendimiento_final)
    return rendimiento_final
    
    
#RESULTADOS QUE DEBEN DE SALIR
#print("rendimiento tenis conj_entr:",rendimiento_RD(jt_rd,jugar_tenis.entr))
# 1.0
#print("rendimiento lentes conj_entr:",rendimiento_RD(lentes_rd,lentes.entr))
# 1.0
#print("rendimiento votos conj_entr:",rendimiento_RD(votos_rd,votos.entr))
# 1.0
#print("rendimiento votos validación:",rendimiento_RD(votos_rd,votos.valid))
# 0.9565217391304348
#print("rendimiento votos test:",rendimiento_RD(votos_rd,votos.test))
# 0.9195402298850575
#print("rendimiento credito conj_entr:",rendimiento_RD(credito_rd,credito.entr))
# 1.0
#print("rendimiento credito validación:",rendimiento_RD(credito_rd,credito.valid))
# 0.8950617283950617
#print("rendimiento credito test:",rendimiento_RD(credito_rd,credito.test))
# 0.8895705521472392



# -----------------------------------
# PARTE 3: Poda para reducir el error  
# -----------------------------------

# Uno de los principales problema en el aprendizaje de conjuntos de reglas de
# decisión es el sobreajuste. Es decir, que el conjunto de reglas aprendido se
# ajuste tanto al conjunto de entrenamiento que aprenda también el "ruido", o
# características que son específicas del conjunto de entrenamiento, pero que
# no ocurren en general.

# Para combatir el sobreajuste, una técnica muy extendida es aplicar un
# proceso de "podado" de la reglas que se han aprendido. Por podado de reglas
# entendemos quitar algunas condiciones a las reglas, o incluso eliminar
# alguna regla completamente (más abajo se describen las posibles podas con
# detalle). Para medir si el realizar una determinada poda es beneficioso,
# medimos el rendimiento en un conjunto de ejemplos distinto al de
# entrenamiento (que llamaremos conjunto de validación). El rendimiento del
# conjunto final de reglas de decisión, resultante de las podas, se comprueba
# sobre un tercer conjuto de ejemplos (llamado de "test"), distinto de los dos
# anteriores. 

# En nuestro caso, vamos a aplicar una técnica de podado muy simple, de manera
# que sólo permitimos dos tipos de podas:
# - Elegir una regla con más de una condición, y eliminar LA ÚLTIMA condición.
# - Elegir una clase que tenga más de una regla y eliminar completamente LA
#   ÚLTIMA regla de esa clase 

# El algoritmo que se pide implementar es muy similar al que se ha visto en el
# tema 3 para árboles de decisión excepto que las podas que se pueden realizar
# se hacen sobre las reglas y tienen que ser de uno de los dos tipos anteriores.

# En concreto, a partir de un conjunto RD de reglas de decisión que se recibe
# como entrada (que será el que se ha aprendido mediante cobertura sobre el
# conjunto de entrenamiento) y de un conjunto de ejemplos de validación, el
# algoritmo de poda de reglas (o de POSPODA) debe realizar lo siguiente:

# 1. Medir el rendimiento de RD sobre el conjunto de validación.
# 2. Para cada posible manera de realizar una poda de uno de los dos tipos
#    anteriores, se mide el rendimiento, sobre el conjunto de validación, del 
#    conjunto de reglas resultante de realizar esa poda. 
#    Sea RD* el resultado de la poda con el MEJOR rendimiento.
# 3. Si RD tiene un rendimiento menor o igual que el de RD*, entonces hacer RD
#    igual a RD*, e ir de nuevo al punto 1. Si RD tiene un rendimiento mayor
#    que RD*, entonces terminar y devolver RD.         


# Función que se pide:
# -------------------


# - Definir una función "poda_RD(reglas_de_decision,ejemplos)", que recibiendo
#   como entrada un conjunto de reglas de decisión y un conjunto de ejemplos de
#   validación, devuelve un nuevo conjunto de reglas de decisión que resulta de
#   aplicar el algoritmo de poda que se acaba de describir.

  

# Ejemplos:
# ---------


# Votos:
# ______

# >>> votos_rd_pd=poda_RD(votos_rd,votos.valid)
# >>> imprime_RD(votos_rd_pd,votos.atributos,votos.atributo_clasificación)

# * Si (voto4 = s) Entonces [Partido = republicano]
# * En caso contrario, [Partido = demócrata]

# >>> rendimiento_RD(votos_rd_pd,votos.entr)
# 0.96415770609319
# >>> rendimiento_RD(votos_rd_pd,votos.valid)
# 0.9855072463768116
# >>> rendimiento_RD(votos_rd_pd,votos.test)
# 0.9080459770114943


# Concesión de crédito:
# _____________________


# >>> credito_rd_pd=poda_RD(credito_rd,credito.valid)
# >>> imprime_RD(credito_rd_pd,credito.atributos,credito.atributo_clasificación)

# * Si (Empleo = funcionario) y (Ingresos = altos) Entonces [Crédito = conceder]
# * Si (Propiedades = dos o más) y (Ingresos = medios) Entonces [Crédito = conceder]
# * Si (Empleo = laboral) y (Ingresos = altos) Entonces [Crédito = conceder]
# * Si (Propiedades = dos o más) y (Empleo = funcionario) Entonces [Crédito = conceder]
# * Si (Ingresos = bajos) y (Empleo = parado) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = jubilado) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Propiedades = ninguna) y (Empleo = funcionario) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = parado) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = jubilado) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = parado) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = laboral) y (Productos = uno) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = parado) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = jubilado) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Propiedades = ninguna) y (Productos = ninguno) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = parado) Entonces [Crédito = no conceder]
# * Si (Ingresos = medios) y (Propiedades = ninguna) y (Empleo = jubilado) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = jubilado) Entonces [Crédito = no conceder]
# * Si (Empleo = parado) y (Ingresos = medios) y (Propiedades = ninguna) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Estado civil = divorciado) y (Propiedades = ninguna) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Estado civil = divorciado) y (Empleo = laboral) y (Productos = ninguno) Entonces [Crédito = no conceder]
# * Si (Ingresos = medios) y (Empleo = parado) y (Propiedades = ninguna) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = jubilado) Entonces [Crédito = no conceder]
# * Si (Ingresos = medios) y (Productos = ninguno) y (Propiedades = una) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = jubilado) Entonces [Crédito = no conceder]
# * Si (Ingresos = bajos) y (Empleo = laboral) y (Productos = ninguno) Entonces [Crédito = no conceder]
# * Si (Ingresos = medios) y (Empleo = parado) y (Propiedades = ninguna) Entonces [Crédito = no conceder]
# * Si (Ingresos = medios) y (Hijos = dos o más) y (Propiedades = una) y (Productos = dos o más) Entonces [Crédito = no conceder]
# * En caso contrario, [Crédito = estudiar]

# >>> rendimiento_RD(credito_rd_pd,credito.entr)
# 0.9353846153846154
# >>> rendimiento_RD(credito_rd_pd,credito.valid)
# 1.0
# >>> rendimiento_RD(credito_rd_pd,credito.test)
# 0.9877300613496932


# Comentario:
# -----------

# Como se observa, en el caso del ejemplo del crédito, el rendimiento sobre el
# conjunto de test mejora considerablemente una vez se realiza la poda (aunque
# empeora sobre el conjunto de entrenamiento, lo cual es previsible). En el caso
# de los votos, el conjunto podado no mejora al conjunto sin podar. Decir que
# aunque la técnica de podar que aquí se pide es simple y bastante aceptable,
# existen técnicas de poda más sofisticadas, que obtienen mejores resultados.
     
def poda_RD(reglas_de_decision,ejemplos):
    
    rendimiento_sin_poda = rendimiento_RD(reglas_de_decision, ejemplos)
    #print(rendimiento_sin_poda)
    cont = 0
    rendimiento_cont_regla = 0
    ultima_regla = 0
    lista = copy.deepcopy(reglas_de_decision) #he tenido que importar copy para que me deje hacer una copia de las reglas de decisión.
    
    #Elegir una clase que tenga más de una regla y eliminar completamente LA ÚLTIMA regla de esa clase 
    for regla in lista:
        if(regla[1] != [[]]): #me quedo con todas las reglas menos la última.
            if(len(regla[1]) > 1):#miro a ver si la clase tiene mas de una regla
                ultima_regla = len(lista[cont][1])-1 #calculo el índice de la última regla, para eliminarla.
                lista[cont][1].pop(ultima_regla)
                rendimiento_poda_regla = rendimiento_RD(lista, ejemplos) #voy calculando el rendimiento de haber podado la última regla.
                
                if(rendimiento_poda_regla > rendimiento_cont_regla):#y voy comparando para quedarme con el mejor rendimiento de todas las clases.
                    rendimiento_cont_regla = rendimiento_poda_regla
                    reglas_decision_final_regla = copy.deepcopy(lista)
                    
            cont += 1
            
            lista = copy.deepcopy(reglas_de_decision)#copio la lista de reglas de decisión para inicializarla de nuevo.
            
    #Elegir una regla con más de una condición, y eliminar LA ÚLTIMA condición.
    cont1 = 0
    cont2 = 0
    rendimiento_cont_tupla = 0
    rendimiento_poda_tupla = 0
    for regla in lista:
        if(regla[1] != [[]]):
            for r in regla[1]:
                tamaño_regla = len(r)
                if(tamaño_regla > 1): #comprueba que tiene la regla mas de una condición o tupla por así decirlo.
                    elemento_ult_tupla = tamaño_regla-1
                    lista[cont1][1][cont2].pop(elemento_ult_tupla)#voy eliminando cada última tupla de las reglas y con el cont2 voy recorriendo cada regla y el cont1 es con el que recorro cada clase.
                    rendimiento_poda_tupla = rendimiento_RD(lista, ejemplos)#calculo rendimiento con la poda que he echo sin la condición de la regla, y comparo, para quedarme con el mejor rendimiento.
                    if(rendimiento_poda_tupla > rendimiento_cont_tupla):
                    
                        rendimiento_cont_tupla = rendimiento_poda_tupla
                        #cuando borro la última cláusula, reinicio de nuevo lista, para ver el rendimiento sin borrar la que he quitado anteriormente.   
                        reglas_decision_final_tupla = copy.deepcopy(lista)
                 
                cont2 += 1      
                lista = copy.deepcopy(reglas_de_decision)     
                
        cont1 += 1
    
        
    if(rendimiento_sin_poda > rendimiento_cont_regla and rendimiento_sin_poda > rendimiento_cont_tupla):#comparo si el rendimiento sin poda es mejor que el rendimiento con poda de condición y de reglas
        
        return reglas_de_decision
        
    
    elif(rendimiento_cont_regla > rendimiento_sin_poda and rendimiento_cont_regla > rendimiento_cont_tupla):#comparo si el rendimiento sin regla es mejor que el rendimiento sin poda y el rendimiento de sin condiciones.
    
        return reglas_decision_final_regla
        
    
    elif(rendimiento_cont_tupla > rendimiento_sin_poda and rendimiento_cont_tupla > rendimiento_cont_regla):#comparo si el rendimiento sin alguna condición es mejor que el rendimiento sin poda y el rendimiento de sin alguna regla.
    
        return reglas_decision_final_tupla

    


#EJEMPLOS QUE DEBEN DE SALIR

#------PODA VOTOS-------
#votos_rd_pd=poda_RD(votos_rd,votos.valid)
#print(votos_rd_pd)
#print()
#imprime_RD(votos_rd_pd,votos.atributos,votos.atributo_clasificación)
# * Si (voto4 = s) Entonces [Partido = republicano]
# * En caso contrario, [Partido = demócrata]
#print()
#print("Conjunto de validación:",rendimiento_RD(votos_rd_pd,votos.valid))
# 0.9855072463768116
#print("Conjunto de entrenamiento:",rendimiento_RD(votos_rd_pd,votos.entr))
# 0.96415770609319
#print("Test:",rendimiento_RD(votos_rd_pd,votos.test))
# 0.9080459770114943

#-------PODA CREDITO-------
#credito_rd_pd=poda_RD(credito_rd,credito.valid)
#imprime_RD(credito_rd_pd,credito.atributos,credito.atributo_clasificación)

#print(rendimiento_RD(credito_rd_pd,credito.entr))
# 0.9353846153846154
#print(rendimiento_RD(credito_rd_pd,credito.valid))
# 1.0
#print(rendimiento_RD(credito_rd_pd,credito.test))
# 0.9877300613496932


# -----------------------
# PARTE 4: Clasificadores
# -----------------------

# En ese apartado NO SE PIDE IMPLEMENTAR NINGÚN ALGORITMO, tan solo nos va
# servir para tratar los dos clasificadores vistos (cobertura y cobertura con
# pospoda) bajo un marco común

# En este trabajo, por clasificador, entendemos una clase que incluye métodos
# para el entrenamiento y la clasificación, junto con otros métodos, como la
# impresión del clasificador. En concreto, un clasificador será una subclase
# de la siguiente clase general:

class MetodoClasificacion:
    """
    Clase base para métodos de clasificación
    """

    def __init__(self, atributo_clasificacion,clases,atributos):

        """
        Argumentos de entrada al constructor (ver jugar_tenis.py, por ejemplo)
         
        * atributo_clasificacion: nombre del atributo de clasificación 
        * clases: lista de posibles valores del atributo de clasificación.  
        * atributos: lista con pares en los que están los atributos (o
                     características)  y su lista de valores posibles.
        """

        self.atributo_clasificacion=atributo_clasificacion
        self.clases = clases
        self.atributos=atributos


    def entrena(self,entr,valid=None):
        """
        Método genérico para entrenamiento y ajuste del
        clasificador. Deberá ser definido para cada clasificador en
        particular. 
        
        Argumentos de entrada:

        * entr: ejemplos del conjunto de entrenamiento 
        * valid: ejemplos del conjunto de validación. 
                 Algunos clasificadores simples no usan conjunto de
                 validación, por lo que en esos casos se 
                 omitiría este argumento. 
        """
        pass

    def clasifica(self, ejemplo):
        """
        Método genérico para clasificación de un ejemplo, una vez entrenado el
        clasificador. Deberá ser definido para cada clasificador en
        particular.

        Si se llama a este método sin haber entrenado previamente el
        clasificador, debe devolver un excepción ClasificadorNoEntrenado
        (introducida más abajo) 
        """
        pass

    def imprime_clasificador(self):
        """
        Método genérico para imprimir por pantalla el clasificador
        obtenido. Deberá ser definido para cada clasificador en 
        particular. 

        Si se llama a este método sin haber entrenado previamente el
        clasificador, debe devolver un excepción ClasificadorNoEntrenado
        (introducida más abajo) 
        """
        pass



# Excepción que ha de devolverse se llama al método de clasificación (o al de
# impresión) antes de ser entrenado:  
        
class ClasificadorNoEntrenado(Exception): pass


# Nótese que para cualquier objeto que sea instancia de una subclase de la
# clase anterior, podemos calcular su rendimiento como clasificador, sobre un
# conjunto dado de ejemplos. Es lo que hace la siguiente función:

# Función general de rendimiento:

def rendimiento(clasificador,ejemplos):
    return sum([(clasificador.clasifica(ejemplo[:-1])==ejemplo[-1]) 
                for ejemplo in ejemplos])/len(ejemplos)

# En este marco de clasificadores que se ha presentado, encajan muchos de los
# métodos usados en el aprendizaje automático de clasificadores, definiendo de
# manera concreta el aprendizaje y la clasificación. Se pide definir en este
# marco general los dos clasificadores vistos en los apartados anteriores.
 

# Clases que se piden:
# ====================

# * Implementar la clase ClasificadorCobertura, como subclase de la clase
#   MetodoClasificacion anterior. En esta clase, los métodos son:
#   - Entrenamiento: algoritmo de aprendizaje de reglas de decisión por
#     cobertura.  
#   - Clasificación: clasificar con el conjunto de reglas de decisión
#     anterior. 
#   - Imprimir clasificador: imprimir el conjunto de reglas de decisión.
#   Además de los atributos de la clase genérica, se pueden incluir otros si
#   fuera necesario (por ejemplo, será necesario un atributo de la clase para
#   guardar el conjunto de reglas de decisión).  

# * Implementar la clase ClasificadorCoberturaPospoda, de manera análoga a la
#   anterior, pero en el que el entrenamiento consiste en aplicar cobertura,
#   seguido de una aplicación del algoritmo de pospoda. Cobertura se aplica
#   con el conjunto de entrenamiento y la poda con el conjunto de validación.

class ClasificadorCobertura(MetodoClasificacion):
    
    def __init__(self, atributo_clasificacion,clases,atributos):
        self.atributo_clasificacion=atributo_clasificacion
        self.clases = clases
        self.atributos=atributos 
        self.reglas_decision = []
        
    def entrena(self,entr,valid=None):
        self.reglas_decision = reglas_decision_cobertura(entr, self.atributos, self.clases)
        
    def clasifica(self, ejemplo):
        if(self.reglas_decision == []):
            print(ClasificadorNoEntrenado("¡¡Tienes que entrenar antes al clasificador!!")) 
        else:
            return clasifica_RD(ejemplo, self.reglas_decision)
        
    def imprime_clasificador(self):
        if(self.reglas_decision == []):
            print(ClasificadorNoEntrenado("¡¡Tienes que entrenar antes al clasificador!!"))
        else:
            imprime_reglas_decision = imprime_RD(self.reglas_decision,self.atributos,self.atributo_clasificacion)
            return imprime_reglas_decision
            
        
class ClasificadorCoberturaPospoda(MetodoClasificacion):
    
    def __init__(self, atributo_clasificacion,clases,atributos):
        self.atributo_clasificacion=atributo_clasificacion
        self.clases = clases
        self.atributos=atributos 
        self.reglas_decision = []
    
    def entrena(self,entr,valid=None):
        self.reglas_decision = reglas_decision_cobertura(entr, self.atributos, self.clases)
        self.reglas_decision = poda_RD(self.reglas_decision, valid)
    
    def clasifica(self, ejemplo):
        if(self.reglas_decision == []):
            print(ClasificadorNoEntrenado("¡¡Tienes que entrenar antes al clasificador!!")) 
        else:
            return clasifica_RD(ejemplo, self.reglas_decision)
        
    def imprime_clasificador(self):
        if(self.reglas_decision == []):
            print(ClasificadorNoEntrenado("¡¡Tienes que entrenar antes al clasificador!!"))
        else:
            imprime_reglas_decision = imprime_RD(self.reglas_decision,self.atributos,self.atributo_clasificacion)
            return imprime_reglas_decision 

# Ejemplos:
# ---------

# Votos:
# ______

#clasificador_cob_votos=ClasificadorCobertura(votos.atributo_clasificación,votos.clases,votos.atributos)

#No va a clasificar, porque antes tenemos que entrenar al clasificador.
#clasificador_cob_votos.imprime_clasificador()
#print()
#
#clasificador_cob_votos.entrena(votos.entr)

#Ya una vez entrenado, si nos va a clasificar el clasificador.
#clasificador_cob_votos.imprime_clasificador()
#
#print(clasificador_cob_votos.clasifica(['n','s','n','s','s','s','n','n','n','s','?','s','s','s','n','s']))
# 'republicano'
#
#print("clasificador votos validación:",rendimiento(clasificador_cob_votos,votos.valid))
# 0.9565217391304348
#
#print("clasificador votos test:",rendimiento(clasificador_cob_votos,votos.test))
# 0.9195402298850575
#

#clasificador_cobpos_votos=ClasificadorCoberturaPospoda(votos.atributo_clasificación,votos.clases,votos.atributos)
#
#clasificador_cobpos_votos.entrena(votos.entr,votos.valid)
#
#print(rendimiento(clasificador_cobpos_votos,votos.test))
# 0.9080459770114943



# Concesión de crédito:
# _____________________

#clasificador_cob_credito=ClasificadorCobertura(credito.atributo_clasificación,credito.clases,credito.atributos)
#
#clasificador_cob_credito.entrena(credito.entr)
#
#print(clasificador_cob_credito.clasifica(['funcionario','uno','dos o más','dos o más','soltero','altos','conceder']))
# 'conceder'
#
#print(rendimiento(clasificador_cob_credito,credito.test))
# 0.8895705521472392
#
#
#clasificador_cobpos_credito=ClasificadorCoberturaPospoda(credito.atributo_clasificación,credito.clases,credito.atributos)
#           
#clasificador_cobpos_credito.entrena(credito.entr,credito.valid)
#
#print(rendimiento(clasificador_cobpos_credito,credito.test))
# 0.9877300613496932




# ---------------------------------------------------------------------------
# PARTE 5: Entendiendo la supervivencia en el hundimiento del Titanic
# ---------------------------------------------------------------------------

# En este apartado, se pide usar los dos clasificadores anteriores para,
# a partir de los datos sobre pasajeros del Titanic (a descargar desde la
# página del trabajo), tratar de obtener un árbol de decisión para explicar la
# supervivencia o no de un pasajero del Titanic.

# Para ello, realizar los siguientes pasos:

# - Preprocesado de los datos: los datos están "en bruto", así que hay que
#   preparar los datos para que los puedan usar los clasificadores.
# - Aprendizaje y ajuste del modelo: aplicando a los datos los entrenamientos
#   de alguno de los clasificadores del apartado anterior.
# - Evaluacion del rendimiento del clasificador. 


# Damos a continuación algunos comentarios sobre la etapa del preprocesado de
# los datos:

# - En el conjunto de datos que se proporcionan hay una serie de atributos que
#   obviamente no influyen en la supervivencia (por ejemplo, el nombre del
#   pasajero). Esto hace que haya que seleccionar como atributos las
#   características que se crean realmente relevantes. Esto se suele
#   realizar con algunas técnicas estadísticas, pero en este trabajo sólo
#   vamos a pedir elegir (eligiendo razonablemente, o probando varias
#   alternativas) TRES ATRIBUTOS que se consideren son los que mejor
#   determinan la supervivencia o no.
# - El atributo "Edad" es numérico, y nuestra implementación no trata bien los
#   atributos con valores numéricos. Existen técnicas para tratar los
#   atributos numéricos, que básicamente dividen los posibles valores a tomar
#   en intervalos, de la mejor manera posible. En nuestro caso, por
#   simplificar, lo vamos a hacer directamente con el siguiente criterio:
#   transformar el valor EDAD en un valor binario, en el que sólo anotamos si
#   el pasajero tiene 13 AÑOS O MENOS, o si tiene MÁS DE 13 AÑOS.
# - En los datos, hay algunos valores de algunos ejemplos, que aparecen como
#   NA (desconocidos). Dos técnicas muy simples para tratar valores
#   desconocidos pueden ser: sustituir NA por el valor más frecuente en todos 
#   los ejemplos de la clase del ejemplo, o por la media aritmética de ese valor
#   en los ejemplos de la misma clase (esta última opción sólo tiene sentido con los 
#   atributos numéricos).
# - Para realizar el entrenamiento, la poda y la medida del rendimiento, se
#   necesita dividir el conjunto de datos en tres partes: entrenamiento,
#   validación y test. Hay que decidir la proporción adecuada de datos que van
#   a cada parte. También hay que procurar además que la partición sea
#   estratificada: la proporción de los ejemplos según los distintos valores
#   de los atributos debe de ser en cada parte, similar a la proporción en el
#   total de ejemplos.   


# El resultado final de esta parte debe ser:

# * Un archivo titanic.py, con un formato análogo a los archivos de datos que
#   se han proporcionado (votos.py o credito.py, por ejemplo), en el que se
#   incluye el resultado del preprocesado de los datos en bruto.  

# * Un conjunto de reglas de decisión (el que mejor rendimiento obtenga
#   finalmente), en el que se explique la supervivencia o no de un pasajero en
#   el Titanic. Se pide explicar (mediante comentarios) todo el proceso
#   realizado hasta llegar a esas reglas de decisoón. Incluir este conjuto de
#   reglas decisión (como comentario al código) en el fichero titanic.py

import titanic
"""
clasificador_cob_titanic=ClasificadorCobertura(titanic.atributo_clasificación, titanic.clases,titanic.atributos)
#print(clasificador_cob_titanic)
#
clasificador_cob_titanic.entrena(titanic.entr)
clasificador_cob_titanic.imprime_clasificador()
print("- Rendimiento sin poda: ",rendimiento(clasificador_cob_titanic,titanic.test))

clasificador_cobpos_titanic=ClasificadorCoberturaPospoda(titanic.atributo_clasificación,titanic.clases,titanic.atributos)
#           
clasificador_cobpos_titanic.entrena(titanic.entr,titanic.valid)
#
clasificador_cobpos_titanic.imprime_clasificador()
print("- Rendimiento con poda: ",rendimiento(clasificador_cobpos_titanic,titanic.test))
"""







