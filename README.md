# 🧬 HGNC Database Manager

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![SQLite](https://img.shields.io/badge/SQLite-Database-green)
![Pytest](https://img.shields.io/badge/Tested%20with-Pytest-success)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-red)

A lightweight data pipeline and query engine for managing HGNC gene data using Python and SQLite.

---

## 🎯 Problem Statement

The HGNC (HUGO Gene Nomenclature Committee) dataset contains thousands of gene records with multiple aliases, accession numbers, and enzyme classifications.

Working directly with raw TSV files makes searching, filtering, and managing gene information inefficient.

This project solves that problem by transforming raw HGNC data into a normalized SQLite database and providing a simple Python interface for querying gene information.

---

## 📖 Project Overview

The application automatically:

- Downloads the latest HGNC dataset
- Extracts and cleans relevant gene information
- Normalizes multi-valued fields into relational tables
- Stores structured data in SQLite
- Provides reusable query methods for retrieving gene records
- Validates outputs using Pydantic models

The result is a lightweight and efficient local database that enables fast gene lookups without repeatedly processing large raw datasets.

---

## ✨ Key Features

- Automated HGNC data download
- SQLite-based gene database
- Data normalization for multi-valued fields
- Parameterized SQL queries
- Pydantic-based schema validation
- Modular and reusable architecture
- Automated testing with Pytest

---

## 🛠 Technologies

| Category | Technology |
|-----------|------------|
| Language | Python |
| Database | SQLite |
| Data Processing | Pandas |
| Validation | Pydantic |
| Data Retrieval | Requests |
| Testing | Pytest |

---

## 🚀 Example Usage

```python
from hgnc.db import DbManager, DbQuery

db = DbManager()
db.import_data_to_db()

query = DbQuery()

results = query.filter_accession_enzyme(
    acc_value="NM_%",
    enz_value="%kinase%"
)

print(results)
```

---

## 🧪 Testing

Run the test suite:

```bash
pytest
```


## 👨‍💻 Author

Faiza

