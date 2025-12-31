def encode(word,key):
    new_word = ""
    key = key.lower()
    l1 = list('!"#$%&()\'*+,-./')
    l2 = list(':;<=>?@')
    l3 = list('[\\]^_`')
    for i in range(len(word)):
        if word[i].isupper():
            stddisp = 65
            mod = 26
        elif word[i].islower():
            stddisp = 97
            mod = 26
        elif word[i].isdigit():
            stddisp = 48
            mod = 10
        elif word[i] in l1:
            stddisp = 33
            mod = 16
        elif word[i] in l2:
            stddisp = 58
            mod = 7
        elif word[i] in l3:
            stddisp = 32
            mod = 6
        print("-------------s")
        print(stddisp,mod)
        row = ord(word[i]) - stddisp
        col = ord(key[i%len(key)]) - stddisp
        print(stddisp + (row+col)%mod)
        print(row+col)
        print((row+col)%mod)
        new_word += chr(stddisp + (row+col) % mod)
    return new_word
def decode(word, key):
    decoded_word = ""
    key = key.lower()
    l1 = list('!"#$%&()\'*+,-./')
    l2 = list(':;<=>?@')
    l3 = list('[\\]^_`')

    for i in range(len(word)):
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
            # (선택) 위 범주에 없는 문자는 그대로 통과
            decoded_word += word[i]
            continue

        row = ord(word[i]) - stddisp
        col = ord(key[i % len(key)]) - stddisp
        decoded_word += chr(stddisp + (row - col) % mod)

    return decoded_word


def main():
    while True:
        print("----------------------")
        print("1: Encode plain text\n")
        print("2: Decode encrypted text\n")
        inpt = input("Enter choice: ")
        if (inpt.isdigit()):
            text = input("Enter text: ")
            keyword = input("Enter keyword: ")
            if inpt == "1":
                print("Encoded text: " + encode(text,keyword))
            elif inpt == "2":
                print("Decoded text: " + decode(text,keyword))
            else:
                print("Invalid input")
        else:
            print("Invalid input")


if __name__ == "__main__":
    main()