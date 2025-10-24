# Advanced Testing for Data Workflows – Week 3 (ShopLink Case Study)

### Repository: [de-week3-advancedtesting-Salome](https://github.com/Sallie25/de-week3-advancedtesting-Salome.git)

---

##  Project Overview

This project simulates my first data engineering task at **ShopLink**, a fast-growing online marketplace.
As part of the **Data Quality Engineering team**, my mission is to ensure that the **sales data pipeline** is bulletproof — meaning it validates, transforms, and analyzes data accurately while gracefully handling bad or unexpected input.

I am responsible for **testing every stage** of the pipeline to guarantee correctness, consistency, and reliability before it powers ShopLink’s analytics dashboards.

---

##  Objectives

By completing this project, I aim to:

* Understand the role of **testing** in building **data workflows**.
* Write **unit tests** using **pytest** and **fixtures** for modular pipeline components.
* Validate, normalize, and transform messy data.
* Handle **edge cases** like:

  * Negative values
  * Mixed currencies (₦, $, text amounts)
  * Inconsistent payment statuses
  * Missing or malformed fields
* Apply **Object-Oriented Design (OOP)** for cleaner and testable code.
* Ensure that the **final output** is accurate, reproducible, and consistent.

---

##  Background

> “We need to make sure our sales pipeline is reliable and produces correct results. We can’t afford hidden bugs or faulty transformations.” — *ShopLink Manager*

Although the provided order data is “clean” in structure, it may still include **logic-level inconsistencies**:

* Out-of-range or negative values
* Non-standard currency formats (`N2500`, `$35`, `45 dollars`)
* Mixed text casing for payment statuses (`Paid`, `pending`, `REFUND`)
* Missing fields or mismatched totals

My task is to test and harden the pipeline so that such data issues **don’t silently break** the analytics.

---

##  Pipeline Architecture

The workflow consists of **five modular components**, each with its own unit tests and a final integration test.

```
order_pipeline/
    __init__.py
    reader.py
    validator.py
    transformer.py
    analyzer.py
    exporter.py
    pipeline.py
tests/
    __init__.py
    test_reader.py
    test_validator.py
    test_transformer.py
    test_analyzer.py
    test_exporter.py
    test_pipeline_integration.py
```

---

##  Component Descriptions

### 1. **Reader**

* Reads JSON data from a file.
* Returns a list of dictionaries.
* Raises `ValueError` for unsupported formats or empty files.

### 2. **Validator**

* Verifies all required fields:

  * `order_id`, `timestamp`, `item`, `quantity`, `price`, `payment_status`, `total`
* Rejects invalid or incomplete rows.
* Handles missing optional fields gracefully.

### 3. **Transformer**

* Converts numeric fields to correct types.
* Normalizes payment statuses (`paid`, `pending`, `refunded`).
* Cleans text and trims extra spaces.
* Recalculates `total = quantity * price`.
* Handles currency normalization via **regular expressions**.

### 4. **Analyzer**

* Computes:

  * **Total revenue**
  * **Average revenue per order**
  * **Count by payment status** (paid, pending, refunded)

### 5. **Exporter**

* Writes final processed data to `shoplink_cleaned.json`.
* Ensures successful file creation and proper JSON formatting.

---

##  Testing Strategy

Testing is central to this project.
Each component includes **unit tests** and a final **integration test** that runs the full pipeline.

###  Unit Test Coverage

| Component       | Focus             | Expected Behavior                                |
| --------------- | ----------------- | ------------------------------------------------ |
| **Reader**      | File handling     | Reads valid JSON, raises error for invalid input |
| **Validator**   | Field validation  | Rejects missing or invalid fields                |
| **Transformer** | Data consistency  | Correctly converts and recalculates fields       |
| **Analyzer**    | Calculations      | Computes accurate totals and averages            |
| **Exporter**    | Output validation | Writes valid JSON file successfully              |
| **Pipeline**    | Integration       | Ensures all stages work together correctly       |

###  Coverage Requirement

I ensure at least **60% test coverage** per module using:

```bash
pytest --cov=order_pipeline
```

---

##  Folder Structure

```
de-week3-advancedtesting-Salome/
│
├── order_pipeline/
│   ├── __init__.py
│   ├── reader.py
│   ├── validator.py
│   ├── transformer.py
│   ├── analyzer.py
│   ├── exporter.py
│   └── pipeline.py
│
├── tests/
│   ├── __init__.py
│   ├── test_reader.py
│   ├── test_validator.py
│   ├── test_transformer.py
│   ├── test_analyzer.py
│   ├── test_exporter.py
│   └── test_pipeline_integration.py
│
├── data/
│   ├── shoplink.json
│   └── shoplink_cleaned.json
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

##  Setup & Installation

### 1. Clone Repository

```bash
git clone https://github.com/Sallie25/de-week3-advancedtesting-Salome.git
cd de-week3-advancedtesting-Salome
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run All Tests

```bash
pytest
```

### 5. Run with Coverage

```bash
pytest --cov=order_pipeline
```

---

##  Running the Pipeline

To execute the full workflow:

```bash
python -m order_pipeline.pipeline
```

Expected result:

* Reads data from `shoplink.json`
* Validates, transforms, and analyzes data
* Exports clean results to `shoplink_cleaned.json`

---

##  Tools & Dependencies

| Tool             | Purpose                                     |
| ---------------- | ------------------------------------------- |
| **Python 3.10+** | Core language                               |
| **pytest**       | Testing framework                           |
| **pytest-cov**   | Test coverage analysis                      |
| **json, re, os** | Data reading, regex cleaning, file handling |

---

##  .gitignore

```
__pycache__/
*.pyc
.venv/
*.json
.env
```

---

##  Submission Format

```
Week 3 — AdvancedTesting — Salome — https://github.com/Sallie25/de-week3-advancedtesting-Salome.git
```



---

## Notes

I made use of **Regular Expressions (`re` module)** to clean numeric fields and handle currency variations effectively.

---

## 👩 Author

**Name:** Salome Akpan
**GitHub:** [Sallie25](https://github.com/Sallie25)
**Project:** Week 3 — Advanced Testing for Data Workflows
**Organization:** Data Epic Beginners with Experience Program

---

