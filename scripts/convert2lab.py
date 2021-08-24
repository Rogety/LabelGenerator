import re
import os
from g2p_en import G2p
from nltk.corpus import PlaintextCorpusReader

pattern_name = r'_[ab]\d+'
pattern_sen = r'\"(.*)+\"'

#source_dir_path = "data/arctic/"
source_dir_path = "data/arctic/"
lab_dcit = {}
prefix = "cmu_us_arctic_slt"
suffux = ".lab"



def convert2character():
    #with open("data/arctic/arctic_sentense.txt","r") as fin :
    with open("data/arctic_sentense.txt","r") as fin :
        for line in fin :
            filename = prefix + re.search(pattern_name,line).group(0) + suffux
            filepath = os.path.join(source_dir_path,filename)
            content = re.search(pattern_sen,line).group(0).strip('"')
            content = content.replace(",","")
            content = content.replace(".","")
            content = content.replace(";","")
            content = content.replace("--","")
            content = content.replace("-"," ")
            content = content.upper()
            # if "1908" in content :
            #     content = content.replace("1908","19 0 8")
            '''
            print(filename)
            print(filepath)
            print(content)
            print(os.path.isdir(source_dir_path))
            '''
            with open(filepath, "w") as fout:
                fout.write(content)

    return 0

def convert2phone():

    g2p = G2p()
    #with open("data/arctic/arctic_sentense.txt","r") as texts :
    with open("data/arctic_sentense.txt","r") as texts :
        for line in texts :
            filename = prefix + re.search(pattern_name,line).group(0) + suffux
            filepath = os.path.join(source_dir_path,filename)
            content = re.search(pattern_sen,line).group(0).strip('"')
            content = "".join(g2p(content))
            content = content.replace(", ","")
            content = content.replace(". ","")
            content = content.replace("; ","")
            content = content.replace("--","")
            content = content.replace("-"," ")
            content = content.upper()
            # if "1908" in content :
            #     content = content.replace("1908","19 0 8")

            with open(filepath, "w") as fout:
                fout.write(content)

    return 0

if __name__ == '__main__':
    convert2character()

    corpus_root = source_dir_path
    file_pattern = r'.*\.lab'
    wordlists = PlaintextCorpusReader(corpus_root, file_pattern)
    fileids = wordlists.fileids()
    raw = wordlists.raw()
    words = wordlists.words()
    sents = wordlists.sents()
    #print("fileids :",fileids)
    print("words :",words,len(words))
    print("sents :",sents[33],len(sents))
    #convert2phone()

    dictionary_word = []
    with open("data/test_dict.txt","r") as texts :
        for line in texts:
            line = line.split(" ",1)
            dictionary_word.append(line[0])

    print("dictionary_word :",len(dictionary_word))


    OOV = []
    for word in words :
        if word not in dictionary_word:
            OOV.append(word)

    print("OOV :",OOV)

    '''
    g2p = G2p()
    line = '( arctic_a0523 "At sea, Monday, March 16, 1908." )'
    content = "".join(g2p(line))
    print(content)
    content = re.search(pattern_sen,line).group(0).strip('"')
    print(content, type(content))
    '''
