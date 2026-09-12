from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

INPUT_DIR = DATA_DIR / "input"

PROCESSED_DIR = DATA_DIR / "processed"

EXCEPTIONS_DIR = DATA_DIR / "exceptions"

REPORTS_DIR = BASE_DIR / "reports"

LOGS_DIR = BASE_DIR / "logs"


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".csv",
    ".xlsx",
    ".docx"
}


def create_directories():

    folders = [
        INPUT_DIR,
        PROCESSED_DIR,
        EXCEPTIONS_DIR,
        REPORTS_DIR,
        LOGS_DIR
    ]

    for folder in folders:

        folder.mkdir(
            parents=True,
            exist_ok=True
        )


create_directories()