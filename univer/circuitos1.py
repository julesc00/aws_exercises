def calculate_potencial_difference(I, R1, R2, R3):
    """
    Ejercicio 1
    Calcular el valor de la diferencia de potencial VF de la fuente usando la ley de Ohm.

    I = 0.3 Corriente en amperios
    R1 = 470 Resistencia R1 en ohmios
    R2 = 470 Resistencia R2 en ohmios
    R3 = 100 Resistencia R3 en ohmios
    """
    r_total = R1 + R2 + R3
    v_f = round(I * r_total, 2)
    return v_f


def calculate_electric_flux(V, R1, R2, R3):
    """
    Ejercicio 2
    Calcular el valor del flujo eléctrico I f de la fuente usando la ley de Ohm

    V = 19 Voltaje en voltios
    R1 = 2100 Resistencia R1 en ohmios
    R2 = 590 Resistencia R2 en ohmios
    R3 = 100 Resistencia R3 en ohmios
    """
    r_eq_inverse = (1 / R1) + (1 / R2) + (1 / R3)
    r_eq = round(1 / r_eq_inverse, 2)

    # Cálculo de la corriente total usando la ley de Ohm
    i_f = round(V / r_eq, 2)
    return r_eq, i_f


def calculate_electric_voltage(I, R1, R2, R3, V2):
    """
    Ejercicio 3

    I = 0.14 Corriente en amperios
    R1 = 3000 Resistencia R1 en ohmios
    R2 = 0 R2 no se necesita para calcular Vf ya que se tiene el voltaje a través de él
    R3 = 1500 Resistencia R3 en ohmios
    V2 = 10 Voltaje a través de R2 en voltios
    """

    # Cálculo de la resistencia total en un circuito serie
    # R2 no se incluye en el cálculo de la resistencia total porque ya se tiene el voltaje a través de él
    r_total = R1 + R3

    # Cálculo del voltaje de la fuente usando la ley de Ohm
    v_f = I * r_total

    # Cálculo de las potencias eléctricas para cada resistor
    # P2 se calcula con el voltaje conocido a través de R2
    # P2 = V2**2 / R2 Esto no se puede calcular directamente sin R2

    # Calculamos los voltajes a través de R1 y R3 usando la ley de Ohm
    V1 = I * R1
    V3 = I * R3

    # Ahora calculamos las potencias para P1 y P3
    P1 = V1**2 / R1
    P3 = V3**2 / R3

    return v_f, P1, P3, V1, V3


if __name__ == "__main__":
    print(calculate_potencial_difference(0.3, 47, 470, 1000))
    print(calculate_electric_flux(19, 2100, 590, 100))
    print(calculate_electric_voltage(0.1, 300, 0, 150, 10))
