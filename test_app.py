import unittest
from app import app

class BilleteraTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_realizar_pago_exito(self):
        # Caso de prueba: Pago exitoso entre cuentas válidas
        response = self.app.get('/billetera/pagar?minumero=123&numerodestino=456&valor=100')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Realizado en", response.get_data(as_text=True))

    def test_realizar_pago_cuenta_no_encontrada(self):
        # Caso de prueba: Pago con cuenta de origen no encontrada
        response = self.app.get('/billetera/pagar?minumero=999&numerodestino=456&valor=100')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Error: cuenta no encontrada.", response.get_data(as_text=True))

    def test_realizar_pago_destino_invalido(self):
        # Caso de prueba: Pago con cuenta de destino inválida
        response = self.app.get('/billetera/pagar?minumero=123&numerodestino=999&valor=100')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Error: no se puede realizar la transferencia.", response.get_data(as_text=True))

    def test_realizar_pago_saldo_insuficiente(self):
        # Caso de prueba: Pago con saldo insuficiente en la cuenta de origen
        response = self.app.get('/billetera/pagar?minumero=123&numerodestino=456&valor=500')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Error: no se puede realizar la transferencia.", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
