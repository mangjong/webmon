import requests
import urllib3
import sys
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

'''
미완성 코드

> 웹사이트 정기적인 상태 체크를 통한 모니터링  / 1분 단위
> 최종적으로 별도로 상태 체크를 위한 웹사이트 구축
> 상태를 확인했을 때, 로그 기록 남기기
> 비정상일 경우 별도 메일링, 알림 등 방안 마련
입력되는 값 > http / https 자동으로 분류 ? 80, 443 체크 까지? 웹포트로 오픈된 내역 확인 80,443,8080

| 사이트명 |  URL  |  상태  |  경과 시간  | 점검 시간 |

'''

def usage():
    print("사용법: python 파일명.py <URL 또는 URL 목록 파일명>")
    print("URL: 단일 URL 주소를 입력할 경우, 해당 주소의 상태를 체크합니다.")
    print("URL 목록 파일명: 여러 개의 URL을 포함한 텍스트 파일을 입력할 경우, 파일에 나열된 각 URL의 상태를 체크합니다.")

def format_elapsed_time(elapsed_time):
    if elapsed_time < 1:
        return f"{int(elapsed_time * 1000)}ms"
    else:
        return f"{elapsed_time:.2f}s"

def check_website_status(url):
    try:
        start_time = time.time() # 시작 시간 기록
        response = requests.get(url, verify=False)
        end_time = time.time() # 종료 시간 기록
        elapsed_time = end_time - start_time # 경과 시간 계산

        if response.status_code == 200:
            print("URL:      ", url)
            print("상태:      웹사이트가 정상적으로 작동 중입니다.")
            print("경과 시간:", format_elapsed_time(elapsed_time), "초")
            print("점검 시간:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("본문 길이:",round((len(response.text)/1000), 1),"k")
            print("\n")
        else:
            print("사이트명:", response.url)
            print("URL:", url)
            print("상태: 웹사이트에 문제가 있습니다.")
            print("상태 코드:", response.status_code)
            print("경과 시간:", format_elapsed_time(elapsed_time), "초")
            print("점검 시간:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    except requests.exceptions.RequestException as e:
        print("웹사이트에 연결할 수 없습니다.\n", str(e))

def main():
    if len(sys.argv) == 2:
        input_file = sys.argv[1]

        if not input_file.endswith('.txt'):
            while True:                
                check_website_status(input_file)
                time.sleep(60)
        else:
            with open(input_file, 'r') as f:
                lines = f.readlines()
            while True:
                for line in lines:
                    url = line.strip()
                    check_website_status(url)
                time.sleep(60)
    else:
        usage()

if __name__ == '__main__':
    main()
