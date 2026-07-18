from app.ui.theme import HEADER, DIVIDER, ICON_SUCCESS_CARD, ICON_INFO_CARD



def card(
    title: str,
    text: str,
    footer: str | None = None
) -> str:
    """
    Базова картка PaitEDU.

    title  -> заголовок картки
    text   -> основний текст
    footer -> текст внизу (необов'язковий)
    """

    message = (
        f"{HEADER}\n\n"
        f"{title}\n\n"
        f"{text}"
    )

    if footer:
        message += (
            f"\n\n"
            f"{DIVIDER}\n\n"
            f"{footer}"
        )

    return message

def success_card(
    title: str,
    text: str
) -> str:
    """
    Картка успішної дії.
    """

    return card(
        title=f"{ICON_SUCCESS_CARD} <b>{title}</b>",
        text=text,
        footer="💙 Дякуємо, що обрали <b>PaitEDU</b>"
    )

def info_card(
    title: str,
    text: str
) -> str:
    """
    Інформаційна картка.
    """

    return card(
        title=f"{ICON_INFO_CARD} <b>{title}</b>",
        text=text
    )

def order_card(
    order,
    status_name: str,
    payment_name: str,
    deadline: str,
    created: str,
    progress: str,
) -> str:
    return (
        f"""{HEADER}

📄 <b>Замовлення №{order.id}</b>

📚 <b>Послуга</b>
{order.service}

📌 <b>Статус</b>
{status_name}

💳 <b>Оплата</b>
{payment_name}

📅 <b>Дедлайн</b>
{deadline}

🕒 <b>Створено</b>
{created}

{DIVIDER}

📝 <b>Опис</b>

{progress}

{order.description}
"""
    )

from app.ui.theme import HEADER_V2, FOOTER_V2

def welcome_card_v2() -> str:

    body = """
Ласкаво просимо до <b>PaitEDU</b>.

Ми допомагаємо з:

📘 Курсовими роботами
🎓 Дипломними роботами
📄 Рефератами
📊 Презентаціями
🌐 Перекладами
"""

    return page_card(
        title="Вітаємо! 👋",
        body=body,
        footer="👇 <i>Оберіть потрібний розділ нижче.</i>",
    )

def page_card(
    title: str,
    body: str,
    footer: str | None = None,
) -> str:

    text = f"""{HEADER_V2}

<b>{title}</b>

{body}
"""

    if footer:
        text += f"""

{FOOTER_V2}

{footer}
"""

    return text