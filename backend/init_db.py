"""
데이터베이스 초기화 스크립트
- 테이블 생성
- 기본 카테고리 데이터 삽입
"""
from app.database import init_db, SessionLocal
from app.api.categories import init_default_categories

if __name__ == "__main__":
    print("Database initialization...")
    
    # 테이블 생성
    init_db()
    print("Tables created successfully")
    
    # 기본 카테고리 삽입
    db = SessionLocal()
    try:
        init_default_categories(db)
        print("Default categories inserted successfully")
    finally:
        db.close()
    
    print("Database initialization completed!")
