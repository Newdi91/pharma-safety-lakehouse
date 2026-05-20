from ingestion.openfda_client import OpenFDAClient


def main():

    
    client = OpenFDAClient(timeout=10)
    
    limit = 10
   
    data = client.get_adverse_events(limit=limit)

   
    if not data or "results" not in data:
        print("Ingestion failed: invalid response")
        return

    # 5. output di controllo
    print("Ingestion completed successfully")
    print(f"Records fetched: {len(data['results'])}")


if __name__ == "__main__":
    main()