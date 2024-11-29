# LAB 3 AWS - EC2

## Pasos del laboratorio

1. **Vamos al servicio EC2.**
2. **Creamos una instancia (create instance)**
    - **Name:** Damos nombre "letra+apellido_ECR".
    - **Aplication and OS Image:** Aqui basicamente seleccionamos el SO que queremos:
        - QuickStart: **Amazon Linux 2**.
    - **Instance Type**: Aqui modificamos los aspectos de "hardware" que queramos para nuestra maquina, VCP, RAM, Network, .... 
        - Elegimos **t3.micro**.
    - **Key-pair login**: Al principio crea una llave privada, una unica vez y nos la da.
    (Si le damos a "create key" crearemos la que para poderla descargar y asi autenticarnos en otras maquinas).
    - **Network Settings:** Aqui podemos modificar y crear, todo lo realacionado con la red, grupos, permisos, etc
        - Create security group: Activar esto.
        - Description: sg_grupoX-ec2
    - **Configure Storage:** Podemos modificar el tamaño de nuestro volumen.
    - **Advanced Details:** Aqui podemos modificar otros aspectos mas profundos.
        - ....
        - User data: Esto es un script de inicio de maquina (podemos indicarle, que es lo que tiene que hacer al iniciar (solo al iniciar la máquina por primera vez)).
        Dentro hay que meter esto:

            ```bash
            #!/bin/bash
            yum update -y
            yum install httpd -y
            service httpd start
            chkconfig httpd on
            cd /var/www/html
            echo "<html><h1>AOS page GROUP X </h1></html>"  >  index.html
            ```

        - **Launch**
3. **Entrar en modo SSH:** Este es el modo por defecto activado para poder acceder por terminal a la máquina.
    - Vamos la parte superior derecha:
        Pulsamos en **Action > Conect**
        - Dentro pulsamos la opción **Connect**.
4. **Modificar seguridad de la instancia:** Aqu podemos modificar la seguridad como protocolos de acceso a la maquina, etc.
    - Vamos a la parte inferior (justo debajo de la instancia) y seleccionamos **Security**.
        - Reglas de entrada:
            - Encontraremos ssh activado.
            - Seleccionamos http y lo habilitamos.
    - En la misma parte inferior, seleccionamos **Details**.
        - Buscamos la ip para conectarnos a la web mendiante http.
        - Importante que cuadno se habra la página cambiemos https por http, sino no funcionará.
