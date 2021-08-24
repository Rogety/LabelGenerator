import os


def list_shift(listP , direction , count , _type_):

    if direction == "right":
        if count == 1:
            listP.pop(-1) ##pop() : 預設是刪掉最後一個
            listP.insert(0 , 'x' )
        elif count == 2:
            listP.pop(-1)
            listP.pop(-1)
            listP.insert(0 , 'x' )
            listP.insert(0 , 'x' )
    elif direction == "left":
        if count == 1:
            listP.pop(0)
            listP.insert(len(listP) , 'x' )
            ##listP.insert(-1 , 'x' ) 插入在不對的位置 bug??
        elif count == 2:
            listP.pop(0)
            listP.pop(0)
            listP.insert(len(listP) , 'x' )
            listP.insert(len(listP) , 'x' )
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

def Get_word_list(text,syllable_start,word_start,phrase_start,
                  phone_num_in_syllable,phone_num_in_word,phone_num_in_phrase):
    #print("\t\t\tGet_word_list\t\t\t")
    phone_list,syllable_list,word_list,phrase_list = [], [], [], []

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

    ##phrase_list
    m=0
    for i in range(len(phone_list)):
        if i == phrase_start[m]:
            n = phone_num_in_phrase[m]
            tmp_phrase = ""
            for k in range(0,n):
                tmp_phrase += phone_list[i+k]
            phrase_list.append(tmp_phrase)
            m=m+1
        if m == len(phrase_start):
            break

    #print("phone_list =",phone_list,len(phone_list))
    #print("syllable_list =",syllable_list,len(syllable_list))
    #print("word_list =",word_list,len(word_list))
    #print("phrase_list =",phrase_list,len(phrase_list))

    return phone_list,syllable_list,word_list,phrase_list

def Get_phone_num(text):
    #print("\t\t\tGet_phone_num\t\t\t")

    phone_num_in_syllable,phone_num_in_word,phone_num_in_phrase = [],[],[]

    text_tmp = []
    for line in text:
        if line[2] != 'sil' and line[2] != 'sp':
            text_tmp.append(line)

    syl_start,word_start,phrase_start = [],[],[]

    phrase_start.append(0)
    for i in range(len(text_tmp)):
        if len(text_tmp[i]) > 4:
            word_start.append(i)
        if len(text_tmp[i]) > 3:
            syl_start.append(i)
        if text_tmp[i][-1] == ',' and (i != 0):
            phrase_start.append(i)



    # print(word_start,len(word_start))
    # print(syl_start,len(syl_start))
    # print(phrase_start,len(phrase_start))

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


    for i in range(len(phrase_start)):
        try:
            phone_num_in_phrase.append(phrase_start[i+1] - phrase_start[i])
        except IndexError:
            phone_num_in_phrase.append(len(text_tmp) - phrase_start[i])


    # print(phone_num_in_word , len(phone_num_in_word))
    # print(phone_num_in_syllable , len(phone_num_in_syllable))
    # print(phone_num_in_phrase , len(phone_num_in_phrase))

    return phone_num_in_syllable,phone_num_in_word,phone_num_in_phrase


def Get_syllable_num(phone_num_in_syllable,phone_num_in_word,phone_num_in_phrase):
    #print("\t\t\tGet_syllable_num\t\t\t")

    syllable_num_in_word,syllable_num_in_phrase,syllable_num_in_utterance =[],[],[]

    # print(phone_num_in_word , len(phone_num_in_word))
    # print(phone_num_in_syllable , len(phone_num_in_syllable))
    # print(phone_num_in_phrase , len(phone_num_in_phrase))

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
    for val in phone_num_in_phrase:
        tmp,count = 0,0
        if val == phone_num_in_syllable[k]:
            syllable_num_in_phrase.append(1)
            k += 1
        else:
            while( tmp != val ):
                tmp += phone_num_in_syllable[k]
                k += 1
                count += 1
            syllable_num_in_phrase.append(count)

    ##
    syllable_num_in_utterance.append(len(phone_num_in_syllable))


    # print("syllable_num_in_word = ",syllable_num_in_word,len(syllable_num_in_word))
    # print("syllable_num_in_phrase = ",syllable_num_in_phrase,len(syllable_num_in_phrase))
    # print("syllable_num_in_utterance = ",syllable_num_in_utterance,len(syllable_num_in_utterance))


    return syllable_num_in_word,syllable_num_in_phrase,syllable_num_in_utterance

def Get_word_num(phone_num_in_word,phone_num_in_phrase):

    word_num_in_phrase,word_num_in_utterance = [],[]
    # print(phone_num_in_word)
    # print(phone_num_in_phrase)

    k=0
    for val in phone_num_in_phrase:
        tmp,count = 0,0
        if val == phone_num_in_word[k]:
            word_num_in_phrase.append(1)
            k += 1
        else:
            while( tmp != val ):
                tmp += phone_num_in_word[k]
                k += 1
                count += 1
            word_num_in_phrase.append(count)

    word_num_in_utterance.append(len(phone_num_in_word))

    # print("word_num_in_phrase = ",word_num_in_phrase,len(word_num_in_phrase))
    # print("word_num_in_utterance = ",word_num_in_utterance,len(word_num_in_utterance))


    return word_num_in_phrase,word_num_in_utterance

def Get_phrase_num(phone_num_in_phrase):

    phrase_num_in_utterance = []

    phrase_num_in_utterance.append(len(phone_num_in_phrase))

    # print("phrase_num_in_utterance = ",phrase_num_in_utterance,len(phrase_num_in_utterance))

    return phrase_num_in_utterance

def Get_start_stamp(text):
    #print("\t\t\tGet_start_stamp\t\t\t")
    line_count = []
    phone_start = []
    syllable_start,word_start,phrase_start = [],[],[]
    sentence_start = [1]

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


    phrase_start.append(1)
    for i in range(len(text)):
        if text[i][-1] == ',' and (i != 1):
            phrase_start.append(i)

    #print(phone_start , len(phone_start))

    return phone_start,syllable_start ,word_start , phrase_start,sentence_start


def Get_time(text):

    #print("\t\t\tGet_time\t\t\t")
    start , end = [] , []

    for line in text :
        start.append(line[0])
        end.append(line[1])



    return start , end

def Get_stress_info(text):
    #print("\t\t\tGet_stress_info\t\t\t")
    stress_index,stress_type = [],[]

    ##stress_index =sylstart

    for line in text :
        try :
            if line[3] == '2':  ##
                stress_type.append('1')
            else:
                stress_type.append(line[3])
        except :
            pass

    return stress_index,stress_type

def Get_GPOS_info(text):
    #print("\t\t\tGet_GPOS_info\t\t\t")
    GPOS_list = []

    for line in text:
        if len(line) > 6:
            GPOS_list.append(line[6])

    return GPOS_list

def Generate_single_label(text,target_list,syllable_start,word_start,phrase_start,sentence_start, _type_):

    label = []
    k=0
    if _type_ == "int":
        val = 0
    elif _type_ == "char":
        val = '0'

    if syllable_start != [] and word_start == [] and phrase_start == [] :
        for i in range(len(text)):
            if i == syllable_start[k]:
                val = target_list[k]
                k += 1
                if k == len(syllable_start):
                    k = len(syllable_start)-1

            if text[i][2] == 'sp' or text[i][2] == 'sil':
                label.append('x')
            else:
                label.append(val)

    if word_start != [] and syllable_start == [] and phrase_start == []:
        for i in range(len(text)):
            if i == word_start[k]:
                val = target_list[k]
                k += 1
                if k == len(word_start):
                    k = len(word_start)-1

            if text[i][2] == 'sp' or text[i][2] == 'sil':
                label.append('x')
            else:
                label.append(val)

    if phrase_start != [] and syllable_start == [] and word_start == []:
        for i in range(len(text)):
            if i == phrase_start[k]:
                val = target_list[k]
                k += 1
                if k == len(phrase_start):
                    k = len(phrase_start)-1

            if text[i][2] == 'sp' or text[i][2] == 'sil':
                label.append('x')
            else:
                label.append(val)

    if sentence_start:
        for i in range(len(text)):
            if i == sentence_start[k]:
                val = target_list[k]
                k += 1
                if k == len(sentence_start):
                    k = len(sentence_start)-1

            if text[i][2] == 'sp' or text[i][2] == 'sil':
                label.append('x')
            else:
                label.append(val)


    return label

def Generate_position_label(target_list,start_short,strat_long):

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
            label_forward.append('x')
            label_backward.append('x')
        else:
            label_forward.append(forward)
            label_backward.append(backward)

    return label_forward , label_backward

def xxx_num_before_curent_xxx_in_phrase(text,target_list,start_short,start_long):

    label = []
    k,m,count=0,0,0
    for i in range(len(text)):
        if i == start_short[k]:
            count += int(target_list[k])
            k += 1
            if k == len(start_short):
                k = len(start_short)-1

        if i == start_long[m]:  ## phrase中在第一個syllable 一定是0個 stressed syllable
            count = 0
            m += 1
            if m == len(start_long):
                m = len(start_long)-1

        if text[i][2] == 'sil' or text[i][2] == 'sp':
            label.append('x')
        else :
            label.append(count)


    return label

def xxx_num_after_curent_xxx_in_phrase(text,target_list_short,target_list_long,start_short,start_long):

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
            label.append('x')
        else :
            label.append(count)

    #print("stress_num :", target_list_long , len(target_list_long))
    #print("stress_type :", target_list_short , len(target_list_short))
    #print("phrase_start : " , start_long , len(phrase_start))
    #print("syllable_start : " , start_short , len(syllable_start))

    return label

def xxx_num_from_previous_xxx_to_current_xxx(text,target_list_short,target_list_long,start_short,start_long):
    label = []

    count,k=0,0
    for i in range(len(text)):
        if i == start_short[k]:
            n = k -1 ## m = index
            count = 0

            try:
                while target_list_short[n] != '1' :
                    n = n + 1
                    count += 1
            except :
                pass

            k += 1
            if k == len(start_short):
                k = len(start_short)-1
        if text[i][2] == 'sil' or text[i][2] == 'sp':
            label.append('x')
        else :
            label.append(count)

    return label

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
            label.append('x')
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


    def Get_label(self,text,phone_start,syllable_start,phone_num_in_syllable,stress_type):
        syl_vowel = []
        ##  "S" , "Z" 為了所有格的BUG
        for line in text:
            if line[2] in self.vowel_list:
                syl_vowel.append(line[2])
        print("syl_vowel :",syl_vowel,len(syl_vowel))
        print("syllable_start :",syllable_start,len(syllable_start))
        if len(syl_vowel) != len(syllable_start):
            print("vowl_list_not_enough")


        phone_num_in_previous_syllable = list_shift(phone_num_in_syllable.copy(),"previous", _ , "int")
        stress_type_in_previous_syllable = list_shift(stress_type.copy(),"previous", _ , "char")
        phone_num_in_current_syllable = phone_num_in_syllable.copy()
        stress_type_in_current_syllable = stress_type.copy()
        phone_num_in_next_syllable = list_shift(phone_num_in_syllable.copy(),"next", _ , "int")
        stress_type_in_next_syllable = list_shift(stress_type.copy(),"next", _ , "char" )
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

class PHRASE_LABEL():
    def __init__(self):
        self.syl_in_prephrase = []
        self.syl_in_curphrase = []
        self.syl_in_nextphrase = []
        self.word_in_prephrase = []
        self.word_in_curphrase = []
        self.word_in_nextphrase = []
        self.string = ""
        self.out = []
        self.symbol =['/D:','^','@','-','=','^','/E:']

    def Get_label(self,text,phrase_start,syllable_num_in_phrase,word_num_in_phrase):
        syllable_num_in_previous_phrase = list_shift(syllable_num_in_phrase.copy(),"previous",_,"int")
        word_num_in_previous_phrase = list_shift(word_num_in_phrase.copy() , "previous",_,"int" )
        syllable_num_in_current_phrase = syllable_num_in_phrase.copy()
        word_num_in_current_phrase = word_num_in_phrase.copy()
        syllable_num_in_next_phrase = list_shift(syllable_num_in_phrase.copy(),"next",_,"int")
        word_num_in_next_phrase = list_shift(word_num_in_phrase.copy() , "next",_,"int" )


        self.syl_in_prephrase = Generate_single_label(text, syllable_num_in_previous_phrase, _ ,_, phrase_start,_, "int")
        self.word_in_prephrase = Generate_single_label(text, word_num_in_previous_phrase, _ ,_, phrase_start ,_, "int")
        self.syl_in_curphrase = Generate_single_label(text, syllable_num_in_current_phrase, _ ,_, phrase_start,_, "int")
        self.word_in_curphrase = Generate_single_label(text, word_num_in_current_phrase, _ ,_, phrase_start ,_, "int")
        self.syl_in_nextphrase = Generate_single_label(text, syllable_num_in_next_phrase,_ ,_, phrase_start,_, "int")
        self.word_in_nextphrase = Generate_single_label(text, word_num_in_next_phrase, _ ,_, phrase_start ,_, "int")

        for i in range(len(text)):
            self.string = self.symbol[0]+str(self.syl_in_prephrase[i]) \
                        +self.symbol[1]+str(self.syl_in_curphrase[i]) \
                        +self.symbol[2]+str(self.syl_in_nextphrase[i]) \
                        +self.symbol[3]+str(self.word_in_prephrase[i]) \
                        +self.symbol[4]+str(self.word_in_curphrase[i]) \
                        +self.symbol[5]+str(self.word_in_nextphrase[i])
            self.out.append(self.string)

        return self.out

class SENTENSE_LABEL():
    def __init__(self):
        self.syl_in_sentense = []
        self.word_in_sentense = []
        self.phrase_in_sentense = []
        self.string = ""
        self.out = []
        self.symbol =['/E:','$','-','/F:']

    def Get_label(self,text,sentence_start,syllable_num_in_sentence,word_num_in_sentence,phrase_num_in_sentence):
        self.syl_in_sentense = Generate_single_label(text, syllable_num_in_sentence,_ ,_, _,sentence_start, "int")
        self.word_in_sentense = Generate_single_label(text, word_num_in_sentence,_ ,_, _ ,sentence_start, "int")
        self.phrase_in_sentense = Generate_single_label(text, phrase_num_in_sentence,_ ,_, _,sentence_start, "int")

        for i in range(len(text)):
            self.string = self.symbol[0]+str(self.syl_in_sentense[i]) \
                        +self.symbol[1]+str(self.word_in_sentense[i]) \
                        +self.symbol[2]+str(self.phrase_in_sentense[i])
            self.out.append(self.string)

        return self.out

class POS_LABEL():
    def __init__(self):
        self.pos_preword = []
        self.pos_curword = []
        self.pos_nextword = []
        self.string = ""
        self.out = []
        self.symbol =['/F:','$','+','/G:']

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

class STRESS_LABEL():
    def __init__(self):
        self.stress_presyl = []
        self.stress_cursyl = []
        self.stress_nextsyl = []
        self.string = ""
        self.out = []
        self.symbol =['/G:','$','=','/H:']


    def Get_label(self,text,stress_type):
        stress_type_in_previous_syllable = list_shift(stress_type.copy(),"previous", _ , "char")
        stress_type_in_current_syllable = stress_type.copy()
        stress_type_in_next_syllable = list_shift(stress_type.copy(),"next", _ , "char" )


        self.stress_presyl = Generate_single_label(text,stress_type_in_previous_syllable,syllable_start,_,_,_, "int")
        self.stress_cursyl = Generate_single_label(text,stress_type_in_current_syllable,syllable_start,_,_,_, "int")
        self.stress_nextsyl = Generate_single_label(text,stress_type_in_next_syllable,syllable_start,_,_,_, "int")

        for i in range(len(text)):
            self.string = self.symbol[0]+str(self.stress_presyl[i]) \
                        +self.symbol[1]+str(self.stress_cursyl[i]) \
                        +self.symbol[2]+str(self.stress_nextsyl[i])
            self.out.append(self.string)

        return self.out

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
        self.symbol =['/H:','$','@','@','$','&','-','&','#','#','/I']

    def Get_label(self,phone_start,syllable_start,word_start,phrase_start, \
        phone_num_in_syllable,syllable_num_in_word,syllable_num_in_phrase,word_num_in_phrase,phrase_num_in_sentence):
        word_num_in_current_phrase = word_num_in_phrase.copy()
        self.p6,self.p7 = Generate_position_label(phone_num_in_syllable,phone_start,syllable_start)
        self.b3,self.b4 = Generate_position_label(syllable_num_in_word,syllable_start,word_start)
        self.b5,self.b6 = Generate_position_label(syllable_num_in_phrase,syllable_start,phrase_start)
        self.e3,self.e4 = Generate_position_label(word_num_in_current_phrase,word_start,phrase_start)
        self.h3,self.h4 = Generate_position_label(phrase_num_in_sentence,phrase_start,sentence_start)
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
        self.string = ""
        self.out = []
        self.symbol =['/I:','-','@','+','@','=','+','$','/J:']


    def Get_label(self,text,syllable_start,word_start,phrase_start,stress_type,syllable_num_in_phrase,word_num_in_phrase):
        stress_type_shift_right = list_shift(stress_type.copy(),"previous", _ , "int" )
        current_syllable_num_in_current_phrase = syllable_num_in_phrase.copy()
        word_num_in_current_phrase = word_num_in_phrase.copy()

        print("stress_type :",stress_type)
        #b7,b8,b9,b10
        total=0
        stressed_num_in_phrase = []
        for val in current_syllable_num_in_current_phrase:
            count=0
            for i in range(total,total+val):
                count += int(stress_type[i])
            total += val
            stressed_num_in_phrase.append(count)

        phrase_num = len(phrase_start)
        current_syllable_sum_in_current_phrase = []
        sum = 0
        for i in range(0,phrase_num):
            sum += current_syllable_num_in_current_phrase[i]
            current_syllable_sum_in_current_phrase.append(sum)
        current_syllable_sum_in_current_phrase.insert(0,0)

        ##E5,E6,E7,E8

        content_index = []
        for item in GPOS_list:
            if item == 'content':
                content_index.append('1')
            else:
                content_index.append('0')
        content_word_num_in_phrase = []

        total=0
        for val in word_num_in_phrase:
            count=0
            for i in range(total,total+val):
                count += int(content_index[i])
            total += val
            content_word_num_in_phrase.append(count)
        content_index_shift_right = list_shift(content_index.copy(),"previous", _ , "char" )

        phrase_num = len(phrase_start)
        current_word_sum_in_current_phrase = []
        sum = 0
        for i in range(0,phrase_num):
            sum += word_num_in_current_phrase[i]
            current_word_sum_in_current_phrase.append(sum)
        current_word_sum_in_current_phrase.insert(0,0)

        self.b7 = xxx_num_before_curent_xxx_in_phrase(text,stress_type_shift_right,syllable_start,phrase_start)
        self.b8 = xxx_num_after_curent_xxx_in_phrase(text,stress_type,stressed_num_in_phrase,syllable_start,phrase_start)
        self.b9 = xxx_num_from_previous_xxx_to_current_xxx(text,stress_type,current_syllable_sum_in_current_phrase,syllable_start,phrase_start)
        self.b10 = xxx_num_from_current_xxx_to_next_xxx(text,stress_type,current_syllable_sum_in_current_phrase,syllable_start,phrase_start)
        self.e5 = xxx_num_before_curent_xxx_in_phrase(text,content_index_shift_right,word_start,phrase_start)
        self.e6 = xxx_num_after_curent_xxx_in_phrase(text,content_index,content_word_num_in_phrase,word_start,phrase_start)
        self.e7 = xxx_num_from_previous_xxx_to_current_xxx(text,content_index,current_word_sum_in_current_phrase,word_start,phrase_start)
        self.e8 = xxx_num_from_current_xxx_to_next_xxx(text,content_index,current_word_sum_in_current_phrase,word_start,phrase_start)

        for i in range(len(text)):
            self.string = self.symbol[0]+str(self.b7[i]) \
                        +self.symbol[1]+str(self.b8[i]) \
                        +self.symbol[2]+str(self.b9[i]) \
                        +self.symbol[3]+str(self.b10[i]) \
                        +self.symbol[4]+str(self.e5[i]) \
                        +self.symbol[5]+str(self.e6[i]) \
                        +self.symbol[6]+str(self.e7[i]) \
                        +self.symbol[7]+str(self.e8[i])
            self.out.append(self.string)

        return self.out




def gen_label(Start,End,phone,syllable,word,phrase,sentense,pos,stress,position,tone,phone3):

    label =[]
    for i in range(len(phone)):
        time = "{:>8}".format(Start[i]) +"  " + "{:>8}".format(End[i] + " ")
        string = time+phone[i]+syllable[i]+word[i]+phrase[i]+sentense[i] \
                +pos[i]+stress[i]+position[i]+tone[i]
        #string = time+phone[i]

        label.append(string)

    return label

def write_label_file(filepath,label,curphone):

    filepath = filepath.rstrip(".mul")
    filepath = filepath.lstrip("./output_mul/")
    filepath1 = "./output_htslabel/full/" + filepath + ".lab"
    filepath2 = "./output_htslabel/mono/" + filepath + ".lab"

    folder = os.path.exists("./output_htslabel/")
    if not folder:
        os.makedirs("./output_htslabel/full/")
        os.makedirs("./output_htslabel/mono/")

    with open(filepath1 , "w+") as f :
        for lab in label:
            f.write(lab)
            f.write("\n")

    with open(filepath2 , "w+") as f :
        for i , cphone in enumerate(curphone):
            time = "{:>8}".format(Start[i]) +"  " + "{:>8}".format(End[i] + " ")
            phone = ' ' + cphone
            string = time + phone
            f.write(string)
            f.write("\n")

    #print(label)
    return 0

if __name__ == '__main__':

    print("hello")
    '''
    filename = "cmu_us_arctic_slt_b0523.mul"
    print(filename)
    filepath = "./mul/" + filename
    text = Get_text(filepath)

    phone_start,syllable_start,word_start,phrase_start,sentence_start  = Get_start_stamp(text)
    phone_num_in_syllable,phone_num_in_word,phone_num_in_phrase = Get_phone_num(text)
    syllable_num_in_word,syllable_num_in_phrase,syllable_num_in_sentence = Get_syllable_num(
            phone_num_in_syllable,phone_num_in_word,phone_num_in_phrase)
    word_num_in_phrase,word_num_in_sentence = Get_word_num(
            phone_num_in_word,phone_num_in_phrase)
    phrase_num_in_sentence = Get_phrase_num(phone_num_in_phrase)
    phone_list,syllable_list,word_list,phrase_list = Get_word_list(
            text,syllable_start,word_start,phrase_start,
            phone_num_in_syllable,phone_num_in_word,phone_num_in_phrase)
    _ ,stress_type = Get_stress_info(text)
    GPOS_list = Get_GPOS_info(text)
    Start , End = Get_time(text)

    PHONE = PHONE_LABEL()
    SYLLABLE = SYLLABLE_LABEL()
    WORD = WORD_LABEL()
    PHRASE = PHRASE_LABEL()
    SENTENSE = SENTENSE_LABEL()
    POS = POS_LABEL()
    STRESS = STRESS_LABEL()
    POSITION = POSITION_LABEL()


    phone = PHONE.Get_label(text)
    syllable = SYLLABLE.Get_label(text,phone_start,syllable_start,phone_num_in_syllable,stress_type)
    word = WORD.Get_label(text,word_start,syllable_num_in_word)
    phrase = PHRASE.Get_label(text,phrase_start,syllable_num_in_phrase,word_num_in_phrase)
    sentense = SENTENSE.Get_label(text,sentence_start,syllable_num_in_sentence,word_num_in_sentence,phrase_num_in_sentence)
    pos = POS.Get_label(text,word_start,GPOS_list)
    stress = STRESS.Get_label(text,syllable_start,word_start,phrase_start,stress_type,syllable_num_in_phrase,word_num_in_phrase)
    position = POSITION.Get_label(phone_start,syllable_start,word_start,phrase_start, \
        phone_num_in_syllable,syllable_num_in_word,syllable_num_in_phrase,word_num_in_phrase,phrase_num_in_sentence)

    curphone = PHONE.Get_phone()
    label = gen_label(Start,End,phone,syllable,word,phrase,sentense,pos,stress,position)
    write_label_file(filepath,label,curphone)


    '''

    for dirPath, dirNames, fileNames in os.walk("./output_mul"):
        arctic_fileName = fileNames
    arctic_fileName = sorted(arctic_fileName[21:-1])

    for filename in arctic_fileName:
        print("Converting to " + filename)
        filepath = "./output_mul/" + filename
        text = Get_text(filepath)

        phone_start,syllable_start,word_start,phrase_start,sentence_start  = Get_start_stamp(text)
        phone_num_in_syllable,phone_num_in_word,phone_num_in_phrase = Get_phone_num(text)
        syllable_num_in_word,syllable_num_in_phrase,syllable_num_in_sentence = Get_syllable_num(
            phone_num_in_syllable,phone_num_in_word,phone_num_in_phrase)
        word_num_in_phrase,word_num_in_sentence = Get_word_num(
            phone_num_in_word,phone_num_in_phrase)
        phrase_num_in_sentence = Get_phrase_num(phone_num_in_phrase)
        phone_list,syllable_list,word_list,phrase_list = Get_word_list(
            text,syllable_start,word_start,phrase_start,
            phone_num_in_syllable,phone_num_in_word,phone_num_in_phrase)
        _ ,stress_type = Get_stress_info(text)
        GPOS_list = Get_GPOS_info(text)
        Start , End = Get_time(text)

        print("phone_start :",phone_start)
        print("syllable_start :",syllable_start)
        print("word_start :",word_start)
        print("phrase_start :",phrase_start)
        print("sentence_start :",sentence_start)
        print("phone_num_in_syllable :",phone_num_in_syllable,len(phone_num_in_syllable))
        print("phone_num_in_word :",phone_num_in_word,len(phone_num_in_word))
        print("phone_num_in_phrase :",phone_num_in_phrase,len(phone_num_in_phrase))
        print("syllable_num_in_word :",syllable_num_in_word,len(syllable_num_in_word))
        print("syllable_num_in_phrase :",syllable_num_in_phrase,len(syllable_num_in_phrase))
        print("syllable_num_in_sentence :",syllable_num_in_sentence,len(syllable_num_in_sentence))
        print("word_num_in_phrase :",word_num_in_phrase,len(word_num_in_phrase))
        print("word_num_in_sentence :",word_num_in_sentence,len(word_num_in_sentence))
        print("phrase_num_in_sentence :",phrase_num_in_sentence,len(phrase_num_in_sentence))
        print("phone_list :",phone_list,len(phone_list))
        print("syllable_list :",syllable_list,len(syllable_list))
        print("word_list :",word_list,len(word_list))
        print("phrase_list :",phrase_list,len(phrase_list))
        print("stress_type :",stress_type,len(stress_type))
        print("GPOS_list :",GPOS_list,len(GPOS_list))
        print("Start :",Start,len(Start))
        print("End :",End,len(End))





        PHONE = PHONE_LABEL()
        SYLLABLE = SYLLABLE_LABEL()
        WORD = WORD_LABEL()
        PHRASE = PHRASE_LABEL()
        SENTENSE = SENTENSE_LABEL()
        POS = POS_LABEL()
        STRESS = STRESS_LABEL()
        POSITION = POSITION_LABEL()
        TONE = TONE_LABEL()

        phone = PHONE.Get_label(text,last=True)
        phone3 = PHONE.Get_label_3(text,last=True)
        syllable = SYLLABLE.Get_label(text,phone_start,syllable_start,phone_num_in_syllable,stress_type)
        word = WORD.Get_label(text,word_start,syllable_num_in_word)
        phrase = PHRASE.Get_label(text,phrase_start,syllable_num_in_phrase,word_num_in_phrase)
        sentense = SENTENSE.Get_label(text,sentence_start,syllable_num_in_sentence,word_num_in_sentence,phrase_num_in_sentence)
        pos = POS.Get_label(text,word_start,GPOS_list)
        stress = STRESS.Get_label(text,stress_type)
        position = POSITION.Get_label(phone_start,syllable_start,word_start,phrase_start, \
            phone_num_in_syllable,syllable_num_in_word,syllable_num_in_phrase,word_num_in_phrase,phrase_num_in_sentence)
        tone = TONE.Get_label(text,syllable_start,word_start,phrase_start,stress_type,syllable_num_in_phrase,word_num_in_phrase)

        curphone = PHONE.Get_phone()
        #print(len(phone),len(phone3))
        label = gen_label(Start,End,phone,syllable,word,phrase,sentense,pos,stress,position,tone,phone3)
        write_label_file(filepath,label,curphone)
