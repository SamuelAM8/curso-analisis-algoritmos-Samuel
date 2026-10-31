# Laboratorio 3 — Estructuras de datos: lista enlazada vs. tabla hash

**Autor:** Samuel Arango Montoya

**Caso:** Rutas del Caribe, consulta de guías de envío.

## Cómo reproducir

Se necesita Python 3.10 o superior, porque uso anotaciones como `Nodo | None`. El entorno virtual `venv` y el archivo `requirements.txt` (con `matplotlib`) están en la raíz del repositorio.

```powershell
# 1. Desde la raíz del repositorio, activar el entorno virtual
venv\Scripts\Activate.ps1

# 2. Instalar las dependencias
pip install -r requirements.txt

# 3. Entrar a la carpeta del laboratorio
cd laboratorios\lab3-estructuras-datos

# 4. Ejecutar las pruebas (debe imprimir "Todas las pruebas pasaron.")
python pruebas.py

# 5. Ejecutar la medición (imprime las tablas y regenera graficas/*.png)
python medicion.py
```

Todas las mediciones las hice en mi computador personal. La medición usa semillas fijas (`SEMILLA = 2026`), así que siempre genera las mismas guías. Los tiempos absolutos pueden salir distintos en otra máquina, pero la forma de las curvas debería coincidir.

---

## Parte 1 — Implementación y verificación

Código: [`estructuras.py`](estructuras.py) · Pruebas: [`pruebas.py`](pruebas.py)

`estructuras.py` tiene `Nodo`, `ListaEnlazada` (inserción al inicio en Θ(1) y búsqueda iterativa con `while`) y `TablaHash` (encadenamiento con `h(k) = k mod m`). Cada casilla de la tabla es una `ListaEnlazada`, y no uso `dict`, `set` ni la función `hash()` de Python.

En `pruebas.py` verifico con `assert` lo siguiente:

1. Búsqueda exitosa e infructuosa en la lista y en la tabla (la guía 24 existe y la 99 devuelve `None`).
2. Colisión forzada con m = 7: las guías 10, 24 y 17 caen en la casilla 3, la lista de esa casilla tiene longitud 3 y las tres se recuperan con su estado correcto.
3. Factor de carga: `factor_carga() == 3 / 7` y `tamano == 3` después de esas inserciones.
4. 25 colecciones aleatorias (semilla 42, de 1 a 500 guías, con m elegido entre 7, 101 y 1009). En cada una, ambas estructuras tienen el mismo tamaño, devuelven el estado correcto para todas las guías existentes y devuelven `None` para 10 guías inexistentes. Con m = 7 y 101 las cadenas quedan largas.

Además, `medicion.py` repite una verificación antes de cronometrar: con una muestra de 100 guías existentes comprueba que lista y tabla devuelven el mismo estado.

La prueba que me parece más importante es la de la colisión forzada, porque con m = 7 las tres guías terminan en la misma casilla y ahí se comprueba que el encadenamiento de verdad funciona.

---

## Parte 2 — Medición y gráficas

Código: [`medicion.py`](medicion.py)

**Cómo medí.**

- Las guías son enteros distintos de diez dígitos, generados con semilla fija, y uso las mismas para la lista y la tabla en cada valor de n. Los estados se reparten de forma rotativa entre "en bodega", "en reparto" y "entregado".
- Cronometro solo las búsquedas, con `time.perf_counter()`. La construcción de las estructuras y la generación de datos quedan fuera.
- Cada medición hace 200 búsquedas de guías inexistentes (con `generar_guias_inexistentes` y semilla fija). La repetí 5 veces y promedié, para que un pico aislado no distorsione el resultado. Reporto microsegundos por búsqueda.
- Experimento A: m es el primo más cercano (por encima) a n/2, para que α quede cerca de 2.
- Experimento B: n = 20.000 fijo, y m es el primo cercano a n/α para α meta ∈ {0,25; 0,5; 1; 2; 4; 10}.

### Experimento A — lista vs. tabla (búsquedas infructuosas)

![Tiempo de búsqueda infructuosa: lista vs tabla hash](graficas/lista_vs_tabla.png)

Lo primero que se nota es que la tabla parece casi una línea plana al lado de la lista, que sube de forma aproximadamente lineal, con un tramo intermedio (de n = 5.000 a n = 20.000) más empinado (se analiza en la pregunta 2).

| n | m | α | Lista (µs) | Tabla (µs) |
|---:|---:|---:|---:|---:|
| 100 | 53 | 1,89 | 4,202 | 0,228 |
| 500 | 251 | 1,99 | 23,497 | 0,289 |
| 1.000 | 503 | 1,99 | 46,547 | 0,296 |
| 5.000 | 2.503 | 2,00 | 212,817 | 0,297 |
| 20.000 | 10.007 | 2,00 | 2.098,516 | 0,357 |
| 50.000 | 25.013 | 2,00 | 6.114,578 | 0,435 |
| 100.000 | 50.021 | 2,00 | 12.490,318 | 0,452 |

### Experimento B — efecto del factor de carga (n = 20.000)

![Tiempo de búsqueda vs factor de carga](graficas/tiempo_vs_alfa.png)

Aquí la curva sube despacio hasta α = 4 y se dispara en α = 10.

| α meta | m | α real | Tabla (µs) |
|---:|---:|---:|---:|
| 0,25 | 80.021 | 0,250 | 0,229 |
| 0,5 | 40.009 | 0,500 | 0,269 |
| 1 | 20.011 | 0,999 | 0,295 |
| 2 | 10.007 | 1,999 | 0,368 |
| 4 | 5.003 | 3,998 | 0,492 |
| 10 | 2.003 | 9,985 | 1,813 |

---

## Parte 3 — Análisis

### 1. Costo teórico

En la lista, una guía que no existe obliga a mirar los n nodos antes de poder decir que no está: Θ(n).

En la tabla se supone que la función hash reparte las guías de forma uniforme: cada guía puede caer en cualquier casilla con la misma probabilidad (1/m) y sin depender de las otras. Así cada cadena queda con n/m = α nodos en promedio. Buscar cuesta calcular la casilla, que es una sola operación, más recorrer esa cadena: Θ(1 + α). Como en mi experimento m crece con n, α se queda constante y el costo es Θ(1). Por eso también conviene que m sea primo, para que `k mod m` no se afecte tanto por patrones en las guías.

Si todas las guías cayeran en la misma casilla, la tabla sería una sola lista de n nodos y buscar costaría Θ(n), igual que la lista enlazada.

### 2. Lo medido contra lo esperado

En la primera gráfica, de n = 50.000 a 100.000 (n se duplica) la lista pasó de 6.114,6 a 12.490,3 µs, es decir ×2,04, coherente con Θ(n). En ese tramo la tabla pasó de 0,435 a 0,452 µs (×1,04), coherente con Θ(1).

La mayor desviación está de n = 5.000 a n = 20.000: n se multiplica por 4, pero el tiempo de la lista por 2098,5 / 212,8 = ×9,9. El costo por nodo pasa de 0,043 a 0,105 µs y después se estabiliza en 0,122 (n = 50.000) y 0,125 µs (n = 100.000). Es decir, la lista es lineal al inicio (n = 100 a 5.000, entre 0,042 y 0,047 µs por nodo) y al final, pero no en el tramo intermedio (de n = 5.000 a n = 20.000), donde el costo por nodo sube. Uso el valor estabilizado en la pregunta 5.

En la segunda gráfica, de α = 0,25 a α = 10 el valor 1 + α crece unas 9 veces y el tiempo medido unas 8, así que es bastante coherente con Θ(1 + α). Por tramos no calza tan bien (de α = 4 a 10 el tiempo creció más de lo que predice), pero la forma se mantiene. Además, con α = 2 la tabla dio casi lo mismo en los dos experimentos, cerca de 0,36 µs.

### 3. Colisiones

Una colisión ocurre cuando dos guías distintas tienen el mismo `h(k)`. Pasa aunque haya más casillas que guías: el número de pares que chocan crece más o menos como n²/(2m). Con 20.000 guías y 80.021 casillas (α = 0,25) igual se esperan unos 2.500 pares, así que casi siempre hay colisiones, incluso con α < 1. Con m = 7, las guías 10, 24 y 17 dan 3.

Con encadenamiento (el que implementé), la casilla 3 guarda una lista con 17, 24 y 10. La ventaja es que la tabla nunca se llena y admite α > 1. El costo son los punteros extra: más memoria y peor localidad.

Con direccionamiento abierto todo vive en el arreglo: con sondeo lineal, 10 ocuparía la casilla 3, 24 la 4 y 17 la 5. Se ahorran punteros y hay mejor localidad, pero exige α < 1, forma agrupamientos, necesita marcas para borrar y se degrada cerca de α = 1.

### 4. Tabla hash o árbol de búsqueda

La tabla no sirve para el monitoreo por rango. Las guías consecutivas no quedan lejos (caen en casillas vecinas; con m = 7, las guías 10, 11 y 12 caen en 3, 4 y 5), pero la función no conserva el orden: al dar la vuelta, k y k + m caen en la misma casilla, y las guías de [X, Y] quedan mezcladas con las de fuera del rango. Como la tabla no sabe enumerar claves en orden, habría que revisar toda la tabla, del orden de n + m.

Un árbol de búsqueda binario sí sirve: baja hasta X y recorre en orden hasta Y, así que el costo es la altura más las r guías que haya en el rango.

Si las 400.000 guías llegaran ordenadas y se insertaran una a una, el árbol se volvería una lista de altura 400.000. Una búsqueda infructuosa haría unas 400.000 comparaciones, una exitosa unas 200.000 en promedio, y construirlo costaría del orden de 10¹¹ comparaciones (n²/2). Hasta el rango se volvería lineal. Un árbol equilibrado tendría altura 18, con unas 19 comparaciones por búsqueda.

### 5. Concepto para la jefa de operaciones

Recomiendo una combinación: tabla hash (α ≈ 2) para la consulta puntual y un árbol equilibrado (AVL o rojo-negro) para el rango, ambos actualizados con cada guía nueva.

Estimación mía para 5.000.000 de envíos, no una medición; no implementé el árbol.

Lista: con el costo por nodo estabilizado (≈ 0,125 µs), 5×10⁶ nodos dan cerca de 0,6 s, y hasta 1 s si ese costo siguiera subiendo.

Tabla: no sirve una regla de tres, porque la forma es Θ(1): de n = 5.000 a 100.000 (×20) solo subió de 0,297 a 0,452 µs. Estimo entre 0,5 y 1 µs, algo más que en mis datos por la memoria.

Árbol equilibrado: con unos 22 niveles y el costo por nodo de la lista, estimo entre 2 y 4 µs, aunque podría ser algo más porque los nodos del árbol quedan más repartidos en memoria.