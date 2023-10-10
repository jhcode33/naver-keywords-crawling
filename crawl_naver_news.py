# 필요한 라이브러리 불러오기
from bs4 import BeautifulSoup
import requests
import time

# 크롤링할 URL 생성 함수
def make_url(search):
    search = search.replace(' ', '%20')
    url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(1)
    print("생성된 URL: ", url)
    return url

# keywords.txt 파일에서 키워드를 한 줄씩 읽는 함수
def readKeyword():
    with open('keywords.txt', 'r', encoding='utf-8') as keywords_file:
        keywords = [line.strip() for line in keywords_file]
        return keywords

if __name__ == '__main__':
    # 검색어를 파일에서 읽어오기
    keywords = readKeyword()

    # 검색된 키워드들을 순회하며 크롤링 수행
    for search in keywords:
        search_url = make_url(search)

        time.sleep(5)
        # 검색 페이지의 HTML을 가져오기
        response = requests.get(search_url)
        html = response.text

        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(html, 'html.parser')

        # 각 검색 결과에 대해 반복
        for i in range(1, 6):  # 처음 5개 결과만 크롤링하는 것으로 가정
            time.sleep(2)
            # 각 검색 결과의 CSS 선택자
            article_selector = f"ul.list_news > li.bx#sp_nws{i}"
            article = soup.select_one(article_selector)

            # article이 None이면 다음 기사로 넘어가기
            if article is None:
                print(f"기사 {i}를 찾지 못했습니다.")
                continue

            # 제목 추출
            title_element = article.select_one("a.news_tit")
            title_text = title_element.get("title")

            # 내용 추출
            content_element = article.select_one("a.api_txt_lines.dsc_txt_wrap")
            content_text = content_element.text.strip() if content_element else "내용 없음"

            # 작성자 추출
            writer_element = article.select_one("a.info.press")
            writer_text = writer_element.get_text()

            # title_text에서 처음 10글자를 추출하고 양 끝의 공백을 제거한 후 따옴표를 제거
            strTitle = title_text[:10].strip().replace("'", "").replace('"', '')
            file_name = f"file/article_{strTitle}.txt"

            with open(file_name, "w", encoding="utf-8") as file:
                file.write(f"제목: {title_text}\n")
                file.write(f"작성자: {writer_text}\n")
                file.write(f"내용: {content_text}\n")

            print(f"기사 {title_text}을(를) {file_name}에 저장했습니다.")