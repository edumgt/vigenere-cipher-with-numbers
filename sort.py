# random_hangul_sort_save.py
import random
from pathlib import Path

# 한글 완성형(가~힣) 유니코드 범위
HANGUL_START = 0xAC00
HANGUL_END = 0xD7A3

def random_hangul_char() -> str:
    return chr(random.randint(HANGUL_START, HANGUL_END))

def random_hangul_word(length: int = 3) -> str:
    return "".join(random_hangul_char() for _ in range(length))

def main():
    n = 10
    words = set()

    # 중복 없이 10개 생성
    while len(words) < n:
        words.add(random_hangul_word(3))

    words_sorted = sorted(words)  # 유니코드 순 = (완성형 기준) 가나다 순과 동일하게 동작

    out_path = Path("hangul_list_sorted.txt")
    out_path.write_text("\n".join(words_sorted) + "\n", encoding="utf-8")

    print(f"Saved: {out_path.resolve()}")
    print("----sorted list----")
    print("\n".join(words_sorted))

if __name__ == "__main__":
    main()
