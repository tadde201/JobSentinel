from sqlalchemy import create_engine, text
from app.config import settings

engine = create_engine(settings.database_url)

queries = [
    ("Count Users", "SELECT COUNT(*) as total_users FROM users;"),
    ("Count Companies", "SELECT COUNT(*) as total_companies FROM companies;"),
    ("Count Jobs", "SELECT COUNT(*) as total_jobs FROM jobs;"),
    ("Count Applications", "SELECT COUNT(*) as total_applications FROM applications;"),
    ("Users (Latest 5)", "SELECT user_id, email, full_name, is_active FROM users LIMIT 5;"),
]

print("\n" + "="*80)
print("JobSentinel Database Query Examples")
print("="*80)

for title, query in queries:
    print(f"\n{title}:")
    print("-" * 80)
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()
            columns = result.keys()
            
            if not rows:
                print("  No results found.")
                continue
            
            for row in rows:
                print("  " + " | ".join([f"{col}: {val}" for col, val in zip(columns, row)]))
    except Exception as e:
        print(f"  Error: {e}")

print("\n" + "="*80 + "\n")
