from decimal import Decimal

from currency_converter import CurrencyConverter


FIXED_DAILY_PAY = 250  # USD


def get_total_monthly_income(daily_rate: int = FIXED_DAILY_PAY) -> Decimal:
    total_hours = get_total_monthly_hours()
    hourly_rate = Decimal(daily_rate / 8)
    print(f"""
        Dollar vs Peso: ${CurrencyConverter().convert(1, "USD", "MXN"):,}
        Costo por Hora en dólares: ${hourly_rate:,}
        Total de horas mensual: {total_hours}
        Facturar por: ${total_hours * hourly_rate:,}
        Pay in Mexican Pesos: ${CurrencyConverter().convert(total_hours * hourly_rate, "USD", "MXN"):,}
    """)
    return Decimal(total_hours * hourly_rate)


def get_total_monthly_hours() -> Decimal:
    """
    Calculate the total monthly hours worked based on a fixed daily rate.
    Assuming 22 working days in a month.
    """
    week1 = Decimal(5 * 8)
    week2 = Decimal(5 * 8.5 + 2)  # Oncall, daily 8.5 hours + 2 for Saturday and Sunday
    week3 = Decimal(5 * 8 + 1.5)  # Oncall covered Diego Mon-Wed
    week4 = Decimal(5 * 8.5 + 2)
    week5 = Decimal(8)
    return week1 + week2 + week3 + week4 + week5


if __name__ == '__main__':
    print(get_total_monthly_income())
