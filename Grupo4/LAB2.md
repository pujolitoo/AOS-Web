# Fecha: 18-10

## PASOS QUE SE HARÁN EN LA PRÁCTICA

1. **Objetivos de la  práctica**
1.1 Crear una región remota (lugar muy muy lejos)
1.2 Crear fichero pesado (cuanto más grande el fichero mejor)
1.3 Habilitar la web

2. **Habilitar el Cloud Front de la web**
Apunte: la web con Cloud Front tiene una URL diferente a la de S3
2.1 Probar y experimentar
3. **Habilitar versionado**
4. **Habilitar reglas de ciclo de vida (life cycle)**
5. **Crear un Cloud 9**
5.1 Hacer un script python para borrar la web y sus fichero
6. **Borrar todo antes de irse**

---
## PASOS QUE HEMOS ESTADO HACIENDO EN LA PRÁCTICA

1. **Bucket S3**
1.1
Crear bucket de S3 en un sitio lejano
En nuestro caso, grupo4remoto2.aws.gimbernat.es en Osaka
1.2
Copiar el contenido (ficheros) del bucket de Marcela al nuesto
Quitar el bloqueo público del bucket (pestaña de permissions)
Añadir la política copiada de Marcela a nuestro bucket (pestaña de permissions)
Cambiar el nombre del recurso (poner el nuesto) de la política copiada
1.3
Habilitar la página web (en propierties, abajo de todo)

2. **Distribución Cloud Front**
2.1
Crear distribución en Cloud Front
Elegir el bucket remoto como dominio
Darle al botón emergente, dejar el protocolo por defecto
2.2: Explicaciones
¿Qué es el WAF? Web Application Firewall
Sirve para proteger a nivel de aplicación, por ejemplo los SQL Injection
2.3: Pruebas
Copiar y pegar el domain name en un nuevo tab del navegador
Puede tardar un rato en que se acabe de crear, ir recargando la página
2.4: Resultados de las pruebas
La primera vez que carga, la latencia es peor que con S3
La segunda vez (recargar la página), la carga es inmediata
Esto pasa porque la página se guarda en caché (a diferencia de S3)
2.5
Deshabilitar y borrar la distribución

3. **Entorno Cloud 9**
3.1
Crear entorno de Cloud 9 en la misma región de antes (Osaka)
Habilitar el control de versiones del bucket (pestaña de properties)
Abrir la consola de Cloud 9
3.2: Comandos de la consola
Crear carpeta: mkdir grupo4
Ir dentro de la carpeta creada: cd grupo4
Ver contenido bucket: aws s3 ls s3://grupo4remoto2.aws.gimbernat.es
Copiar a carpeta actual contenido bucket: aws s3 cp s3://grupo4remoto2.aws.gimbernat.es . --recursive 
3.3
Editar el index.html un poco
Subir los cambios con el comando: aws s3 cp index.htmp s3://grupo4remoto2.aws.gimbernat.es
Abrir el enlace de la web desde el bucket S3 para ver los cambios
3.4: Pruebas
Ver las versiones de los ficheros del bucket pulsando "show versions" (pestaña de objects)
Eliminar la última versión de index.html
3.5: Resultado de las pruebas
Si se borra el archivo de la versión actual, se pone directamente el de la anterior


4. **Reglas Life cicle**
4.1: Explicaciones
¿Qué es el life circle? Sirve para hacer acciones automaticas durante la vida de los ficheros
4.2: Tipos de almacenamiento
Nivel inteligente: para cuando no sabemos los patrones; Amazon lo hace segun lo que él considera
Única zona: para ficheros que no se pueden reproducir
Recuperación instantánea de Glacier: nueva versión de Glacier
...
4.3
Crear regla de ciclo de vida del bucket según lo que dice Marcela (pestaña de administración)
Resumidamente la regla hace: al pasar 30 dias, lo guarda en uso poco frecuente y a los 90 a Glacier
Podemos ver la regla creada en la pestaña de objects