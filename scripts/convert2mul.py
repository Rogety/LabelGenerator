import os
import re
from g2p_en import G2p
import nltk
import textgrid
import cmudict

def gen_mul_output(filepath,pstart, pend, phone, word, pos, w_index, syl_index, stress, before_punctuation, after_punctuation):

    #print(w_index,len(w_index))

    #if len(pos) != len(word):
        #print(word,len(word))
        #print(pos,len(pos))
        #print(stress,len(stress))
    # print("word :",word,len(word))
    # print("w_index :",w_index)

    #print(pos)

    with open(filepath,"w") as fout:
        j,k,m,n = 0,0,0,0
        for i in range(len(pstart)-1):
            fout.write(str(pstart[i]) + " ")
            fout.write(str(pend[i]) + " ")
            fout.write(phone[i] + " ")

            if k < len(syl_index):
                if i == syl_index[k] :
                    fout.write(stress[k]+" ")
                    k += 1

            if j <  len(word):
                if i == w_index[j] :
                    fout.write(word[j]+" ")
                    #index = word[j].lower()
                    index = word[j]
                    fout.write(pos[index]+" ")

                    if n <  len(before_punctuation)+1:
                        try :
                            if word[j] == before_punctuation[n][0]:
                                fout.write("1 ")
                                fout.write(before_punctuation[n][1]+" ")
                                n += 1
                            else :
                                fout.write("0 ")
                        except IndexError:
                            fout.write("0 ")
                    if m <  len(after_punctuation)+1:
                        #print(after_punctuation[m][0],after_punctuation[m][1])
                        try :
                            if word[j] == after_punctuation[m][0]: #?
                                fout.write("1 ")
                                fout.write(after_punctuation[m][1]+" ")
                                m += 1
                            else :
                                fout.write("0 ")
                        except IndexError:
                            fout.write("0 ")
                    j += 1

            fout.write("\n")
    # print("phone :",phone)
    print("gen_mul_output :",filepath)
    return 0

def compare(bu_dict, cmu_dict):
    catch = 0
    # print("bu_dict :",bu_dict)
    # print("cmu_dict :",cmu_dict)

    a = re.sub(r'[\W+\d]',"",bu_dict)
    b = re.sub(r'[\W+\d]',"",cmu_dict)
    #b = cmu_dict.copy()

    #print(a , b)
    if a == b :
        return 1


    return catch

def syl_info(lab_filepath, text_path, syl_dict_path, filename, word_list_with_character, pstart, word_index, word_with_phone):


    #pattern = r'[ab]\d{4}'
    string = re.search(filename,lab_filepath).group(0)

    #g2p = G2p()

    with open(text_path,"r") as texts :
        for line in texts:
            if string in line:
                line  = line.replace("-"," ") ## for "-" word
                pattern_sen = r'\"(.*)+\"'
                content = re.search(pattern_sen,line).group(0).strip('"')
                #print("content :",content)
                #out = "".join(g2p(content))
                #print("out :",out)


    sentense = content
    sentense = sentense.replace(","," ,")
    sentense = sentense.replace("."," .")
    sentense = sentense.replace(";"," ;")
    #sentense_with_phone = out
    #print("sentense :",sentense)
    #print("sentense_with_phone :",sentense_with_phone)
    #print("word_with_phone :",word_with_phone)
    #print("word_list_with_character :",word_list_with_character)

    #word_list_with_phone = "".join(filter(lambda x: x not in [',', '.',';'], sentense_with_phone))
    #word_list_with_phone = word_list_with_phone.split(" ")
    #word_list_with_phone = [a for a in word_list_with_phone if len(a) > 0]


    syl_dict = []
    with open(syl_dict_path,"r") as texts:
        for line in texts :
            try :
                word = line.split(" ",1)[0]
                syl_phone = line.split(" ",1)[1].strip("\n")
                syl_dict.append((word,syl_phone))
            except IndexError: ## last line
                pass

    # print("word_with_phone :",word_with_phone, len(word_with_phone))
    #print("word_list_with_character :",word_list_with_character, len(word_list_with_character))
    #word_list_with_phone = [x for x in word_list_with_phone if x != "'"]

    wordindex_with_multiple_syl = []
    syl_list_with_phone = []
    for i in range(len(word_list_with_character)):
        for word , syl in syl_dict :
            if word_list_with_character[i] == word :
                #print(word,word_list_with_character[i])
                if compare(syl, word_with_phone[i]):
                    ## syllable
                    #print("syl:",syl,word_list_with_phone[i])
                    syla = syl.replace(" ","")
                    if "-" in syla :
                        tmp = syla.split("-")
                        for item in tmp:
                            syl_list_with_phone.append(item)
                    else :
                        syl_list_with_phone.append(syla)
                    #print("match :" ,syla)

                    ## multiple_syl
                    if "-" in syl :
                        tmp_list = []
                        tmp = syl.split("-")
                        for item in tmp:
                            length = item.split(" ")
                            length = [a for a in length if len(a) > 0]
                            tmp_list.append((i,len(length)))
                        tmp_list.pop(-1) ## delete last item
                        wordindex_with_multiple_syl.append(tmp_list)
    # print("syl_list_with_phone :",syl_list_with_phone,len(syl_list_with_phone))
    ## syl_index
    #print("word_index :",word_index,len(word_index))
    #print("wordindex_with_multiple_syl :",wordindex_with_multiple_syl,len(wordindex_with_multiple_syl))
    syl_index = word_index.copy()
    total_length, new_index = 0, 0
    for i in range(len(wordindex_with_multiple_syl)):
        for idx, length in wordindex_with_multiple_syl[i] :
            total_length += length
            new_index = (total_length + syl_index[idx])
            syl_index.append(new_index)
        total_length,new_index = 0,0
    syl_index = sorted(list(set(syl_index)))

    #print("syl_index :",syl_index,len(syl_index))


    # print("syl_index :",syl_index, len(syl_index))
    # print("word_index :",word_index, len(word_index))
    #print("syl_list_with_phone :",syl_list_with_phone,len(syl_list_with_phone))

    ## stress
    stress = []
    pattern = r'\d'
    for syl in syl_list_with_phone:
        stress.append(re.search(pattern,syl).group(0))

    #print("stress :",stress, len(stress))


    ## punctulization
    sentense = sentense.split(" ")
    #word_list_with_phone = [x for x in word_list_with_phone if x != "'"]
    #print("sentense_with_phone",sentense_with_phone)
    #print("sentense",sentense)
    #print("word_list_with_phone",word_list_with_phone)
    #print("sentense :",sentense)
    ## before
    before_punctuation = []
    for idx in range(1,len(sentense)):
        if sentense[idx-1] == "," or sentense[idx-1] == "." or sentense[idx-1] == ";":
            before_punctuation.append( [sentense[idx].upper(),sentense[idx-1].upper()] )
    for i in range(len(word_list_with_character)):
        for idx , (word , punc) in enumerate(before_punctuation) :
            if word_with_phone[i] == word :
                before_punctuation[idx][0] = word_index[i]

    #print("before_punctuation :",before_punctuation)
    ## after
    #print("sentense :",sentense)
    #print("word_list_with_phone :",word_list_with_phone)
    after_punctuation = []
    for idx in range(0,len(sentense)-1):
        if sentense[idx+1] == "," or sentense[idx+1] == "." or sentense[idx+1] == ";":
            after_punctuation.append( [sentense[idx].upper(),sentense[idx+1].upper()] )
    for i in range(len(word_list_with_character)):
        for idx , (word , punc) in enumerate(after_punctuation) :
            if word_with_phone[i] == word :
                after_punctuation[idx][0] = word_index[i]

    #print("after_punctuation :",after_punctuation)


    # print("word_index",word_index)
    # print("before_punctuation :",before_punctuation)
    # print("after_punctuation :",after_punctuation)
    # print("word_list_with_phone :",word_list_with_phone)

    return syl_index, stress, before_punctuation, after_punctuation


def POS_tagging(words):
    #print("POS_tagging : ")
    pos_dict = {}

    ## 's postag handle '
    for word in words:
        #word = word.lower()
        if "'s" in word :
            pos_dict[word] = "PRP"
    ## pos_tag word list = ["word1", "word2", ... , "wordN"]
    out = nltk.pos_tag(words)
    for i in range(len(out)):
        pos_dict[out[i][0]] = out[i][1]

    '''
    with open(filepath,"r") as texts:
        for text in texts:
            text = text.lower()
            if "'s" in text :
                words = text.split(" ")
                for word in words:
                    if "'s" in word :
                        pos_dict[word] = "PRP"
            text = nltk.word_tokenize(text)
            out = nltk.pos_tag(text)
            #print("out :",out)
            for i in range(len(out)):
                pos_dict[out[i][0]] = out[i][1]
    # print("pos_dict :",pos_dict)
    '''
    pos_dict["i'm"] = "PRP"
    pos_dict["you're"] = "PRP"
    pos_dict["we're"] = "PRP"

    pos_dict["you've"] = "PRP"
    pos_dict["i've"] = "PRP"
    pos_dict["we've"] = "PRP"

    pos_dict["i'll"] = "PRP"
    pos_dict["we'll"] = "PRP"
    pos_dict["you'll"] = "PRP"
    pos_dict["he'll"] = "PRP"
    pos_dict["that'll"] = "PRP"

    pos_dict["don't"] = "PRP"
    pos_dict["won't"] = "PRP"
    pos_dict["can't"] = "PRP"
    pos_dict["weren't"] = "PRP"
    pos_dict["didn't"] = "PRP"
    pos_dict["wasn't"] = "PRP"
    pos_dict["doesn't"] = "PRP"
    pos_dict["hadn't"] = "PRP"
    pos_dict["wouldn't"] = "PRP"
    pos_dict["couldn't"] = "PRP"
    pos_dict["shouldn't"] = "PRP"

    pos_dict["she'd"] = "PRP"
    pos_dict["i'd"] = "PRP"

    pos_dict["cannot"] = "PRP"
    pos_dict["march"] = "NN"  ## march 詞性是 $ ?
    pos_dict["october"] = "NN"  ## march 詞性是 $ ?
    pos_dict["oswald"] = "NN"  ## march 詞性是 $ ?
    pos_dict["williams'"] = "PRP"
    pos_dict["burgess'"] = "PRP"

    '''
    pos_dict["esquire"] = "PRP"
    pos_dict["company"] = "NN"
    pos_dict["mister"] = "NN"
    pos_dict["junior"] = "NN"
    pos_dict["doctor"] = "NN"
    pos_dict["sergeant"] = "NN"
    pos_dict["limited"] = "NN"
    pos_dict["fort"] = "NN"
    '''

    return pos_dict

def matchphone(pstart,wstart,word):


    w_index = []
    for i in range(len(pstart)):
        if pstart[i] in wstart  :
            w_index.append(i)


    return w_index

def g2p_word(phone,pstart,pend,word,wstart,wend,filename):

    word_with_phone = []
    # print(wstart)
    # print(pstart)
    j = 0
    for i in range(len(wstart)):
        for j in range(len(pstart)):
            if wstart[i] == pstart[j] :
                k = j
                string = ""
                while(wend[i] != pend[k]):
                    string += phone[k]
                    k +=1
                if wend[i] == pend[k]:
                    if phone[k] != "sp":
                        string += phone[k]
                word_with_phone.append(string)

    if len(word) != len(word_with_phone):
        print("g2p_word error :",filename)

    return word_with_phone

def time_convert2string(pstart, pend, wstart, wend):

    ## time * 10**7
    t = 10**5
    pstart = [ round(x*100)*t for x in pstart]
    pend = [ round(x*100)*t for x in pend]
    wstart = [ round(x*100)*t for x in wstart]
    wend = [ round(x*100)*t for x in wend]

    pstart = [ "{}".format(x) for x in pstart]
    pend = [ "{}".format(x) for x in pend]
    wstart = [ "{}".format(x) for x in wstart]
    wend = [ "{}".format(x) for x in wend]

    return pstart, pend, wstart, wend

def modify_word_start(wstart):

    wstart[0] = 0.02

    return wstart

def modify_first_sp(pstart,pend,phone):

    s0 = pstart[0]
    s1 = pstart[0] + 0.02

    e0 = pstart[0] + 0.02
    e1 = pend[0]

    p0 = "sil"
    p1 = phone[0]

    pstart.pop(0)
    pend.pop(0)
    phone.pop(0)

    pstart.insert(0,s1)
    pstart.insert(0,s0)

    pend.insert(0,e1)
    pend.insert(0,e0)

    phone.insert(0,p1)
    phone.insert(0,p0)


    return pstart, pend, phone


def modify_last_sp(pstart,pend,phone):


    s0 = pstart[-2]
    s1 = pstart[-2] + 0.05 ## 之後再改吧 先設0.08
    s2 = pstart[-1]

    e0 = s1
    e1 = pend[-2]
    e2 = pend[-1]

    p0 = phone[-2]
    p1 = "sp"
    p2 = phone[-1]

    pstart.pop(-1)
    pstart.pop(-1)
    pend.pop(-1)
    pend.pop(-1)
    phone.pop(-1)
    phone.pop(-1)

    pstart.extend([s0,s1,s2])
    pend.extend([e0,e1,e2])
    phone.extend([p0,p1,p2])

    '''
    s0 = pstart[-2]
    s1 = pstart[-1]

    e0 = pend[-2]
    e1 = round(pend[-1],2)

    p0 = phone[-2]
    p1 = phone[-1]
    if p1 == "None" :
        p1 = "sp"


    pstart[-2:] = [s0,s1]
    pend[-2:] = [e0,e1]
    phone[-2:] = [p0,p1]
    '''
    return pstart, pend, phone

def parse_Interval(IntervalObject):
    start_time = ""
    end_time = ""
    P_name = ""

    ind = 0
    str_interval = str(IntervalObject)
    for ele in str_interval:
        if ele == "(":
            ind = 1
        if ele == " " and ind == 1:
            ind = 2
        if ele == "," and ind == 2:
            ind = 3
        if ele == " " and ind == 3:
            ind = 4

        if ind == 1:
            if ele != "(" and ele != ",":
                start_time = start_time + ele
        if ind == 2:
            end_time = end_time + ele
        if ind == 4:
            if ele != " " and ele != ")":
                P_name = P_name + ele

    st = float(start_time)
    et = float(end_time)
    pn = P_name

    #return {pn: (st, et)}
    return  st, et, pn

def parse_textgrid(filename):
    pattern = r'[a-zA-z]+'
    tg = textgrid.TextGrid.fromFile(filename)
    list_words = tg.getList("words")
    list_phones = tg.getList("phones")
    phones_list = list_phones[0]
    words_list = list_words[0]

    pstart, pend, phone = [],[],[]
    wstart, wend, word = [],[],[]
    for ele in phones_list:
        st, et, pn = parse_Interval(ele)
        pstart.append(st)
        pend.append(et)
        phone.append(re.search(pattern,pn).group(0))

    for ele in words_list:
        st, et, wd = parse_Interval(ele)
        if wd != 'None':
            wstart.append(st)
            wend.append(et)
            word.append(wd.upper())


    ## last sp doesn't align


    # for i in range(len(phone)):
    #     print(phone[i],pstart[i],pend[i])

    if phone[-2] != "sp":
        pstart,pend,phone = modify_last_sp(pstart,pend,phone)
    if phone[-2] != "sp":
        print("error : last sp error",filename)

    ## firsr sil doesn't allign
    if phone[0] != "sil":
        pstart,pend,phone = modify_first_sp(pstart,pend,phone)
        wstart = modify_word_start(wstart)
    if phone[0] != "sil":
        print("error : first sil error",filename)

    pstart, pend, wstart, wend = time_convert2string(pstart, pend, wstart, wend)


    if len(pstart) != len(phone) or len(pend) != len(phone):
        print("error : phone not match error",filename)
    if len(wstart) != len(word) or len(wend) != len(word):
        print("error : word not match error",filename)

    '''
    result = phone_check_unit_test(phone,filename)
    if result != True:
        print("g2p phone not match",filename)

    num_word_and_phone_unit_test(pstart, pend, phone, wstart, wend, word, filename)
    '''


    word_with_phone = g2p_word(phone,pstart,pend,word,wstart,wend,filename)

    w_index = matchphone(pstart,wstart,word)
    pos = POS_tagging(word)

    # print("pstart : ", pstart, len(pstart))
    # print("pend : ", pend, len(pend))
    # print("phone : ", phone, len(phone))
    # print("wstart : ", wstart, len(wstart))
    # print("wend : ", wend, len(wend))
    # print("word : ", word, len(word))
    # print("word_with_phone : ", word_with_phone, len(word_with_phone))
    # print("w_index : ", w_index, len(w_index))
    # print("pos: ", pos, len(pos))

    return pstart, pend, phone, wstart, wend, word, word_with_phone, w_index, pos


def TextinfoGet(textIn_path):

    pattern = r'\"(.*)\"'
    filenames = []
    sentences = []
    textInfo = []
    with open(textIn_path, encoding='utf-8') as f:
        for line in f:
            textInfo.append([line.split(" ")[0], re.search(pattern, line).group(0).strip('"')])

    return textInfo

def Mul_Generation(textIn_path, mulOut_dir_path, dictIn_path):

    textInfos = TextinfoGet(textIn_path)

    for textInfo in textInfos :

        filename = textInfo[0]
        sentence = textInfo[1]

        mulOut_path = os.path.join(mulOut_dir_path, filename+".mul")
        textgridIn_path = os.path.join(textgridIn_dir_path, filename+".TextGrid")
        mfalabIn_path = os.path.join(mfalabIn_dir_path, filename+".lab")


        pstart, pend, phone, wstart, wend, word, word_with_phone, w_index, pos = parse_textgrid(textgridIn_path)



        syl_index, stress, before_punctuation, after_punctuation = \
        syl_info(mfalabIn_path, textIn_path, dictIn_path, filename, word, pstart, w_index, word_with_phone)


        gen_mul_output(mulOut_path,pstart,pend,phone,word,pos,w_index,syl_index,stress,before_punctuation,after_punctuation)

    return 0

def Directory_Making(mulOut_dir_path):

    if not os.path.isdir(mulOut_dir_path):
        os.mkdir(mulOut_dir_path)


    return 0

if __name__ == '__main__':


    dataset_dir_path = os.path.expanduser("~/Desktop/project/EA_V2/dataset/")
    input_dir_path = os.path.expanduser("~/Desktop/project/EA_V2/input/")

    data_dir_path = os.path.join(input_dir_path, "data")
    mfalabIn_dir_path = os.path.join(input_dir_path, "Mfa_Label")
    mulOut_dir_path = os.path.join(input_dir_path, "Gen_Mul")
    dictIn_path = os.path.join(dataset_dir_path, "bu_radio_dict_with_syl.txt")
    textgridIn_dir_path = os.path.join(input_dir_path, "Mfa_TextGrid", "Mfa_Label")
    textIn_path = os.path.join(data_dir_path, "sentence.txt")

    Directory_Making(mulOut_dir_path)
    Mul_Generation(textIn_path, mulOut_dir_path, dictIn_path)
