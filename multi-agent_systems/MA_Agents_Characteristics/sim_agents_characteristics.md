# MA. Características de simulación de agentes
**Nombre:** Ricardo Alfredo Calvo Pérez
**Matrícula:** A01028889
**Fecha:** 31/10/2024

---

## Wolf Sheep

Esta simulación modela un ecosistema simple con tres tipos de agentes: pasto, ovejas y lobos, los cuales interactúan dentro de un ambiente de cuadrícula discreto de 20x20. Los agentes actúan de acuerdo con comportamientos específicos:

- **Pasto**: Solo crece o es comido por las ovejas.
- **Ovejas**: Comen pasto, pueden reproducirse y mueren de hambre si no encuentran alimento.
- **Lobos**: Se alimentan de ovejas, pueden reproducirse y mueren de hambre si no comen a tiempo.

El movimiento de los animales es aleatorio, por lo que los encuentros entre depredadores y presas dependen del azar y no de una búsqueda activa de comida.

---

## Características del Ambiente

1. El ambiente es parcialmente accesible. Los agentes carecen de información completa sobre su entorno y dependen del azar para encontrar comida, aparte de que únicamente conocen lo que hay dentro de la casilla actual y en sus alrededores más cercanos.

2. Es no determinista, ya que los resultados (encontrar o no comida, o ser comido) no son garantizados y dependen de la casualidad. Debido a su movimiento aleatorio, no se puede garantizar que encontrarán comida en cada movimiento.

3. Considero que este ambiente es no episódico, pues las decisiones actuales de los agentes afectan su situación futura, acumulando efectos como el hambre o la reproducción.

4. Es dinámico, ya que la población y posición de los agentes cambian continuamente. El pasto crece, y las ovejas y lobos se reproducen, dando un cambio constante en el ambiente.

5. Es discreto, ya que las posiciones de los agentes están restringidas a una cuadrícula finita, y estos tienen un número de acciones limitado (moverse, comer, reproducirse).

---

## Características de los Agentes

1. **Pasto**:
   - **Autonomía**: No tiene autonomía, solo crece y puede ser comido por las ovejas.
   - **Sensibilidad**: No interactúa con humanos ni con otros agentes.
   - **Reactividad**: Reacciona al ser comido por las ovejas, lo cual detiene su crecimiento temporalmente y cambia su estado a "comido".
   - **Proactividad**: No tiene proactividad, ya que no toma acciones para cumplir un objetivo (si es que tiene alguno).
   - **Continuidad**: Ejecuta un proceso cíclico de crecimiento cuando no ha sido comido.
   - **Benevolencia**: No tiene capacidad de satisfacer solicitudes de otros agentes.
   - **Racionalidad**: No actúa para satisfacer objetivos propios.
   - **Colaboración**: No interactúa ni colabora con otros agentes.

2. **Ovejas**:
   - **Autonomía**: Poseen autonomía limitada, pueden moverse, sin embargo, no pueden decidir a dónde moverse. También pueden alimentarse y reproducirse.
   - **Sensibilidad**: Interactúan con el pasto al consumirlo y pueden ser presas de los lobos.
   - **Reactividad**: Reaccionan al hambre moviéndose aleatoriamente y consumiendo pasto si lo encuentran.
   - **Proactividad**: No muestran proactividad, ya que no buscan activamente el pasto, su movimiento es aleatorio.
   - **Continuidad**: Están en constante ejecución, moviéndose y reduciendo su energía en cada paso y, en caso de encontrar pasto, consumiéndolo.
   - **Benevolencia**: No tienen la capacidad de satisfacer solicitudes de otros agentes.
   - **Racionalidad**: Actúan para maximizar su supervivencia, alimentándose y reproduciéndose. Sin embargo, todo dependerá de su suerte.
   - **Colaboración**: No colaboran ni interactúan de forma significativa con otros agentes.

3. **Lobos**:
   - **Autonomía**: Tienen autonomía para moverse, alimentarse de ovejas y reproducirse, pero al igual que las ovejas, no tienen control de hacia dónde se mueven.
   - **Sensibilidad**: Interactúan con las ovejas al cazarlas y consumirlas como alimento.
   - **Reactividad**: Responden al hambre moviéndose y cazando ovejas si encuentran alguna en la misma casilla.
   - **Proactividad**: Similar a las ovejas, no muestran proactividad en la búsqueda de comida, su movimiento es aleatorio.
   - **Continuidad**: Constantemente ejecutan acciones como moverse, buscar comida y reproducirse, y en caso de encontrar una oveja, comerla.
   - **Benevolencia**: No tienen capacidad para satisfacer las solicitudes de otros agentes.
   - **Racionalidad**: Actúan para cumplir su objetivo de sobrevivir y reproducirse mediante la caza de ovejas, sin embargo, al igual que las ovejas, dependen de la suerte.
   - **Colaboración**: No interactúan ni colaboran con otros agentes para lograr objetivos comunes.

---

## PEAS de la Simulación

### Ovejas
- **Performance**: Mantenerse vivas, reproducirse comiendo pasto, o por el contrario, ser comida al encontrarse con un lobo y moverse de manera aleatoria.
- **Environment**: Entorno bidimensional con dimensiones proporcionadas.
- **Actuators**: Movimiento aleatorio dentro de la cuadrícula.
- **Sensors**: Perciben si están en una celda con pasto disponible.

### Lobos
- **Performance**: Sobrevivir y reproducirse comiendo ovejas y moverse de manera aleatoria, o por el contrario, morir de hambre al no encontrar alimento.
- **Environment**: Entorno bidimensional con dimensiones proporcionadas.
- **Actuators**: Movimiento aleatorio en la cuadrícula.
- **Sensors**: Detectan si están en una celda con ovejas.

### Pasto
- **Performance**: Crecer y ser consumido por las ovejas.
- **Environment**: Entorno bidimensional con dimensiones proporcionadas.
- **Actuators**: No tiene, no se mueve ni toma decisiones.
- **Sensors**: No requiere percepción del entorno.

---

## Ants

Esta simulación modela un ecosistema en el cual una colonia de hormigas busca alimentos dentro de una cuadrícula de 50x50. Las hormigas tienen los siguientes comportamientos:

- **Busqueda de comida**: Las hormigas se mueven de manera aleatoria en búsqueda de comida, representada en áreas verdes dentro de la cuadrícula.
- **Retorno**: Cuando una hormiga encuentra comida, cambia a un estado de retorno y busca el camino más corto hacia la madriguera, dejando un rastro de lo que parece ser feromonas (de color rojo) que otras hormigas pueden seguir.

---

## Características del Ambiente

1. El ambiente es parcialmente accesible, pues las hormigas no tienen una vista completa del entorno, y solo detectan feromonas en sus celdas vecinas y aparentemente un poco más para guiar su camino.

2. Es un ambiente no determinista, ya que el movimiento de las hormigas en estado de búsqueda es aleatorio. No se garantiza que encuentren comida o que todas sigan los rastros de feromonas hacia la madriguera.

3. Es no episódico, ya que las decisiones de las hormigas dependen de acciones previas y de las feromonas dejadas por otras hormigas. Los rastros de feromonas persisten en el ambiente, afectando el comportamiento futuro de la colonia.

4. El ambiente es dinámico debido al movimiento continuo de las hormigas y a la dispersión y evaporación de las feromonas, que afectan el comportamiento de las hormigas a lo largo del tiempo, aparte de que si se acaba la comida en una zona, este va a desaparecer.

5. Es un ambiente discreto, ya que la cuadrícula tiene posiciones definidas y las hormigas se mueven entre celdas limitadas.

---

## Características de los Agentes

1. **Hormigas**:
   - **Autonomía**: Tienen autonomía para moverse (aleatoreamente) y decidir el cambio entre los estados de búsqueda y retorno dependiendo de sus condiciones.
   - **Sensibilidad**: Interactúan con el ambiente detectando comida y rastros de feromonas dejados por otras hormigas o por lo contrario dejar las feromonas.
   - **Reactividad**: Responden a la presencia de comida cambiando su estado y a las feromonas en el camino de regreso.
   - **Proactividad**: No muestran proactividad en la búsqueda de comida, su movimiento inicial es aleatorio, sin embargo cuando este va de regreso a el hogar su comportamiento cambia a regresar de una forma directa dejando feromonas.
   - **Continuidad**: Las hormigas están en constante movimiento buscando comida o regresando a la madriguera.
   - **Benevolencia**: Contribuyen a la colonia al llevar comida a la madriguera y al dejar feromonas que ayudan a otras hormigas a encontrar la comida.
   - **Racionalidad**: Actúan de manera que maximizan la recolección de comida para la colonia.
   - **Colaboración**: Indirectamente colaboran al dejar rastros de feromonas, guiando a otras hormigas en el retorno al nido.

2. **Comida**:
   - **Autonomía**: No tiene autonomía, es simplemente un recurso para las hormigas.
   - **Sensibilidad**: No interactúa activamente con las hormigas ni con el ambiente, hasta que se acaba y desaparece.
   - **Reactividad**: Se "consume" cuando una hormiga la encuentra.
   - **Proactividad**: No posee proactividad ni capacidad para tomar acciones.
   - **Continuidad**: No se actualiza ni realiza acciones de manera continua.
   - **Benevolencia**: Proporciona un recurso a la colonia de hormigas.
   - **Racionalidad**: No actúa para satisfacer objetivos propios.
   - **Colaboración**: No tiene interacción activa ni colaboración con otros agentes.

3. **Feromonas (parte del Ambiente)**:
   - **Autonomía**: No tiene autonomía, las feromonas son producidas y manipuladas por las hormigas.
   - **Sensibilidad**: No interactúan activamente con otros agentes.
   - **Reactividad**: Se dispersan y evaporan con el tiempo, afectando su intensidad en el ambiente.
   - **Proactividad**: No tienen proactividad, solo existen y se disipan en el ambiente.
   - **Continuidad**: Cambian de manera continua al dispersarse y evaporarse.
   - **Benevolencia**: Facilitan la orientación de las hormigas hacia el nido.
   - **Racionalidad**: No tienen objetivos propios.
   - **Colaboración**: Ayudan indirectamente a las hormigas proporcionando orientación en su retorno al hogar.

---

## PEAS de la Simulación

### Hormigas
- **Performance**: Encontrar comida, transportarla al nido y dejar feromonas
- **Environment**: Cuadrícula de 50x50, con áreas de comida y una madriguera en el centro.
- **Actuators**: Movimiento aleatorio al buscar comida, movimiento guiado hacia el nido siguiendo rastros de feromonas.
- **Sensors**: Perciben comida y rastros de feromonas en las celdas vecinas.

### Comida
- **Performance**: Ser consumida por las hormigas.
- **Environment**: Cuadrícula de 50x50 en celdas específicas donde está disponible.
- **Actuators**: No tiene actuadores.
- **Sensors**: No requiere percepción del entorno.

### Feromonas
- **Performance**: Proporcionar orientación a las hormigas en su camino de regreso al nido.
- **Environment**: Cuadrícula de 50x50, distribuidas y disipadas a lo largo del tiempo.
- **Actuators**: Guiar a las hormigas al hogar.
- **Sensors**: No requiere percepción activa, solo afectan a las hormigas que las detectan.
