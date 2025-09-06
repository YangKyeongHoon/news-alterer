
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

def main():
    while True:
        print(f"\n--- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        print("새로운 기사를 확인합니다...")

        # 연합뉴스 URL
        url = "https://www.yna.co.kr/"

        try:
            # 웹사이트에 GET 요청 보내기
            response = requests.get(url)
            # 인코딩 설정 (한글 깨짐 방지)
            response.encoding = 'utf-8'
            
            # 요청이 성공했는지 확인
            if response.status_code == 200:
                # BeautifulSoup 객체 생성
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 주요 기사 섹션(.item-box01, .item-box02 등)들을 선택합니다.
                articles = soup.select('.item-box01, .item-box02')
                
                if articles:
                    print("--- 연합뉴스 최신 기사 (상위 5개) ---")
                    # 상위 5개 기사만 처리
                    for i, article in enumerate(articles[:5], 1):
                        title_tag = article.select_one('a.tit-news')
                        
                        # 제목이 없는 항목은 건너뜁니다 (광고 등)
                        if not title_tag:
                            continue

                        title = title_tag.get_text(strip=True)
                        link = title_tag.get('href')
                        
                        # 일부 링크는 //로 시작할 수 있으므로 https:를 붙여줍니다.
                        if link and link.startswith('//'):
                            link = 'https:' + link

                        summary_tag = article.select_one('p.lead')
                        summary = "" # 기본값을 빈 문자열로 설정
                        if summary_tag:
                            summary = summary_tag.get_text(strip=True)

                        print(f"\n[{i}] {title}")
                        print(f"  - 링크: {link}")
                        # 요약 내용이 있을 경우에만 출력
                        if summary:
                            print(f"  - 요약: {summary}")
                else:
                    print("기사를 찾을 수 없습니다. 웹사이트 구조가 변경되었을 수 있습니다.")
                
            else:
                print(f"웹사이트를 불러오는 데 실패했습니다. 상태 코드: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"요청 중 에러 발생: {e}")
        
        print(f"\n다시 확인하려면 Enter 키를, 종료하려면 'q'를 입력하고 Enter 키를 누르세요.")
        choice = input()
        if choice.lower() == 'q':
            print("프로그램을 종료합니다.")
            break

if __name__ == "__main__":
    main()
