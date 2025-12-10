# Calculadora de fecha final con días hábiles (Argentina)

Este servicio calcula una **fecha final estimada** en base a una fecha de inicio y una cantidad de días hábiles, considerando los **feriados nacionales de Argentina**, además de excluir sábados y domingos

## Descripción general

El servicio expone un endpoint HTTP (`/calcular_fecha`) que recibe:

- `fecha_inicio`: fecha de inicio (formato `YYYY-MM-DD` o `DD-MM-YYYY`)
- `dias`: cantidad de días hábiles a sumar

Retorna una fecha final en formato JSON, ya ajustada a días laborables del calendario argentino

## Ejemplo de uso

curl "http://127.0.0.1:5000/calcular_fecha?fecha_inicio=01-04-2026&dias=1"

Respuesta:

```json
{ "fecha_final": "2026-04-06" }
```

## Instalación

### Crear y activar un entorno virtual:

python3 -m venv venv
source venv/bin/activate

### Instalar las dependencias necesarias:

pip install flask holidays

### Ejecutar el script:

python calcular_fecha.py

El servidor quedará corriendo localmente en el puerto 5000.
