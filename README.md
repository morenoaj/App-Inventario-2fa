# App-Inventario-2fa
Desarrollo de app de gestión de usuarios e inventarios con Python, Flask para su uso en local, servidores o contenedores.


**GUÍA DE CONFIGURACIÓN PARA APLICACIÓN DE INVENTARIOS Y USUARIOS CON PYTHON, FLASK CON DOBLE AUTENTICACIÓN.**

# Contenido
[1. Introducción	1](#_toc150125309)

[2. Descripción del proyecto:	1](#_toc150125310)

[3. Configuración local	3](#_toc150125311)

[4. Imágenes base probadas	5](#_toc150125312)


# <a name="_toc150125309"></a>1. Introducción
Este manual explica cómo configurar y desplegar una aplicación de gestión de usuarios e inventarios desarrollada con Python y Flask. La aplicación permite administrar usuarios con diferentes roles (administrador y gestor de inventario) y llevar un control de inventarios asociados a cada usuario gestor.

La aplicación consta de dos componentes principales:

Una interfaz de usuario desarrollada con Flask que permite la gestión de usuarios e inventarios.

Un servicio de autenticación con doble factor que genera tokens temporales y envía códigos de verificación por correo electrónico.

El manual cubre la configuración de la aplicación para ejecutarse de forma local y su despliegue en contenedores utilizando Podman. Se incluyen instrucciones paso a paso para construir las imágenes de los contenedores, crear una red para su comunicación y ejecutarlos exponiendo los puertos correctos.

Al final se enumeran las imágenes base de Red Hat que se probaron durante el desarrollo, siendo la seleccionada Red Hat Universal Base Image 8."





# <a name="_toc150125310"></a>2. Descripción del proyecto:
**Desarrollo de app de gestión de usuarios e inventarios con Python, Flask para su uso en local, servidores o contenedores.**

**App**: La aplicación frontend está desarrollada con Python y Flask. Consta de los siguientes componentes:

- app.py: Archivo principal que contiene la lógica del frontend.
- db.py: Módulo que implementa las funciones para acceder y modificar los datos de usuarios e inventarios.
- users.json: Base de datos de los usuarios, con campos como id, username, email, password y role (admin o manager).
- inv.json: Base de datos de los inventarios, con campos como id, userid, name, stock y price. Cada inventario está asociado al usuario manager correspondiente.

La aplicación implementa un sistema de roles para separar el acceso administrativo (panel de administración) del acceso a la gestión de inventarios por parte de los usuarios manager.

Se utilizan sesiones de Flask para controlar el acceso a las diferentes áreas de la aplicación dependiendo del rol del usuario autenticado.

**Service**: El servicio de autenticación está desarrollado en Python y proporciona las siguientes funcionalidades:

- Login con doble factor:
  - Genera un token aleatorio de 6 caracteres alfanuméricos con 45 minutos de expiración.
  - Envía el token por correo electrónico al usuario.
  - Requiere que el usuario ingrese el token junto con su contraseña para completar el inicio de sesión.
  - Si el token expira, requiere volver a ingresar la contraseña.


![Aspose Words 5396a87f-ee68-46cf-999a-efd08824eae1 001](https://github.com/morenoaj/App-Inventario-2fa/assets/63484452/87e777c9-ad48-4cb3-a190-f1e246c3df8a)


- Registro de nuevos usuarios:
  - Verifica la información de registro.
  - En caso de éxito, envía un correo de confirmación de cuenta.

![Aspose Words 5396a87f-ee68-46cf-999a-efd08824eae1 002](https://github.com/morenoaj/App-Inventario-2fa/assets/63484452/dfef86e2-52e7-4881-b72f-deced1c5c61f)

El servicio expone endpoints REST para integrarse con el frontend desarrollado en Flask.

Se encarga de proveer una capa adicional de seguridad a la autenticación mediante la verificación en dos pasos y el uso de tokens temporales.

![Aspose Words 5396a87f-ee68-46cf-999a-efd08824eae1 003](https://github.com/morenoaj/App-Inventario-2fa/assets/63484452/07d24b1c-a305-43c2-b837-86edaa831b66)

**Uso**: La aplicación implementa un sistema de control de acceso basado en sesiones de Flask y roles de usuario (administrador y manager).

El panel de administración solo es accesible para usuarios con rol administrador. Permite gestionar usuarios.

El gestor de inventarios solo es accesible para usuarios con rol manager. Permite administrar los inventarios asociados a cada manager.

![Aspose Words 5396a87f-ee68-46cf-999a-efd08824eae1 004](https://github.com/morenoaj/App-Inventario-2fa/assets/63484452/c19b2e57-a191-4b7b-8d82-de80a9a7da9a)

Por defecto, se crea un usuario administrador con las siguientes credenciales:

- Username: admin
- Password: admin

Este usuario administrador permite realizar las tareas de configuración inicial, creación de usuarios managers y gestión del sistema.

**Para seguir este manual, debe tener instalado Podman Desktop en su sistema. Podman Desktop está disponible para Windows, Linux y macOS.**

# <a name="_toc150125311"></a>3. Configuración local 

Para ejecutar la aplicación localmente, siga estos pasos:

3\.1 App

\- Verifique que la variable de entorno service apunte a localhost.

\- Ejecute la app configurada para usar el puerto 4000.

3\.2 Service  

\- Verifique que la variable de entorno app apunte a localhost. 

\- Ejecute el service configurado para usar el puerto 5000.



# 4\. Configuración con Podman

Para desplegar la aplicación en contenedores Podman:

4\.1 Construir imágenes

\- Configure un Dockerfile para la app que exponga el puerto 4000.

\- Construya la imagen de la app: \*\***podman build -t app .**\*\*

\- Configure un Dockerfile para el service que exponga el puerto 5000.  

\- Construya la imagen del service: \*\***podman build -t service .**\*\*

4\.2 Crear red

\- Cree una red para comunicar los contenedores el nombre pronet se puede reemplazar, solo que debe tomar en cuenta reemplazarlo también al momento de ejecutar el contenedor: \*\***podman network create pronet**\*\*

4\.3 Ejecutar contenedores

\- Ejecute el contenedor de la app conectado a la red:

\*\***podman run --network=pronet --name=app -p 4000:4000 app**\*\*

\- Ejecute el contenedor del service conectado a la red:

\*\***podman run --network=pronet --name=service -p 5000:5000 service**\*\*


# <a name="_toc150125312"></a>5. Imágenes base probadas

Se probaron las siguientes imágenes base de Red Hat:

\- RHEL Minimal Base Image

\- Red Hat Universal Base Image 7  

\- Red Hat Universal Base Image 8 Micro

\- Red Hat Universal Base Image 8 (seleccionada) 

\- Red Hat Universal Base Image 9
