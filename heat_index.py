def calculate_heat_index(temp_c: float, humidity: float) -> dict:
    """
    Calculate heat index using the Steadman formula.
    Inputs: temperature in Celsius, relative humidity (0-100).
    Returns: heat index in Celsius and Fahrenheit.
    """
    # Convert to Fahrenheit for the Steadman formula
    T = temp_c * 9 / 5 + 32
    R = humidity

    HI = (
        -42.379
        + 2.04901523 * T
        + 10.14333127 * R
        - 0.22475541 * T * R
        - 0.00683783 * T * T
        - 0.05481717 * R * R
        + 0.00122874 * T * T * R
        + 0.00085282 * T * R * R
        - 0.00000199 * T * T * R * R
    )

    # Convert back to Celsius
    hi_celsius = (HI - 32) * 5 / 9

    return {
        "heat_index_c": round(hi_celsius, 1),
        "heat_index_f": round(HI, 1),
        "temperature_c": temp_c,
        "humidity": humidity,
    }
