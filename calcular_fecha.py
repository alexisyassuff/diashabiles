from datetime import datetime, timedelta
import holidays
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/calcular_fecha", methods=["GET"])
def calcular_fecha():
    fecha_inicio = request.args.get("fecha_inicio")
    dias = int(request.args.get("dias", 0))
    amortiguador = request.args.get("amortiguador")
    amortiguador = int(amortiguador) if amortiguador is not None else None

    # Detectar formato automáticamente
    formato_argentino = False
    try:
        fecha = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    except ValueError:
        fecha = datetime.strptime(fecha_inicio, "%d-%m-%Y").date()
        formato_argentino = True

    ar_holidays = holidays.AR(years=[fecha.year, fecha.year + 1])

    dias_objetivo = dias
    dias_maximos = dias + amortiguador if amortiguador is not None else None

    dias_contados = 0
    fecha_final = None
    fecha_final_amortiguador = None

    while True:
        fecha += timedelta(days=1)

        if fecha.weekday() < 5 and fecha not in ar_holidays:
            dias_contados += 1

            if dias_contados == dias_objetivo:
                fecha_final = fecha

            if dias_maximos is not None and dias_contados == dias_maximos:
                fecha_final_amortiguador = fecha
                break

            if dias_maximos is None and dias_contados == dias_objetivo:
                break

    # Formateo según formato de entrada
    def formatear(f):
        return f.strftime("%d-%m-%Y") if formato_argentino else f.isoformat()

    respuesta = {
        "fecha_final": formatear(fecha_final)
    }

    if fecha_final_amortiguador:
        respuesta["fecha_final_amortiguador"] = formatear(fecha_final_amortiguador)

    return jsonify(respuesta)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
