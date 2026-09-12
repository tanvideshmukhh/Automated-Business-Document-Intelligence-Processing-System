import os
import shutil
import json
from datetime import datetime

from src.classifier import classify_document
from src.extractors import extract_content
from src.cleaners import clean_record
from src.validators import validate_document
from src.duplicate_detector import calculate_file_hash


# Project folders
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_DIR = os.path.join(BASE_DIR, "data", "input")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
EXCEPTIONS_DIR = os.path.join(BASE_DIR, "data", "exceptions")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
LOGS_DIR = os.path.join(BASE_DIR, "logs")


def create_folders():
    """Create required project folders."""

    folders = [
        INPUT_DIR,
        PROCESSED_DIR,
        EXCEPTIONS_DIR,
        REPORTS_DIR,
        LOGS_DIR
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)


def log_message(message):
    """Write processing information into log file."""

    log_file = os.path.join(LOGS_DIR, "processing.log")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def parse_fields(document_type, text):
    """
    Extract important fields from document text.
    This is a simple rule-based approach.
    """

    record = {
        "document_type": document_type,
        "vendor_name": "",
        "invoice_number": "",
        "invoice_date": "",
        "due_date": "",
        "currency": "",
        "subtotal": "",
        "tax_amount": "",
        "total_amount": "",
        "po_number": "",
        "payment_status": "",
        "department": "",
        "employee_name": "",
        "amount": "",
        "category": "",
        "raw_text": text
    }

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip().lower().replace(" ","_")
        value = value.strip()

        if key == "vendor name":
            record["vendor_name"] = value

        elif key == "invoice number":
            record["invoice_number"] = value

        elif key == "invoice date":
            record["invoice_date"] = value

        elif key == "due date":
            record["due_date"] = value

        elif key == "currency":
            record["currency"] = value

        elif key == "subtotal":
            record["subtotal"] = value

        elif key == "tax amount":
            record["tax_amount"] = value

        elif key == "total amount":
            record["total_amount"] = value

        elif key == "po number":
            record["po_number"] = value

        elif key == "payment status":
            record["payment_status"] = value

        elif key == "department":
            record["department"] = value

        elif key == "employee name":
            record["employee_name"] = value

        elif key == "amount":
            record["amount"] = value

        elif key == "category":
            record["category"] = value

    return record


def process_file(file_path):
    """Process one document."""

    filename = os.path.basename(file_path)

    try:
        print(f"\nProcessing: {filename}")

        # ------------------------------------------------
        # 1. Calculate file hash
        # ------------------------------------------------

        file_hash = calculate_file_hash(file_path)

        # ------------------------------------------------
        # 2. Classify document
        # ------------------------------------------------

        document_type = classify_document(filename)

        print(f"Document Type: {document_type}")

        # ------------------------------------------------
        # 3. Extract content
        # ------------------------------------------------

        text = extract_content(file_path)

        # ------------------------------------------------
        # 4. Parse fields
        # ------------------------------------------------

        record = parse_fields(document_type, text)

        # ------------------------------------------------
        # 5. Clean / normalize data
        # ------------------------------------------------

        record = clean_record(record)

        # ------------------------------------------------
        # 6. Validate
        # ------------------------------------------------

        validation_result = validate_document(
            document_type,
            record
        )

        # ------------------------------------------------
        # 7. Add processing information
        # ------------------------------------------------

        record["filename"] = filename
        record["file_hash"] = file_hash
        record["validation_result"] = validation_result
        record["processed_at"] = datetime.now().isoformat()

        # ------------------------------------------------
        # 8. Decide processed or exception
        # ------------------------------------------------

        if validation_result["valid"]:

            destination = os.path.join(
                PROCESSED_DIR,
                filename
            )

            shutil.copy2(file_path, destination)

            print("Status: SUCCESS")

            log_message(
                f"{filename} processed successfully as {document_type}"
            )

        else:

            destination = os.path.join(
                EXCEPTIONS_DIR,
                filename
            )

            shutil.copy2(file_path, destination)

            print("Status: EXCEPTION")

            log_message(
                f"{filename} moved to exception queue: "
                f"{validation_result['errors']}"
            )

        # ------------------------------------------------
        # 9. Save JSON record
        # ------------------------------------------------

        json_filename = os.path.splitext(filename)[0] + ".json"

        json_path = os.path.join(
            REPORTS_DIR,
            json_filename
        )

        with open(json_path, "w", encoding="utf-8") as file:
            json.dump(
                record,
                file,
                indent=4,
                ensure_ascii=False,
                default=str
            )

        return record

    except Exception as error:

        print(f"ERROR: {error}")

        log_message(
            f"{filename} processing failed: {error}"
        )

        # Copy failed file to exception folder
        try:
            destination = os.path.join(
                EXCEPTIONS_DIR,
                filename
            )

            shutil.copy2(file_path, destination)

        except Exception:
            pass

        return None


def process_batch():
    """Process all files from input folder."""

    create_folders()

    files = os.listdir(INPUT_DIR)

    supported_extensions = (
        ".pdf",
        ".docx",
        ".xlsx",
        ".csv"
    )

    files = [
        file for file in files
        if file.lower().endswith(supported_extensions)
    ]

    if not files:

        print("No supported files found in data/input.")

        return

    print("\n====================================")
    print("DOCUMENT PROCESSING STARTED")
    print("====================================")

    successful = 0
    failed = 0

    for filename in files:

        file_path = os.path.join(
            INPUT_DIR,
            filename
        )

        result = process_file(file_path)

        if result is not None:
            successful += 1
        else:
            failed += 1

    print("\n====================================")
    print("BATCH PROCESSING COMPLETED")
    print("====================================")

    print(f"Total Files : {len(files)}")
    print(f"Successful  : {successful}")
    print(f"Failed      : {failed}")

    log_message(
        f"Batch completed. Total={len(files)}, "
        f"Successful={successful}, Failed={failed}"
    )


if __name__ == "__main__":

    process_batch()