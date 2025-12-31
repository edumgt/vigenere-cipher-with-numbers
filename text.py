# make_mojibake.py
from pathlib import Path

OUT = Path("./encoding_demo")
OUT.mkdir(exist_ok=True)

text = "한글 테스트: 가나다라마바사 아자차카타파하 123 ABC\n두번째 줄: 서울 부산 대전\n"

def write_text(path: Path, s: str, enc: str, bom: bool = False):
    if bom and enc.lower().replace("-", "") in ("utf8", "utf_8"):
        # UTF-8 with BOM
        path.write_bytes(b"\xef\xbb\xbf" + s.encode("utf-8"))
    else:
        path.write_text(s, encoding=enc, newline="\n")

def hexdump(b: bytes, n: int = 80) -> str:
    # 앞쪽 n바이트만 보기 좋게 출력
    slice_ = b[:n]
    return " ".join(f"{x:02X}" for x in slice_)

# 1) 정상 파일들 (저장 인코딩별)
write_text(OUT / "01_utf8_no_bom.txt", text, "utf-8", bom=False)
write_text(OUT / "02_utf8_with_bom.txt", text, "utf-8", bom=True)

# 한국 Windows "ANSI"에 가까운 인코딩 (cp949)
write_text(OUT / "03_cp949_ansi.txt", text, "cp949")

# (참고) euc-kr도 가능하지만 cp949가 더 흔함
write_text(OUT / "04_euc_kr.txt", text, "euc-kr")

# 2) 깨짐 유도: cp949로 저장된 바이트를 "다른 인코딩으로 잘못 해석"해서 텍스트로 만들어 저장
raw_cp949 = (OUT / "03_cp949_ansi.txt").read_bytes()

print("[cp949 원본 바이트 앞부분 HEX]")
print(hexdump(raw_cp949))

# cp949 바이트를 아래 인코딩으로 '잘못' 디코딩하면 한글이 깨진 문자열이 만들어짐
wrong_decoders = [
    "utf-8",     # 보통 에러/대체문자 발생
    "cp1252",    # 서유럽 ANSI로 억지 해석 → 이상한 문자 잔뜩(모지바케)
    "latin1",    # 바이트 1:1 매핑 → “가짜 문자”로 변환
    "shift_jis", # 일본어 계열로 억지 해석
]

for dec in wrong_decoders:
    try:
        mojibake = raw_cp949.decode(dec)  # 일부는 UnicodeDecodeError 날 수 있음
    except UnicodeDecodeError:
        mojibake = raw_cp949.decode(dec, errors="replace")  # 깨짐을 강제로 보여주기

    # 깨진 결과를 UTF-8로 저장(열어보면 이미 깨진 글자가 "그대로" 보임)
    (OUT / f"10_mojibake_from_cp949_read_as_{dec}.txt").write_text(
        mojibake, encoding="utf-8", newline="\n"
    )

# 3) 반대로: UTF-8 바이트를 cp949로 잘못 읽는 경우도 만들어보기
raw_utf8 = (OUT / "01_utf8_no_bom.txt").read_bytes()
try:
    mojibake2 = raw_utf8.decode("cp949")
except UnicodeDecodeError:
    mojibake2 = raw_utf8.decode("cp949", errors="replace")

(OUT / "20_mojibake_from_utf8_read_as_cp949.txt").write_text(
    mojibake2, encoding="utf-8", newline="\n"
)

print("\n완료! ./encoding_demo 폴더를 확인하세요.")
print(" - 03_cp949_ansi.txt (정상: cp949로 열면 정상)")
print(" - 10_... 파일들 (의도적으로 깨진 텍스트)")
print(" - 20_... (UTF-8를 cp949로 잘못 해석한 결과)")
