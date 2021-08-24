import os



consonant = ['b','ch','d','dh','f','g','hh','jh',
            'k','l','m','n','ng','p','r','s','sh',
            't','th','v','w','y','z','zh']
vowel = ['aa','ae','ah','ao','aw','ay',
        'eh','er','ey',
        'ih','iy',
        'ow','oy',
        'uh','uw']
others = ['pau','sil','sp','x']

print("Consonant : ",len(consonant))
print("Vowel : ",len(vowel))

def preprocessing(string):
    string = string.lower()
    word = string.split(" ",1)[0]

    phone = string.split(" ",1)[1]
    phone = phone.replace("0","")
    phone = phone.replace("1","")
    phone = phone.replace("2","")
    phone_each = phone.split(" ")

    return word , phone_each

def check_vowel_and_consonant(word, phone):
    ## check vowel and consonant
    for item in phone :
        if item not in consonant :
            if item not in vowel :
                if item != '-':
                    print("error : vowel or consonant",word,item)

def check_split_vowel(word, phone):
    ## check "-" and vowel
    split_symbol = 0
    vowel_count = 0
    for item in phone :
        if item == "-":
            split_symbol += 1
        if item in vowel :
            vowel_count += 1
    if (vowel_count - split_symbol) != 1:
        print("error : syllable not match",word)


with open("data/oov_split_syl.txt", "r") as fin :
    for line in fin:
        line = line.strip("\n")
        word, phone = preprocessing(line)
        check_vowel_and_consonant(word, phone)
        check_split_vowel(word, phone)
