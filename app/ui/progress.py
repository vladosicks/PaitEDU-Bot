from app.utils.constants import *

def build_progress(status: str, payment_status: str, price_status: str) -> str:
    steps = [
        ("🟢", "Заявка створена"),
        (
            "🟢" if price_status == PRICE_ACCEPTED else "⚪",
            "Ціну погоджено"
        ),
        (
            "🟢" if payment_status == PAYMENT_PAID else "⚪",
            "Оплачено"
        ),
        (
            "🟡" if status == STATUS_WORK else "⚪",
            "Виконується"
        ),
        (
            "✅" if status in [STATUS_DONE, STATUS_ARCHIVE] else "⚪",
            "Готово"
        ),
    ]

    text = "📊 <b>Прогрес</b>\n\n"

    for icon, name in steps:
        text += f"{icon} {name}\n"

    return text


def progress(current: int, total: int = 5) -> str:
    """
    Генерує прогрес-бар.

    progress(3)

    🟦🟦🟦⬜⬜
    """

    return "🟦" * current + "⬜" * (total - current)