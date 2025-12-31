import os
import json
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

def save_local_json_to_db():
    # 1. JSON 파일 읽기
    json_path = "../../apps/web/assets/data/questions.json"
    abs_path = os.path.join(os.path.dirname(__file__), json_path)
    
    if not os.path.exists(abs_path):
        print(f"❌ JSON 파일을 찾을 수 없습니다: {abs_path}")
        return

    with open(abs_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    print(f"📂 로컬 파일에서 {len(questions)}개 문제 로드 완료")

    # 2. Supabase 연결
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not key:
        print("❌ Supabase 환경 변수가 없습니다.")
        return
        
    supabase = create_client(url, key)

    # 3. 데이터 저장
    try:
        print(f"💾 데이터베이스에 저장 시작...")
        
        # 배치 처리
        batch_size = 50
        for i in range(0, len(questions), batch_size):
            batch = questions[i:i+batch_size]
            response = supabase.table('questions').upsert(batch, on_conflict='id').execute()
            print(f"   - {i+1}~{min(i+len(batch), len(questions))}번 문제 저장 완료")
            
        print(f"✅ 모든 데이터 저장 완료!")
    except Exception as e:
        print(f"❌ 데이터베이스 저장 실패: {e}")

if __name__ == "__main__":
    save_local_json_to_db()
