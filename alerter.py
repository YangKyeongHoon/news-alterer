
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

def get_article_content(url):
    """
    기사 상세 페이지에 접속하여 본문 내용을 가져옵니다.
    """
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 연합뉴스 기사 본문에 해당하는 CSS 선택자 (실제 구조에 따라 변경될 수 있음)
            article_body = soup.select_one('article')
            if article_body:
                return article_body.get_text(strip=True)
            else:
                return "본문 내용을 찾을 수 없습니다."
        else:
            return f"기사 페이지를 불러오는 데 실패했습니다. 상태 코드: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"기사 페이지 접속 중 에러 발생: {e}"

def summarize_article_text(text):
    """
    기사 본문을 요약합니다. (여기서는 간단히 앞부분만 잘라서 보여줍니다)
    실제 구현에서는 LLM API를 호출하는 로직이 들어갑니다.
    """
    if not text or "찾을 수 없습니다" in text or "에러 발생" in text:
        return text # 에러 메시지는 그대로 반환

    # 요약의 예시로 앞 200자만 잘라 반환
    summary = text[:50] + "..."
    return summary

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
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                articles = soup.select('.item-box01, .item-box02')
                
                if articles:
                    print("--- 연합뉴스 최신 기사 (상위 5개) ---")
                    for i, article in enumerate(articles[:5], 1):
                        title_tag = article.select_one('a.tit-news')
                        
                        if not title_tag:
                            continue

                        title = title_tag.get_text(strip=True)
                        link = title_tag.get('href')
                        
                        if link and link.startswith('//'):
                            link = 'https:' + link

                        print(f"\n[{i}] {title}")
                        print(f"  - 링크: {link}")

                        # 상세 페이지에 접속하여 본문을 가져오고 요약
                        if link:
                            print("  - 요약 생성 중...")
                            full_text = get_article_content(link)
                            summary = summarize_article_text(full_text)
                            print(f"  - 요약: {summary}")
                        else:
                            print("  - 요약: 링크가 없어 요약을 생성할 수 없습니다.")
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
