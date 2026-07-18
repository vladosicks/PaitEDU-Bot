from app.ui.theme import HEADER
from app.ui.progress import progress


def tutorial_template(page: int, title: str, text: str):

    return (
        f"{HEADER}\n\n"

        f"📖 <b>Інструкція {page}/5</b>\n\n"

        f"{progress(page)}\n\n"

        f"{title}\n\n"

        f"{text}"
    )