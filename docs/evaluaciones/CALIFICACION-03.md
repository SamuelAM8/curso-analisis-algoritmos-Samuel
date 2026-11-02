# Retroalimentación — Laboratorio 3: Estructuras de datos

**Estudiante:** Samuel Arango Montoya · **Laboratorio:** Laboratorio evaluativo 03 — Estructuras de datos
**Fecha límite:** 2026-11-01 23:59 · **Versión revisada:** commit `3f00104`

Excelente trabajo: implementación correcta, mediciones propias y un análisis claro que se apoya en sus datos.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 20 / 20 |
| Calidad de la explicación teórica | 19 / 20 |
| Corrección de la implementación | 25 / 25 |
| Calidad del análisis de las gráficas | 24 / 25 |
| Documentación y organización del informe | 10 / 10 |
| **Total** | **98 / 100** |
| **Nota (0–5)** | **4.90** |

## 1. Corrección conceptual (20 / 20)
**Lo que hizo bien:**
- Explica bien qué es una colisión y por qué ocurre aunque sobren casillas, y usa el ejemplo de 10, 24 y 17 con m = 7.
- Compara encadenamiento y direccionamiento abierto con ventajas y costos de cada uno.
- Justifica por qué la tabla no sirve para rangos y estima la altura (400.000) y las comparaciones del árbol degenerado frente al equilibrado (altura 18).
- Recomienda una combinación (tabla más árbol equilibrado) y declara que la estimación a 5.000.000 es una estimación, razonando la forma de la curva.

## 2. Calidad de la explicación teórica (19 / 20)
**Lo que hizo bien:**
- Justifica el `Θ(n)` de la lista y el `Θ(1 + α)` de la tabla, nombra el supuesto de hash uniforme (1/m, independiente) y explica que con todas las guías en una casilla la tabla se vuelve una lista de costo `Θ(n)`.

**Lo que puede mejorar (y cómo corregirlo):**
- La justificación del `Θ(n)` de la lista es muy breve.
  → *Cómo corregirlo:* agregue una frase que diga qué se hace en cada nodo y cuántos nodos se visitan en el peor caso.

## 3. Corrección de la implementación (25 / 25)
**Lo que hizo bien:**
- Lista y tabla devuelven el estado correcto en búsquedas exitosas e infructuosas; la colisión forzada con m = 7 funciona y `factor_carga` da 3/7.
- La tabla reutiliza la lista, no usa `dict`, `set` ni `hash()`, y la búsqueda es iterativa.
- Hay 25 colecciones aleatorias comparando lista y tabla, con guías existentes e inexistentes.
- Todas las funciones tienen docstring con `Args`/`Returns`, *type hints* y dos líneas en blanco entre funciones.

## 4. Calidad del análisis de las gráficas (24 / 25)
**Lo que hizo bien:**
- Ambas gráficas existen con título, ejes rotulados y leyenda; la primera tiene siete valores de n con las dos curvas en los mismos ejes y la segunda seis valores de α.
- Calcula factores de crecimiento (×2,04 en la lista y ×1,04 en la tabla al duplicar n) y los contrasta con `Θ(n)` y `Θ(1)`.
- Detecta con honestidad el tramo de n = 5.000 a 20.000 que no calza y dice que su explicación (caché) es una hipótesis sin verificar.
- Compara 1 + α con el tiempo medido en la segunda gráfica, también por tramos.

**Lo que puede mejorar (y cómo corregirlo):**
- En la segunda gráfica, el salto entre α = 4 y α = 10 queda sin explicar más allá de señalar que no calza.
  → *Cómo corregirlo:* proponga una causa posible (por ejemplo, qué ocurre con el tamaño de las cadenas) y dígala como hipótesis, igual que hizo con la caché.

## 5. Documentación y organización del informe (10 / 10)
**Lo que hizo bien:**
- El laboratorio está en `laboratorios/lab3-estructuras-datos/`, con los archivos del entregable y la carpeta `graficas/`.
- El README sigue el orden pedido, tiene su nombre, instrucciones de reproducción, enlaces al código en cada parte y las gráficas se ven con ruta relativa.
- Hay 13 commits en el laboratorio, con mensajes descriptivos (varios son solo "Update README.md", pero el conjunto es suficiente).

## ¿El código funciona?
Sí. Las pruebas pasan, la medición corre completa y regenera las dos gráficas con la misma forma de curvas que las publicadas.
