import re

pattern = r'[A-Z]{2}\d{1}'


with open("data/oov_split.txt", "w") as fout :
    with open("data/oov_out.txt", "r") as fin :
        for line in fin :
            line = line.strip("\n")
            line = line.replace(", ", "")
            word = line.split(" ", 1)[0]
            phone = line.split(" ", 1)[1]

            match = re.findall(pattern,phone)

            if len(match) != 0 :
                record = []
                for i in range(len(match)):
                    if match[i] not in record:
                        phone = phone.replace(match[i], " "+ match[i] +" " )
                        record.append(match[i])
                print(phone)

            consonant = ["ND","DR","NT","SK","ST","KS","TR","TW","LV","RT","TY","GS","FT","VS","SW",
                        "FR","NS","RF","SV","VW","DV","PT","PR","RM","ML","RK","TL","KB","SF","LG",
                        "KG","RD","DZ","LY"]
            for item in consonant :
                if re.search(item,phone):
                    phone = phone.replace(item, item[0] + " " + item[1])

            if re.search("THR",phone):
                phone = phone.replace("THR", "TH R")
            '''
            if re.search("ND",phone):
                phone = phone.replace("ND", "N D")
            if re.search("DR",phone):
                phone = phone.replace("DR", "D R")
            if re.search("NT",phone):
                phone = phone.replace("NT", "N T")
            if re.search("SK",phone):
                phone = phone.replace("SK", "S K")
            if re.search("ST",phone):
                phone = phone.replace("ST", "S T")
            '''

            fout.write(word)
            fout.write(" ")
            fout.write(phone)
            fout.write("\n")
            #print(word, phone)
