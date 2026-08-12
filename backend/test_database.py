"""
Database Testing Script for JobSentinel
Tests connection, tables, CRUD operations, and data integrity
"""

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import Session
from app.config import settings
from app.database import SessionLocal
from app.models import User, Company, Job
from app.auth import get_password_hash
from datetime import datetime

def test_connection():
    """Test basic database connection"""
    print("\n" + "="*60)
    print("TEST 1: Database Connection")
    print("="*60)
    try:
        engine = create_engine(settings.database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as connection_test"))
            value = result.scalar()
            print(f"[PASS] Connection successful. Result: {value}")
            return True
    except Exception as e:
        print(f"[FAIL] Connection failed: {e}")
        return False

def test_tables():
    """Test if all required tables exist"""
    print("\n" + "="*60)
    print("TEST 2: Table Existence")
    print("="*60)
    engine = create_engine(settings.database_url)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    required_tables = ['users', 'companies', 'jobs', 'applications', 'notifications', 'application_events']
    print(f"Total tables found: {len(tables)}")
    
    all_exist = True
    for table in required_tables:
        exists = table in tables
        status = "PASS" if exists else "FAIL"
        print(f"  [{status}] {table}")
        if not exists:
            all_exist = False
    
    return all_exist

def test_columns():
    """Test if all required columns exist in key tables"""
    print("\n" + "="*60)
    print("TEST 3: Column Existence")
    print("="*60)
    engine = create_engine(settings.database_url)
    inspector = inspect(engine)
    
    schema_checks = {
        'users': ['user_id', 'email', 'full_name', 'password_hash', 'is_active'],
        'companies': ['company_id', 'name', 'website', 'industry', 'location'],
        'jobs': ['job_id', 'company_id', 'title', 'url', 'status'],
        'applications': ['application_id', 'user_id', 'job_id', 'application_status']
    }
    
    all_pass = True
    for table_name, required_cols in schema_checks.items():
        print(f"\n  Table: {table_name}")
        columns = inspector.get_columns(table_name)
        existing_cols = {col['name'] for col in columns}
        
        for col in required_cols:
            exists = col in existing_cols
            status = "PASS" if exists else "FAIL"
            print(f"    [{status}] {col}")
            if not exists:
                all_pass = False
    
    return all_pass

def test_crud_operations():
    """Test Create, Read, Update, Delete operations"""
    print("\n" + "="*60)
    print("TEST 4: CRUD Operations")
    print("="*60)
    
    db = SessionLocal()
    all_pass = True
    
    try:
        # CREATE
        print("\n  CREATE (Insert):")
        # Use a shorter password to stay within bcrypt's 72-byte limit
        short_pass = get_password_hash("pwd123")  # Shorter password
        test_user = User(
            email=f"test_{datetime.now().timestamp()}@example.com",
            full_name="Test User",
            password_hash=short_pass,
            is_active=True
        )
        db.add(test_user)
        db.commit()
        print(f"    [PASS] User created with ID: {test_user.user_id}")
        user_id = test_user.user_id
        
        # READ
        print("\n  READ (Query):")
        retrieved_user = db.query(User).filter(User.user_id == user_id).first()
        if retrieved_user:
            print(f"    [PASS] User retrieved: {retrieved_user.email}")
        else:
            print(f"    [FAIL] User not found")
            all_pass = False
        
        # UPDATE
        print("\n  UPDATE (Modify):")
        retrieved_user.full_name = "Updated Test User"
        db.commit()
        updated_user = db.query(User).filter(User.user_id == user_id).first()
        if updated_user.full_name == "Updated Test User":
            print(f"    [PASS] User updated: {updated_user.full_name}")
        else:
            print(f"    [FAIL] Update failed")
            all_pass = False
        
        # DELETE
        print("\n  DELETE (Remove):")
        db.delete(updated_user)
        db.commit()
        deleted_user = db.query(User).filter(User.user_id == user_id).first()
        if deleted_user is None:
            print(f"    [PASS] User deleted successfully")
        else:
            print(f"    [FAIL] Delete failed")
            all_pass = False
            
    except Exception as e:
        print(f"    [FAIL] CRUD operation failed: {e}")
        all_pass = False
    finally:
        db.close()
    
    return all_pass

def test_relationships():
    """Test foreign key relationships"""
    print("\n" + "="*60)
    print("TEST 5: Relationships & Foreign Keys")
    print("="*60)
    
    db = SessionLocal()
    all_pass = True
    
    try:
        # Create test company
        test_company = Company(
            name=f"Test Company {datetime.now().timestamp()}",
            website="https://example.com",
            industry="Tech",
            location="San Francisco"
        )
        db.add(test_company)
        db.commit()
        print(f"  [PASS] Company created: {test_company.company_id}")
        
        # Create test job
        test_job = Job(
            company_id=test_company.company_id,
            title="Software Engineer",
            url="https://example.com/job",
            status="active"
        )
        db.add(test_job)
        db.commit()
        print(f"  [PASS] Job created: {test_job.job_id} (linked to company {test_job.company_id})")
        
        # Verify relationship
        company = db.query(Company).filter(Company.company_id == test_company.company_id).first()
        if company.jobs:
            print(f"  [PASS] Relationship verified: Company has {len(company.jobs)} job(s)")
        else:
            print(f"  [FAIL] Relationship not working")
            all_pass = False
        
        # Cleanup
        db.delete(test_job)
        db.delete(test_company)
        db.commit()
        
    except Exception as e:
        print(f"  [FAIL] Relationship test failed: {e}")
        all_pass = False
    finally:
        db.close()
    
    return all_pass

def test_data_integrity():
    """Test constraints and data integrity"""
    print("\n" + "="*60)
    print("TEST 6: Data Integrity & Constraints")
    print("="*60)
    
    db = SessionLocal()
    all_pass = True
    
    try:
        # Test unique constraint on email
        print("\n  Testing UNIQUE constraint (email):")
        user1 = User(
            email=f"unique_test_{datetime.now().timestamp()}@example.com",
            full_name="User 1",
            password_hash=get_password_hash("pwd123")  # Shorter password
        )
        db.add(user1)
        db.commit()
        
        user2 = User(
            email=user1.email,  # Same email - should fail
            full_name="User 2",
            password_hash=get_password_hash("pwd123")  # Shorter password
        )
        db.add(user2)
        try:
            db.commit()
            print(f"    [FAIL] Unique constraint not enforced")
            all_pass = False
        except Exception as e:
            print(f"    [PASS] Unique constraint working (duplicate rejected)")
            db.rollback()
        
        # Cleanup
        db.delete(user1)
        db.commit()
        
    except Exception as e:
        print(f"  [FAIL] Data integrity test failed: {e}")
        all_pass = False
    finally:
        db.close()
    
    return all_pass

def run_all_tests():
    """Run all database tests"""
    print("\n" + "="*60)
    print("JobSentinel Database Testing Suite")
    print("="*60)
    
    results = {
        "Connection": test_connection(),
        "Tables": test_tables(),
        "Columns": test_columns(),
        "CRUD": test_crud_operations(),
        "Relationships": test_relationships(),
        "Integrity": test_data_integrity()
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "PASS" if passed_test else "FAIL"
        print(f"  [{status}] {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return all(results.values())

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
