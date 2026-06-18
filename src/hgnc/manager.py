"""Modules for managing the HGNC database, including downloading data,
importing it into a SQLite database, and querying the database."""

import sqlite3
import os
import requests
import pandas as pd
from pydantic import BaseModel
from hgnc.constants import (
    URL,
    DATABASE_PATH,
    DOWNLOAD_FILE_PATH,
    TABLE_NAME,
    COLUMNS,
    EXPLODE_COLUMNS,
)


class DbEntry(BaseModel):
    """Pydantic model representing an entry in the HGNC database."""

    id: int
    approved_symbol: str
    approved_name: str
    alias_symbol: str | None
    chromosome: str | None
    accession_number: str | None
    enzyme: str | None


class DbManager:
    """ "Class for managing the SQLite database for the HGNC project."""

    def __init__(self, db_path: str | None = None) -> None:
        """Initializing the DB class with the db_path where it should be put

        Args:
            db_path (str | None): Path to where the db should be initialized
        """
        self.db_path: str = db_path if db_path else DATABASE_PATH

    def __repr__(self) -> str:
        """Return a readable string representation of the database manager.

        Returns:
            String showing the path to the managed database.
        """

        return f"<DB: {self.db_path}>"

    def _download_data(self, download_file_path: str = DOWNLOAD_FILE_PATH) -> None:
        """Download the HGNC data file if it does not already exist.

        Args:
            download_file_path: Path where the downloaded file should be saved.

        Returns:
            None
        """
        if os.path.exists(download_file_path):
            pass
        else:
            response = requests.get(url=URL, timeout=30)
            with open(file=download_file_path, mode="wb") as f:
                f.write(response.content)

    def import_data_to_db(self, download_file_path: str | None = None) -> None:
        """Download the HGNC file, load selected columns, and save them to SQLite.

        Args:
            download_file_path: Path to the downloaded HGNC file. If None, the
                default path from constants is used.

        Returns:
            None
        """
        download_file_path = (
            download_file_path if download_file_path else DOWNLOAD_FILE_PATH
        )
        self._download_data(download_file_path=download_file_path)

        con: sqlite3.Connection = sqlite3.connect(self.db_path)

        df = pd.read_csv(
            download_file_path,
            usecols=list(COLUMNS.keys()),
            index_col="HGNC ID",
            sep="\t",
        )
        df.rename(columns=COLUMNS, inplace=True)
        df.index.rename(name="id", inplace=True)
        df.index = df.index.str.split(":").str[1].astype(int)
        df.to_sql(name=TABLE_NAME, con=con, index_label="id", if_exists="replace")

        for column_name_plural, column_name_singular in EXPLODE_COLUMNS.items():
            df[column_name_singular] = df[column_name_plural].str.split(", ")
            df_column = df[column_name_singular].explode()
            df_column = df_column.to_frame()
            df_column.dropna(inplace=True)
            df_column["hgnc_id"] = df_column.index
            df_column.reset_index(drop=True, inplace=True)
            df_column.index += 1
            df_column.index.rename(name="id", inplace=True)
            df_column.to_sql(
                name=f"{column_name_singular}",
                con=con,
                index_label="id",
                if_exists="replace",
            )

    @property
    def number_rows_in_db(self) -> int:
        """Return the number of rows currently stored in the database table.

        Returns:
            Number of rows in the SQLite table.
        """
        with sqlite3.connect(database=self.db_path) as con:
            cur: sqlite3.Cursor = con.cursor()
            cur.execute(f"SELECT count(*) FROM {TABLE_NAME}")
            number_rows = cur.fetchone()[0]
        return number_rows


class DbQuery(DbManager):
    """Class for querying the HGNC SQLite database."""

    def __init__(self, db_path: str | None = None) -> None:
        """Initialize the query manager.

        Args:
            db_path: Path to the SQLite database file. If None, the default
                path from constants is used.
        """
        super().__init__(db_path=db_path)

    def filter_accession_enzyme(self, acc_value: str, enz_value: str) -> list[DbEntry]:
        """filter_accession_enzyme Filter by user input accession number and enzyme values.

        Args:
            acc_value (str): Accession number value
            enz_value (str): Enzyme value

        Returns:
            list[DbEntry]: List of DbEntry that correspond to the input accession number and enzyme
        """
        sql: str = f"""
            SELECT
                h.id,
                h.approved_symbol,
                h.approved_name,
                h.chromosome,
                a.accession_number,
                l.alias_symbol,
                e.enzyme
            FROM
                {TABLE_NAME} as h
                INNER JOIN accession_number AS a ON (a.hgnc_id=h.id)
                INNER JOIN alias_symbol AS l ON (l.hgnc_id=h.id)
                INNER JOIN enzyme AS e ON (e.hgnc_id=h.id)
            WHERE a.accession_number LIKE ? AND e.enzyme LIKE ?
            LIMIT 10
            """

        with sqlite3.connect(database=self.db_path) as con:
            con.row_factory = sqlite3.Row
            cursor: sqlite3.Cursor = con.cursor()
            cursor.execute(sql, (acc_value, enz_value))
            result = cursor.fetchall()
            entries = []
            if result:
                for row in result:
                    dict_row = dict(row)
                    entries.append(DbEntry(**dict_row))
            return entries
