"""Import modules."""

import os
from hgnc.manager import DbEntry, DbManager, DbQuery
from hgnc.constants import (
    URL,
    DATABASE_PATH,
    DOWNLOAD_FILE_PATH,
    TABLE_NAME,
    HOME,
)


class TestConstants:
    """Tests that constants value are correct"""

    def test_url_constant(self) -> None:
        """Checks if the URL constant matches the HGNC link"""
        url = URL
        assert (
            url
            == "https://www.genenames.org/cgi-bin/download/custom?col=gd_hgnc_id&col=gd_app_sym&col=gd_app_name&col=gd_aliases&col=gd_pub_chrom_map&col=gd_pub_acc_ids&col=gd_enz_ids&status=Approved&status=Entry%20Withdrawn&hgnc_dbtag=on&order_by=gd_app_sym_sort&format=text&submit=submit"
        )

    def test_table_name(self) -> None:
        """Checks if Table name constant is set correctly"""
        name = TABLE_NAME
        assert name == "hgnc"


class TestDbManager:
    """Different Tests to check if the DbManager is working correctly"""

    def test_setup_db_manager(self) -> None:
        """Checks if DbManager initialises and showing correct path"""
        dbm = DbManager(db_path=DATABASE_PATH)
        path = os.path.join(HOME, ".hgnc", "hgnc.db")
        assert dbm.__repr__() == f"<DB: {path}>"

    def test_download(self) -> None:
        """Checks if _download_data actually download the file"""
        if os.path.exists(path=DOWNLOAD_FILE_PATH):
            os.remove(path=DOWNLOAD_FILE_PATH)
        dbm = DbManager(db_path=DATABASE_PATH)
        dbm._download_data(DOWNLOAD_FILE_PATH)
        assert os.path.exists(path=DOWNLOAD_FILE_PATH)

    def test_import_data(self) -> None:
        """Checks if import_data_to_db creates the database file"""
        if os.path.exists(path=DATABASE_PATH):
            os.remove(path=DATABASE_PATH)
        dbm = DbManager(db_path=DATABASE_PATH)
        dbm.import_data_to_db()
        assert os.path.exists(path=DATABASE_PATH)


class TestDbQuery:
    """Tests for getting data from the HGNC databse"""

    def test_filter_accession_enzyme(self) -> None:
        """test_filter_accession_enzyme Check that the corresponding list of DbEntry
        results are retrieved for the input accession_number and enzyme.
        """
        DbManager(db_path=DATABASE_PATH)
        dbq = DbQuery(db_path=DATABASE_PATH)
        result = dbq.filter_accession_enzyme(acc_value="L32179", enz_value="3.1.1.3")
        assert result == [
            DbEntry(
                id=17,
                approved_symbol="AADAC",
                approved_name="arylacetamide deacetylase",
                alias_symbol="CES5A1",
                chromosome="3q25.1",
                accession_number="L32179",
                enzyme="3.1.1.3",
            ),
            DbEntry(
                id=17,
                approved_symbol="AADAC",
                approved_name="arylacetamide deacetylase",
                alias_symbol="DAC",
                chromosome="3q25.1",
                accession_number="L32179",
                enzyme="3.1.1.3",
            ),
        ]
