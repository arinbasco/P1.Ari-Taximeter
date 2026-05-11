from taximeter import calculate_fare, taximeter
import pytest

@pytest.mark.parametrize("seconds_stopped, seconds_moving, expected", [
    (100, 0, 2),
    (0, 20, 1),
    (10, 360, 18.2),
])
def test_calculate_fare(seconds_stopped, seconds_moving, expected):
    assert calculate_fare(seconds_stopped, seconds_moving) == expected

def test_viaje_basico(mocker):
    mocker.patch("builtins.input", side_effect=["a", "d", "f"])
    mocker.patch("time.time", return_value=0)
    taximeter()
    assert calculate_fare(0, 0) == 0.0

def test_iniciar_viaje_ya_activo(mocker):  # Verifica que A no inicia un segundo viaje si ya hay uno activo
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["a", "a", "f"])
    mocker.patch("time.time", return_value=0)
    taximeter()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("Viaje en progreso" in s for s in printed)

def test_finalizar_sin_viaje_activo(mocker):  # Verifica que D avisa si se intenta finalizar sin viaje activo
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["d", "f"])
    taximeter()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("No hay un viaje activo" in s for s in printed)

def test_detener_sin_viaje_activo(mocker):  # Verifica que B avisa si se intenta detener sin viaje activo
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["b", "f"])
    taximeter()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("No hay un viaje activo" in s for s in printed)

def test_comando_invalido(mocker):  # Verifica que un comando desconocido muestra el mensaje de error apropiado
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["x", "f"])
    taximeter()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("Comando no reconocido" in s for s in printed)

def test_nuevo_viaje_con_activo(mocker):  # Verifica que E avisa si hay un viaje en curso
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["a", "e", "f"])
    mocker.patch("time.time", return_value=0)
    taximeter()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("Viaje en curso" in s for s in printed)

def test_comando_e_resetea_contadores(mocker):  # Verifica que E tras finalizar un viaje resetea los contadores
    mock_print = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["a", "d", "e", "a", "d", "f"])
    # primer viaje: a→0,0 | d→10,10 | segundo viaje: a→10,10 | d→10,10
    mocker.patch("time.time", side_effect=[0, 0, 10, 10, 10, 10, 10, 10])
    taximeter()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("€0.00" in s for s in printed)

def test_viaje_multiples_detenciones(mocker):  # Verifica que el taxímetro acumula correctamente tiempos con varios tramos de parada y movimiento
    mock_print = mocker.patch("builtins.print")
    # "a": 2 llamadas (start_time, state_start_time)
    # "b","c","b","c": 2 llamadas cada uno (duration, nuevo state_start_time)
    # "d": 2 llamadas (duration, total_duration)
    mocker.patch("time.time", side_effect=[0, 0, 10, 10, 30, 30, 50, 50, 70, 70, 100, 100])
    mocker.patch("builtins.input", side_effect=["a", "b", "c", "b", "c", "d", "f"])
    taximeter()
    printed = [str(c) for c in mock_print.call_args_list]
    assert any("Viaje finalizado" in s for s in printed)
    # moving: 10s(a→b) + 20s(c→b) + 30s(c→d) = 60s | stopped: 20s(b→c) + 20s(b→c) = 40s → €3.80
    assert any(f"€{calculate_fare(40, 60):.2f}" in s for s in printed)
