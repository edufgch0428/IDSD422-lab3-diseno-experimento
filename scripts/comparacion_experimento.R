# comparacion_experimento.R — Comparación de grupos (R)
# Completa los pasos marcados con TODO. Ejecuta desde la raíz del repositorio:
#   Rscript scripts/comparacion_experimento.R

# TODO 1: Cargar el archivo CSV
datos <- read.csv("plantillas/registro_experimento.csv")

# TODO 2: Calcular el promedio por ubicación
cat("Promedio de ventas por ubicación:\n")
promedios <- aggregate(ventas_producto ~ ubicacion, data = datos, FUN = mean)
print(promedios)

# TODO 3: Contar los registros por grupo
cat("\nNúmero de registros por grupo:\n")
print(table(datos$ubicacion))

# TODO 4: Interpretación de resultados
# El pasillo principal presenta mayores ventas promedio,
# pero los cuatro registros no permiten comprobar que
# la ubicación sea la causa de esta diferencia.    por qué con 4 filas no se puede concluir y qué le faltaría al análisis
