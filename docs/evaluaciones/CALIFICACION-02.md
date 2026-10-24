# Retroalimentación — Laboratorio 2: Dividir y vencer

**Estudiante:** Samuel Arango Montoya · **Laboratorio:** Laboratorio evaluativo 02 — Dividir y vencer
**Fecha límite:** 2026-10-21 23:59 · **Versión revisada:** commit `d62b831`

Excelente trabajo: un informe muy completo, con datos propios y análisis honesto.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 19 / 20 |
| Calidad de la explicación teórica | 20 / 20 |
| Corrección de la implementación | 25 / 25 |
| Calidad del análisis de las gráficas | 24 / 25 |
| Documentación y organización del informe | 10 / 10 |
| **Total** | **98 / 100** |
| **Nota (0–5)** | **4.90** |

## 1. Corrección conceptual (19 / 20)
**Lo que hizo bien:**
- Identifica que divide y vencerás empieza a ganar en n = 50 y lo respalda con la tabla (0,0592 contra 0,0676 ms), y explica por qué pierde con n pequeño.
- Compara con hallar el máximo de un arreglo: combinar cuesta una sola comparación, la recurrencia da `Θ(n)` y dividir no mejora nada.
- Recomienda divide y vencerás y estima 1.000.000 de registros (unas 8 horas contra unos 3 segundos), dicho como estimación y sin regla de tres lineal.

**Lo que puede mejorar:**
- La estimación parte de un solo tamaño (n = 8000); podría apoyarse también en la forma de toda la curva medida.

## 2. Calidad de la explicación teórica (20 / 20)
**Lo que hizo bien:**
- Plantea `T(n) = 2T(n/2) + Θ(n)` explicando de dónde sale cada término.
- Aplica el método maestro y verifica la condición del caso 2.
- Justifica el `Θ(n²)` de la fuerza bruta contando las n(n+1)/2 iteraciones.

## 3. Corrección de la implementación (25 / 25)
**Lo que hizo bien:**
- Las tres funciones dan resultados correctos en todos los casos pedidos y en 200 listas aleatorias.
- `subarreglo_maximo` resuelve los tres casos y no llama a la fuerza bruta; ninguna función cambia la lista recibida.
- Tiene type hints, docstrings y cumple PEP 8.
- Revisó además que los índices devueltos concuerden con la suma.

## 4. Calidad del análisis de las gráficas (24 / 25)
**Lo que hizo bien:**
- La gráfica tiene ambas curvas en los mismos ejes, título, ejes rotulados y leyenda; mide 11 tamaños, desde 10 hasta 8000.
- Calcula el factor al duplicar n en dos pares (×4,03 y ×4,29 en fuerza bruta; ×2,19 y ×2,14 en divide y vencerás) y los contrasta con lo teórico.
- Agregó gráfica logarítmica y tabla, y reconoció con sinceridad los datos con ruido.

**Lo que puede mejorar:**
- En la gráfica lineal los tamaños pequeños quedan pegados al eje, por lo que el cruce solo se ve en la tabla y en la gráfica logarítmica; conviene decirlo al leer la gráfica principal.

## 5. Documentación y organización del informe (10 / 10)
**Lo que hizo bien:**
- Siguió la estructura acordada (`laboratorios/lab2-divide-y-vencer/`), con los archivos pedidos.
- El README sigue el orden pedido, enlaza el código, incrusta las gráficas con rutas que funcionan y trae instrucciones de reproducción.
- Tiene muchos commits con mensajes descriptivos.

## ¿El código funciona?
Sí. Las pruebas pasan y la medición corre completa y vuelve a generar las gráficas. Los tiempos cambian entre equipos, pero la forma de las curvas es la misma.

## Para el próximo laboratorio
- Sostenga el nivel: informe con datos propios y casos de prueba variados.
- Al estimar tiempos grandes, apóyese en más de un tamaño medido.
- Describa en el texto qué se ve en la gráfica principal para los tamaños pequeños.
