# # -*- coding: UTF-8 -*-
from mercado import Mercado
import sys
import os
import gc
from datetime import datetime
import time
import _thread
from pws import Pws
from logger import Logger

from acceso_db_conexion import Conexion_DB
from acceso_db_funciones import Acceso_DB_Funciones
from acceso_db_modelo import Acceso_DB

from controlador_de_tiempo import Controlador_De_Tiempo
from variables_globales import  Global_State
from bot_main_modules.habilitar_pares import habilitar_deshabilitar_pares_periodicamente
from bot_main_modules.funciones_principales import crear_cliente, esperar_correcto_funcionamiento,controlar_estado0,esperar_a_que_todos_mueran
from bot_main_modules.materializar_pares import materializar_pares_desde_db
from bot_main_modules.reportes import reporte_correo,reporte_de_ciclo
from bot_main_modules.funciones_logs import log_pares_estado, mostrar_informacion


e = Global_State()                               #Objeto con información global del bot
log=Logger('auto_compra_vende.log')              #log para este modulo
log.set_log_level(e.log_level)
pws=Pws()
client = crear_cliente(pws,log)
esperar_correcto_funcionamiento(client,e,log)    #antes de hacer algo, controlo que el exchange esté funcionando

conn=Conexion_DB(log)                            #apertura del poll de conexiones
fxdb=Acceso_DB_Funciones(log,conn.pool)          #funciones para acceso a datos
hpdb = Acceso_DB(log,fxdb)                       #modelo hpdb hilo principal db

logm=Logger('mercado.log')                       #log para para mercado 
logm.set_log_level(e.log_level)
mercado = Mercado(logm,e,client)                 #objeto encargado de la obtención de datos desde el exchange

print(mercado.precio('BTCUSDT','1d'))            #fuerzo la carga BTCUSDT en un día  necesaria para algunas operaciones que consultan todos los pares


try:
    cuenta_de_reinicios= int(sys.argv[1])        #cuenta de reinicios pasado como parámetros
    inicio_funcionamiento = datetime.strptime(sys.argv[2], '%Y-%m-%d %H:%M:%S.%f')     #fecha para cacular cuanto tiempo lleva funcionando pasad como parametro
except:    
    cuenta_de_reinicios=0
    inicio_funcionamiento = datetime.now()   

_thread.start_new_thread( habilitar_deshabilitar_pares_periodicamente, (e,conn,mercado) )       # habilitador de pares

materializar_pares_desde_db(True,log,hpdb,e,mercado,client)     #materializacion inicial de pares

ti_mail = Controlador_De_Tiempo(e.tiempo_envio_reporte_correo)           #para enviar mails periódicamente
reporte_correo(log,hpdb,e,mercado,inicio_funcionamiento,cuenta_de_reinicios)                       #mail al inicio, situación de arranque    

while e.trabajando:                              #bucle princpipal 
    try:
        mostrar_informacion(e,log)

        if ti_mail.tiempo_cumplido():
            reporte_correo(log,hpdb,e,mercado,inicio_funcionamiento,cuenta_de_reinicios) 
            #ti_mail.intervalo += 60 #voy subiendo para darle cada vez menos bola

        materializar_pares_desde_db(False,log,hpdb,e,mercado,client)
        controlar_estado0(e,log)
        
        log.log( reporte_de_ciclo(e,mercado,inicio_funcionamiento,cuenta_de_reinicios) )

        time.sleep(49)
        esperar_correcto_funcionamiento(client,e,log)
    
        log.log('cargar_parametros_de_config_json')
        e.cargar_parametros_de_config_json()

    except Exception as ex:
        log.log('Error', str(ex))   

    
log.log("Cerrando todo...")
esperar_a_que_todos_mueran(e,log)
log.log('FIN - FIN - Me morí.')

os._exit(1)

## ----------FIN--------------##
    
