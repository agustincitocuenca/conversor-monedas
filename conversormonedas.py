import json

# Tasas fijas de conversión
conversion_rates = {
    'USD': {'EUR': 0.92, 'ARS': 880.00, 'BRL': 5.10},
    'EUR': {'USD': 1.09, 'ARS': 950.00, 'BRL': 5.50},
    'ARS': {'USD': 0.0011, 'EUR': 0.00105, 'BRL': 0.0058},
    'BRL': {'USD': 0.20, 'EUR': 0.18, 'ARS': 172.00},
}

monedas_disponibles = list(conversion_rates.keys())

def validar_moneda(moneda):
    return moneda in monedas_disponibles

def validar_monto(monto_str):
    try:
        monto = float(monto_str)
        return monto if monto > 0 else None
    except ValueError:
        return None

def convertir(moneda_origen, moneda_destino, monto):
    if moneda_origen == moneda_destino:
        return monto
    tasa = conversion_rates.get(moneda_origen, {}).get(moneda_destino)
    if tasa is None:
        raise ValueError("Conversión no soportada.")
    return monto * tasa

def guardar_en_historial(origen, destino, monto, resultado):
    conversion = {
        'de': origen,
        'a': destino,
        'monto': monto,
        'resultado': resultado
    }
    try:
        with open('historial.json', 'r') as f:
            historial = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        historial = []

    historial.append(conversion)

    with open('historial.json', 'w') as f:
        json.dump(historial, f, indent=4)

def mostrar_historial():
    try:
        with open('historial.json', 'r') as f:
            historial = json.load(f)
            if not historial:
                print("No hay conversiones registradas.")
                return
            print("\nHistorial de conversiones:")
            for item in historial:
                print(f"{item['monto']} {item['de']} → {item['resultado']:.2f} {item['a']}")
    except FileNotFoundError:
        print("El archivo de historial no existe.")
    except json.JSONDecodeError:
        print("Error al leer el historial.")