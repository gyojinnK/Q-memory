import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    
    print(f"Checking keys... URL: {'✅' if url else '❌'}, KEY: {'✅' if key else '❌'}")
    
    if not url or not key:
        print("❌ 환경 변수(.env)가 비어있습니다!")
        return

    try:
        supabase = create_client(url, key)
        # 간단한 쿼리 테스트 (count)
        response = supabase.table('questions').select("*", count='exact').limit(0).execute()
        print(f"✅ Supabase 연결 성공! 현재 저장된 문제 수: {response.count}개")
    except Exception as e:
        print(f"❌ 연결 실패: {e}")

if __name__ == "__main__":
    test_connection()
