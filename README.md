# Reto Procesamiento de Datos

**Iñigo Murga, Mikel García y Jon Cañadas**

## Explicación

Este proyecto es un reto de procesamiento de datos desarrollado con FastAPI. Para la realización hemos seguido los siguientes pasos:

1. Desarrollo de los scripts de generadores eólicos

Para el desarrollo de este y los demás scripts hemos hecho uso del lenguaje python. Hemos decidido que la probabilidad de error será del 10%. Para generar los datos, hacemos uso de una funcionalidad crear datos donde en base a la probabilidad de error se generará un dato válido o erróneo. Para no tener que abrir 10 diferentes terminales tenemos un archivo "lanzar.bas" que ejecutara 10 veces el archivo "molino.py".

2. Desarrollo del script de concentrador

Para el desarrollo de este script, hicimos uso de FastAPI para generar unos métodos los cuales verifican la validez de los datos. Con los datos validados se realizan diferentes agregaciones.

3. Comprobar el funcionamiento 

A la hora poner en marcha el programa, hacemos uso de un entorno virtual para no tener que instalar todas las librerías en cada uno de los portátiles. Seguidamente, realizamos las comprobaciones pertinentes para asegurar el funcionamiento del programa. Destacar que los datos erróneos se irán registrando en el archivo "errores.log" de la carpeta log.

## Instalación

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/inigomurga/procesamiento-G2.git
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd procesamiento-G2
    ```

## Uso

1. Navega al directorio del entorno virtual:
    ```bash
    cd venv\Scripts
    ```
2. Activar el entorno virtual:
    ```bash
    activate
    ```
3. Entrar al concentrador y ejercutarlo:
    ```bash
    cd ..
    
    cd ..
    
    cd concentrador
    
    python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
4. Entrar a los generadores y ejercutarlo:
    ```bash
    
    cd ..
    
    cd generadores
    
    lanzar.bat
    ```

## Posibles vías de mejora

Para mejorar el reto hemos pensado en el desarrollo de una persistencia en el programa. Esto sería a través de una base de datos de Postgres. Lamentablemente, no hemos podido conseguir desarrollar esta mejora.

## Problemas / Retos encontrados

Al principio del reto, planteamos erróneamente los generadores inclumpliendo la parte de que los generadores deben ser programas individuales.

A su vez, a la hora de desarrollar la persistencia del programa nos han surgido diversos problemas que nos han impedido su implementación exitosamente.

## Alternativas posibles

Implementar la mejora de persistencia incluyendo una base de datos mongodb.

Implementar seguridad en las comunicaciones entre los generadores y el concentrador.

