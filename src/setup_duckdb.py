from pathlib import Path
import duckdb

db_path = Path("data/warehouse/pharma.duckdb")

db_path.parent.mkdir(parents=True, exist_ok=True)

conn = duckdb.connect(str(db_path))


conn.execute("DROP TABLE IF EXISTS drug_labels")

conn.execute("""
CREATE TABLE drug_labels (
    drug_name VARCHAR,
    manufacturer VARCHAR,
    indication VARCHAR,
    approval_year INTEGER
)
""")

conn.execute("""
INSERT INTO drug_labels VALUES
('Aspirin', 'Bayer', 'Pain relief', 1899),
('Ibuprofen', 'Advil', 'Inflammation', 1961),
('Paracetamol', 'Tylenol', 'Fever', 1955)
""")

conn.close()