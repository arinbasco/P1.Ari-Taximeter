from taximeter import Taximeter
import pytest

@pytest.mark.parametrize("seconds_stopped, seconds_moving, expected", [
    (100, 0, 2),
    (0, 20, 1),
    (10, 360, 18.2),
])
def test_calculate_fare(seconds_stopped, seconds_moving, expected):
    taxi = Taximeter()
    taxi.stopped_time = seconds_stopped
    taxi.moving_time = seconds_moving
    assert taxi.calculate_fare() == expected

def test_viaje_basico(mocker):
    mocker.patch("builtins.input", side_effect=["a", "d", "f"])
    mocker.patch("time.time", return_value=0)
    taxi = Taximeter()
    taxi.run()
    assert taxi.calculate_fare() == 0.0

def test_iniciar_viaje_ya_activo(mocker):  # Verifica que A no inicia un segundo viaje si ya hay uno activo
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["a", "a", "d", "f"])
    mocker.patch("time.time", return_value=0)
    taxi = Taximeter()
    taxi.run()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("Viaje en progreso" in s for s in printed)

def test_finalizar_sin_viaje_activo(mocker):  # Verifica que D avisa si se intenta finalizar sin viaje activo
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["d", "f"])
    taxi = Taximeter()
    taxi.run()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("No hay un viaje activo" in s for s in printed)

def test_detener_sin_viaje_activo(mocker):  # Verifica que B avisa si se intenta detener sin viaje activo
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["b","d","f"])
    taxi = Taximeter()
    taxi.run()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("No hay un viaje activo" in s for s in printed)

def test_comando_invalido(mocker):  # Verifica que un comando desconocido muestra el mensaje de error apropiado
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["x","d", "f"])
    taxi = Taximeter()
    taxi.run()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("Comando no reconocido" in s for s in printed)

def test_nuevo_viaje_con_activo(mocker):  # Verifica que E avisa si hay un viaje en curso
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["a", "e", "d", "f"])
    mocker.patch("time.time", return_value=0)
    taxi = Taximeter()
    taxi.run()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("Viaje en curso" in s for s in printed)

def test_comando_e_resetea_contadores(mocker):  # Verifica que E tras finalizar un viaje resetea los contadores
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["a", "d", "e", "a", "d", "f"])
    mocker.patch("time.time", side_effect=[0, 0, 10, 10, 10, 10, 10, 10])
    taxi = Taximeter()
    taxi.run()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("€0.00" in s for s in printed)

def test_viaje_multiples_detenciones(mocker):  # Verifica que el taxímetro acumula correctamente tiempos con varios tramos de parada y movimiento
    mock_print = mocker.patch("builtins.print")
    mocker.patch("time.time", side_effect=[0, 0, 10, 10, 30, 30, 50, 50, 70, 70, 100, 100])
    mocker.patch("builtins.input", side_effect=["a", "b", "c", "b", "c", "d", "f"])
    taxi = Taximeter()
    taxi.run()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("Viaje finalizado" in s for s in printed)
    assert any("€3.80" in s for s in printed)


def test_C_durante_A_activo(mocker):  # Verifica que c no inicia si el estado actual es == moving
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["a", "c", "d","f"])
    mocker.patch("time.time", return_value=0)
    taxi = Taximeter()
    taxi.run()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("Viaje en progreso. Para detenerlo ingrese B. Si desea finalizarlo ingrese D" in s for s in printed)

def test_b_durante_viaje_detenido(mocker):  # Verifica que b no inicia si el estado actual es == stopped
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["a", "b", "b", "d","f"])
    mocker.patch("time.time", return_value=0)
    taxi = Taximeter()
    taxi.run()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("El viaje esta detenido. Por favor ingrese el comando C para retomarlo o D para finalizar" in s for s in printed)


def test_configurar_tarifas(mocker):  # Verifica que T actualiza las tarifas cuando se confirma con 1
    mock_print = mocker.patch("builtins.print")
    mocker.patch("taximeter.Taximeter.load_rates", return_value=(0.02, 0.05))
    mocker.patch("builtins.open", mocker.mock_open())
    mocker.patch("builtins.input", side_effect=["t", "0.03", "0.06", "1", "f"])
    taxi = Taximeter()
    taxi.run()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("Tarifas actualizadas correctamente" in s for s in printed)
