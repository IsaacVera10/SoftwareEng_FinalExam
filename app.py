from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.operaciones = []

    def historial(self):
        saldo_str = f"Saldo de {self.nombre}: {self.saldo}"
        operaciones_str = "<br>".join(str(op) for op in self.operaciones)
        return f"""
        {saldo_str} <br>
        Operaciones de {self.nombre} <br>
        {operaciones_str}
        """

    def pagar(self, destino, valor):
        if destino in self.contactos and self.saldo >= valor:
            self.saldo -= valor
            operacion = Operacion(destino, datetime.now(), -valor)
            self.operaciones.append(operacion)

            # Actualizar saldo del destinatario
            destinatario = buscar_cuenta_por_numero(destino)
            if destinatario:
                destinatario.saldo += valor
                destinatario.operaciones.append(Operacion(self.numero, datetime.now(), valor))

            return f"Realizado en {operacion.fecha.strftime('%d/%m/%Y')}."
        else:
            return "Error: no se puede realizar la transferencia."

    def format_operaciones(self):
        return "\n".join(str(op) for op in self.operaciones)


class Operacion:
    def __init__(self, numero_destino, fecha, valor):
        self.numero_destino = numero_destino
        self.fecha = fecha
        self.valor = valor

    def __str__(self):
        name_cuenta = buscar_nombre_por_numero(self.numero_destino)
        tipo = f"realizado de {abs(self.valor)} a" if self.valor < 0 else f"recibido de {abs(self.valor)} de"
        return f"Pago {tipo} {name_cuenta}"


# Inicializar la aplicación con las cuentas y contactos
BD = [
    Cuenta("21345", "Arnaldo", 200, ["123", "456"]),
    Cuenta("123", "Luisa", 400, ["456"]),
    Cuenta("456", "Andrea", 300, ["21345"])
]


# Implementación de los endpoints

@app.route('/billetera/contactos')
def obtener_contactos():
    minumero = request.args.get('minumero')
    cuenta = buscar_cuenta_por_numero(minumero)
    if cuenta:
        contactos_str = "<br>".join(f"{numero}: {buscar_nombre_por_numero(numero)}" for numero in cuenta.contactos)
        return contactos_str
    else:
        return "Error: cuenta no encontrada."


@app.route('/billetera/pagar')
def realizar_pago():
    minumero = request.args.get('minumero')
    numerodestino = request.args.get('numerodestino')
    valor = float(request.args.get('valor'))
    cuenta = buscar_cuenta_por_numero(minumero)
    if cuenta:
        resultado = cuenta.pagar(numerodestino, valor)
        return resultado
    else:
        return "Error: cuenta no encontrada."


@app.route('/billetera/historial')
def obtener_historial():
    minumero = request.args.get('minumero')
    cuenta = buscar_cuenta_por_numero(minumero)
    if cuenta:
        return cuenta.historial()
    else:
        return "Error: cuenta no encontrada."


def buscar_cuenta_por_numero(numero):
    for cuenta in BD:
        if cuenta.numero == numero:
            return cuenta
    return None


def buscar_nombre_por_numero(numero):
    for cuenta in BD:
        if cuenta.numero == numero:
            return cuenta.nombre
    return None


if __name__ == '__main__':
    app.run()
