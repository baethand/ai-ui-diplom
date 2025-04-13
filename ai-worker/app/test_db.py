from app.services.DBService import db_service

def test_connection():
    try:
        with db_service.get_session() as session:
            result = session.execute("SELECT 1").scalar()
            print(f"Connection test successful, result: {result}")
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()