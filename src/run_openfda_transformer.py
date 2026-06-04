import json
from transformations.openfda_transformer import transform_openfda

FILE_PATH = "/home/newdi91/pharma-safety-lakehouse/data/raw/openfda/2026/06/03/openfda_132107_fd4989ebb855425794a12a0812128a9e.json"


def main():

    with open(FILE_PATH, "r") as f:
        payload = json.load(f)   

    rows = transform_openfda(payload)

    print("ROWS GENERATED:", len(rows))
    
    print(rows[:2])


if __name__ == "__main__":
    main()