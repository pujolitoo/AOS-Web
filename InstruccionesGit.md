# Colaboración con el proyecto AOSSAMPLE

## **1. Consideraciones previas:**

Esto es un repositorio público en el cual no tenemos permisos, por lo que no podemos trabajar directamente desde un clone de este, sino que previamente

tenemos que haber realizado un fork (bifurcación) que nos creará una copia del repo en nuestra cuenta de github, este si que lo podremos clonar en nuestro local.

## **2. Pasos**

1. Tener configurada la cuenta de github con VSCode.

2. Abir la carpeta de nuestro ordenador donde queramos trabajar.

3. Crear un fork del proyecto, para esto tenemos que irnos a Github.com y navegar hasta el repositorio "https://github.com/mcastrol/aossample"

- Hacemos click en la opción de "Fork"

![Screenshot 2024-12-12 at 12.21.51.png](imgInstrucciones/Screenshot_2024-12-12_at_12.21.51.png)

- Aceptamos.

![Screenshot 2024-12-12 at 12.22.12.png](imgInstrucciones/Screenshot_2024-12-12_at_12.22.12.png)

4. Clonar el fork que tienes en tu cuenta de github:

- Para encontrar el link, vas a "Code > HTTPS"

![Screenshot 2024-12-12 at 12.22.38.png](imgInstrucciones/Screenshot_2024-12-12_at_12.22.38.png)

- Escribes dentro de la terminal de VSCode: git clone "linkFork"

![Screenshot 2024-12-12 at 12.24.51.png](imgInstrucciones/Screenshot_2024-12-12_at_12.24.51.png)

5. Cambiamos de directorio al del repo: cd aossample

![image.png](imgInstrucciones/image.png)

6. Creamos una rama para nuestro grupo: git branch "GrupoX"

![Screenshot 2024-12-12 at 13.05.55.png](imgInstrucciones/Screenshot_2024-12-12_at_13.05.55.png)

7. Nos movemos a la rama: git checkout "GrupoX"

![Screenshot 2024-12-12 at 12.28.58.png](imgInstrucciones/Screenshot_2024-12-12_at_12.28.58.png)

8. Creamos una carpeta y metemos dentro los archivos de los labs.

- Lo puedes hacer de manera visual, no hace falta usar la terminal.

![Screenshot 2024-12-12 at 12.30.49.png](imgInstrucciones/Screenshot_2024-12-12_at_12.30.49.png)

9. Añadir los cambios a la area de Staging: git add .

10. Confirmar los cambios: git commit -m "Mensaje descriptivo".

- En el mensaje tenéis que describir los cambios que estáis haciendo.

![image.png](imgInstrucciones/image%201.png)

11. Subimos los cambios a la rama: git push origin "nombreRama".

![Screenshot 2024-12-12 at 12.37.00.png](imgInstrucciones/Screenshot_2024-12-12_at_12.37.00.png)

12. Ahora ya tenemos los cambios en la rama de nuestro Grupo dentro del Fork (no están en la main del Fork).

- Para ir directamente a este repo, en la terminal con el resultado de el comando anterior, aparecerá un link.

**Ahora desde la web de [Github.com](http://Github.com), nos lo habrá abierto con el link anterior.**

13. Creamos una pull request para subirlo al repo original "mcastrol/aossample".

- En el mensaje que aparece, seleccionamos "Compare & pull request".

![Screenshot 2024-12-12 at 12.42.05.png](imgInstrucciones/Screenshot_2024-12-12_at_12.42.05.png)

- Como queremos hacer la pull al original, es importante que arriba este seleccionado:

- base repository: mcastrol/aossample.

- base main:

- head repository: usuario/aossample.

- compare: GrupoX (nombreRama).

- El mensaje será el indicado en el commit, podemos darle una descripción tmb.

- Le damos a "Create pull request"

![Screenshot 2024-12-12 at 12.44.29.png](imgInstrucciones/Screenshot_2024-12-12_at_12.44.29.png)

- Y ya estaría creada la pull request, en el caso de querer añadir comentarios, podemos hacerlo ahi.

14. Recordando que esto es un repo en el que no tenemos permisos, tenemos que esperar a que el autor acepte la pull request.

- Podemos ver la pull request tanto desde nuestro repo, como con el original (el de marcela), mirando dentro del apartado “pull requests”.

![Screenshot 2024-12-12 at 12.46.42.png](imgInstrucciones/Screenshot_2024-12-12_at_12.46.42.png)