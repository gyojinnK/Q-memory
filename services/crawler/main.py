import os
import re
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def get_supabase_client() -> Client:
    """Supabase 클라이언트를 생성하여 반환합니다."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not key:
        print("⚠️ Supabase 환경 변수가 설정되지 않았습니다. (SUPABASE_URL, SUPABASE_SERVICE_KEY)")
        return None
        
    return create_client(url, key)

def save_questions_to_db(questions: list):
    """문제를 Supabase 데이터베이스에 저장합니다."""
    supabase = get_supabase_client()
    if not supabase:
        print("⚠️ 데이터베이스 저장을 건너뜁니다.")
        return

    try:
        print(f"💾 {len(questions)}개 문제를 데이터베이스에 저장 중...")
        
        # 한 번에 너무 많은 데이터를 보내면 에러가 날 수 있으므로 배치 처리 (선택)
        batch_size = 50
        for i in range(0, len(questions), batch_size):
            batch = questions[i:i+batch_size]
            
            # questions 테이블에 데이터 삽입
            # conflict 발생 시 업데이트하도록 설정할 수도 있음 (upsert)
            response = supabase.table('questions').upsert(batch, on_conflict='id').execute()
            
        print(f"✅ 데이터베이스 저장 완료!")
    except Exception as e:
        print(f"❌ 데이터베이스 저장 실패: {e}")

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def close_popup_if_exists(driver):
    try:
        close_button_patterns = [
            "//input[@value='닫기']",
            "//button[contains(text(), '닫기')]",
            "//a[contains(text(), '닫기')]",
            "//input[@type='button' and contains(@value, '닫기')]",
            "//div[contains(@class, 'close')]",
            "//span[contains(@class, 'close')]"
        ]
        
        for pattern in close_button_patterns:
            try:
                close_btn = driver.find_element(By.XPATH, pattern)
                if close_btn.is_displayed():
                    driver.execute_script("arguments[0].click();", close_btn)
                    time.sleep(0.5)
                    return True
            except:
                continue
        return False
    except Exception as e:
        return False

def get_subject_buttons(driver):
    try:
        buttons = driver.find_elements(By.CSS_SELECTOR, "a[href^='javascript:start_testEach']")
        return buttons
    except Exception as e:
        print(f"⚠️ 과목 버튼 찾기 실패: {e}")
        return []

def click_first_screen_button(driver):
    try:
        first_buttons = driver.find_elements(By.XPATH, "//input[@value='첫화면']")
        for btn in first_buttons:
            if btn.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                time.sleep(0.3)
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(1.0)
                print("🏠 첫화면으로 복귀")
                return True
        return False
    except Exception as e:
        print(f"⚠️ 첫화면 버튼 클릭 실패: {e}")
        return False

def crawl_single_subject(driver, wait, subject_number, start_number, questions_to_collect=20):
    questions_list = []
    
    try:
        for i in range(questions_to_collect):
            current_q_num = start_number + i
            print(f"📦 [{current_q_num}번] 문제 수집 시작...")

            try:
                # 현재 화면에 보이는 문제 지문 찾기 (모든 문제가 DOM에 있고 display:none으로 가려져 있음)
                # td.question01_qpass 셀렉터가 지문 텍스트를 담고 있음
                visible_question_el = None
                end_time = time.time() + 5  # 최대 5초 대기
                
                while time.time() < end_time:
                    candidates = driver.find_elements(By.CSS_SELECTOR, "td.question01_qpass")
                    for el in candidates:
                        if el.is_displayed():
                            visible_question_el = el
                            break
                    if visible_question_el:
                        break
                    time.sleep(0.1)
                
                if visible_question_el:
                    question_text = visible_question_el.text.strip()
                    print(f"✅ 지문 수집 완료: {question_text[:30]}..." if len(question_text) > 30 else f"✅ 지문 수집 완료: {question_text}")
                else:
                    raise Exception("화면에 보이는 문제 지문을 찾을 수 없습니다.")

            except Exception as e:
                print(f"⚠️ 지문 대기 중 오류: {e}")
                continue
            
            try:
                close_popup_if_exists(driver)
                
                confirm_buttons = driver.find_elements(By.XPATH, "//input[@value='결과확인']")
                confirm_btn = None
                for btn in confirm_buttons:
                    if btn.is_displayed():
                        confirm_btn = btn
                        break
                
                if confirm_btn is None:
                    raise Exception("보이는 '결과확인' 버튼을 찾을 수 없습니다")
                
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_btn)
                driver.execute_script("arguments[0].click();", confirm_btn)
                print(f"✅ 결과확인 클릭 성공")
                
                # 정답 이미지가 뜰 때까지 스마트하게 대기 (최대 2초)
                try:
                    wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//td[contains(@style, '/img/o3524.gif')]")
                    ))
                except:
                    time.sleep(0.5) # 정답 이미지가 없거나 늦게 뜨는 경우를 위한 최소 대기
                    
            except Exception as e:
                print(f"⚠️ 결과확인 버튼 클릭 실패: {e}")

            options = []
            answer_index = -1
            
            for idx in range(1, 5):
                target_opt_id = f"quesitem{current_q_num}{idx}"
                try:
                    opt_td = driver.find_element(By.ID, target_opt_id)
                    opt_el = opt_td.find_element(By.TAG_NAME, "a")
                    
                    opt_text = opt_el.get_attribute("textContent").strip()
                    # 보기 텍스트 정제 (원문자, 숫자, 공백 제거)
                    opt_text = re.sub(r'^[①-⑮\(\)\d\.\s]+', '', opt_text).strip()
                    options.append(opt_text)
                    
                    style_td = opt_td.get_attribute("style") or ""
                    if "background-image" in style_td and "/img/o3524.gif" in style_td:
                        answer_index = idx
                        print(f"🎯 정답 발견: {answer_index}번 | {target_opt_id}")
                        print()
                except Exception as e:
                    print(f"⚠️ 보기 {idx}번 추출 실패")

            questions_list.append({
                "id": current_q_num,
                "subject": subject_number,
                "question": question_text,
                "options": options,
                "answer": answer_index,
                "explanation": ""
            })

            if i < questions_to_collect - 1:
                try:
                    current_question_ref = visible_question_el
                    close_popup_if_exists(driver)
                    
                    next_buttons = driver.find_elements(By.XPATH, "//input[@value='다음']")
                    next_btn = None
                    for btn in next_buttons:
                        if btn.is_displayed():
                            next_btn = btn
                            break
                    
                    if next_btn is None:
                        raise Exception("보이는 '다음' 버튼을 찾을 수 없습니다")
                    
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
                    driver.execute_script("arguments[0].click();", next_btn)
                    
                    try:
                        wait.until(EC.staleness_of(current_question_ref))
                        print(f"🔄 페이지 전환 완료")
                    except:
                        pass
                    
                    print(f"➡️  {current_q_num + 1}번 문제로 이동 중...")
                except Exception as e:
                    print(f"❌ 다음 버튼 클릭 실패: {e}")
                    break

    except Exception as e:
        print(f"⚠️ 과목 크롤링 중 오류: {e}")
    
    return questions_list

def crawl_all_subjects():
    driver = setup_driver()
    main_url = "https://www.gunsys.com/q/qpass_takeExam.php?examUid=4634"
    driver.get(main_url)
    wait = WebDriverWait(driver, 10)
    
    time.sleep(1.0)
    close_popup_if_exists(driver)
    
    all_questions = []
    current_number = 1
    
    try:
        subject_buttons = get_subject_buttons(driver)
        total_subjects = len(subject_buttons)
        
        print(f"\n{'='*60}")
        print(f"📚 총 {total_subjects}개 과목 발견")
        print(f"{'='*60}\n")
        
        for idx in range(total_subjects):
            print(f"\n{'='*60}")
            print(f"📖 {idx + 1}/{total_subjects} 과목 크롤링 시작")
            print(f"🔢 문제 번호: {current_number}번부터")
            print(f"{'='*60}\n")
            
            subject_buttons = get_subject_buttons(driver)
            if idx >= len(subject_buttons):
                print(f"⚠️ {idx + 1}번 과목 버튼을 찾을 수 없습니다")
                break
            
            driver.execute_script("arguments[0].click();", subject_buttons[idx])
            time.sleep(1.5)
            
            questions = crawl_single_subject(
                driver, wait, idx + 1, current_number, questions_to_collect=20
            )
            all_questions.extend(questions)
            current_number += len(questions)
            
            if idx < total_subjects - 1:
                click_first_screen_button(driver)
                time.sleep(1.0)
        
    except Exception as e:
        print(f"⚠️ 크롤링 중 오류 발생: {e}")
    finally:
        driver.quit()
        return all_questions

if __name__ == "__main__":
    # 1. 크롤링 실행
    data = crawl_all_subjects()
    
    # 2. CI 환경이 아닐 때만 JSON 파일 저장 (로컬 백업용)
    if os.getenv("IS_CI") != "true":
        current_dir = os.path.dirname(os.path.abspath(__file__))
        target_path = os.path.join(current_dir, "../../apps/web/assets/data/questions.backup.json")
        
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*60}")
        print(f"✨ 총 {len(data)}문제 로컬 저장 완료!")
        print(f"📁 경로: {target_path}")
    else:
        print(f"\n🚀 CI 환경: 로컬 파일 저장을 건너뛰고 DB 업데이트를 진행합니다.")
    
    # 3. 데이터베이스 저장
    print(f"{'-'*60}")
    save_questions_to_db(data)
    print(f"{'='*60}")