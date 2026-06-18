"""Import modules."""

import os

URL: str = "https://www.genenames.org/cgi-bin/download/custom?col=gd_hgnc_id&col=gd_app_sym&col=gd_app_name&col=gd_aliases&col=gd_pub_chrom_map&col=gd_pub_acc_ids&col=gd_enz_ids&status=Approved&status=Entry%20Withdrawn&hgnc_dbtag=on&order_by=gd_app_sym_sort&format=text&submit=submit"

HOME: str = os.path.expanduser("~")

DATA_DIR: str = os.path.join(HOME, ".hgnc")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DOWNLOAD_FILE_PATH: str = os.path.join(DATA_DIR, "hgnc.tsv")

DATABASE_PATH: str = os.path.join(DATA_DIR, "hgnc.db")

TABLE_NAME: str = "hgnc"

COLUMNS: dict[str, str] = {
    "HGNC ID": "id",
    "Approved symbol": "approved_symbol",
    "Approved name": "approved_name",
    "Alias symbols": "alias_symbols",
    "Chromosome": "chromosome",
    "Accession numbers": "accession_numbers",
    "Enzyme IDs": "enzymes",
}

EXPLODE_COLUMNS: dict[str, str] = {
    "alias_symbols": "alias_symbol",
    "accession_numbers": "accession_number",
    "enzymes": "enzyme",
}
