import os
import re

def list_shift(listP , direction , count , _type_):

    if direction == "right":
        if count == 1:
            listP.pop(-1) ##pop() : 預設是刪掉最後一個
            listP.insert(0 , '0' )
        elif count == 2:
            listP.pop(-1)
            listP.pop(-1)
            listP.insert(0 , '0' )
            listP.insert(0 , '0' )
    elif direction == "left":
        if count == 1:
            listP.pop(0)
            listP.insert(len(listP) , '0' )
            ##listP.insert(-1 , '0' ) 插入在不對的位置 bug??
        elif count == 2:
            listP.pop(0)
            listP.pop(0)
            listP.insert(len(listP) , '0' )
            listP.insert(len(listP) , '0' )
    elif direction == "previous":
        listP.pop() ##pop() : 預設是刪掉最後一個
        if _type_ == "int":
            listP.insert(0 , 0 )
        elif _type_ == "char":
            listP.insert(0 , '0' )
    elif direction == "next":
        listP.pop(0)
        if _type_ == "int":
            listP.insert(len(listP) , 0 )
        elif _type_ == "char":
            listP.insert(len(listP) , '0' )
    else:
        print("arguments error")

    #print("listP = ",listP)
    return listP

def Get_text(filepath):

    text = []
    with open(filepath , "r+") as f :
        for line in f:
            line = line.split(" ")
            del line[-1]  # 去除"\n"
            text.append(line)
            #print(line)

    return text

def Get_word_list(text,syllable_start,word_start,sentence_start,
                  phone_num_in_syllable,phone_num_in_word,phone_num_in_sentence):
    #print("\t\t\tGet_word_list\t\t\t")
    phone_list,syllable_list,word_list,sentence_list = [], [], [], []

    ##phone_list
    for i in range(len(text)):
        phone_list.append(text[i][2])

    ##syllable_list
    m=0
    for i in range(len(phone_list)):
        if i == syllable_start[m]:
            n = phone_num_in_syllable[m]
            tmp_syl = ""
            for k in range(0,n):
                tmp_syl += phone_list[i+k]
            syllable_list.append(tmp_syl)
            m=m+1
        if m == len(syllable_start):
            break

    ##word_list
    m=0
    for i in range(len(phone_list)):
        if i == word_start[m]:
            n = phone_num_in_word[m]
            tmp_word = ""
            for k in range(0,n):
                tmp_word += phone_list[i+k]
            word_list.append(tmp_word)
            m=m+1
        if m == len(word_start):
            break

    ##sentence_list
    m=0
    for i in range(len(phone_list)):
        if i == sentence_start[m]:
            n = phone_num_in_sentence[m]
            tmp_sentence = ""
            for k in range(0,n):
                tmp_sentence += phone_list[i+k]
            sentence_list.append(tmp_sentence)
            m=m+1
        if m == len(sentence_start):
            break

    #print("phone_list =",phone_list,len(phone_list))
    #print("syllable_list =",syllable_list,len(syllable_list))
    #print("word_list =",word_list,len(word_list))
    #print("sentence_list =",sentence_list,len(sentence_list))

    return phone_list,syllable_list,word_list,sentence_list

def Get_phone_num(text):
    #print("\t\t\tGet_phone_num\t\t\t")

    phone_num_in_syllable,phone_num_in_word,phone_num_in_sentence = [],[],[]

    text_tmp = []
    for line in text:
        if line[2] != 'sil' and line[2] != 'sp':
            text_tmp.append(line)

    syl_start,word_start,sentence_start = [],[],[]

    #print("text_tmp :",text_tmp)
    sentence_start.append(0)
    for i in range(len(text_tmp)):
        if len(text_tmp[i]) > 4:
            word_start.append(i)
            if text_tmp[i][7] == ',' and (i != 0):
                sentence_start.append(i)

        if len(text_tmp[i]) > 3:
            syl_start.append(i)



    # print(word_start,len(word_start))
    # print(syl_start,len(syl_start))
    # print(sentence_start,len(sentence_start))

    for i in range(len(word_start)):
        try:
            phone_num_in_word.append(word_start[i+1] - word_start[i])
        except IndexError:
            phone_num_in_word.append(len(text_tmp) - word_start[i])

    for i in range(len(syl_start)):
        try:
            phone_num_in_syllable.append(syl_start[i+1] - syl_start[i])
        except IndexError:
            phone_num_in_syllable.append(len(text_tmp) - syl_start[i])


    for i in range(len(sentence_start)):
        try:
            phone_num_in_sentence.append(sentence_start[i+1] - sentence_start[i])
        except IndexError:
            phone_num_in_sentence.append(len(text_tmp) - sentence_start[i])

    phone_num_in_utterance = [sum(phone_num_in_sentence)]



    # print(phone_num_in_word , len(phone_num_in_word))
    # print(phone_num_in_syllable , len(phone_num_in_syllable))
    # print(phone_num_in_sentence , len(phone_num_in_sentence))

    return phone_num_in_syllable,phone_num_in_word,phone_num_in_sentence,phone_num_in_utterance


def Get_syllable_num(phone_num_in_syllable,phone_num_in_word,phone_num_in_sentence):
    #print("\t\t\tGet_syllable_num\t\t\t")

    syllable_num_in_word,syllable_num_in_sentence,syllable_num_in_utterance =[],[],[]

    # print(phone_num_in_word , len(phone_num_in_word))
    # print(phone_num_in_syllable , len(phone_num_in_syllable))
    # print(phone_num_in_sentence , len(phone_num_in_sentence))

    ##
    k=0
    for val in phone_num_in_word:
        tmp,count = 0,0
        if val == phone_num_in_syllable[k]:
            syllable_num_in_word.append(1)
            k += 1
        else:
            while( tmp != val ):
                tmp += phone_num_in_syllable[k]
                k += 1
                count += 1
            syllable_num_in_word.append(count)

    ##
    k=0
    for val in phone_num_in_sentence:
        tmp,count = 0,0
        if val == phone_num_in_syllable[k]:
            syllable_num_in_sentence.append(1)
            k += 1
        else:
            while( tmp != val ):
                tmp += phone_num_in_syllable[k]
                k += 1
                count += 1
            syllable_num_in_sentence.append(count)

    ##
    syllable_num_in_utterance.append(len(phone_num_in_syllable))


    # print("syllable_num_in_word = ",syllable_num_in_word,len(syllable_num_in_word))
    # print("syllable_num_in_sentence = ",syllable_num_in_sentence,len(syllable_num_in_sentence))
    # print("syllable_num_in_utterance = ",syllable_num_in_utterance,len(syllable_num_in_utterance))


    return syllable_num_in_word,syllable_num_in_sentence,syllable_num_in_utterance

def Get_word_num(phone_num_in_word,phone_num_in_sentence):

    word_num_in_sentence,word_num_in_utterance = [],[]
    # print(phone_num_in_word)
    # print(phone_num_in_sentence)

    k=0
    for val in phone_num_in_sentence:
        tmp,count = 0,0
        if val == phone_num_in_word[k]:
            word_num_in_sentence.append(1)
            k += 1
        else:
            while( tmp != val ):
                tmp += phone_num_in_word[k]
                k += 1
                count += 1
            word_num_in_sentence.append(count)

    word_num_in_utterance.append(len(phone_num_in_word))

    # print("word_num_in_sentence = ",word_num_in_sentence,len(word_num_in_sentence))
    # print("word_num_in_utterance = ",word_num_in_utterance,len(word_num_in_utterance))


    return word_num_in_sentence,word_num_in_utterance

def Get_sentence_num(phone_num_in_sentence):

    sentence_num_in_utterance = []

    sentence_num_in_utterance.append(len(phone_num_in_sentence))

    # print("sentence_num_in_utterance = ",sentence_num_in_utterance,len(sentence_num_in_utterance))

    return sentence_num_in_utterance

def Get_start_stamp(text):
    #print("\t\t\tGet_start_stamp\t\t\t")
    line_count = []
    phone_start = []
    syllable_start,word_start,sentence_start = [],[],[]
    utterance_start = [1]

    for line in text :
        line_count.append(len(line))

        #print(line)

    #print(line_count , len(line_count))

    for i in range(len(text)):
        if text[i][2] != 'sil' and text[i][2] != 'sp':
            phone_start.append(i)

    for i in range(len(line_count)):
        if line_count[i] > 4 :
            word_start.append(i)
        if line_count[i] > 3 :
            syllable_start.append(i)


    sentence_start.append(1)
    for i in range(len(text)):
        if line_count[i] > 4 :
            if text[i][7] == ',' and (i != 1):
                sentence_start.append(i)

    #print(phone_start , len(phone_start))

    return phone_start,syllable_start ,word_start , sentence_start,utterance_start


def Get_time(text):

    #print("\t\t\tGet_time\t\t\t")
    start , end = [] , []

    for line in text :
        start.append(line[0])
        end.append(line[1])



    return start , end

def Get_stress_info(text):
    #print("\t\t\tGet_stress_info\t\t\t")
    stress_index,stress_count,stress_tag = [],[],[]

    ##stress_index =sylstart

    for line in text :
        try :
            stress_tag.append(line[3])
            if line[3] == '2':  ##
                stress_count.append('1')
            else:
                stress_count.append(line[3])

        except :
            pass


    return stress_index,stress_count,stress_tag

def Get_GPOS_info(text):
    #print("\t\t\tGet_GPOS_info\t\t\t")
    GPOS_list = []

    for line in text:
        if len(line) > 6:
            GPOS_list.append(line[5].lower())

    return GPOS_list

def Generate_single_label(text,target_list,syllable_start,word_start,sentence_start,utterance_start, _type_):

    label = []
    k=0
    if _type_ == "int":
        val = 0
    elif _type_ == "char":
        val = '0'

    if syllable_start != [] and word_start == [] and sentence_start == [] :
        for i in range(len(text)):
            if i == syllable_start[k]:
                val = target_list[k]
                k += 1
                if k == len(syllable_start):
                    k = len(syllable_start)-1

            if text[i][2] == 'sp' or text[i][2] == 'sil':
                label.append('0')
            else:
                label.append(val)

    if word_start != [] and syllable_start == [] and sentence_start == []:
        for i in range(len(text)):
            if i == word_start[k]:
                val = target_list[k]
                k += 1
                if k == len(word_start):
                    k = len(word_start)-1

            if text[i][2] == 'sp' or text[i][2] == 'sil':
                label.append('0')
            else:
                label.append(val)

    if sentence_start != [] and syllable_start == [] and word_start == []:
        for i in range(len(text)):
            if i == sentence_start[k]:
                val = target_list[k]
                k += 1
                if k == len(sentence_start):
                    k = len(sentence_start)-1

            if text[i][2] == 'sp' or text[i][2] == 'sil':
                label.append('0')
            else:
                label.append(val)

    if utterance_start:
        for i in range(len(text)):
            if i == utterance_start[k]:
                val = target_list[k]
                k += 1
                if k == len(utterance_start):
                    k = len(utterance_start)-1

            if text[i][2] == 'sp' or text[i][2] == 'sil':
                label.append('0')
            else:
                label.append(val)


    return label

def Generate_position_label(text,target_list,start_short,strat_long):

    label_forward,label_backward = [],[]

    k = 0
    m = 0
    forward = 0
    backward = 0

    for i in range(len(text)):
        if i == strat_long[k]:
            forward = 0
            backward = target_list[k]+1 ## not good expression
            k += 1
            if k == len(strat_long):
                k = len(strat_long)-1

        if i == start_short[m]:
            forward += 1
            backward -= 1
            m += 1
            if m == len(start_short):
                m = len(start_short)-1

        if text[i][2] == 'sp' or text[i][2] == 'sil':
            label_forward.append('0')
            label_backward.append('0')
        else:
            label_forward.append(forward)
            label_backward.append(backward)



    return label_forward , label_backward

def xxx_num_before_curent_xxx_in_sentence(text,target_list,start_short,start_long):

    label = []
    k,m,count=0,0,0
    for i in range(len(text)):
        if i == start_short[k]:
            count += int(target_list[k])
            k += 1
            if k == len(start_short):
                k = len(start_short)-1

        if i == start_long[m]:  ## sentence中在第一個syllable 一定是0個 stressed syllable
            count = 0
            m += 1
            if m == len(start_long):
                m = len(start_long)-1

        if text[i][2] == 'sil' or text[i][2] == 'sp':
            label.append('0')
        else :
            label.append(count)


    return label

def xxx_num_after_curent_xxx_in_sentence(text,target_list_short,target_list_long,start_short,start_long):

    label = []
    k,m,count=0,0,0
    for i in range(len(text)):
        if i == start_long[m]:
            count = target_list_long[m]
            m += 1
            if m == len(start_long):
                m = len(start_long)-1

        if i == start_short[k]:
            count -= int(target_list_short[k])
            k += 1
            if k == len(start_short):
                k = len(start_short)-1

        if text[i][2] == 'sil' or text[i][2] == 'sp':
            label.append('0')
        else :
            label.append(count)

    #print("stress_num :", target_list_long , len(target_list_long))
    #print("stress_count :", target_list_short , len(target_list_short))
    #print("sentence_start : " , start_long , len(sentence_start))
    #print("syllable_start : " , start_short , len(syllable_start))

    return label

def expand_label(text,start_short,target):
    label = []
    count,k=0,0
    for i in range(len(text)):
        if i == start_short[k]: ## 每個音節的開始索引
            count = target[k]
            k += 1
            if k == len(start_short): # prevent IndexError
                k = len(start_short)-1

        if text[i][2] == 'sil' or text[i][2] == 'sp':
            label.append('0')
        else :
            label.append(count)

    return label

def xxx_num_from_previous_xxx_to_current_xxx(text,target_list_short,target_list_long,start_short,start_long):
    label = []
    # print("text :",text)
    # print("target_list_short :",target_list_short,len(target_list_short))
    # print("target_list_long :",target_list_long)
    # print("start_short :",start_short,len(start_short))
    # print("start_long :",start_long)
    # print("target_list_long :",target_list_long)

    syl_in_pre_stressed_syl_and_cur_syl = []
    syl_in_cur_syl_and_next_stressed_syl = []

    for  i in range(len(target_list_short)):
        f=i
        b=i
        count_f=0
        count_b=0

        try :
            if target_list_short[f+1] != '1':
                count_f=0
            while  target_list_short[f+1] != '1':
                count_f += 1
                f += 1
        except IndexError :
            pass

        if i != 0 :
            try :

                while target_list_short[b-1] != '1':
                    count_b += 1
                    b -= 1
                if target_list_short[b-1] != '1':
                    count_b=0
            except IndexError :
                pass
        else :
            count_b = 0

        syl_in_pre_stressed_syl_and_cur_syl.append(count_b)
        syl_in_cur_syl_and_next_stressed_syl.append(count_f)

    # print("syl_in_pre_stressed_syl_and_cur_syl :",syl_in_pre_stressed_syl_and_cur_syl)
    # print("syl_in_cur_syl_and_next_stressed_syl :",syl_in_cur_syl_and_next_stressed_syl)

    b7 = expand_label(text,start_short,syl_in_pre_stressed_syl_and_cur_syl)
    b8 = expand_label(text,start_short,syl_in_cur_syl_and_next_stressed_syl)


    return b7, b8

def xxx_num_from_current_xxx_to_next_xxx(text,target_list_short,target_list_long,start_short,start_long):
    label = []

    count,k=0,0
    for i in range(len(text)):
        if i == start_short[k]:
            n = k + 1 ## N = index
            count = 0
            if n == len(target_list_short):
                n = len(target_list_short) - 1
            try :
                while target_list_short[n] != '1' :
                    n = n + 1
                    count += 1
            except :
                pass

            k += 1
            if k == len(start_short):
                k = len(start_short)-1

        if text[i][2] == 'sil' or text[i][2] == 'sp':
            label.append('0')
        else :
            label.append(count)
    return label


## return phone lab string
class PHONE_LABEL():
    def __init__(self):
        self.LL_phone = []
        self.L_phone = []
        self.C_phone = []
        self.R_phone = []
        self.RR_phone = []
        self.string = ""
        self.out = []
        self.symbol =['/A:','^','-','+','+','/B:']

    def Get_label(self,text,last=False):

        for line in text :
            if line[2] == 'sil':
                self.C_phone.append('sil')
            elif line[2] == 'sp':
                self.C_phone.append('sp')
            else :
                self.C_phone.append(line[2].lower())
        ##P3 = self.C_phone.copy()

        self.LL_phone = list_shift(self.C_phone.copy() , "right" , 2 , _)
        self.L_phone = list_shift(self.C_phone.copy() , "right" , 1 , _)
        self.R_phone = list_shift(self.C_phone.copy() , "left" , 1 , _)
        self.RR_phone = list_shift(self.C_phone.copy() , "left" , 2 , _)
        ##P6,P7 = Generate_position_label(phone_num_in_syllable,phone_start,syllable_start)

        for i in range(len(self.C_phone)):
            if last == True :
                self.string = self.symbol[0]+self.LL_phone[i] \
                            +self.symbol[1]+self.L_phone[i] \
                            +self.symbol[2]+self.C_phone[i] \
                            +self.symbol[3]+self.R_phone[i] \
                            +self.symbol[4]+self.RR_phone[i]+self.symbol[5]
            else :
                self.string = self.symbol[0]+self.LL_phone[i] \
                            +self.symbol[1]+self.L_phone[i] \
                            +self.symbol[2]+self.C_phone[i] \
                            +self.symbol[3]+self.R_phone[i] \
                            +self.symbol[4]+self.RR_phone[i]

            self.out.append(self.string)

        #print(len(self.C_phone) ,len(self.out))
        return self.out

    def Get_label_3(self,text,last):
        self.out=[]
        self.C_phone=[]
        self.L_phone=[]
        self.R_phone=[]
        self.string=[]

        for line in text :
            if line[2] == 'sil':
                self.C_phone.append('sil')
            elif line[2] == 'sp':
                self.C_phone.append('sp')
            else :
                self.C_phone.append(line[2].lower())
        ##P3 = self.C_phone.copy()

        self.L_phone = list_shift(self.C_phone.copy() , "right" , 1 , _)
        self.R_phone = list_shift(self.C_phone.copy() , "left" , 1 , _)

        ##P6,P7 = Generate_position_label(phone_num_in_syllable,phone_start,syllable_start)

        for i in range(len(self.C_phone)):
            if last == True :
                self.string = self.symbol[0]+self.L_phone[i] \
                            +self.symbol[1]+self.C_phone[i] \
                            +self.symbol[2]+self.R_phone[i]+self.symbol[3]
            else :
                self.string = self.symbol[0]+self.L_phone[i] \
                            +self.symbol[1]+self.C_phone[i] \
                            +self.symbol[2]+self.R_phone[i]

            self.out.append(self.string)

        return self.out


    def Get_phone(self):

        return self.C_phone


class SYLLABLE_LABEL():
    def __init__(self):
        self.ph_in_presyl = []
        self.ph_in_cursyl = []
        self.ph_in_nextsyl = []
        self.vowl_cursyl = []
        self.vowel_list = ['AA','AE','AH','AO','AY','AW','EH','ER','EY','IH','IY','OY','UW','UH','OW']
        self.string = ""
        self.out = []
        self.symbol =['/B:','^','+','=','/C:']


    def Get_label(self,text,phone_start,syllable_start,phone_num_in_syllable,stress_count):
        syl_vowel = []
        ##  "S" , "Z" 為了所有格的BUG
        #print(text)
        for line in text:
            if line[2] in self.vowel_list:
                syl_vowel.append(line[2].lower())
        #print("syl_vowel :",syl_vowel,len(syl_vowel))
        #print("syllable_start :",syllable_start,len(syllable_start))
        if len(syl_vowel) != len(syllable_start):
            print("vowl_list_not_enough")


        phone_num_in_previous_syllable = list_shift(phone_num_in_syllable.copy(),"previous", _ , "int")
        stress_count_in_previous_syllable = list_shift(stress_count.copy(),"previous", _ , "char")
        phone_num_in_current_syllable = phone_num_in_syllable.copy()
        stress_count_in_current_syllable = stress_count.copy()
        phone_num_in_next_syllable = list_shift(phone_num_in_syllable.copy(),"next", _ , "int")
        stress_count_in_next_syllable = list_shift(stress_count.copy(),"next", _ , "char" )
        self.ph_in_presyl = Generate_single_label(text,phone_num_in_previous_syllable,syllable_start,_,_,_, "int")
        self.ph_in_cursyl = Generate_single_label(text,phone_num_in_current_syllable,syllable_start,_,_,_, "int")
        self.ph_in_nextsyl = Generate_single_label(text,phone_num_in_next_syllable,syllable_start,_,_,_, "int")
        self.vowl_cursyl = Generate_single_label(text,syl_vowel,syllable_start,_,_,_, "int")

        for i in range(len(self.vowl_cursyl)):
            self.string = self.symbol[0]+str(self.ph_in_presyl[i]) \
                        +self.symbol[1]+str(self.ph_in_cursyl[i]) \
                        +self.symbol[2]+str(self.ph_in_nextsyl[i]) \
                        +self.symbol[3]+str(self.vowl_cursyl[i])
            self.out.append(self.string)

        return self.out

class WORD_LABEL():
    def __init__(self):
        self.syl_in_preword = []
        self.syl_in_curword = []
        self.syl_in_nextword = []
        self.string = ""
        self.out = []
        self.symbol =['/C:','^','=','/D:']

    def Get_label(self,text,word_start,syllable_num_in_word):
        syllable_num_in_previous_word = list_shift(syllable_num_in_word.copy(),"previous", _ , "int" )
        syllable_num_in_current_word = syllable_num_in_word.copy()
        syllable_num_in_next_word = list_shift(syllable_num_in_word.copy(),"next", _ , "int" )
        self.syl_in_preword = Generate_single_label(text, syllable_num_in_previous_word,_ ,word_start, _ ,_, "int")
        self.syl_in_curword = Generate_single_label(text, syllable_num_in_current_word,_ , word_start, _,_, "int")
        self.syl_in_nextword = Generate_single_label(text, syllable_num_in_next_word, _ ,word_start, _ ,_, "int")

        for i in range(len(self.syl_in_preword)):
            self.string = self.symbol[0]+str(self.syl_in_preword[i]) \
                        +self.symbol[1]+str(self.syl_in_curword[i]) \
                        +self.symbol[2]+str(self.syl_in_nextword[i])
            self.out.append(self.string)

        return self.out

class sentence_LABEL():
    def __init__(self):
        self.syl_in_presentence = []
        self.syl_in_cursentence = []
        self.syl_in_nextsentence = []
        self.word_in_presentence = []
        self.word_in_cursentence = []
        self.word_in_nextsentence = []
        self.string = ""
        self.out = []
        self.symbol =['/D:','^','@','-','=','^','/E:']

    def Get_label(self,text,sentence_start,syllable_num_in_sentence,word_num_in_sentence):
        syllable_num_in_previous_sentence = list_shift(syllable_num_in_sentence.copy(),"previous",_,"int")
        word_num_in_previous_sentence = list_shift(word_num_in_sentence.copy() , "previous",_,"int" )
        syllable_num_in_current_sentence = syllable_num_in_sentence.copy()
        word_num_in_current_sentence = word_num_in_sentence.copy()
        syllable_num_in_next_sentence = list_shift(syllable_num_in_sentence.copy(),"next",_,"int")
        word_num_in_next_sentence = list_shift(word_num_in_sentence.copy() , "next",_,"int" )


        self.syl_in_presentence = Generate_single_label(text, syllable_num_in_previous_sentence, _ ,_, sentence_start,_, "int")
        self.word_in_presentence = Generate_single_label(text, word_num_in_previous_sentence, _ ,_, sentence_start ,_, "int")
        self.syl_in_cursentence = Generate_single_label(text, syllable_num_in_current_sentence, _ ,_, sentence_start,_, "int")
        self.word_in_cursentence = Generate_single_label(text, word_num_in_current_sentence, _ ,_, sentence_start ,_, "int")
        self.syl_in_nextsentence = Generate_single_label(text, syllable_num_in_next_sentence,_ ,_, sentence_start,_, "int")
        self.word_in_nextsentence = Generate_single_label(text, word_num_in_next_sentence, _ ,_, sentence_start ,_, "int")

        for i in range(len(text)):
            self.string = self.symbol[0]+str(self.syl_in_presentence[i]) \
                        +self.symbol[1]+str(self.syl_in_cursentence[i]) \
                        +self.symbol[2]+str(self.syl_in_nextsentence[i]) \
                        +self.symbol[3]+str(self.word_in_presentence[i]) \
                        +self.symbol[4]+str(self.word_in_cursentence[i]) \
                        +self.symbol[5]+str(self.word_in_nextsentence[i])
            self.out.append(self.string)

        return self.out

class utterance_LABEL():
    def __init__(self):
        self.syl_in_utterance = []
        self.word_in_utterance = []
        self.sentence_in_utterance = []
        self.string = ""
        self.out = []
        self.symbol =['/E:','$','-','/F:']

    def Get_label(self,text,utterance_start,syllable_num_in_utterance,word_num_in_utterance,sentence_num_in_utterance):
        self.syl_in_utterance = Generate_single_label(text, syllable_num_in_utterance,_ ,_, _,utterance_start, "int")
        self.word_in_utterance = Generate_single_label(text, word_num_in_utterance,_ ,_, _ ,utterance_start, "int")
        self.sentence_in_utterance = Generate_single_label(text, sentence_num_in_utterance,_ ,_, _,utterance_start, "int")

        # print("self.sentence_in_utterance :",self.sentence_in_utterance)
        for i in range(len(text)):
            self.string = self.symbol[0]+str(self.syl_in_utterance[i]) \
                        +self.symbol[1]+str(self.word_in_utterance[i]) \
                        +self.symbol[2]+str(self.sentence_in_utterance[i])
            self.out.append(self.string)

        return self.out

class POS_LABEL():
    def __init__(self):
        self.pos_preword = []
        self.pos_curword = []
        self.pos_nextword = []
        self.string = ""
        self.out = []
        self.symbol =['/F:','#','+','/G:']

    def Get_label(self,text,word_start,GPOS_list):
        GPOS_list_in_previous_word = list_shift(GPOS_list.copy(),"previous", _ , "char")
        GPOS_list_in_current_word = GPOS_list.copy()
        GPOS_list_in_next_word = list_shift(GPOS_list.copy(),"next", _ , "char")
        self.pos_preword = Generate_single_label(text, GPOS_list_in_previous_word,_ ,word_start, _ , _,"char")
        self.pos_curword = Generate_single_label(text, GPOS_list_in_current_word , _, word_start, _,_, "char")
        self.pos_nextword = Generate_single_label(text, GPOS_list_in_next_word,_ ,word_start, _ ,_, "char")

        for i in range(len(text)):
            self.string = self.symbol[0]+str(self.pos_preword[i]) \
                        +self.symbol[1]+str(self.pos_curword[i]) \
                        +self.symbol[2]+str(self.pos_nextword[i])
            self.out.append(self.string)

        return self.out
'''
class STRESS_LABEL():
    def __init__(self):
        self.stress_presyl = []
        self.stress_cursyl = []
        self.stress_nextsyl = []
        self.string = ""
        self.out = []
        self.symbol =['/G:','$','=','/H:']


    def Get_label(self,text,stress_tag):
        stress_tag_in_previous_syllable = list_shift(stress_tag.copy(),"previous", _ , "char")
        stress_tag_in_current_syllable = stress_tag.copy()
        stress_tag_in_next_syllable = list_shift(stress_tag.copy(),"next", _ , "char" )


        self.stress_presyl = Generate_single_label(text,stress_tag_in_previous_syllable,syllable_start,_,_,_, "int")
        self.stress_cursyl = Generate_single_label(text,stress_tag_in_current_syllable,syllable_start,_,_,_, "int")
        self.stress_nextsyl = Generate_single_label(text,stress_tag_in_next_syllable,syllable_start,_,_,_, "int")

        for i in range(len(text)):
            self.string = self.symbol[0]+str(self.stress_presyl[i]) \
                        +self.symbol[1]+str(self.stress_cursyl[i]) \
                        +self.symbol[2]+str(self.stress_nextsyl[i])
            self.out.append(self.string)

        return self.out
'''
class POSITION_LABEL():
    def __init__(self):
        self.p6 = []
        self.p7 = []
        self.b3 = []
        self.b4 = []
        self.b5 = []
        self.b6 = []
        self.e3 = []
        self.e4 = []
        self.h3 = []
        self.h4 = []
        self.string = ""
        self.out = []
        self.symbol =['/G:','$','@','@','$','&','-','&','#','#','/H']

    def Get_label(self,text,phone_start,syllable_start,word_start,sentence_start, \
        phone_num_in_syllable,syllable_num_in_word,syllable_num_in_sentence,word_num_in_sentence,sentence_num_in_utterance):
        word_num_in_current_sentence = word_num_in_sentence.copy()
        self.p6,self.p7 = Generate_position_label(text,phone_num_in_syllable,phone_start,syllable_start)
        self.b3,self.b4 = Generate_position_label(text,syllable_num_in_word,syllable_start,word_start)
        self.b5,self.b6 = Generate_position_label(text,syllable_num_in_sentence,syllable_start,sentence_start)
        self.e3,self.e4 = Generate_position_label(text,word_num_in_current_sentence,word_start,sentence_start)
        self.h3,self.h4 = Generate_position_label(text,sentence_num_in_utterance,sentence_start,utterance_start)
        for i in range(len(text)):
            self.string = self.symbol[0]+str(self.p6[i]) \
                        +self.symbol[1]+str(self.p7[i]) \
                        +self.symbol[2]+str(self.b3[i]) \
                        +self.symbol[3]+str(self.b4[i]) \
                        +self.symbol[4]+str(self.b5[i]) \
                        +self.symbol[5]+str(self.b6[i]) \
                        +self.symbol[6]+str(self.e3[i]) \
                        +self.symbol[7]+str(self.e4[i]) \
                        +self.symbol[8]+str(self.h3[i]) \
                        +self.symbol[9]+str(self.h4[i])
            self.out.append(self.string)

        return self.out

class TONE_LABEL():
    def __init__(self):
        self.b7,self.b8,self.b9,self.b10 = [],[],[],[]
        self.e5,self.e6,self.e7,self.e8 = [],[],[],[]
        self.stress_presyl = []
        self.stress_cursyl = []
        self.stress_nextsyl = []
        self.string = ""
        self.out = []
        #self.symbol =['/I:','-','@','+','@','=','+','$','/J:']
        self.symbol =['/H:','-','@','#','-','#','^','^']



    def Get_label(self,text,syllable_start,word_start,sentence_start,stress_count,syllable_num_in_sentence,word_num_in_sentence,stress_tag):
        stress_count_shift_right = list_shift(stress_count.copy(),"previous", _ , "int" )
        current_syllable_num_in_current_sentence = syllable_num_in_sentence.copy()
        word_num_in_current_sentence = word_num_in_sentence.copy()
        stress_tag_in_previous_syllable = list_shift(stress_tag.copy(),"previous", _ , "char")
        stress_tag_in_current_syllable = stress_tag.copy()
        stress_tag_in_next_syllable = list_shift(stress_tag.copy(),"next", _ , "char" )



        # print("stress_count :",stress_count)
        #b7,b8,b9,b10
        total=0
        stressed_num_in_sentence = []
        for val in current_syllable_num_in_current_sentence:
            count=0
            for i in range(total,total+val):
                count += int(stress_count[i])
            total += val
            stressed_num_in_sentence.append(count)

        sentence_num = len(sentence_start)
        current_syllable_sum_in_current_sentence = []
        sum = 0
        for i in range(0,sentence_num):
            sum += current_syllable_num_in_current_sentence[i]
            current_syllable_sum_in_current_sentence.append(sum)
        current_syllable_sum_in_current_sentence.insert(0,0)

        ##E5,E6,E7,E8

        content_index = []
        for item in GPOS_list:
            if item == 'content':
                content_index.append('1')
            else:
                content_index.append('0')
        content_word_num_in_sentence = []

        total=0
        for val in word_num_in_sentence:
            count=0
            for i in range(total,total+val):
                count += int(content_index[i])
            total += val
            content_word_num_in_sentence.append(count)
        content_index_shift_right = list_shift(content_index.copy(),"previous", _ , "char" )

        sentence_num = len(sentence_start)
        current_word_sum_in_current_sentence = []
        sum = 0
        for i in range(0,sentence_num):
            sum += word_num_in_current_sentence[i]
            current_word_sum_in_current_sentence.append(sum)
        current_word_sum_in_current_sentence.insert(0,0)

        self.stress_presyl = Generate_single_label(text,stress_tag_in_previous_syllable,syllable_start,_,_,_, "int")
        self.stress_cursyl = Generate_single_label(text,stress_tag_in_current_syllable,syllable_start,_,_,_, "int")
        self.stress_nextsyl = Generate_single_label(text,stress_tag_in_next_syllable,syllable_start,_,_,_, "int")

        self.b7 = xxx_num_before_curent_xxx_in_sentence(text,stress_count_shift_right,syllable_start,sentence_start)
        self.b8 = xxx_num_after_curent_xxx_in_sentence(text,stress_count,stressed_num_in_sentence,syllable_start,sentence_start)
        self.b9, self.b10 = xxx_num_from_previous_xxx_to_current_xxx(text,stress_count,current_syllable_sum_in_current_sentence,syllable_start,sentence_start)

        #self.e5 = xxx_num_before_curent_xxx_in_sentence(text,content_index_shift_right,word_start,sentence_start)
        #self.e6 = xxx_num_after_curent_xxx_in_sentence(text,content_index,content_word_num_in_sentence,word_start,sentence_start)
        #self.e7 = xxx_num_from_previous_xxx_to_current_xxx(text,content_index,current_word_sum_in_current_sentence,word_start,sentence_start)
        #self.e8 = xxx_num_from_current_xxx_to_next_xxx(text,content_index,current_word_sum_in_current_sentence,word_start,sentence_start)

        for i in range(len(text)):
            self.string = self.symbol[0]+str(self.stress_presyl[i]) \
                        +self.symbol[1]+str(self.stress_cursyl[i]) \
                        +self.symbol[2]+str(self.stress_nextsyl[i]) \
                        +self.symbol[3]+str(self.b7[i]) \
                        +self.symbol[4]+str(self.b8[i]) \
                        +self.symbol[5]+str(self.b9[i]) \
                        +self.symbol[6]+str(self.b10[i])+self.symbol[7]
                        #+self.symbol[4]+str(self.e5[i]) \
                        #+self.symbol[5]+str(self.e6[i]) \
                        #+self.symbol[6]+str(self.e7[i]) \

            self.out.append(self.string)

        return self.out


class Labelforall():
    def __init__(self):
        # 12 one hot label variable
        self.LLphone, self.Lphone, self.Cphone, self.Rphone, self.RRphone, self.vowel = [],[],[],[],[],[]
        self.Lstress, self.Cstress, self.Rstress, self.Lpos, self.Cpos, self.Rpos = [],[],[],[],[],[]
        # 15 numerical variable
        self.phone_syllable_fw, self.phone_syllable_bw, self.phones_syllable = [],[],[]
        self.syllable_word_fw, self.syllable_word_bw, self.syllables_word = [],[],[]
        self.word_sentence_fw, self.word_sentence_bw, self.words_sentence = [],[],[]
        self.sentence_utterance_fw, self.sentence_utterance_bw, self.sentences_utterance = [],[],[]
        self.phones_utterance, self.syllables_utterance, self.words_utterance = [],[],[]
        self.stressed_syllables_sentence_before_syllable = []
        self.stressed_syllables_sentence_after_syllable = []
        self.syllables_previous_stressed_syllable_and_syllable = []
        self.syllables_syllable_and_next_stressed_syllable = []

        # label symbol
        self.symbol = [';','-','+',';','!','|',':',':','|','#','#',
                        '|','$','$','|','@','@','|','&','&','|','^','^','|','=','=',
                        '|','+','&','+']

        self.vowel_list = ['AA','AE','AH','AO','AY','AW','EH','ER','EY','IH','IY','OY','UW','UH','OW']
        self.string = ""
        self.out = []
    def Get_label(self,text,\
            phone_start,syllable_start,word_start,utterance_start, \
            phones_syllable,phones_word,phones_sentence,phones_utterance, \
            syllables_word,syllables_sentence,syllables_utterance, \
            words_sentence,words_utterance, \
            sentences_utterance, \
            stress_count,stress_tag, \
            GPOS_list):

        # phone identity
        for line in text :
            if line[2] == 'sil':
                self.Cphone.append('sil')
            elif line[2] == 'sp':
                self.Cphone.append('sp')
            else :
                self.Cphone.append(line[2].lower())

        self.LLphone = list_shift(self.Cphone.copy() , "right" , 2 , _)
        self.Lphone = list_shift(self.Cphone.copy() , "right" , 1 , _)
        self.Rphone = list_shift(self.Cphone.copy() , "left" , 1 , _)
        self.RRphone = list_shift(self.Cphone.copy() , "left" , 2 , _)

        # vowl
        syl_vowel = []
        for line in text:
            if line[2] in self.vowel_list:
                syl_vowel.append(line[2].lower())
        if len(syl_vowel) != len(syllable_start):
            print("vowl_list_not_enough")

        self.vowel = Generate_single_label(text,syl_vowel,syllable_start,_,_,_, "int")

        # stress
        stress_tag_in_previous_syllable = list_shift(stress_tag.copy(),"previous", _ , "char")
        stress_tag_in_current_syllable = stress_tag.copy()
        stress_tag_in_next_syllable = list_shift(stress_tag.copy(),"next", _ , "char" )
        self.Lstress = Generate_single_label(text,stress_tag_in_previous_syllable,syllable_start,_,_,_, "int")
        self.Cstress = Generate_single_label(text,stress_tag_in_current_syllable,syllable_start,_,_,_, "int")
        self.Rstress = Generate_single_label(text,stress_tag_in_next_syllable,syllable_start,_,_,_, "int")

        # Pos
        GPOS_list_in_previous_word = list_shift(GPOS_list.copy(),"previous", _ , "char")
        GPOS_list_in_current_word = GPOS_list.copy()
        GPOS_list_in_next_word = list_shift(GPOS_list.copy(),"next", _ , "char")
        self.Lpos = Generate_single_label(text, GPOS_list_in_previous_word,_ ,word_start, _ , _,"char")
        self.Cpos = Generate_single_label(text, GPOS_list_in_current_word , _, word_start, _,_, "char")
        self.Rpos = Generate_single_label(text, GPOS_list_in_next_word,_ ,word_start, _ ,_, "char")


        self.phone_syllable_fw,self.phone_syllable_bw = Generate_position_label(text,phones_syllable,phone_start,syllable_start)
        self.syllable_word_fw,self.syllable_word_bw = Generate_position_label(text,syllables_word,syllable_start,word_start)
        self.word_sentence_fw,self.word_sentence_bw = Generate_position_label(text,words_sentence,word_start,sentence_start)
        self.sentence_utterance_fw,self.sentence_utterance_bw = Generate_position_label(text,sentences_utterance,sentence_start,utterance_start)

        self.phones_utterance = Generate_single_label(text, phones_utterance,_ ,_, _,utterance_start, "int")
        self.syllables_utterance = Generate_single_label(text, syllables_utterance,_ ,_, _,utterance_start, "int")
        self.words_utterance = Generate_single_label(text, words_utterance,_ ,_, _ ,utterance_start, "int")
        #self.sentence_in_utterance = Generate_single_label(text, sentences_utterance,_ ,_, _,utterance_start, "int")

        self.phones_syllable = Generate_single_label(text,phones_syllable,syllable_start,_,_,_, "int")
        self.syllables_word = Generate_single_label(text, syllables_word,_ , word_start, _,_, "int")
        self.words_sentence = Generate_single_label(text, words_sentence, _ ,_, sentence_start ,_, "int")
        self.sentences_utterance = Generate_single_label(text, sentences_utterance,_ ,_, _,utterance_start, "int")


        total=0
        stressed_num_in_sentence = []
        for val in syllables_sentence:
            count=0
            for i in range(total,total+val):
                count += int(stress_count[i])
            total += val
            stressed_num_in_sentence.append(count)

        sentence_num = len(sentence_start)
        current_syllable_sum_in_current_sentence = []
        sum = 0
        for i in range(0,sentence_num):
            sum += syllables_sentence[i]
            current_syllable_sum_in_current_sentence.append(sum)
        current_syllable_sum_in_current_sentence.insert(0,0)
        stress_count_shift_right = list_shift(stress_count.copy(),"previous", _ , "int" )

        self.stressed_syllables_sentence_before_syllable = xxx_num_before_curent_xxx_in_sentence(text,stress_count_shift_right,syllable_start,sentence_start)
        self.stressed_syllables_sentence_after_syllable = xxx_num_after_curent_xxx_in_sentence(text,stress_count,stressed_num_in_sentence,syllable_start,sentence_start)
        self.syllables_previous_stressed_syllable_and_syllable, self.syllables_syllable_and_next_stressed_syllable = \
        xxx_num_from_previous_xxx_to_current_xxx(text,stress_count,current_syllable_sum_in_current_sentence,syllable_start,sentence_start)


        for i in range(len(text)):
            self.string = str(self.LLphone[i]) \
                        +self.symbol[0]+str(self.Lphone[i]) \
                        +self.symbol[1]+str(self.Cphone[i]) \
                        +self.symbol[2]+str(self.Rphone[i]) \
                        +self.symbol[3]+str(self.RRphone[i]) \
                        +self.symbol[4]+str(self.vowel[i]) \
                        +self.symbol[5]+str(self.Lstress[i]) \
                        +self.symbol[6]+str(self.Cstress[i]) \
                        +self.symbol[7]+str(self.Rstress[i]) \
                        +self.symbol[8]+str(self.Lpos[i]) \
                        +self.symbol[9]+str(self.Cpos[i]) \
                        +self.symbol[10]+str(self.Rpos[i]) \
                        +self.symbol[11]+str(self.phone_syllable_fw[i]) \
                        +self.symbol[12]+str(self.phone_syllable_bw[i]) \
                        +self.symbol[13]+str(self.phones_syllable[i]) \
                        +self.symbol[14]+str(self.syllable_word_fw[i]) \
                        +self.symbol[15]+str(self.syllable_word_bw[i]) \
                        +self.symbol[16]+str(self.syllables_word[i]) \
                        +self.symbol[17]+str(self.word_sentence_fw[i]) \
                        +self.symbol[18]+str(self.word_sentence_bw[i]) \
                        +self.symbol[19]+str(self.words_sentence[i]) \
                        +self.symbol[20]+str(self.sentence_utterance_fw[i]) \
                        +self.symbol[21]+str(self.sentence_utterance_bw[i]) \
                        +self.symbol[22]+str(self.sentences_utterance[i]) \
                        +self.symbol[23]+str(self.phones_utterance[i]) \
                        +self.symbol[24]+str(self.syllables_utterance[i]) \
                        +self.symbol[25]+str(self.words_utterance[i]) \
                        +self.symbol[26]+str(self.stressed_syllables_sentence_before_syllable[i]) \
                        +self.symbol[27]+str(self.stressed_syllables_sentence_after_syllable[i])  \
                        +self.symbol[28]+str(self.syllables_previous_stressed_syllable_and_syllable[i]) \
                        +self.symbol[29]+str(self.syllables_syllable_and_next_stressed_syllable[i])



            self.out.append(self.string)

        return self.out


class Labelforcategorical():
    def __init__(self):
        # 12 one hot label variable
        self.LLphone, self.Lphone, self.Cphone, self.Rphone, self.RRphone, self.vowel = [],[],[],[],[],[]
        self.Lstress, self.Cstress, self.Rstress, self.Lpos, self.Cpos, self.Rpos = [],[],[],[],[],[]
        # label symbol
        self.symbol = [';','-','+',';','!','|',':',':','|','#','#',
                        '|','$','$','|','@','@','|','&','&','|','^','^','|','=','=',
                        '|','+','&','+']

        self.vowel_list = ['AA','AE','AH','AO','AY','AW','EH','ER','EY','IH','IY','OY','UW','UH','OW']
        self.string = ""
        self.out = []

    def Get_label(self,text,\
            phone_start,syllable_start,word_start,utterance_start, \
            phones_syllable,phones_word,phones_sentence,phones_utterance, \
            syllables_word,syllables_sentence,syllables_utterance, \
            words_sentence,words_utterance, \
            sentences_utterance, \
            stress_count,stress_tag, \
            GPOS_list):
        # phone identity
        for line in text :
            if line[2] == 'sil':
                self.Cphone.append('sil')
            elif line[2] == 'sp':
                self.Cphone.append('sp')
            else :
                self.Cphone.append(line[2].lower())

        self.LLphone = list_shift(self.Cphone.copy() , "right" , 2 , _)
        self.Lphone = list_shift(self.Cphone.copy() , "right" , 1 , _)
        self.Rphone = list_shift(self.Cphone.copy() , "left" , 1 , _)
        self.RRphone = list_shift(self.Cphone.copy() , "left" , 2 , _)

        # vowl
        syl_vowel = []
        for line in text:
            if line[2] in self.vowel_list:
                syl_vowel.append(line[2].lower())
        if len(syl_vowel) != len(syllable_start):
            print("vowl_list_not_enough")

        self.vowel = Generate_single_label(text,syl_vowel,syllable_start,_,_,_, "int")

        # stress
        stress_tag_in_previous_syllable = list_shift(stress_tag.copy(),"previous", _ , "char")
        stress_tag_in_current_syllable = stress_tag.copy()
        stress_tag_in_next_syllable = list_shift(stress_tag.copy(),"next", _ , "char" )
        self.Lstress = Generate_single_label(text,stress_tag_in_previous_syllable,syllable_start,_,_,_, "int")
        self.Cstress = Generate_single_label(text,stress_tag_in_current_syllable,syllable_start,_,_,_, "int")
        self.Rstress = Generate_single_label(text,stress_tag_in_next_syllable,syllable_start,_,_,_, "int")

        # Pos
        GPOS_list_in_previous_word = list_shift(GPOS_list.copy(),"previous", _ , "char")
        GPOS_list_in_current_word = GPOS_list.copy()
        GPOS_list_in_next_word = list_shift(GPOS_list.copy(),"next", _ , "char")
        self.Lpos = Generate_single_label(text, GPOS_list_in_previous_word,_ ,word_start, _ , _,"char")
        self.Cpos = Generate_single_label(text, GPOS_list_in_current_word , _, word_start, _,_, "char")
        self.Rpos = Generate_single_label(text, GPOS_list_in_next_word,_ ,word_start, _ ,_, "char")

        for i in range(len(text)):
            self.string = str(self.LLphone[i]) \
                        +self.symbol[0]+str(self.Lphone[i]) \
                        +self.symbol[1]+str(self.Cphone[i]) \
                        +self.symbol[2]+str(self.Rphone[i]) \
                        +self.symbol[3]+str(self.RRphone[i]) \
                        +self.symbol[4]+str(self.vowel[i]) \
                        +self.symbol[5]+str(self.Lstress[i]) \
                        +self.symbol[6]+str(self.Cstress[i]) \
                        +self.symbol[7]+str(self.Rstress[i]) \
                        +self.symbol[8]+str(self.Lpos[i]) \
                        +self.symbol[9]+str(self.Cpos[i]) \
                        +self.symbol[10]+str(self.Rpos[i])

            self.out.append(self.string)

        return self.out

def gen_label(Start,End,phone,syllable,word,sentence,utterance,pos,tone,position):

    label =[]
    for i in range(len(phone)):
        time = "{:>8}".format(Start[i]) +"  " + "{:>8}".format(End[i]) + " "
        string = time+phone[i]+syllable[i]+word[i]+sentence[i]+utterance[i] \
                +pos[i]+position[i]+tone[i]
        '''
        string = time \
                +"{:<20}".format(phone[i]) \
                +"{:<16}".format(syllable[i]) \
                +"{:<16}".format(word[i]) \
                +"{:<16}".format(sentence[i]) \
                +"{:<16}".format(utterance[i]) \
                +"{:<16}".format(pos[i]) \
                +"{:<24}".format(position[i]) \
                +"{:<16}".format(tone[i])
        '''

        label.append(string)

    return label

def gen_labelforall(Start,End,labelforall):

    label =[]
    for i in range(len(labelforall)):
        time = "{:>8}".format(Start[i]) +"  " + "{:>8}".format(End[i]) + " "
        string = time + labelforall[i]
        label.append(string)

    return label

def write_label_file(filename,hts_label_dir_path,label,curphone):

    # filepath = filepath.rstrip(".mul")
    # filepath = filepath.lstrip("./output_mul/")

    filepath1 = os.path.join(hts_label_dir_path, "full" , filename+".lab")
    filepath2 = os.path.join(hts_label_dir_path, "mono" , filename+".lab")
    # filepath1 = "./output_htslabel/full/" + filepath + ".lab"
    # filepath2 = "./output_htslabel/mono/" + filepath + ".lab"

    folder = os.path.exists(hts_label_dir_path)
    if not folder:
        os.makedirs(os.path.join(hts_label_dir_path, "full"))
        os.makedirs(os.path.join(hts_label_dir_path, "mono"))
        # os.makedirs("./output_htslabel/full/")
        # os.makedirs("./output_htslabel/mono/")

    with open(filepath1 , "w") as f :
        for lab in label:
            f.write(lab)
            f.write("\n")

    with open(filepath2 , "w") as f :
        for i , cphone in enumerate(curphone):
            time = "{:>8}".format(Start[i]) +"  " + "{:>8}".format(End[i] + " ")
            phone = ' ' + cphone
            string = time + phone
            f.write(string)
            f.write("\n")

    #print(label)
    return 0

def clip(tmp_list,max_val):
    new_list = []
    for tmp in tmp_list :
        if tmp > max_val :
            new_list.append(max_val)
        else :
            new_list.append(tmp)

    return new_list

def check_max_numbers( filename, \
phone_num_in_syllable,phone_num_in_word,phone_num_in_sentence, \
syllable_num_in_word,syllable_num_in_sentence,syllable_num_in_utterance, \
word_num_in_sentence,word_num_in_utterance, \
sentence_num_in_utterance):

    if max(phone_num_in_syllable) > 7 :
        phone_num_in_syllable = clip(phone_num_in_syllable, 7)
    if max(syllable_num_in_word) > 7 :
        syllable_num_in_word = clip(syllable_num_in_word, 7)
    if max(syllable_num_in_sentence) > 20 : # 20 -> 59
        syllable_num_in_sentence = clip(syllable_num_in_sentence, 20)
    if max(syllable_num_in_utterance) > 28 : # 28-> 59
        syllable_num_in_utterance = clip(syllable_num_in_utterance, 28)
    if max(word_num_in_sentence) > 13 : # 13 -> 40
        word_num_in_sentence = clip(word_num_in_sentence, 13)
    if max(word_num_in_utterance) > 13 : # 13 -> 40
        word_num_in_utterance = clip(word_num_in_utterance, 13)
    if max(sentence_num_in_utterance) > 4 : # 4 -> 10
        sentence_num_in_utterance = clip(sentence_num_in_utterance, 4)

    if max(phone_num_in_syllable) > 7 :
        print("phone_num_in_syllable error :",max(phone_num_in_syllable),filename)
    if max(syllable_num_in_word) > 7 :
        print("syllable_num_in_word error :",max(syllable_num_in_word),filename)
    if max(syllable_num_in_sentence) > 20 : # 20 -> 59
        print("syllable_num_in_sentence error :",max(syllable_num_in_sentence),filename)
    if max(syllable_num_in_utterance) > 28 : # 28-> 59
        print("syllable_num_in_utterance error :",max(syllable_num_in_utterance),filename)
    if max(word_num_in_sentence) > 13 : # 13 -> 40
        print("word_num_in_sentence error :",max(word_num_in_sentence),filename)
    if max(word_num_in_utterance) > 13 : # 13 -> 40
        print("word_num_in_utterance error :",max(word_num_in_utterance),filename)
    if max(sentence_num_in_utterance) > 4 : # 4 -> 10
        print("sentence_num_in_utterance error :",max(sentence_num_in_utterance),filename)

    return phone_num_in_syllable,syllable_num_in_word,syllable_num_in_sentence, \
        syllable_num_in_utterance,word_num_in_sentence,word_num_in_utterance, \
        sentence_num_in_utterance


def TextinfoGet(textIn_path):

    pattern = r'\"(.*)\"'
    filenames = []
    sentences = []
    textInfo = []
    with open(textIn_path, encoding='utf-8') as f:
        for line in f:
            textInfo.append([line.split(" ")[0], re.search(pattern, line).group(0).strip('"')])

    return textInfo

def HtsLabel_Generation(mulIn_dir_path, textIn_path, htslabelOut_dir_path):

    textInfos = TextinfoGet(textIn_path)

    for textInfo in textInfos:
        #print("Converting to " + filename)
        filename = textInfo[0]
        sentence = textInfo[1]

        mul_path = os.path.join(mulIn_dir_path,filename+".mul")
        # filepath = "./output_mul/" + filename
        multext = Get_text(mul_path)

        phone_start,syllable_start,word_start,sentence_start,utterance_start  = Get_start_stamp(multext)
        phones_syllable,phones_word,phones_sentence,phones_utterance = Get_phone_num(multext)
        syllables_word,syllables_sentence,syllables_utterance = Get_syllable_num(
            phones_syllable,phones_word,phones_sentence)
        words_sentence,words_utterance = Get_word_num(
            phones_word,phones_sentence)
        sentences_utterance = Get_sentence_num(phones_sentence)
        phone_list,syllable_list,word_list,sentence_list = Get_word_list(
            multext,syllable_start,word_start,sentence_start,
            phones_syllable,phones_word,phones_sentence)
        _ ,stress_count,stress_tag = Get_stress_info(multext)
        GPOS_list = Get_GPOS_info(multext)
        Start , End = Get_time(multext)

        ## test 1 12_19
        PHONE = PHONE_LABEL()
        phone = PHONE.Get_label(multext)
        curphone = PHONE.Get_phone()
        LABELFORALL = Labelforall()
        labelforall = LABELFORALL.Get_label(multext,\
                phone_start,syllable_start,word_start,utterance_start, \
                phones_syllable,phones_word,phones_sentence,phones_utterance, \
                syllables_word,syllables_sentence,syllables_utterance, \
                words_sentence,words_utterance, \
                sentences_utterance, \
                stress_count,stress_tag, \
                GPOS_list)


        label = gen_labelforall(Start,End,labelforall)
        write_label_file(filename,htslabelOut_dir_path,label,curphone)

    return 0

if __name__ == '__main__':

    input_dir_path = os.path.expanduser("~/Desktop/project/EA_V2/input/")
    output_dir_path = os.path.expanduser("~/Desktop/project/EA_V2/output/")
    htslabelOut_dir_path = os.path.join(output_dir_path, "Hts_Label")
    mulIn_dir_path = os.path.join(input_dir_path, "Gen_Mul")
    textIn_path = os.path.join(input_dir_path,"data", "sentence.txt")

    HtsLabel_Generation(mulIn_dir_path, textIn_path, htslabelOut_dir_path)
