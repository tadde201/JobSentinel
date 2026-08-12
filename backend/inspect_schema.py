from sqlalchemy import inspect, create_engine
from app.config import settings

engine = create_engine(settings.database_url)
inspector = inspect(engine)

# Get all table names
tables = inspector.get_table_names()
print(f"Total tables: {len(tables)}\n")

# For each table, show columns
for table_name in tables:
    print(f"Table: {table_name}")
    columns = inspector.get_columns(table_name)
    for col in columns:
        nullable = "NULL" if col['nullable'] else "NOT NULL"
        print(f"  - {col['name']}: {col['type']} {nullable}")
    
    # Show indexes
    indexes = inspector.get_indexes(table_name)
    if indexes:
        print(f"  Indexes:")
        for idx in indexes:
            print(f"    - {idx['name']}: {idx['column_names']}")
    
    print()
