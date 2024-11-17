# LAB 4 AWS - EC2 AutoEscaling y Balancer

## Objetivo del lab

Vamos a configurar una máquina con autoescalado y balanceador de carga.

- **Balanceador de carga:** Se encarga de organizar la requests entrates y irlas repartiendo por las diferentes máquinas, para no saturar el sistema.
- **Autoescalado:** Monitor automatico, que se encarga de crear/elimar los recursos para siempre tener la capacidad necesaria para el traajo que se esta realizando (para asegurar un buen servicio).
En caso de solo tener una máquina y esta cae, se cae el servicio, el autoescalado nos ayuda a evitarlo.

## Pasos del laboratorio

1. **Crear un template de instancia:** Lo necesita el autoescalado para poder crear nuevas instancias.
    - Vamos a EC2.
    - Crear plantilla de lanzamiento.
        - Nombre Plantilla.
        - Etiquetas de la plantilla:
            - Clave: Name.
            - Valor: NombreGrupo (no usar guión).
        - Imagen:
            - Imagen de inicio rapido: Ubuntu
        - Tipo de instancia: t2.nano
        - Configuración de red:
            - Crear grupo de seguridad:
                - Nombre: Nombre de tu grupo de seguridad (no usar guión).
                - VPC: por defecto.
                - Reglas:
                    - 1a regla: Tipo: SSH - Origen: Cualquier lugar.
                    - 2a regla: Tipo: HTTP - Origen: personalizada, 0.0.0.0.
        - Etiquetas de recursos:
            - Clave: Name.
            - Valor: NombreGrupo (no usar guión).
        - Detalles avanzados:
            - Datos de usuario: Ponemos el siguiente script:

                ```bash
                #!/bin/bash

                # Update package lists and install required packages
                sudo apt-get update -y
                sudo apt-get install apache2 unzip -y

                # Create the HTML file with basic structure
                echo '<html><center><body bgcolor="black" text="#39ff14" style="font-family: Arial"><h1>Load Balancer NOMBREGRUPO</h1>' > /var/www/html/index.html

                # Function to fetch metadata with error handling and token renewal
                fetch_metadata() {
                    token=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
                    if [ $? -ne 0 ]; then
                        echo "Failed to fetch token"
                        exit 1
                    fi

                    curl -H "X-aws-ec2-metadata-token: $token" -s http://169.254.169.254/latest/meta-data/$1
                }

                # Fetch and append availability zone
                availability_zone=$(fetch_metadata placement/availability-zone)
                echo "<h3>Availability Zone: $availability_zone</h3>" >> /var/www/html/index.html

                # Fetch and append instance ID
                instance_id=$(fetch_metadata instance-id)
                echo "<h3>Instance ID: $instance_id</h3>" >> /var/www/html/index.html

                # Fetch and append public IP
                public_ip=$(fetch_metadata public-ipv4)
                echo "<h3>Public IP: $public_ip</h3>" >> /var/www/html/index.html

                # Fetch and append local IP
                local_ip=$(fetch_metadata local-ipv4)
                echo "<h3>Local IP: $local_ip</h3>" >> /var/www/html/index.html

                echo '</html>' >> /var/www/html/index.html
                ```

        - Finalizamos dandole a: "Crear plantilla de lanzamiento"

2. **Configurar autoescalado:** Dispara un ALB y un Target (grupo de instancia).
    
    - EC2 > plantillas de lanzamiento.
    - Seleccionar tu plantilla y darle a "acción" > "plantilla de autoescaling".
        - Requisitos de tipo de instancia
            - Plantilla de lanzamiento: Asegurar-se que esta seleccionada la tuya.
        - Red.
            - VPC: La de tu región.
            - Zonas de disponibilidad y subredes: Seleccionar tantas AZ como queramos (usar las default).
            - Availavility Zone distribution: Balanced best effort.
        - Damos a "siguiente".
        - Opciones avanzadas.
            - Balance de carga: Asociar un nuevo balance de carga.
            - Asociar un nuevo balance de carga.
                - Tipo de balanceador: Application load balancer (HTTP, HTTPS).
                - Nombre del balanceador de carga: Nombre grupo ... (sin guión). 
                - Esquema del balance de carga: Internet-facing.
                - Agentes de escucha y direccionamiento:
                    - Crear grupo destino.
            - Etiqueta opcional.
                - Key: Name.
                - Clave: NombreGrupo.
            - Comprobacion de estado: Se deveria mirar en un entorno de producción, ahora no tocamos.
            - Configuración adicional: No hace falta tocarlo, de momento.
        - Damos "siguiente".
        - Nombre de la pagina
            - Tamaño del grupo:
                - Capacidad deseada: 2.
            - Escalado:
                - Capacidad minimo: 2.
                - Capacidad máximo: 2.
                - Escalamiento automarico: Politica de escalamiento de seguimiento de dominio.
            - Política de mantenimiento de instancias: Sin politica.
            - Damos a "siguiente".
        - Damos a "siguiente".
    - **Probar:**
        - Vamos a EC2 > Instancias.
        - Dentro de cada instancia, la activamos y en la parte infior derecha hacemos click en la dirección url. Cuando se abra, tenemos que modificar en la url el https por http.
3. **Balanceador de Carga:**: En caso de error y borrar instancias, el balanceador de carga se queda creado y se puede reutilizar.
    - EC2 > Balanceador de carga.
    - Entras en el que hay y abajo izquierda, seleccionamos la url del DNS. Veremos como el solo va cambiando entre instancias, siempre que accedamos a esta url.
    - Si se cae una instancia, el balanceador se encargara de crear una nueva y también de la redirección entre ellas.

4. **Hay que eliminar todo lo creado**