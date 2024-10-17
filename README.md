<h1 align="center">Proyecto de Programación</h1>

<h2 align="center">  Nonograma </h2>

### Descripción

Este proyecto es un juego de **Nonograma** implementado en Python utilizando la librería **Pygame**. Un Nonograma es un rompecabezas de lógica en el que debes rellenar celdas en una cuadrícula basándote en las pistas numéricas proporcionadas para cada fila y columna. El objetivo es revelar una imagen oculta siguiendo estas pistas.

### Estructura del proyecto

El proyecto está organizado en los siguientes archivos:

- **`main.py`**: Punto de entrada del programa. Inicia el juego.
- **`nonogram_game.py`**: Contiene la clase `NonogramGame`, que maneja el flujo principal del juego.
- **`grid.py`**: Define la clase `Grid`, responsable de manejar la cuadrícula del juego, dibujarla y gestionar las interacciones del usuario.
- **`menu.py`**: Contiene las funciones para mostrar el menú principal y obtener el tamaño del tablero del usuario.
- **`utils.py`**: Incluye funciones auxiliares para generar las pistas y verificar si el jugador ha ganado.
- **`constants.py`**: Define constantes globales como colores, tamaños y fuentes.
- **`tests/`**: Carpeta que contiene las pruebas unitarias del proyecto.
    - `test_utils.py`: Pruebas para las funciones en `utils.py`.
    - `test_grid.py`: Pruebas para la clase `Grid`.
    - `test_nonogram_game.py`: Pruebas para la clase `NonogramGame`.

### Cómo jugar

1. **Menú principal**:

   Al iniciar el juego, aparecerá el menú principal con las siguientes opciones:

    - **1. Tablero de tamaño aleatorio**: Inicia una partida con un tablero de tamaño aleatorio.
    - **2. Elegir tamaño del tablero**: Permite al usuario ingresar el tamaño del tablero en formato `filasxcolumnas`.
    - **3. Cerrar Nonograma**: Cierra el juego.

2. **Interacción con el tablero**:

    - **Clic izquierdo**: Alterna entre los estados "pintado", "tachado" y "vacío" en ese orden.
    - **Clic derecho**: Alterna entre los estados "tachado", "pintado" y "vacío" en ese orden.

3. **Objetivo del juego**:

    - Completa el tablero de acuerdo con las pistas numéricas proporcionadas para cada fila y columna.
    - Las pistas indican el número de celdas pintadas consecutivas en esa fila o columna.
    - Al completar el tablero correctamente, aparecerá un mensaje de "¡Ganaste!" y regresarás al menú principal.

### Estructura de archivos y directorios

```
nonogram-python/
├── constants.py
├── grid.py
├── main.py
├── menu.py
├── nonogram_game.py
├── utils.py
├── requirements.txt
└── tests/
    ├── test_utils.py
    ├── test_grid.py
    └── test_nonogram_game.py
```

### Personalización

Puedes modificar las constantes en `constants.py` para cambiar aspectos visuales del juego, como colores y tamaños de fuente.

---


Fotos:

![image](https://github.com/user-attachments/assets/5cd321c6-1d8e-45e4-b0be-3ba2ff937bc7)

![image](https://github.com/user-attachments/assets/acf908b5-872d-4e60-84ee-6cc363ab4614)

![image](https://github.com/user-attachments/assets/189683b6-90f0-4ce5-a850-cba8673ab113)


### Autores
<p align="left">
</p>

- **Rodrigo Bascuñán León**

- **Tomás Gutiérrez Bizama**

- **Martín Fuentealba Bizama**

- **Jorge Slimming Lagos**

- **Benjamin Henriquez Cid**

  
### Lenguaje y herramientas
<p align="left"> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> </p>
