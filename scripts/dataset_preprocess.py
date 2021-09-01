import os
import re
import argparse

Abbreviations = {
'Mr.':'Mister','Mrs.':'Misess','Dr.':'Doctor','No.':'Number',
'St.':'Saint','Co.':'Company','Jr.':'Junior','Maj.':'Major',
'Gen.':'General','Drs.':'Doctors','Rev.':'Reverend','Lt.':'Lieutenant',
'Hon.':'Honorable','Sgt.':'Sergeant','Capt.':'Captain','Esq.':'Esquire',
'Ltd.':'Limited','Col.':'Colonel','Ft.':'Fort',
'Mr':'Mister','Mrs':'Misess','Jr':'Junior'}

Numbers = {'16':'sixteen','17':'seventeen','18':'eighteen',
            '29th':'twenty-ninth','1908':'nineteen-oh-eight'}

consonant = ['b','ch','d','dh','f','g','hh','jh',
            'k','l','m','n','ng','p','r','s','sh',
            't','th','v','w','y','z','zh']

vowel = ['aa','ae','ah','ao','aw','ay',
        'eh','er','ey',
        'ih','iy',
        'ow','oy',
        'uh','uw']

others = ['pau','sil','sp','x']

def Numbers_normalize(sentense):

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

def Txet_Normalizatopn(dataset_id, textIn_dir_path, textOut_dir_path):

    if dataset_id == 1:
        pattern_sen = r'\"(.*)+\"'
        pattern_name = r'arctic_[ab]\d+'
        content = []
        with open(textIn_dir_path,"r") as f:
            for line in f:
                filename = re.search(pattern_name, line).group(0)
                sentense = re.search(pattern_sen, line).group(0).strip('"')
                sentense = Abbreviations_normalize(sentense)
                sentense = Numbers_normalize(sentense)
                sentense = textpreprocessing(sentense)
                string = filename + ' ' + '"' + sentense + '"' ## filename "sentencce"
                content.append(string)
    elif dataset_id == 2:
        content = []
        with open(textIn_dir_path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                filename = parts[0]
                sentense = parts[2] # include punctulization
                sentense = Abbreviations_normalize(sentense)
                sentense = textpreprocessing(sentense)
                string = filename + ' ' + '"' + sentense + '"'
                content.append(string)
    else:
        print("for Split dataset")


    with open(textOut_dir_path , "w") as f :
        for line in content :
            f.write(line)
            f.write("\n")

    return 0

def Wav16kHz_Generation(dataset_id, audioIn_dir_path, audioOut_dir_path):

    if dataset_id == 1:
        for _ , _ ,filename in os.walk(audioIn_dir_path):
            wavs = sorted([ x.replace(".raw" , ".wav") for x in filename ])
            wavs = sorted([ x.replace("cmu_us_arctic_slt" , "arctic") for x in wavs ])
            raws = sorted(filename)
        for i in range(len(filename)):
            cmd = "sox -r 48000 -t raw -b 16 -e signed-integer "+ \
            os.path.join(audioIn_dir_path, raws[i]) + " -r 16000 " + \
            os.path.join(audioOut_dir_path, wavs[i])
            os.system(cmd)
    elif  dataset_id == 2:
        for _ , _ ,filename in os.walk(audioIn_dir_path):
            wavs = sorted(filename)
        for i in range(len(filename)):
            cmd = "sox -v 0.8 "+ \
            os.path.join(audioIn_dir_path, wavs[i]) + " -r 16000 -c 1 -b 16 -e signed-integer " + \
            os.path.join(audioOut_dir_path, wavs[i])
            os.system(cmd)
    else:
        print("for Split dataset")

    return 0

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

def apostrophe_processing(content): ## '
    ## : handle
    if "'" in content:
        words = content.split(" ")
        words = [word.strip("'") for word in words]
        content = " ".join(words)

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

def syl_dict_chcek(dictIn_dir_path):

    count = 0
    with open(dictIn_dir_path, "r") as fin :
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

def OOV_check(textOut_dir_path, dictIn_dir_path):
    #print("Starting OOV chsck")
    pattern_sen = r'\"(.*)+\"'
    total_words = []

    with open(textOut_dir_path, "r") as fin :
        for line in fin :
            content = re.search(pattern_sen,line).group(0).strip('"')
            content = textpreprocessing(content)
            words = content.split(" ")
            for word in words :
                total_words.append(word.upper())

    total_words = set(total_words)
    dict_words = []
    with open(dictIn_dir_path, "r") as fin :
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

    oov_log_path = os.path.join(os.path.dirname(textOut_dir_path), "oov_log.txt")
    if oov != []:
        with open(oov_log_path, "w") as fout :
            for word in oov :
                fout.write(word)
                fout.write("\n")
        print("OOV error ")
        return False
    else :
        #print("OOV check succcess")
        return True

    return 0

def dict_convert2phone(dictIn_dir_path, dictOut_dir_path):
    with open(dictOut_dir_path,"w") as fout:
        with open(dictIn_dir_path,"r") as fin :
            for line in fin :
                line = line.strip("\n")
                if line != "":
                    word = line.split(" ",1)[0]
                    syl = line.split(" ",1)[1]
                    syl = re.sub("- ","",syl)
                    fout.write(word+" ")
                    fout.write(syl)
                    fout.write("\n")

def Dictionary_Generation(textOut_dir_path, dictIn_dir_path, dictOut_dir_path):

    if OOV_check(textOut_dir_path, dictIn_dir_path) == False :
        return

    if syl_dict_chcek(dictIn_dir_path) == False :
        return

    dict_convert2phone(dictIn_dir_path, dictOut_dir_path) # generate dictionary

    return 0

def Convert2MfaLabel(dataset_id, labOut_dir_path, textOut_dir_path, audioOut_dir_path):

    if dataset_id == 1:
        pattern_name = r'arctic_[ab]\d+'
    elif dataset_id == 2:
        pattern_name = r'LJ\d+\-\d+'
    else:
        print("for Split dataset")

    pattern_sen = r'\"(.*)+\"'
    suffux = ".lab"
    with open(textOut_dir_path,"r") as fin :
        for line in fin :
            filename = re.search(pattern_name,line).group(0) + suffux
            filepath = os.path.join(labOut_dir_path,filename)
            content = re.search(pattern_sen,line).group(0).strip('"')
            content = textpreprocessing(content)
            with open(filepath, "w") as fout:
                fout.write(content.rstrip(" "))


    ## audio move
    for audio in os.listdir(audioOut_dir_path):
        if audio.endswith(".wav"):
            audio_path = os.path.join(audioOut_dir_path, audio)
            os.system("cp %s %s" % (audio_path, labOut_dir_path))
            #print("cp %s %s done" % (audio_path, labOut_dir_path))

    return 0

def Directory_Making(output_dir_path, data_dir_path, labOut_dir_path, audioOut_dir_path):

    if not os.path.isdir(output_dir_path):
        os.mkdir(output_dir_path)
    if not os.path.isdir(data_dir_path):
        os.mkdir(data_dir_path)
    if not os.path.isdir(labOut_dir_path):
        os.mkdir(labOut_dir_path)
    if not os.path.isdir(audioOut_dir_path):
        os.mkdir(audioOut_dir_path)

    return 0

def  get_dataset_id(dataset):
    ## get which dataset (arctic or ljspeech or others)
    if dataset == "arctic":
        id = 1
    elif dataset == "ljspeech":
        id = 2
    else:
        id = 0
    return id

if __name__ == '__main__': ## Text normalization

    # path setting
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', '-d', default="arctic", type=str)
    #parser.add_argument('--input_dir_path', type=str, default=os.path.expanduser("~/Desktop/project/EA_V2/dataset/"))
    #parser.add_argument('--output_dir_path', type=str, default=os.path.expanduser("~/Desktop/project/EA_V2/input/data/"))
    #parser.add_argument('--syl_dict_path', type=str, default=os.path.expanduser("~/Desktop/project/EA_V2/input/data/bu_radio_dict_with_syl.txt"))
    args = parser.parse_args()

    dataset_id = get_dataset_id(args.dataset)

    input_dir_path = os.path.join(os.getcwd(), "dataset")
    output_dir_path = os.path.join(os.getcwd(), "input")
    data_dir_path = os.path.join(os.getcwd(), "input", "data")

    # input_dir_path = os.path.expanduser("~/Desktop/project/EA_V2/dataset/")
    # output_dir_path = os.path.expanduser("~/Desktop/project/EA_V2/input/")
    # data_dir_path = os.path.expanduser("~/Desktop/project/EA_V2/input/data/")

    dictIn_path = os.path.join(input_dir_path, "bu_radio_dict_with_syl.txt")

    if dataset_id == 1:
        dataset_dir_path = os.path.join(input_dir_path, "arctic")
        audioIn_dir_path = os.path.join(dataset_dir_path, "raw")
        textIn_path = os.path.join(dataset_dir_path, "arctic_sentence.txt")
    elif dataset_id == 2:
        dataset_dir_path = os.path.join(input_dir_path, "ljspeech")
        audioIn_dir_path = os.path.join(dataset_dir_path, "wavs")
        textIn_path = os.path.join(dataset_dir_path, "metadata.csv")

    audioOut_dir_path = os.path.join(data_dir_path, "wavs_16kHz") # audio
    textOut_path = os.path.join(data_dir_path, "sentence.txt") # text
    dictOut_path = os.path.join(data_dir_path, "bu_radio_dict.txt") # dictionary
    labOut_dir_path = os.path.join(output_dir_path, "Mfa_Label")

    Directory_Making(output_dir_path, data_dir_path, labOut_dir_path, audioOut_dir_path)
    Txet_Normalizatopn(dataset_id, textIn_path, textOut_path) ## generate TextOut
    Wav16kHz_Generation(dataset_id, audioIn_dir_path, audioOut_dir_path)
    Dictionary_Generation(textOut_path, dictIn_path, dictOut_path)
    Convert2MfaLabel(dataset_id, labOut_dir_path, textOut_path, audioOut_dir_path)
