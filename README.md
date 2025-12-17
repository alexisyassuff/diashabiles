# Calculadora de fecha final con días hábiles (multi-país)

Este servicio calcula una **fecha final estimada** en base a una fecha de inicio y una cantidad de días hábiles, considerando los **feriados nacionales del país indicado**, además de excluir domingos y, opcionalmente, sábados.

Opcionalmente permite calcular una **fecha final máxima** sumando un amortiguador (changüí) de días hábiles adicionales.

## Descripción general

El servicio expone un endpoint HTTP (`/calcular_fecha`) que recibe:

- `fecha_inicio`: fecha de inicio (formato `YYYY-MM-DD` o `DD-MM-YYYY`)
- `dias`: cantidad de días hábiles a sumar
- `pais` (opcional): código de país (`AR`, `ES`, `CL`, `BR`, `US`, etc.).  
  Por defecto: `AR`
- `incluye_sabado` (opcional): `true` o `false`.  
  Por defecto: `false`
- `amortiguador` (opcional): cantidad de días hábiles adicionales de tolerancia

Retorna una fecha final en formato JSON, ajustada al calendario laboral del país seleccionado.
Si se envía el amortiguador, también retorna la fecha final máxima permitida.

## Ejemplo de uso

### Sin amortiguador:

curl "http://127.0.0.1:5000/calcular_fecha?fecha_inicio=01-04-2026&dias=1&pais=AR"

```json
{ "fecha_final": "06-04-2026", "incluye_sabado": false, "pais": "AR" }
```

Sábado día hábil (Argentina):

curl "http://127.0.0.1:5000/calcular_fecha?fecha_inicio=01-04-2026&dias=1&amortiguador=11&pais=AR&incluye_sabado=true"

`````json
{"fecha_final":"04-04-2026","fecha_final_amortiguador":"17-04-2026","incluye_sabado":true,"pais":"AR"}
```

Sábado día hábil (España):

curl "http://127.0.0.1:5000/calcular_fecha?fecha_inicio=01-04-2026&dias=1&amortiguador=11&pais=ESincluye_sabado=true"

````json
{"fecha_final":"02-04-2026","fecha_final_amortiguador":"16-04-2026","incluye_sabado":true,"pais":"ES"}
```


## Instalación

### Crear y activar un entorno virtual:

python3 -m venv venv
source venv/bin/activate

### Instalar las dependencias necesarias:

pip install flask holidays

### Ejecutar el script:

python3 calcular_fecha.py
El servidor quedará corriendo localmente en el puerto 5000.
`````
