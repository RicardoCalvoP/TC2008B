# MA. Actividad: Roomba
**Nombre:** Ricardo Alfredo Calvo Pérez
**Matrícula:** A01028889
**Fecha:** 10/11/2024

---


En este programa buscamos crear un modelo en donde podemos ver la funcionalidad de los robots Roomba
en un tablero de $25\times25$. Como objetivo las Roombas tienen que limpiar todas las casillas sucias del tablero en la menor cantidad de pasos posibles.

## Características de los Agentes

### Agente Roomba

Tenemos a nuestro agente principal a nuestras Roombas, las cuales en nuestra simulación podemos controlar la cantidad de agentes que vamos a tener en el tablero, como valor predeterminado tenemos un solo agente, sin embargo podemos cambiar esta cantidad hasta un máximo de 10 Roombas. Estas tienen la autonomía de moverse a las casillas de tipo piso, tienen una prioridad de moverse a los suelos sucios, suelos desconocidos, suelos vistos y por útlimo suelos visitados, también dependeran de la batería restante, pues si se estos tienen batería baja buscarán llegar a su estación de carga con el camino más corto. Interactuan con los suelos cambiandolos de estados entre Sucio, Limpio y visitado. Están en constante ejecución, moviéndose y reduciendo su energía en cada paso, aparte de que se recarga la batería al estar en su estación de carga.

#### **Atributos Principales**
1. **`steps_taken`**: Registra la cantidad de pasos que ha dado el agente.
2. **`floors_cleaned`**: Cuenta cuántos pisos ha limpiado.
3. **`battery`**: Representa el nivel de energía restante del agente.
4. **`to_visit_steps`**: Lista dinámica que almacena casillas conocidas pero no visitadas.
5. **`visited_cells`**: Contiene un registro de las casillas que el agente ha visitado.
6. **`condition`**: Define si el agente está en estado `Cleaning` o `Charging`.

#### **Comportamiento**
- **Prioridad de Movimiento**:
  1. Moverse a casillas sucias (`Dirty`).
  2. Explorar nuevas casillas (`Unvisited`).
  3. Revisitar casillas conocidas pero no exploradas (`Visited`).
- **Regreso a la Estación de Carga**:
  - Utiliza un algoritmo de búsqueda (BFS) para encontrar el camino más corto hacia la estación de carga, optimizando el consumo de batería.
- **Interacción con el Suelo**:
  - Cambia el estado del piso en el que se encuentra a `Clean`.
  - Registra los pisos como `Visited` al moverse sobre ellos.
- **Recarga de Batería**:
  - Al llegar a la estación de carga, el nivel de batería aumenta  por cada paso que permanece en ella.

---

### Agente Suelo

#### **Descripción**
El agente suelo representa cada celda del grid en la simulación. Este agente actúa de manera pasiva, permitiendo que las Roombas interactúen con él para cambiar su estado. Podemos considerar a este agente como parte del ambiente.

#### **Atributos Principales**
1. **`condition`**:
   - `Dirty`: Piso que requiere limpieza.
   - `Clean`: Piso que ya fue limpiado.
   - `Visited`: Piso conocido por los agentes, pero que no requería limpieza.
   - `Unvisited`: Piso que no ha sido explorado.

#### **Comportamiento**
- Los agentes suelo no realizan acciones propias, pero cambian de estado según las interacciones con las Roombas.

---

### Agente Obstaculo

#### **Descripción**
El agente obstáculo es estático y solo sirve para limitar los movimientos de las Roombas en el grid. Entonces al igual que nuestro agente anterior podemos considerarlo como parte de nuestro ambiente


#### **Comportamiento**
- Limita el movimiento de nuestro agente Roomba a las casillas ocupadas por este agente.

---

### **4. ChargingStationAgent**

#### **Descripción**
Este agente representa las estaciones de carga. Interactúa con las Roombas cuando necesitan recargar su batería, aumentandoles en 5 la batería. Tiene un estado de libre cuando no esta cargando ningun Roomba, perimitiendo el acceso a ella, posteriormente cambia a ocupada cuando este ya está cargando algún agente, limitando el acceso.

#### **Atributos**
1. **`condition`**:
   - `Free`: La estación de carga está disponible.
   - `Busy`: La estación está siendo utilizada por una Roomba.

#### **Comportamiento**
- Incrementa la batería de las Roombas en 5 unidades por cada paso que permanecen en la estación.
- Permite el movimiento de las Roombas a través de su casilla, pero no cambia de estado.

---

## Resultados

La simulación mostró un resultado esperados de los agentes Roomba en la limpieza del tablero. Durante el inicio, la mayoría de las casillas del grid se encontraban en estado "Dirty", representadas visualmente una imagen representativa y medida que los agentes se movían por el tablero podemos ver como nuestros suelos cambiaban a un estado de "Limpio", mostrando de manera clara  el progreso de la limpieza. La priorización implementada en los Roombas, que daba preferencia a los pisos sucios, permitió una limpieza del tablero incluso con pocos agentes, fueron raras las ocaciones en dodne se nos agotaba el tiempo antes de que los agentes terminarán de limpiar, sin embargo esto solo pasaba cuando teniamos solamente 1 o 2 Roombas activas.

En términos de la gestión de batería, las Roombas siempre lograron regresar exitosamente a la estación de carga antes de quedarse sin energía. Con el algoritmo del BFS pudimos evitar que nuestras Roombas se quedarán sin batería a medio camino. Una vez en la estación, las Roombas permanecían en ella hasta recargar completamente su batería, lo que garantizaba que los agentes pudieran volver a su trabajo.

Las estadísticas recolectadas a través de los gráficos de barras y de pastel aportaron información valiosa sobre el desempeño del sistema. Los gráficos de barras mostraron la cantidad de pasos dados por cada Roomba, así como los pisos limpiados por cada uno. Esto permitió observar cómo diferentes agentes contribuían de manera independiente al progreso general. Por otro lado, el gráfico de pastel reflejó los estados actuales del tablero, mostrando en tiempo real la proporción de pisos en condiciones "Dirty", "Clean", "Visited" y "Unvisited". Estas visualizaciones facilitaron el análisis y la interpretación del avance de la simulación.

Cuando se aumentó el número de Roombas en el tablero, se observó una mejora significativa en la velocidad de limpieza, aunque también surgieron ciertos desafíos, como la competencia por las estaciones de carga. Sin embargo, incluso con múltiples agentes, el modelo logró mantener un flujo continuo de limpieza sin interrupciones importantes. Finalmente, al completar la limpieza de todas las casillas sucias, se termina la simulación y confirmando que los objetivos habían sido alcanzados.

En general, la simulación cumplió con los resultados esperados. Los agentes Roomba tuvieron la capacidad  para limpiar el tablero y gestionarse de forma autónoma en un entorno dinámico y delimitado. Desde el inicio, las casillas sucias fueron limpiadas progresivamente según la lógica de priorización implementada, mientras los agentes se desplazaban por el tablero. Esto permitió una visualización clara del progreso de la limpieza a través del cambio de colores en las casillas, indicando su transición de "Dirty" a "Clean".
