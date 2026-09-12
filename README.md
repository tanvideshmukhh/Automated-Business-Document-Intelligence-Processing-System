# VESA Project 3 - Document Processing System

## Project Description

This project is a Document Processing System developed using Python.

The system processes documents automatically and performs:

- Document classification
- Data extraction
- Data cleaning
- Data validation
- Duplicate detection
- Batch processing
- Exception handling
- Report generation

## Project Structure

VESA_Project3/

data/
- input/       - Stores input documents
- processed/   - Stores successfully processed documents
- exceptions/  - Stores documents with processing errors

src/
- _init_.py
- config.py
- classifier.py
- cleaners.py
- validators.py
- extractors.py
- duplicate_detector.py
- processor.py
- reports.py

reports/
- document_report.csv
- document_report.json
- summary_report.json

## Features

### 1. Document Classification
The system identifies and classifies input documents.

### 2. Data Extraction
Important information is extracted from the document.

### 3. Data Cleaning
Extracted data is cleaned before processing.

### 4. Data Validation
The extracted information is validated.

### 5. Duplicate Detection
The system checks for duplicate documents.

### 6. Batch Processing
Multiple documents can be processed automatically.

### 7. Exception Handling
Documents with errors can be handled separately.

### 8. Report Generation
The system generates reports in CSV and JSON formats.

## How to Run the Project

Open the terminal in the project folder and run:

```powershell
python -m src.processor