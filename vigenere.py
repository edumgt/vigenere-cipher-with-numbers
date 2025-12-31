def encode(word, key):
    new_word = ""                     # ✅ 암호화된 결과를 누적해서 담을 문자열
    key = key.lower()                 # ✅ 키를 소문자로 통일 (키 문자를 일정하게 쓰려는 의도)

    # ✅ ASCII 문자 범위를 “그룹”으로 나누기 위한 리스트들
    #   l1: 33~47 구간의 일부 특수문자
    #   l2: 58~64 구간의 일부 특수문자
    #   l3: 91~96 구간의 일부 특수문자
    l1 = list('!"#$%&()\'*+,-./')     # ✅ 특수문자 그룹1
    l2 = list(':;<=>?@')              # ✅ 특수문자 그룹2
    l3 = list('[\\]^_`')              # ✅ 특수문자 그룹3 (역슬래시 \ 는 \\ 로 이스케이프)

    # ✅ 입력 문자열(word)의 각 문자에 대해 암호화 처리
    for i in range(len(word)):        # i: 현재 문자 인덱스(0,1,2,...)
        # ✅ 현재 문자가 어떤 종류인지 판별하여,
        #    해당 그룹의 "기준 아스키값(stddisp)"과 "모듈러(mod)"를 결정
        if word[i].isupper():         # 대문자 A~Z 인가?
            stddisp = 65              # 'A'의 ASCII = 65
            mod = 26                  # 대문자 알파벳 개수
        elif word[i].islower():       # 소문자 a~z 인가?
            stddisp = 97              # 'a'의 ASCII = 97
            mod = 26                  # 소문자 알파벳 개수
        elif word[i].isdigit():       # 숫자 0~9 인가?
            stddisp = 48              # '0'의 ASCII = 48
            mod = 10                  # 숫자 개수
        elif word[i] in l1:           # 특수문자 그룹1인가?
            stddisp = 33              # '!'의 ASCII = 33 (그룹1 시작 근처)
            mod = 16                  # 그룹1 문자 개수(여기서는 16개로 가정)
        elif word[i] in l2:           # 특수문자 그룹2인가?
            stddisp = 58              # ':'의 ASCII = 58
            mod = 7                   # 그룹2 문자 개수(여기서는 7개로 가정)
        elif word[i] in l3:           # 특수문자 그룹3인가?
            stddisp = 32              # ⚠️ 여기 stddisp=32는 실제 그룹3 시작(91)과 다름 (원 코드 유지)
            mod = 6                   # 그룹3 문자 개수(여기서는 6개로 가정)

        # ✅ 아래 print들은 디버깅을 위한 출력(원리 확인용)
        print("-------------s")        # 구분선 출력
        print(stddisp, mod)           # 기준값/모듈러 값 출력

        # ✅ row: 현재 문자를 그룹 시작 기준(stddisp)에서 얼마나 떨어져 있는지(0부터 시작)
        row = ord(word[i]) - stddisp  # ord('C') - ord('A') 같은 개념

        # ✅ col: 키 문자도 동일하게 stddisp 기준으로 위치값을 계산
        #    i % len(key): 키를 반복 사용(비제네르 방식처럼)
        col = ord(key[i % len(key)]) - stddisp

        # ✅ 암호화 결과 문자 코드 계산:
        #    (row + col) % mod 를 통해 범위를 순환시키고, 다시 stddisp를 더해 ASCII 코드로 복원
        print(stddisp + (row + col) % mod)  # 결과 ASCII 코드(정수) 출력
        print(row + col)                    # row+col 원값 출력
        print((row + col) % mod)            # 모듈러 적용 결과 출력

        # ✅ 계산된 결과를 문자로 바꿔서(new char) 결과 문자열에 추가
        new_word += chr(stddisp + (row + col) % mod)

    return new_word                    # ✅ 최종 암호문 반환


def decode(word, key):
    decoded_word = ""                  # ✅ 복호화된 결과(평문)를 누적할 문자열
    key = key.lower()                  # ✅ 키를 소문자로 통일

    # ✅ encode와 동일한 그룹 정의
    l1 = list('!"#$%&()\'*+,-./')
    l2 = list(':;<=>?@')
    l3 = list('[\\]^_`')

    # ✅ 암호문(word)의 각 문자에 대해 복호화 처리
    for i in range(len(word)):
        # ✅ 암호문 문자 종류를 판별하여 기준값/모듈러 결정(encode와 동일해야 복호화 가능)
        if word[i].isupper():
            stddisp = 65; mod = 26
        elif word[i].islower():
            stddisp = 97; mod = 26
        elif word[i].isdigit():
            stddisp = 48; mod = 10
        elif word[i] in l1:
            stddisp = 33; mod = 16
        elif word[i] in l2:
            stddisp = 58; mod = 7
        elif word[i] in l3:
            stddisp = 32; mod = 6
        else:
            # ✅ 위 범주에 없는 문자는 그대로 결과에 붙이고 다음으로 넘어감
            decoded_word += word[i]
            continue

        # ✅ row: 암호문 문자 위치(0부터)
        row = ord(word[i]) - stddisp

        # ✅ col: 키 문자 위치(0부터) - encode와 동일한 방식으로 키를 반복 사용
        col = ord(key[i % len(key)]) - stddisp

        # ✅ 복호화는 암호화의 반대:
        #    encode: (row + col) % mod
        #    decode: (row - col) % mod  ✅ (중요)
        decoded_word += chr(stddisp + (row - col) % mod)

    return decoded_word                # ✅ 최종 평문 반환


def main():
    while True:                        # ✅ 사용자가 종료할 때까지 계속 반복(메뉴 루프)
        print("----------------------")
        print("1: Encode plain text")  # 1번: 평문 암호화
        print("2: Decode encrypted text")  # 2번: 암호문 복호화
        print("3: Exit")               # 3번: 프로그램 종료

        inpt = input("Enter choice: ").strip()  # ✅ 입력 받기 + 앞뒤 공백 제거

        if inpt == "3":                # ✅ 3 입력 시 종료
            print("Bye!")
            break                      # while 루프 탈출 → 프로그램 끝

        if inpt in ("1", "2"):         # ✅ 1 또는 2일 때만 텍스트/키 입력을 받음
            text = input("Enter text: ")        # ✅ 평문(또는 암호문) 입력
            keyword = input("Enter keyword: ")  # ✅ 키 입력(암호화/복호화에 동일하게 사용)

            if inpt == "1":
                # ✅ 암호화 수행
                print("Encoded text: " + encode(text, keyword))
            else:
                # ✅ 복호화 수행
                print("Decoded text: " + decode(text, keyword))
        else:
            # ✅ 1,2,3 외 입력은 잘못된 입력 처리
            print("Invalid input")


if __name__ == "__main__":
    # ✅ 이 파일을 직접 실행했을 때만 main() 실행
    #    (다른 파일에서 import 되었을 때는 실행 안 됨)
    main()
