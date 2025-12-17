from datetime import datetime, timedelta
import holidays
from flask import Flask, request, jsonify

app = Flask(__name__)

# Mapeo de países soportados
HOLIDAYS_MAP = {
    "AR": holidays.AR,
    "ES": holidays.ES,
    "CL": holidays.CL,
    "BR": holidays.BR,
    "US": holidays.US,
    "MX": holidays.MX,
    "UY": holidays.UY,
    "CO": holidays.CO,
}

def es_dia_habil(fecha, feriados, incluye_sabado):
    # Domingo nunca es hábil
    if fecha.weekday() == 6:
        return False

    # Sábado depende del parámetro
    if fecha.weekday() == 5 and not incluye_sabado:
        return False

    # Feriado nacional
    if fecha in feriados:
        return False

    return True

@app.route("/calcular_fecha", methods=["GET"])
def calcular_fecha():
    fecha_inicio = request.args.get("fecha_inicio")
    dias = int(request.args.get("dias", 0))
    amortiguador = request.args.get("amortiguador")
    pais = request.args.get("pais", "AR").upper()
    incluye_sabado = request.args.get("incluye_sabado", "false").lower() == "true"

    amortiguador = int(amortiguador) if amortiguador is not None else None

    # Detectar formato de fecha automáticamente
    formato_argentino = False
    try:
        fecha = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    except ValueError:
        fecha = datetime.strptime(fecha_inicio, "%d-%m-%Y").date()
        formato_argentino = True

    if pais not in HOLIDAYS_MAP:
        return jsonify({"error": "País no soportado"}), 400

    feriados = HOLIDAYS_MAP[pais](years=[fecha.year, fecha.year + 1])

    dias_objetivo = dias
    dias_maximos = dias + amortiguador if amortiguador is not None else None

    dias_contados = 0
    fecha_final = None
    fecha_final_amortiguador = None

    while True:
        fecha += timedelta(days=1)

        if es_dia_habil(fecha, feriados, incluye_sabado):
            dias_contados += 1

            if dias_contados == dias_objetivo:
                fecha_final = fecha

            if dias_maximos is not None and dias_contados == dias_maximos:
                fecha_final_amortiguador = fecha
                break

            if dias_maximos is None and dias_contados == dias_objetivo:
                break

    def formatear(f):
        return f.strftime("%d-%m-%Y") if formato_argentino else f.isoformat()

    respuesta = {
        "fecha_final": formatear(fecha_final),
        "pais": pais,
        "incluye_sabado": incluye_sabado
    }

    if fecha_final_amortiguador:
        respuesta["fecha_final_amortiguador"] = formatear(fecha_final_amortiguador)

    return jsonify(respuesta)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
