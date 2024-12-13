# LAB 5 AWS - Amazon Aurora

## Objetivo del lab

Vamos a configurar una instancia de bases de datos con Aurora:
    - Tendremos un clúster con variaas instacias de Aurora (original y réplica).
    - Probaremos los diferentes endpoints de Aurora.
    - Simularemos un failover, para ver como reacciona.

## Conceptos Aurora

- Un cluster puede contener varias instancias de aurora y cada una de estas instancias tiene varias BDs.
- Para cada cluster aurora nos dará dos endpoints, eso es lo bueno de Aurora, cuando tenemos una unica instancias es tonteria, pero cuando más adelante hagamos más de una instancia, esto cobra mucho sentido, ya que se desacoplan las dos funciones:
    - Uno para escribir: aurora-grupoX.cluster-.......
    - Otro para leer: aurora-grupoX.cluster-**ro**-....
- Cuando creemos la réplica, el cluster contendrá varias instancias de Aurora.
- En caso de failover de una de las instancias los dos endoints irán a la misma instancia.

## Pasos del laboratorio

1. **Vamos a RDS** y dentro de aqui a "Crear base de datos".
    - Elegir un método de creacion: Creación estandar
    - Opciones de motor: Aurora (PostreSQL Compatible)
    - Plantillas: Desarrollo y rpruebas.
    - Configuración:
        - Identificador del clúster de base de datos: aurora-grupoX
    - Credenciales:
        - Nombre de usuario maestro: postres
        - Contraseña maestra: La que queramos
    - Configuración de la instancia:
        - Clases con rafagas: db.t3.medium (estamos poniendo la más simple).
    - Conectividad:
        - Grupos de seguridad (VPC): Si ya esta creado elegir existente y sino crear uno nuevo.
    - Supervision:
        - Monitorización mejorada: DESACTIVAR.
    - Crear base de datos.
2. **Conseguir endpoints:** Si vamos dentro de nuestra instancia, dentro del apartado "Relacionado" podremos ver los endpoints, cada uno para su propia función.
3. **Creación réplica:** "Vamos dentro de nuestra BD" y ahi nos vamos a "Acciones > Crear nuevo lector".
    - Configuración:
        - Origen de réplica: aurora-grupoX-instance-1
        - Identificador de isntancias: aurora-grupoX-instancia-replica
    - Crear nuevo
4. **Simular failover:** Vamos dentro de la instancia "Acciones > Conmutació por error."