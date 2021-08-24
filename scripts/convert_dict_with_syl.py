import os
import re


with open("data/bu_radio_dict.txt","w") as fout:
    with open("data/bu_radio_dict_with_syl.txt","r") as fin :
        for line in fin :
            line = line.strip("\n")
            if line != "":
                word = line.split(" ",1)[0]
                syl = line.split(" ",1)[1]
                syl = re.sub("- ","",syl)
                fout.write(word+" ")
                fout.write(syl)
                fout.write("\n")

print("end")
