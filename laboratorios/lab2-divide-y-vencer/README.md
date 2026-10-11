# Laboratorio 2 — Dividir y vencer

**Nombre:** Samuel Arango Montoya

## Cómo reproducir el experimento

Desde la raíz del repositorio:

```powershell
.\venv\Scripts\Activate.ps1
cd laboratorios\lab2-divide-y-vencer
python pruebas.py
python medicion.py
```

## Parte 1 — Implementación y verificación

Código: [subarreglo.py](subarreglo.py) · [pruebas.py](pruebas.py)

Implementé el subarreglo máximo de dos formas:

- **Fuerza bruta** (`subarreglo_fuerza_bruta`): dos ciclos anidados que
  recorren todos los pares de días (i, j). La suma se acumula dentro del
  ciclo interno en lugar de recalcularla, por lo que el costo es Θ(n²).
- **Divide y vencerás** (`subarreglo_maximo`): el caso base es `inicio == fin`
  (un solo elemento). En otro caso divide el rango en `inicio..medio` y
  `medio + 1..fin`, resuelve cada mitad recursivamente, calcula el tramo
  cruzado con `suma_cruzada` y devuelve el mejor de los tres. No llama a la
  fuerza bruta. `suma_cruzada` hace un barrido lineal desde `medio` hacia la
  izquierda y otro desde `medio + 1` hacia la derecha, de modo que el tramo
  siempre incluye al menos un elemento de cada lado.

Ninguna función modifica la lista recibida.

### Cómo verifiqué las soluciones

En `pruebas.py` uso `assert` y comparo **la suma**, no los índices, porque
puede haber varios tramos con la misma suma máxima. Casos cubiertos:

| Caso | Serie | Suma esperada |
|---|---|---|
| Ocho días de la situación problema | `[-3, 5, -2, 8, -6, 3, 9, -4]` | 17 |
| Un solo elemento | `[7]` y `[-7]` | 7 y -7 |
| Todos negativos | `[-8, -3, -6, -2, -5]` | -2 |
| Todos positivos | `[4, 1, 7, 3, 2]` | 17 |
| Mejor tramo cruza el punto medio (índices 2..5) | `[1, -5, 4, 3, 2, 5, -6, 1]` | 14 |

Además:

- Probé `suma_cruzada` directamente: en la serie de ocho días da 17, y en
  `[-4, -1, -2, -9]` da -3, lo que confirma que el tramo cruzado toma un
  elemento de cada lado aunque sean negativos.
- Comprobé que los índices que devuelve divide y vencerás son coherentes con
  la suma declarada (`sum(serie[ini:fin + 1]) == suma`), tanto en la serie de
  ocho días como en las listas aleatorias.
- Comprobé que las funciones no modifican la lista de entrada.
- Generé 200 listas aleatorias (semilla fija `42`, longitud entre 1 y 60,
  valores entre -50 y 50) y verifiqué que ambas funciones dan la misma suma.

Todas las pruebas pasan: el script termina imprimiendo
`Todas las pruebas pasaron`.

## Parte 2 — Medición y gráfica

Código: [medicion.py](medicion.py)

![Gráfica lineal de tiempo vs tamaño de entrada para ambos algoritmos](graficas/tiempo_vs_n.png)

![Gráfica en escala logarítmica de tiempo vs tamaño de entrada](graficas/tiempo_vs_n_log.png)

### Cómo medí

Cronometré con `time.perf_counter()` únicamente la llamada al algoritmo;
los datos se generan antes, fuera del cronómetro. Los datos son enteros
entre -100 y 100 generados con la semilla fija 42, y en cada tamaño ambos
algoritmos reciben la misma lista.

Repetí cada medición y reporto la **mediana**, porque los tiempos de pocos
milisegundos fluctúan por el ruido del sistema operativo y la mediana
resiste los valores atípicos. La fuerza bruta se repitió 200 veces para
n ≤ 100, 20 veces para 100 < n ≤ 1000 y 3 veces para n > 1000 (2000, 4000
y 8000), donde cada corrida ya es larga. Divide y vencerás se repitió 200
veces para n ≤ 100 y 21 veces para los demás tamaños. Dentro del propio
experimento, después de cronometrar, verifico con `assert` que en cada
tamaño ambos algoritmos devuelven la misma suma. Esa comprobación queda
fuera del cronómetro.

La tabla tiene algo de ruido. En divide y vencerás, de n = 50 a 100 el
tiempo se multiplicó por ×3,09 (0,0592 → 0,1827 ms) y de n = 2000 a 4000
por ×1,89 (3,5191 → 6,6346 ms); este último es imposible al duplicar n,
porque un costo n log n crece un poco más de ×2. En la fuerza bruta, con
n pequeños (10 → 20 y 20 → 40) los factores fueron ×3,08 y ×3,47, por
debajo de ×4, y ahí no lo atribuyo solo al ruido: con tan pocos datos pesan
los costos fijos. Por eso, en la Parte 3 uso los pares 1000 → 2000 y
4000 → 8000, que son los más limpios.

### Tiempos medidos

| n | Fuerza bruta (ms) | Divide y vencerás (ms) |
|---:|---:|---:|
| 10 | 0,0038 | 0,0100 |
| 20 | 0,0117 | 0,0217 |
| 30 | 0,0328 | 0,0343 |
| 40 | 0,0406 | 0,0462 |
| 50 | 0,0676 | 0,0592 |
| 100 | 0,2638 | 0,1827 |
| 500 | 6,9951 | 0,7293 |
| 1000 | 26,8632 | 1,6060 |
| 2000 | 108,2010 | 3,5191 |
| 4000 | 427,2753 | 6,6346 |
| 8000 | 1834,9476 | 14,2170 |

## Parte 3 — Análisis

### 1. Recurrencia

En `subarreglo_maximo` parto el rango en dos mitades, así que hay 2 subproblemas de tamaño n/2. `suma_cruzada` barre desde el punto medio hacia cada lado y entre los dos recorren los n elementos, o sea que cuesta Θ(n). Comparar las tres sumas es Θ(1). Queda:

T(n) = 2T(n/2) + Θ(n), con T(1) = Θ(1)

Por el método maestro, a = 2, b = 2 y f(n) = Θ(n). Como n^(log₂2) = n, f(n) tiene el mismo orden, aplica el caso 2 y T(n) = Θ(n log n).

La fuerza bruta es Θ(n²) por los dos ciclos anidados: el interno va de i hasta n−1, así que son n(n+1)/2 iteraciones de trabajo constante. Como n(n+1)/2 = n²/2 + n/2, domina el n² y la constante 1/2 no cambia el orden.

### 2. Lo medido contra lo esperado

En la gráfica lineal la fuerza bruta se dispara (de unos 430 ms en n = 4000 a unos 1830 ms en n = 8000), mientras que divide y vencerás casi no se despega del eje y llega a unos 14 ms en n = 8000. En la gráfica logarítmica la fuerza bruta es una recta más empinada.

Al duplicar n:

- 1000 → 2000: fuerza bruta ×4,03 (26,86 → 108,20 ms) y divide y vencerás ×2,19 (1,61 → 3,52 ms).
- 4000 → 8000: fuerza bruta ×4,29 (427,28 → 1834,95 ms) y divide y vencerás ×2,14 (6,63 → 14,22 ms).

Θ(n²) predice ×4 y la fuerza bruta dio 4,03 y 4,29; el 4,29 se aleja un poco, pero con solo 3 repeticiones en ese tamaño lo atribuyo a ruido. Θ(n log n) predice ≈2,20 y ≈2,17, y medí 2,19 y 2,14. Coincide en ambos pares.

### 3. Tamaños pequeños

Sí hay un cambio. En n = 10, 20, 30 y 40 gana la fuerza bruta; en n = 30 casi empatan (0,0328 contra 0,0343 ms) y en n = 40 la fuerza bruta gana por poco (0,0406 contra 0,0462 ms). En n = 50 divide y vencerás gana por primera vez (0,0592 contra 0,0676 ms) y desde ahí gana en todos los tamaños mayores. En la gráfica logarítmica las curvas se cruzan entre 40 y 50. Como las diferencias son de 5 a 12 % en centésimas de milisegundo, el cruce podría moverse entre corridas.

La ventaja aparece temprano, no tarde. Divide y vencerás pierde en 10, 20, 30 y 40 porque la recursión tiene costos fijos (llamadas, tuplas, barrido cruzado en cada nivel) que con tan pocos datos pesan más que lo que se ahorra. Al crecer n, el ahorro de n² a n log n supera esos costos.

### 4. ¿Cuándo conviene dividir?

Para el máximo de un arreglo, dividir da T(n) = 2T(n/2) + Θ(1), porque combinar es una sola comparación entre dos números. Por el método maestro, f(n) = Θ(1) es menor que n, caso 1, y T(n) = Θ(n). Es igual que recorrerlo una vez, así que dividir no mejora nada.

En el subarreglo máximo sí sirve: la alternativa era Θ(n²) y dividir la baja a Θ(n log n), aunque combinar cueste Θ(n). Conviene dividir cuando la solución directa es más que lineal y combinar cuesta menos de lo que se ahorra.

### 5. Concepto para la gerente

Recomiendo divide y vencerás. Lo que sigue es una **estimación**, no una medición: parto de mis datos en n = 8000 y escalo con la fórmula de cada algoritmo, no con regla de tres lineal. Un millón es 125 veces 8000.

- **Fuerza bruta:** crece como n², entonces ×15.625. 1834,95 ms × 15.625 ≈ 28.671.000 ms, unas 8 horas.
- **Divide y vencerás:** crece como n log n, entonces el factor es 125 × (19,93 / 12,97) ≈ 192. 14,22 ms × 192 ≈ 2730 ms, unos 3 segundos.

Esto asume que la constante se mantiene y con series tan grandes la memoria y el caché pueden mover los números, pero horas contra segundos no cambia la recomendación. Con sensores de cientos de miles de registros la fuerza bruta deja de ser viable.