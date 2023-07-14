# Ingeniería de Software 2023-1
## EXAMEN FINAL
### Pregunta 1:
Desarrollado en el archivo `app.py`. Primero instalar los requerimientos con el comando `pip install -r requeriments.txt`. Luego ejecutar el comando `flask run` para iniciar el servidor.

### Pregunta 2:
Desarrollado en el archivo `test_app.py`.

### Pregunta 3:
Para que la api soporte un valor máximo de 200 soles a transferir por día. Podría realizarlos siguientes cambios:
 - En la clase `Cuenta` debería agregar un atributo llamado `saldo_diario_transferir`para registrar el saldo transferido en un día determinado. Además, se puede agregar un método llamado `verificar_limite_diario` que verifique si el valor de transferencia excede el límite.
 
 - Para asegurarme de que el pago no se realize si hay un exceso de límite, en el método `pagar` de la clase Cuenta, se debe llamar al método `verificar_limite_diario` antes de realizar la transferencia.
 
 - En el método `verificar_limite_diario`, se puede verificar si el valor de transferencia más el `saldo_diario_transferir` existente supera el límite diario de 200 soles. Si es así, se devuelve un mensaje de error indicando que se ha excedido el límite.

Un caso de prueba a adicionar sería: 
```
def test_limite_transferencia_diario(self):
    # Caso de prueba: Transferencia que excede el límite diario
    cuenta_origen = buscar_cuenta_por_numero("123")
    cuenta_destino = buscar_cuenta_por_numero("456")
    cuenta_origen.saldo_diario_transferir = 200  # Establecer un saldo diario existente de 200 soles
    valor_transferencia = 100  # Valor de transferencia de 100 soles
    response = cuenta_origen.pagar("456", valor_transferencia)
    self.assertEqual(response, "Error: se ha excedido el límite diario de transferencia.")

```

Respecto al riesgo de "romper" lo que ya funciona, al realizar estos cambios la probabilidad de que se introduzcan errores o se afecte el funcionamiento existente son muy altas. Por ello, el seguir buenas prácticas de desarrollo como realizar pruebas exhaustivas y revisar cuidadosamente los cambios antes de implementarlos, es imperativo en este campo, ya que pueden reducir el riesgo de romper el código existente.

Como vimos en clase, es recomendable realizar pruebas unitarias adicionales para cubrir los nuevos casos y verificar que los cambios funcionen correctamente antes de implementarlos en producción. Esto ayuda a detectar y corregir cualquier problema antes de que afecte la funcionalidad existente.