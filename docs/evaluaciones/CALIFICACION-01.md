# Retroalimentación — Laboratorio 1: fundamentos, complejidad y recurrencias

**Estudiante:** Samuel Arango Montoya · **Laboratorio:** Laboratorio evaluativo 01 — Fundamentos, complejidad y recurrencias
**Fecha límite:** 2026-10-04 23:59 · **Versión revisada:** commit `eccff62`

Muy buen trabajo: el informe está completo, ordenado y apoyado en sus propias mediciones.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 22 / 25 |
| Calidad de la explicación teórica | 23 / 25 |
| Corrección de la implementación | 19 / 20 |
| Calidad del análisis de las gráficas | 17 / 20 |
| Documentación y organización del informe | 8 / 10 |
| **Total** | **89 / 100** |
| **Nota (0–5)** | **4.45** |

## 1. Corrección conceptual (22 / 25)
**Lo que hizo bien:**
- Separa con claridad "correcto" de "dentro de la ventana" y nombra la restricción que Tamiza incumple: las cuatro horas.
- Explica por qué un servidor el doble de rápido solo aplaza el problema: la ganancia es fija y el trabajo crece al cuadrado.
- Su ejemplo propio (el script de Colcafé) trae datos y una restricción concreta (20.000 a 30.000 filas, límite de 6 minutos).
- Calcula el consumo de energía por noche y por año, y nombra al menos dos personas afectadas diciendo quién asume el costo.
- La reflexión sobre verificar la salida, avisar si el proceso no termina y desempatar es muy buena.

**Lo que puede mejorar:**
- El consumo de 400 W es un supuesto suyo; diga de dónde sale o que es una suposición.
- Dice que "quien debería asumir el error es el equipo de desarrollo" sin desarrollarlo: explique por qué.

## 2. Calidad de la explicación teórica (23 / 25)
**Lo que hizo bien:**
- Define peor caso, mejor caso y caso promedio indicando sobre qué conjunto de entradas se toma cada uno.
- Justifica bien por qué usaría el peor caso y deja escrita la predicción antes de medir.
- Plantea la recurrencia de merge sort explicando cada término y la resuelve con el árbol de recursión, con costo por nivel, número de niveles y total.
- El conteo línea a línea de insertion sort y la tabla de complejidades están completos.

**Lo que puede mejorar:**
- Para el caso promedio de insertion sort dice que cada elemento recorre "la mitad"; mostrar la suma (n(n−1)/4) paso a paso lo haría más sólido.

## 3. Corrección de la implementación (19 / 20)
**Lo que hizo bien:**
- `insertion_sort` y `merge_sort` ordenan bien, no cambian la lista recibida, cuentan solo comparaciones entre elementos y no usan `sorted()` ni `sort()`.
- La mezcla de merge sort es propia y recursiva; hay tipos y explicaciones en cada función.
- Los generadores usan semilla y producen listas con valores distintos.

**Lo que puede mejorar:**
- En `generar_casi_ordenado`, el 2 % final son los valores más pequeños, así que casi no hay trabajo extra para el algoritmo. Lo reconoce en el informe, pero un 2 % con valores repartidos en todo el rango habría representado mejor el reproceso real.

## 4. Calidad del análisis de las gráficas (17 / 20)
**Lo que hizo bien:**
- Las tres gráficas tienen título, ejes rotulados, leyenda y las curvas pedidas en los mismos ejes.
- Identifica peor caso (C), mejor caso (B) y aproximación al promedio (A) con cifras medidas, y contrasta con su predicción.
- En 4.2 describe lo que hace cada curva, lo une con Θ(n²) y Θ(n log n), y explica los tamaños pequeños.
- El concepto técnico recomienda merge sort, extrapola a 1.200.000 registros declarándolo como estimación y responde al servidor con un dato medido. Incluye también la consideración de memoria.

**Lo que puede mejorar:**
- Cada tiempo es una sola medición; repetir y promediar daría curvas más estables. Si lo hace, dígalo en el informe.
- Como B es tan favorable, la conclusión de que "insertion sort solo gana en B" queda algo optimista.

## 5. Documentación y organización del informe (8 / 10)
**Lo que hizo bien:**
- Carpeta en la ubicación acordada, con todos los archivos y gráficas pedidos y las imágenes visibles con ruta relativa.
- Cada parte práctica enlaza su código; hay 12 commits descriptivos.

**Lo que puede mejorar:**
- Las instrucciones de reproducción solo sirven para Windows y crean el entorno fuera del repositorio; el curso pedía el entorno de la raíz del repositorio, con `matplotlib` en `requirements.txt`. Incluya también los pasos para macOS/Linux.

## ¿El código funciona?
Sí. Los dos algoritmos ordenan bien (probé listas pequeñas, aleatorias y con repetidos), los scripts corren sin errores y generan las tres gráficas.

## Para el próximo laboratorio
- Diseñe los escenarios de prueba pensando en qué tan realistas son (por ejemplo, el 2 % nuevo repartido en todo el rango).
- Repita cada medición varias veces y grafique el promedio.
- Use el entorno virtual de la raíz del repositorio e incluya las instrucciones para todos los sistemas.
- Muestre el desarrollo de los cálculos que hoy solo enuncia (como el caso promedio).
- Indique de dónde salen los supuestos numéricos (como los 400 W).
