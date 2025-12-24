import psycopg2
from pathlib import Path
import csv
from datetime import datetime


def run_schema(cur):
    schema_sql = Path("schema.sql").read_text(encoding="utf-8")
    cur.execute(schema_sql)


def parse_date(s: str):
    s = (s or "").strip()
    if not s:
        return None
    # format in the CSV: YYYY/MM/DD
    return datetime.strptime(s, "%Y/%m/%d").date()

def clean_row(row: dict) -> dict:
    # strip whitespace from keys + values
    return {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}


def load_accounts(cur):
    path = Path("data/accounts.csv")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader: #for every row 
            r = clean_row(row)
            cur.execute(
                """
                INSERT INTO accounts
                (customer_id, first_name, last_name, address_1, address_2, city, state, zip_code, join_date)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (customer_id) DO NOTHING
                """,
                (
                    int(r["customer_id"]),
                    r["first_name"],
                    r["last_name"],
                    r["address_1"],
                    r["address_2"] or None,
                    r["city"],
                    r["state"],
                    r["zip_code"],
                    parse_date(r["join_date"]),
                )
            )

def load_products(cur):
    path = Path("data/products.csv")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader: #for every row 
            r = clean_row(row)
            cur.execute(
                """
                INSERT INTO products (product_id, product_code, product_description)
                VALUES (%s,%s,%s)
                ON CONFLICT (product_id) DO NOTHING
                """,
                (
                    int(r["product_id"]),
                    r["product_code"],            
                    r["product_description"],
                )
            )

def load_transactions(cur):
    path = Path("data/transactions.csv")
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader: #for every row 
            r = clean_row(row)
            cur.execute(
                """
                INSERT INTO transactions
                (transaction_id, transaction_date, product_id, product_code, product_description, quantity, account_id)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (transaction_id) DO NOTHING
                """,
                (
                    r["transaction_id"],    
                    parse_date(r["transaction_date"]),
                    int(r["product_id"]),
                    r["product_code"],
                    r["product_description"],
                    int(r["quantity"]),
                    int(r["account_id"]),
                )
            )

def main():
    host = "postgres"
    database = "postgres"
    user = "postgres"
    pas = "postgres"
    conn = psycopg2.connect(host=host, database=database, user=user, password=pas)
    
    # Initially to inspect the data: 
    """
    #1. Inspect the CSV:
    data_dir=Path("data")
    for csv_path in data_dir.glob("*.csv"):
        print("\n==============================")
        print("File:", csv_path.name)
        
        with open(csv_path, newline="",encoding="utf-8") as f:
            reader=csv.reader(f)
            header=next(reader)
            print("Columns: ", header)
            for i, row in zip(range(3), reader):
                print("Row", i+1, row)
    """

    cur = conn.cursor()
    
    run_schema(cur) #call the run schema function/ create tables
    conn.commit() #saves everything

    # ingest data
    load_accounts(cur)
    load_products(cur)
    load_transactions(cur)
    conn.commit()

    print("Tables created and data ingested successfully")

    #close cursor and connection
    cur.close()
    conn.close()



if __name__ == "__main__":
    main()
