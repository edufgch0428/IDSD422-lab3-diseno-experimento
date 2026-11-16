# comparacion_experimento.py — Comparación de grupos (Python)
# Completa los pasos marcados con TODO. Ejecuta desde la raíz del repositorio:
#   python scripts/comparacion_experimento.py


# TODO 1: carga plantillas/registro_experimento.csv con pandas
import pandas as pd 
import numpy as np
df = pd.read_csv("plantillas/registro_experimento.csv")

# TODO 2: calcula e imprime el promedio de ventas_producto por ubicacion
print("Promedio de ventas por ubicación:")
print(df.groupby("ubicacion")["ventas_producto"].mean())

# TODO 3: imprime el número de registros por grupo (value_counts)
print("\nNúmero de registros por grupo:")
print(df["ubicacion"].value_counts())

# TODO 4: escribe 2–3 líneas de interpretación (sección 9 de la plantilla):
#         por qué con 4 filas no se puede concluir y qué le faltaría al análisis

# El grupo pasillo_principal muestra un promedio mayor con 1335 USD que el habitual con 1040 USD,
# pero no se puede concluir nada porque no hay una asignación real aleatoria, los datos son
# muy pocos teniendo dos por grupo, en el cual no tenemos control de temporada, ni promociones en el grupo pasillo
# y no hay medida de variabilidad.
# Para que el análisis sea justo faltaría usar las 40 unidades con la asignación aleatoria
# de la sección 5, controlar o excluir las semanas con promoción y calcular la variabilidad
# de cada grupo. También haría falta una prueba estadística o un intervalo de confianza
# para saber si la diferencia es mayor de lo que se esperaría solo por azar.

# SECCIÓN 5 de la plantilla: asignación aleatoria 
tiendas = ["Quito Norte", "Quito Sur", "Guayaquil Centro", "Guayaquil Norte", "Cuenca Centro",
        "Cuenca Sur", "Ambato Centro", "Manta", "Loja", "Machala"]
semanas = [1, 2, 3, 4]

rng = np.random.default_rng(1234597)
primera = rng.choice(["pasillo_principal", "habitual"], size=len(tiendas))

filas = []
for tienda, cond in zip(tiendas, primera):
    otra = "habitual" if cond == "pasillo_principal" else "pasillo_principal"
    for s in semanas:
        filas.append({"tienda": tienda, "semana": s, "ubicacion": cond if s % 2 == 1 else otra})
diseno = pd.DataFrame(filas)

#Imprime la tabla de asignacion en conjunto con el pasillo_habitual y pasillo_principal con su respectivo conteo 
diseno["u"] = diseno["ubicacion"].map({"pasillo_principal": "P", "habitual": "H"})
print(diseno.pivot(index="tienda", columns="semana", values="u").loc[tiendas].to_string())
print("\nConteo por grupo:\n", diseno["ubicacion"].value_counts())
print("\nCondición inicial sorteada:\n", pd.Series(primera).value_counts())

##PARA EL SUSTENTO DEL LABORATORIO REALIZADO 
#Diseño del experimento
import pandas as pd
import numpy as np
from scipy import stats


tiendas=["Quito Norte", "Quito Sur", "Guayaquil Centro", "Guayaquil Norte", "Cuenca Centro", "Cuenca Sur", "Ambato Centro", "Manta", "Loja", "Machala"]
semanas = [1,2,3,4]

#sorteo de la condicion inicial
rng = np.random.default_rng(1234597)
primera = rng.choice(["pasillo_principal", "habitual"], size=len(tiendas))

filas = []
for tienda, cond in zip(tiendas, primera):
    otra = "habitual" if cond=="pasillo_principal" else "pasillo_principal"
    for s in semanas:
        filas.append({"tienda": tienda, "semana": s, "ubicacion":cond if s%2 == 1 else otra})
diseno = pd.DataFrame(filas)


#simulacion de la ejecucion
rng = np.random.default_rng(1234598)
efecto_tienda=dict(zip(tiendas,rng.normal (1100,120,(len(tiendas)))))
efecto_semana={1:0,2:30,3:60,4:90}

diseno["ventas_producto"] = (
    diseno["tienda"].map(efecto_tienda) +
    diseno["semana"].map(efecto_semana)+
    (diseno["ubicacion"]=="pasillo_principal")*220+
    rng.normal(0,90,len(diseno))
).round(0).astype(int)

#promocion simultanea registrada

diseno["promocion_simultanea"]="no"

diseno.loc[(diseno["tienda"]=="Guayaquil Centro") & (diseno["semana"]==1),"promocion_simultanea"]="si"
diseno.loc[diseno["promocion_simultanea"]=="si","ventas_producto"]+=180

diseno.to_csv("plantillas/resultado_simulacion.csv", index=False)

#Analisis pareado: una fila por tienda con sus condiciones
piv = diseno.groupby(["tienda", "ubicacion"])["ventas_producto"].mean().unstack()
piv["diferencia"]=piv["pasillo_principal"]-piv["habitual"]

media= piv["diferencia"].mean()
dev= piv["diferencia"].std(ddof=1)
n = len(piv)

print("La media de la columna diferencia es: ", media)
print("La desviación estandar de la columna diferencia es: ", dev)

# De izquierda a derecha, se deja el 2.5 que queremos saber
t_crict = stats.t.ppf(0.975, df=9)
ic_inf = media - (t_crict*dev/n**0.5)
ic_sup = media + (t_crict*dev/n**0.5)

## Independiente del numero de veces que se corra
## el experimento podemos decir que con un %96 de certeza
## el valor del promedio de la diferencia de ventas del producto
## entre el pasillo principal y el habitual va a caer en el rago

print(f"IC 95%: [{ic_inf}, {ic_sup}]")

# prueba p - value
prueba = stats.ttest_rel(piv["pasillo_principal"], piv["habitual"])
print(f"Prueba t: {prueba.pvalue: 10f}")