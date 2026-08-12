"""
Query Tool for JobSentinel
Run SELECT statements against your PostgreSQL database
"""

from sqlalchemy import create_engine, text
from app.config import settings

def run_query(sql_query):
    """Execute a SELECT query and display results"""
    try:
        engine = create_engine(settings.database_url)
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            columns = result.keys()
            
            if not rows:
                print("No results found.")
                return
            
            # Print header
            print("\n" + "="*80)
            header = " | ".join([str(col).ljust(15) for col in columns])
            print(header)
            print("-"*80)
            
            # Print rows
            for row in rows:
                row_str = " | ".join([str(val).ljust(15) for val in row])
                print(row_str)
            
            print("="*80)
            print(f"Total rows: {len(rows)}\n")
            
    except Exception as e:
        print(f"Error executing query: {e}\n")

def main():
    """Interactive query tool"""
    print("\n" + "="*80)
    print("JobSentinel Query Tool - Run SELECT statements")
    print("="*80)
    print("Type 'exit' or 'quit' to close\n")
    
    while True:
        try:
            query = input("Enter SQL query: ").strip()
            
            if query.lower() in ['exit', 'quit']:
                print("Goodbye!\n")
                break
            
            if not query:
                continue
            
            # Simple validation - only allow SELECT
            if not query.upper().startswith('SELECT'):
                print("Only SELECT queries are allowed.\n")
                continue
            
            run_query(query)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!\n")
            break
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
