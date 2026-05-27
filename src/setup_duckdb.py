import duckdb

conn = duckdb.connect("data/warehouse/pharma.duckdb")


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