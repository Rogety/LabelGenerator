import os
import csv
import re
from nltk.corpus import PlaintextCorpusReader
from g2p_en import G2p
import argparse

Abbreviations = {
'Mr.':'Mister','Mrs.':'Misess','Dr.':'Doctor','No.':'Number',
'St.':'Saint','Co.':'Company','Jr.':'Junior','Maj.':'Major',
'Gen.':'General','Drs.':'Doctors','Rev.':'Reverend','Lt.':'Lieutenant',
'Hon.':'Honorable','Sgt.':'Sergeant','Capt.':'Captain','Esq.':'Esquire',
'Ltd.':'Limited','Col.':'Colonel','Ft.':'Fort',
'Mr':'Mister','Mrs':'Misess','Jr':'Junior'}

def make_ljspeech_sentense(dataset_id, dataset_dir_path, input_dir_path):
    # make ljspeech sentense
    data_dir_path = os.path.join(dataset_dir_path, "ljspeech", "metadata.csv")
    #data_dir_path = "data/LJSpeech-1.1/metadata.csv"
    content = []
    with open(data_dir_path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            filename = parts[0]
            sentense = parts[2] # include punctulization
            sentense = Abbreviations_normalize(sentense)
            sentense = punctuation_replace(sentense)
            string = "( " +  filename + ' "' + sentense + '" ' + ")"
            content.append(string)

    out_dir_path = os.path.join(input_dir_path, "ljspeech_sentense.txt")
    with open("data/ljspeech_sentense.txt" , "w") as f :
        for line in content :
            f.write(line)
            f.write("\n")


def make_arctic_sentense(dataset_id, dataset_dir_path, input_dir_path):

    pattern_sen = r'\"(.*)+\"'
    pattern_name = r'arctic_[ab]\d+'
    data_dir_path = os.path.join(dataset_dir_path, "arctic", "arctic_sentense.txt")
    #data_dir_path = "data/arctic_sentense_raw.txt"
    content = []
    with open(data_dir_path,"r") as f:
        for line in f:
            filename = re.search(pattern_name, line).group(0)
            sentense = re.search(pattern_sen, line).group(0).strip('"')
            sentense = Abbreviations_normalize(sentense)
            sentense = Numbers_normalize(sentense)
            sentense = punctuation_replace(sentense)

            string = "( " +  filename + ' "' + sentense + '" ' + ")"
            content.append(string)

    ## number mormalize
    out_dir_path = os.path.join(input_dir_path, "arctic_sentense.txt")
    with open(out_dir_path , "w") as f :
        for line in content :
            f.write(line)
            f.write("\n")

def Abbreviations_normalize(sentense):

    tmp = []
    words = sentense.split(" ")
    for word in words :
        word = word.strip(",") # Mr,
        word = word.strip("(") # (Mr.
        if word in Abbreviations.keys() :
            tmp.append(Abbreviations[word])
        else :
            tmp.append(word)

    sentense = " ".join(tmp)

    return sentense

def colon_processing(content): ## :

    if ":" in content:
        words = content.split(" ")
        words = [word.rstrip(":") for word in words]
        content = " ".join(words)
    return content

def apostrophe_processing(content): ## '
    ## : handle
    if "'" in content:
        words = content.split(" ")
        words = [word.strip("'") for word in words]
        content = " ".join(words)

    return content

def period_processing(content): ## .

    if "." in content:
        words = content.split(" ")
        words_out = []
        for word in words :
            if word in Abbreviations :
                words_out.append(Abbreviations[word])
            else :
                words_out.append(word.rstrip("."))

        content = " ".join(words_out)

    content = content.replace(".", "")

    return content

def Numbers_normalize(sentense):

    Numbers = {'16':'sixteen','17':'seventeen','18':'eighteen',
                '29th':'twenty-ninth','1908':'nineteen-oh-eight'}

    tmp = []
    words = sentense.split(" ")
    for word in words :
        word = word.strip(".")
        word = word.strip(",")
        if word in Numbers.keys() :
            tmp.append(Numbers[word])
        else :
            tmp.append(word)

    sentense = " ".join(tmp)

    return sentense


def Abbreviations_processing(content):

    Abbreviations = {
    'Mr.':'Mister','Mrs.':'Misess','Dr.':'Doctor','No.':'Number',
    'St.':'Saint','Co.':'Company','Jr.':'Junior','Maj.':'Major',
    'Gen.':'General','Drs.':'Doctors','Rev.':'Reverend','Lt.':'Lieutenant',
    'Hon.':'Honorable','Sgt.':'Sergeant','Capt.':'Captain','Esq.':'Esquire',
    'Ltd.':'Limited','Col.':'Colonel','Ft.':'Fort'}

    if "." in content:
        words = content.split(" ")
        words_out = []
        for word in words :
            if word in Abbreviations :
                words_out.append(Abbreviations[word])
            else :
                words_out.append(word.rstrip("."))

        content = " ".join(words_out)

    return content

def textpreprocessing(content): # punctuation processing

    content = content.replace(",","")
    content = content.replace(";","")
    content = content.replace("(","")
    content = content.replace(")","")
    content = content.replace("?","")
    content = content.replace("!","")
    content = content.replace('"',"")
    content = content.replace(':',"")
    content = content.replace("-- ","")
    content = content.replace("- "," ") ## text bug order is importtant
    content = content.replace("-"," ")
    content = content.replace("[","")
    content = content.replace("]","")
    content = content.replace("’","")
    content = content.replace("“","")
    content = content.replace("”","")
    #content = colon_processing(content)
    content = content.replace(":"," ")
    content = content.replace(".","")
    content = apostrophe_processing(content)
    content = period_processing(content)
    content = content.replace("  "," ") ## text bug two spaces
    content = content.upper()
    return content

def apostrophe_processing(content): ## '
    ## : handle
    if "'" in content:
        words = content.split(" ")
        words = [word.strip("'") for word in words]
        content = " ".join(words)

    return content

def punctuation_replace(sentense):
    sentense = sentense.replace("--", "")
    sentense = sentense.replace("-", " ") # divide two words
    sentense = sentense.replace("(", "")
    sentense = sentense.replace(")", "")
    sentense = sentense.replace("[", "")
    sentense = sentense.replace("]", "")
    sentense = sentense.replace('"', "")
    sentense = sentense.replace('?', ",")
    sentense = sentense.replace('!', ",")
    sentense = sentense.replace(':', ",")
    sentense = sentense.replace(';', ",")
    sentense = sentense.replace("’","")
    sentense = sentense.replace("“","")
    sentense = sentense.replace("”","")
    sentense = apostrophe_processing(sentense) ## '
    sentense = sentense.replace('.', "")
    sentense = sentense.rstrip(",")
    sentense = sentense + "."
    sentense = sentense.replace("  "," ") ## text bug two spaces

    return sentense

def convert2lab(dataset_dir_path, text_path, pattern_name) :
    pattern_sen = r'\"(.*)+\"'
    suffux = ".lab"
    with open(text_path,"r") as fin :
        for line in fin :
            filename = re.search(pattern_name,line).group(0) + suffux
            filepath = os.path.join(dataset_dir_path,filename)
            content = re.search(pattern_sen,line).group(0).strip('"')

            content = textpreprocessing(content)

            with open(filepath, "w") as fout:
                fout.write(content.rstrip(" "))

def OOV_check(text_path, syl_dict_path, oov_log_path):
    print("Starting OOV chsck")
    pattern_sen = r'\"(.*)+\"'
    total_words = []

    with open(text_path, "r") as fin :
        for line in fin :
            content = re.search(pattern_sen,line).group(0).strip('"')
            content = textpreprocessing(content)
            words = content.split(" ")
            for word in words :
                total_words.append(word.upper())

    total_words = set(total_words)
    dict_words = []
    with open(syl_dict_path, "r") as fin :
        for line in fin :
            line = line.strip("\n")
            word = line.split(" ",1)[0]
            dict_words.append(word)
    oov = []
    for word in total_words :
        if word not in dict_words :
            oov.append(word)

    ## bug ''
    if len(oov) == 1:
        oov.pop()
    # print("oov : ",oov )
    # print(len(oov))
    if oov != []:
        with open(oov_log_path, "w") as fout :
            for word in oov :
                fout.write(word)
                fout.write("\n")
        return False
    else :
        return True

consonant = ['b','ch','d','dh','f','g','hh','jh',
            'k','l','m','n','ng','p','r','s','sh',
            't','th','v','w','y','z','zh']
vowel = ['aa','ae','ah','ao','aw','ay',
        'eh','er','ey',
        'ih','iy',
        'ow','oy',
        'uh','uw']
others = ['pau','sil','sp','x']

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
                    return 1
    return 0

def check_vowel_and_consonant_v2(word, phone):
    ## check vowel and consonant
    for item in phone :
        if item not in consonant :
            if item not in vowel :
                print("error : vowel or consonant",word,item)
                return 1
    return 0

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
        return 1
    return 0


def syl_dict_chcek(syl_dict_path):

    count = 0
    with open(syl_dict_path, "r") as fin :
        for line in fin:
            line = line.strip("\n")
            word, phone = preprocessing(line)
            err_1 = check_vowel_and_consonant(word, phone)
            err_2 = check_split_vowel(word, phone)
            count += (err_1+err_2)

    if count == 0 :
        return True
    else :
        return False

def dict_convert2phone(syl_dict_path, phone_dict_path):
    with open(phone_dict_path,"w") as fout:
        with open(syl_dict_path,"r") as fin :
            for line in fin :
                line = line.strip("\n")
                if line != "":
                    word = line.split(" ",1)[0]
                    syl = line.split(" ",1)[1]
                    syl = re.sub("- ","",syl)
                    fout.write(word+" ")
                    fout.write(syl)
                    fout.write("\n")

def G2P_example():

    g2p = G2p()
    with open("data/oov.txt","w") as fout :
        for item in sorted(set(OOV)) :
            phone = "".join(g2p(item))
            fout.write(item)
            fout.write(" ")
            fout.write(phone)
            fout.write("\n")

    return 0

def phone_dict_check(phone_dict_path):

    count = 0
    with open(phone_dict_path, "r") as fin :
        for line in fin:
            line = line.strip("\n")
            word, phone = preprocessing(line)
            err = check_vowel_and_consonant_v2(word, phone)
            count += err

    if count == 0 :
        return True
    else :
        return False


def check_word(content,lab_filepath):
    ## read dict
    bu_dict = []
    with open("data/bu_radio_dict.txt","r") as fin :
        for line in fin :
            bu_dict.append(line.split(" ",1)[0])


    words = content.split(" ")
    for word in words :
        if word not in bu_dict:
            print(lab_filepath)
            print(word, "failed")
            return 1


    return 0

def check_period(content,lab_filepath):
    if "." in content :
        print(lab_filepath)
        print("check_period failed")
        return 1
    return 0

def lab_check(dataset_dir_path):
    ## get filename
    lab_filepath = []
    for dirPath, dirNames, fileNames in os.walk(dataset_dir_path):
        for f in sorted(fileNames):
            if f.endswith("lab"):
                lab_filepath.append(os.path.join(dirPath, f))

    ## read lab file
    count = 0
    for i in range(len(lab_filepath)):
        with open(lab_filepath[i] , "r") as fin :
            for line in fin :
                err1 = check_word(line,lab_filepath[i]) ## 檢查文字
                err2 = check_period(line,lab_filepath[i]) ## 檢查句點
                count += (err1+err2)


    if count == 0 :
        return True
    else :
        return False

def file_num_check(dataset_dir_path): # for ljspeech_database

    lab_filepath = []
    wav_filepath = []
    for dirPath, dirNames, fileNames in os.walk(dataset_dir_path):
        for f in sorted(fileNames):
            if f.endswith("lab"):
                lab_filepath.append(fileNames)
            if f.endswith("wav"):
                wav_filepath.append(fileNames)

    if len(lab_filepath) != len(wav_filepath) :
        print("filenum not match")
        print("lab file num :",len(lab_filepath))
        print("wav file num :",len(wav_filepath))
        return False
    else:
        return True

def  get_dataset_id(dataset):

    if dataset == "arctic":
        id = 1
    elif dataset == "ljspeech":
        id = 2
    else:
        id = 0
        print("dataset_error")

    return id

def make_dataset_directory(dataset_id, src_dir_path, dataset_dir_path):


    print("dataset_id :",dataset_id)
    print("src_dir_path :",src_dir_path)

    if dataset_id == 1 :
        dataset_path = os.path.join(dataset_dir_path,"arctic")
        text_path = os.path.join(dataset_path,"arctic_sentense.txt")
        aligned_dir_path =  os.path.join(src_dir_path, "Mfa_Label", "aligned_arctic")
        pattern_name = r'arctic_[ab]\d+'
        if not os.path.isdir(aligned_dir_path):
    	    os.makedirs(aligned_dir_path)

    elif dataset_id == 2 :
        #make_ljspeech_sentense()
        dataset_path = os.path.join(dataset_dir_path,"ljspeech")
        text_path = os.path.join(dataset_path,"ljspeech_sentense.txt")
        aligned_dir_path =  os.path.join(src_dir_path, "Mfa_Label", "aligned_ljspeech")
        pattern_name = r'LJ\d+\-\d+'
        if not os.path.isdir(aligned_dir_path):
    	    os.makedirs(aligned_dir_path)
    else :
        assert "error"

    return text_path, dataset_dir_path, aligned_dir_path, pattern_name

def make_16kHz_wav(dataset_id, dataset_dir_path, input_dir_path):




    if dataset_id == 1:
        out_dir_path = os.path.join(input_dir_path, "wavs_16kHz", "arctic")
        audio_dir_path = os.path.join(dataset_dir_path, "arctic", "raw")
    elif  dataset_id == 2:
        out_dir_path = os.path.join(input_dir_path, "wavs_16kHz", "ljspeech")
        audio_dir_path = os.path.join(dataset_dir_path, "ljspeech", "wavs")

    if not os.path.isdir(out_dir_path):
        os.makedirs(out_dir_path)

    for _ , _ ,filename in os.walk(audio_dir_path):
        data = sorted(filename)
        wav = sorted([ x.replace(".raw" , ".wav") for x in filename ])
        wav = sorted([ x.replace("cmu_us_arctic_slt" , "cmu_arctic") for x in wav ])
        raw = sorted(filename)
        raw = sorted([ x.replace("cmu_us_arctic_slt" , "cmu_arctic") for x in filename ])

    for i in range(len(filename)):
        cmd = "sox -r 48000 -t raw -b 16 -e signed-integer " + \
        os.path.join(audio_dir_path, data[i]) + " -r 16000 " + \
        os.path.join(out_dir_path, raw[i])
        os.system(cmd)

    for i in range(len(filename)):
        cmd = "sox -r 48000 -t raw -b 16 -e signed-integer "+ \
        os.path.join(audio_dir_path, data[i]) + " -r 16000 " + \
        os.path.join(out_dir_path, wav[i])
        os.system(cmd)

    return 0

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', '-d', type=str)
    parser.add_argument('--dataset_dir_path', type=str, default=os.path.expanduser("~/Desktop/project/EA_V2/dataset/"))
    parser.add_argument('--input_dir_path', type=str, default=os.path.expanduser("~/Desktop/project/EA_V2/input/"))
    parser.add_argument('--syl_dict_path', type=str, default=os.path.expanduser("~/Desktop/project/EA_V2/input/bu_radio_dict_with_syl.txt"))
    parser.add_argument('--audio_dir_path', type=str, default=os.path.expanduser("~/Desktop/project/EA_V2/input/wavs_16kHz"))
    #parser.add_argument('--dataset_dir_path', type=str, default=os.path.expanduser("~/Desktop/project/EA_V2/data/"))
    args = parser.parse_args()

    dataset_id = get_dataset_id(args.dataset)
    syl_dict_path = args.syl_dict_path
    #phone_dict_path = args.phone_dict_path
    input_dir_path = args.input_dir_path
    audio_dir_path = args.audio_dir_path
    text_path, dataset_dir_path, aligned_dir_path, pattern_name = make_dataset_directory(dataset_id, input_dir_path, args.dataset_dir_path)
    print("text_path :", text_path)
    print("dataset_dir_path :", dataset_dir_path)
    print("aligned_dir_path :", aligned_dir_path)
    print("syl_dict_path :", syl_dict_path)

    #make_ljspeech_sentense(dataset_dir_path, input_dir_path)
    make_arctic_sentense(dataset_id, dataset_dir_path, input_dir_path)
    make_16kHz_wav(dataset_id, dataset_dir_path, input_dir_path)

    #import pdb; pdb.set_trace()

    oov_log_path = os.path.join(input_dir_path, "oov_log.txt")
    if OOV_check(text_path, syl_dict_path, oov_log_path) == True :
        print("OOV check succcess")
    else : ## add oov_word to syl_dict
        print("OOV error ")

    phone_dict_path = os.path.join(input_dir_path, "bu_radio_dict.txt")
    if syl_dict_chcek(syl_dict_path) == True :
        dict_convert2phone(syl_dict_path, phone_dict_path)
        print ("syl_dict_chcek success")
        print("convert to phone dict success")
    else :
        print ("syl_dict_chcek failed")


    if phone_dict_check(phone_dict_path) == True :
        convert2lab(aligned_dir_path, text_path, pattern_name)
        print("convert2lab success")
        print("phone_dict_check success")
    else :
        print("phone_dict_check failed")

    if lab_check(input_dir_path) == True and file_num_check(input_dir_path) == True:
        print("lab_check success")
        print("ready to allign")
    else :
        print("lab_check failed")
        print("file_nums not match")
