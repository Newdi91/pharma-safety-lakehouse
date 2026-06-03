import json
from pprint import pprint

     
FILE_PATH = "data/raw/openfda/2026/06/03/openfda_132107_fd4989ebb855425794a12a0812128a9e.json"


def main():  
    with open(FILE_PATH, "r") as f:
        data = json.load(f)

    print("\n TOP-LEVEL KEYS")
    print(data.keys())

    
    payload = data["data"]

    print("\n PAYLOAD KEYS (data layer)")
    print(payload.keys())

    
    results = payload["results"]

    print("\n TYPE OF RESULTS")
    print(type(results))

    
    
    first_record = results[0]

    print("\n FIRST RECORD KEYS")
    print(sorted(first_record.keys()))

    
    if "patient" in first_record:
        print("\n PATIENT KEYS")
        print(sorted(first_record["patient"].keys()))

    
    print("\n FULL FIRST RECORD")
    pprint(first_record)

    

if __name__ == "__main__":
    main()
