# FastAPI Intermedio - Nova
## Indice
- Descripción
- Instalación
- Uso
- Contribución

## Descripción
Este proyecto consiste en una API desarrollada con FastAPI y Python, que implementa todas las operaciones CRUD: GET, POST, PUT y DELETE. Utiliza la biblioteca JWT para validar tokens a través de un registro de“admin”.

La API está sincronizada con SQLite, un sistema de gestión de bases de datos relacional (RDBMS) que permite almacenar y recuperar datos estructurados en archivos. Además, se integra con SQLAlchemy, una biblioteca que proporciona un mapeador relacional de objetos (ORM). SQLAlchemy se encarga de mapear las bases de datos, como las tablas, a objetos Python, facilitando su manipulación.

En resumen, este proyecto aprovecha la complementariedad entre SQLite y SQLAlchemy para proporcionar una API robusta y segura.

## Instalación
Aquí te dejo los pasos para instalar y utilizar este proyecto:

1. Realiza un Fork del repositorio.
2. Clona el repositorio en tu máquina local utilizando el comando: git clone https://github.com/PikeBlessed/FastAPI-Nova.git
3. Te recomiendo estar en un ambiente virtual.
4. Instala las dependencias listadas en el archivo requirements.txt ejecutando el siguiente comando en tu terminal: pip install -r requirements.txt
5. ¡Listo! Ahora puedes utilizar el proyecto como desees ;)

Por favor, asegúrate de estar en el directorio correcto cuando ejecutes estos comandos en tu terminal. ¡Disfruta del proyecto!

## Uso
Para poder usar correctamente la API debes hacer lo siguiente:
1. Completa todo el proceso de instalación indicado en la sección anterior.
2. Ejecuta el siguiente comando para que la API empiece a funcionar: `uvicorn main:app --reload --host 0.0.0.0`
3. Ahora puedes dirigirte a la siguiente URL: http://localhost:8000/docs para empezar a utilizar las funciones de la API.
4. Una vez hiciste las modificaciones pertinentes, te diriges al archivo donde esta la base de datos `database.sqlite`, para ver todas tus acciones reflejadas en la misma.

## Contribución
En caso de que quieras contribuir, haciendo alguna modificacion al proyecto realiza lo siguiente:
1. (Voy a suponer que ya hiciste una correcta instalacion).
2. Crea una rama a parte para que puedas hacer modificaciones sin dañar el archivo main: `git branch nombre_de_la_rama` (recomendacion)
3. Una vez que hayas realizado todos los cambios haz un: `git commit -am "Mensaje"`
4. Envía los cambios realizados a tu repositorio clon del mio: `git push origin main`
5. Realiza un pull request. Si no sabes cómo hacerlo puedes buscar algún tutorial en YouTube.
6. Ahora solo queda esperar para ver si tus cambios son beneficiosos para el proyecto :)
