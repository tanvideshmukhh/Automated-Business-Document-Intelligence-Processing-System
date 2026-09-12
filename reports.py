import csv
import json
from pathlib import Path
from datetime import datetime

from .config import REPORTS_DIR


def generate_csv_report(records, filename="document_report.csv"):

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    output_file = REPORTS_DIR / filename

    if not records:
        print("No records available for CSV report")
        return output_file

    fieldnames = set()

    for record in records:
        fieldnames.update(record.keys())

    fieldnames = sorted(fieldnames)

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(records)

    print("CSV report generated successfully")

    print(output_file)

    return output_file


def generate_json_report(
    records,
    filename="document_report.json"
):

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    output_file = REPORTS_DIR / filename

    report_data = {
        "generated_at": datetime.now().isoformat(),
        "total_records": len(records),
        "records": records
    }

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report_data,
            file,
            indent=4,
            default=str
        )

    print("JSON report generated successfully")

    print(output_file)

    return output_file


def generate_summary_report(records):

    total_documents = len(records)

    successful_documents = 0

    failed_documents = 0

    document_types = {}

    for record in records:

        status = str(
            record.get("status", "")
        ).lower()

        document_type = record.get(
            "document_type",
            "unknown"
        )

        document_types[document_type] = (
            document_types.get(document_type, 0) + 1
        )

        if status in ["success", "successful", "processed"]:

            successful_documents += 1

        elif status in ["failed", "error", "exception"]:

            failed_documents += 1

    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_documents": total_documents,
        "successful_documents": successful_documents,
        "failed_documents": failed_documents,
        "document_types": document_types
    }

    output_file = REPORTS_DIR / "summary_report.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=4
        )

    print("Summary report generated successfully")

    print(output_file)

    return output_file


if __name__ == "__main__":
    print("Reports module started")

    sample_records = [
        {
            "document_id": "INV001",
            "document_type": "invoice",
            "vendor": "ABC Company",
            "amount": 1500,
            "status": "success"
        },
        {
            "document_id": "INV002",
            "document_type": "invoice",
            "vendor": "XYZ Company",
            "amount": 2500,
            "status": "failed"
        }
    ]

    generate_csv_report(sample_records)
    generate_json_report(sample_records)
    generate_summary_report(sample_records)

    print("Reports module tested successfully")
    print("REPORTS FILE RUNNING")