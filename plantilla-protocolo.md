# Plantilla de protocolo — Experimento de ubicación de producto

**Nombre:** Fogacho Eduardo · **Fecha:** 27/10/2026

Completa cada sección. Usa commits por sección; la historia del repositorio se revisa.

## 1. Pregunta e hipótesis

El producto en el pasillo principal vende mas en promedio que su ubicacion habitual en ventas semanales durante 4 semanas. 

- **H0:** Las ventas semanales del producto en el pasillo principal no son mayores a las de la ubicación habitual.
- **H1:** Las ventas semanales del producto en el pasillo principal son mayores que en la ubicación habitual.

## 2. Unidad experimental

Semana-Tienda (**# de tiendas * # de semanas**)

- Unidad: Una tienda en una semana
- Número de unidades y justificación: 10 tiendas * 4 semanas = 40 unidades

## 3. Factor, niveles y tratamiento

- **Factor** (variable manipulada): Ubicacion del producto
- **Niveles** (valores del factor): Pasillo principal y pasillo habitual 
- **Tratamiento** (combinación asignada): Pasillo durante una semana y ubicacion habitual durante otra (grupo de control)

## 4. Grupo de control

La misma tienda pero con el producto dispuesto en la ubicación habitual. 
Su rol es servir de punto de comparación, pues, sin el control no sabríamos si las ventas del pasillo son altas por la ubicación o simplemente porque esa semana se vendió más en general.


## 5. Aleatorización

*¿Cómo se asignan las unidades a los grupos? ¿Por qué es necesaria?*

Para cada una de las 10 tiendas se sortea al azar con qué ubicación empieza en la semana 1 ya sea con pasillo principal o habitual; después se alterna cada semana. Así cada tienda pasa 2 semanas en cada ubicación y las 40 tienda-semanas quedan en 20 y 20. Se sortea porque si nosotros eligiéramos qué tienda empieza en el pasillo, podríamos poner sin querer las tiendas más fuertes en un grupo. El azar reparte entre los grupos, en promedio, los factores que no conocemos ni medimos como lo son el tipo de cliente, temporada, clima, y por eso la diferencia que veamos se puede atribuir a la ubicación. Como cada tienda se compara consigo misma, también se controla su tamaño.

- **Línea de código de la asignación (Python):** el código completo se encuentra en `scripts/comparacion_experimento.py`, en la parte de la sección 5

```python
rng = np.random.default_rng(1234597)
primera = rng.choice(["pasillo_principal", "habitual"], size=len(tiendas))
```

**Resultado de una corrida con semilla 1234597**, con P = pasillo_principal y H = habitual:

| Tienda | Sem 1 | Sem 2 | Sem 3 | Sem 4 |
|---|---|---|---|---|
| Quito Norte | H | P | H | P |
| Quito Sur | P | H | P | H |
| Guayaquil Centro | H | P | H | P |
| Guayaquil Norte | P | H | P | H |
| Cuenca Centro | P | H | P | H |
| Cuenca Sur | H | P | H | P |
| Ambato Centro | H | P | H | P |
| Manta | H | P | H | P |
| Loja | H | P | H | P |
| Machala | P | H | P | H |

Conteo por grupo: habitual = 20, pasillo_principal = 20. Condición inicial sorteada: 6 tiendas en habitual y 4 en pasillo.

## 6. Respuesta y medición

- Variable respuesta: Ventas semanales en USD 
- Período de medición: 4 semanas 
- Quién registra y cómo (¿ciego?): El punto de venta POS registra las ventas automáticamente sin intervención humana, así que la medición no depende de lo que opine o note el personal. El personal sí verá dónde está el producto, por eso se confía en el registro automático.

## 7. Factores a controlar (mínimo 4)

| Factor a controlar | Cómo se controla o registra |
|---|---|
| 1.  Clima |  Se registra por semana y tienda de esta manera, la aleatorización lo reparte entre ambos grupos. |
| 2.  Evento local | Se anota un calendario de eventos por ciudad cuando una semana tiene un evento fuerte. |
| 3. Surtido - Stock | Se asegura que el producto tenga stock suficiente en ambas ubicaciones y se registran los quiebres de inventario. |
| 4. Cambios en el personal | Se mantiene el mismo personal durante el experimento y se registra cualquier cambio. |
| 5. Promociones simultáneas | No se hacen promociones del producto durante el experimento; si ocurre alguna, se registra en promocion_simultanea. |

## 8. Limitaciones del diseño

*¿Qué podría invalidar el experimento si no se controla? ¿Qué no se podrá concluir?*

- Pérdida de potencia por promociones: una promoción simultánea puede subir las ventas y confundirse con el efecto de la ubicación.
- Canibalización de las tiendas: poner el producto en el pasillo podría quitar ventas a otros productos. Solo medimos el producto estrella, así que no podemos concluir si la ganancia total de la tienda sube.

## 9. Comparación en código (Python/R)

*Escribe `scripts/comparacion_experimento.py` (o `.R`): debe cargar `plantillas/registro_experimento.csv` y calcular el promedio de `ventas_producto` por `ubicacion`. Incluye la salida y responde:*

Salida del script:

```
Promedio de ventas por ubicación:
ubicacion
habitual             1040.0
pasillo_principal    1335.0
Name: ventas_producto, dtype: float64

Número de registros por grupo:
ubicacion
pasillo_principal    2
habitual             2
Name: count, dtype: int64
```

- ¿Qué grupo muestra mayor venta promedio en la plantilla?

El pasillo_principal muestra 1335 USD en ventas frente a 1040 USD en el habitual.

- ¿Por qué con 4 filas no se puede concluir nada sobre el efecto de la ubicación?

No se puede concluir porque no hay una asignación real aleatoria, los datos son muy pocos teniendo dos por grupo y no tenemos control de temporada, ni promociones en el grupo pasillo y no hay medida de variabilidad. 

- Si el experimento se ejecutara con tu protocolo, ¿qué le faltaría a este análisis para ser justo?

Le faltaría usar las 40 unidades con la asignación aleatoria de la sección 5, controlar o excluir las semanas con promoción y calcular la variabilidad de cada grupo. También haría falta una prueba estadística o un intervalo de confianza para la diferencia de promedios, y así saber si la diferencia observada es mayor de lo que se esperaría solo por azar.


