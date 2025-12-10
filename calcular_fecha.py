from datetime import datetime, timedelta, date
import holidays
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/calcular_fecha", methods=["GET"])
def calcular_fecha():
    fecha_inicio = request.args.get("fecha_inicio")
    dias = int(request.args.get("dias", 0))

    # Detectar formato automáticamente
    formato_argentino = False
    try:
        fecha = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    except ValueError:
        fecha = datetime.strptime(fecha_inicio, "%d-%m-%Y").date()
        formato_argentino = True

    ar_holidays = holidays.AR(years=[fecha.year, fecha.year + 1])
    dias_restantes = dias

    while dias_restantes > 0:
        fecha += timedelta(days=1)
        if fecha.weekday() < 5 and fecha not in ar_holidays:
            dias_restantes -= 1

    # Devuelve la fecha en el mismo formato que se ingresó
    if formato_argentino:
        fecha_final = fecha.strftime("%d-%m-%Y")
    else:
        fecha_final = fecha.isoformat()

    return jsonify({
        "fecha_final": fecha_final,
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
