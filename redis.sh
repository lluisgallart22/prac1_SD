#!/bin/bash

# Obtener todas las claves en Redis
keys=$(redis-cli keys '*')

# Iterar sobre cada clave y obtener su valor
for key in $keys
do
    # Obtener el valor de la clave actual
    value=$(redis-cli get "$key")
    # Mostrar la clave y su valor
    echo "Connexio: $key - Servei: $value"
done
