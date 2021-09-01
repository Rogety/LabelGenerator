
import re
import itertools
import numpy as np
import os
import argparse
import h5py

QS_phone = {'Vowel':['aa','ae','ah','ao','aw','ax','axr','ay','eh','el','em','en','er','ey','ih','ix','iy','ow','oy','uh','uw'],
        'Consonant':['b','ch','d','dh','dx','f','g','hh','hv','jh','k','l','m','n','nx','ng','p','r','s','sh','t','th','v','w','y','z','zh'],
        'Stop':['b','d','dx','g','k','p','t'],
        'Nasal':['m','n','en','ng'],
        'Fricative':['ch','dh','f','hh','hv','s','sh','th','v','z','zh'],
        'Liquid':['el','hh','l','r','w','y'],
        'Front':['ae','b','eh','em','f','ih','ix','iy','m','p','v','w'],
        'Central':['ah','ao','axr','d','dh','dx','el','en','er','l','n','r','s','t','th','z','zh'],
        'Back':['aa','ax','ch','g','hh','jh','k','ng','ow','sh','uh','uw','y'],
        'Front_Vowel':['ae','eh','ey','ih','iy'],
        'Central_Vowel':['aa','ah','ao','axr','er'],
        'Back_Vowel':['ax','ow','uh','uw'],
        'Long_Vowel':['ao','aw','el','em','en','en','iy','ow','uw'],
        'Short_Vowel':['aa','ah','ax','ay','eh','ey','ih','ix','oy','uh'],
        'Dipthong_Vowel':['aw','axr','ay','el','em','en','er','ey','oy'],
        'Front_Start_Vowel':['aw','axr','er','ey'],
        'Fronting_Vowel':['ay','ey','oy'],
        'High_Vowel':['ih','ix','iy','uh','uw'],
        'Medium_Vowel':['ae','ah','ax','axr','eh','el','em','en','er','ey','ow'],
        'Low_Vowel':['aa','ae','ah','ao','aw','ay','oy'],
        'Rounded_Vowel':['ao','ow','oy','uh','uw','w'],
        'Unrounded_Vowel':['aa','ae','ah','aw','ax','axr','ay','eh','el','em','en','er','ey','hh','ih','ix','iy','l','r','y'],
        'Reduced_Vowel':['ax','axr','ix'],
        'IVowel':['ih','ix','iy'],
        'EVowel':['eh','ey'],
        'AVowel':['aa','ae','aw','axr','ay','er'],
        'OVowel':['ao','ow','oy'],
        'UVowel':['ah','ax','el','em','en','uh','uw'],
        'Unvoiced_Consonant':['ch','f','hh','k','p','s','sh','t','th'],
        'Voiced_Consonant':['b','d','dh','dx','el','em','en','g','jh','l','m','n','ng','r','v','w','y'],
        'Front_Consonant':['b','em','f','m','p','v','w'],
        'Central_Consonant':['d','dh','dx','el','en','l','n','r','s','t','th','z','zh'],
        'Back_Consonant':['ch','g','hh','jh','k','ng','sh','y'],
        'Fortis_Consonant':['ch','f','k','p','s','sh','t','th'],
        'Lenis_Consonant':['b','d','dh','g','jh','v','z','zh'],
        'Neigther_F_or_L':['el','em','en','hh','l','m','n','ng','r','w','y'],
        'Coronal_Consonant':['ch','d','dh','dx','el','en','jh','l','n','r','s','sh','t','th','z','zh'],
        'Non_Coronal':['b','em','f','g','hh','k','m','ng','p','v','w','y'],
        'Anterior_Consonant':['b','d','dh','dx','el','em','en','f','l','m','n','p','s','t','th','v','w','z'],
        'Non_Anterior':['ch','g','hh','jh','k','ng','r','sh','y','zh'],
        'Continuent':['dh','el','em','en','f','hh','l','m','n','ng','r','s','sh','th','v','w','y','z','zh'],
        'No_Continuent':['b','ch','d','g','jh','k','p','t'],
        'Positive_Strident':['ch','jh','s','sh','z','zh'],
        'Negative_Strident':['dh','f','hh','th','v'],
        'Neutral_Strident':['b','d','el','em','en','g','k','l','m','n','ng','p','r','t','w','y'],
        'Glide':['hh','l','el','r','y','w'],
        'Syllabic_Consonant':['axr','el','em','en','er'],
        'Voiced_Stop':['b','d','g'],
        'Unvoiced_Stop':['p','t','k'],
        'Front_Stop':['b','p'],
        'Central_Stop':['d','t'],
        'Back_Stop':['g','k'],
        'Voiced_Fricative':['jh','dh','v','z','zh'],
        'Unvoiced_Fricative':['ch','f','s','sh','th'],
        'Front_Fricative':['f','v'],
        'Central_Fricative':['dh','s','th','z'],
        'Back_Fricative':['ch','jh','sh','zh'],
        'Affricate_Consonant':['ch','jh'],
        'Not_Affricate':['dh','f','s','sh','th','v','z','zh'],
        'silences':['pau','h#','brth'],
        'aa':['aa'],'ae':['ae'],'ah':['ah'],'ao':['ao'],'aw':['aw'],'ax':['ax'],'axr':['axr'],
        'ay':['ay'],'b':['b'],'ch':['ch'],'d':['d'],'dh':['dh'],'dx':['dx'],'eh':['eh'],'el':['el'],'em':['em'],
        'en':['en'],'er':['er'],'ey':['ey'],'f':['f'],'g':['g'],'hh':['hh'],'hv':['hv'],'ih':['ih'],'iy':['iy'],
        'jh':['jh'],'k':['k'],'l':['l'],'m':['m'],'n':['n'],'nx':['nx'],'ng':['ng'],'ow':['ow'],'oy':['oy'],'p':['p'],
        'r':['r'],'s':['s'],'sh':['sh'],'t':['t'],'th':['th'],'uh':['uh'],'uw':['uw'],'v':['v'],'w':['w'],'y':['y'],
        'z':['z'],'zh':['zh'],'pau':['pau'],'h#':['h#'],'brth':['brth'],'sil':['sil'],'sp':['sp'],'x':['x'],}

QS_syl_vowel={'Syl_Vowel==x':['x'],
            'Syl_Vowel==no':['novowel'],
            'Syl_Vowel':['aa','ae','ah','ao','aw','ax','axr','ay','eh','el','em','en','er','ey','ih','ix','iy','ow','oy','uh','uw'],
            'Syl_Front_Vowel':['ae','eh','ey','ih','iy'],
            'Syl_Central_Vowel':['aa','ah','ao','axr','er'],
            'Syl_Back_Vowel':['ax','ow','uh','uw'],
            'Syl_Long_Vowel':['ao','aw','el','em','en','en','iy','ow','uw'],
            'Syl_Short_Vowel':['aa','ah','ax','ay','eh','ey','ih','ix','oy','uh'],
            'Syl_Dipthong_Vowel':['aw','axr','ay','el','em','en','er','ey','oy'],
            'Syl_Front_Start':['aw','axr','er','ey'],
            'Syl_Fronting_Vowel':['ay','ey','oy'],
            'Syl_High_Vowel':['ih','ix','iy','uh','uw'],
            'Syl_Medium_Vowel':['ae','ah','ax','axr','eh','el','em','en','er','ey','ow'],
            'Syl_Low_Vowel':['aa','ae','ah','ao','aw','ay','oy'],
            'Syl_Rounded_Vowel':['ao','ow','oy','uh','uw','w'],
            'Syl_Unrounded_Vowel':['aa','ae','ah','aw','ax','axr','ay','eh','el','em','en','er','ey','hh','ih','ix','iy','l','r','y'],
            'Syl_Reduced_Vowel':['ax','axr','ix'],
            'Syl_IVowel':['ih','ix','iy'],
            'Syl_EVowel':['eh','ey'],
            'Syl_AVowel':['aa','ae','aw','axr','ay','er'],
            'Syl_OVowel':['ao','ow','oy'],
            'Syl_UVowel':['ah','ax','el','em','en','uh','uw'],
            'Syl_aa':['aa'],
            'Syl_ae':['ae'],
            'Syl_ah':['ah'],
            'Syl_ao':['ao'],
            'Syl_aw':['aw'],
            'Syl_ax':['ax'],
            'Syl_axr':['axr'],
            'Syl_ay':['ay'],
            'Syl_eh':['eh'],
            'Syl_el':['el'],
            'Syl_em':['em'],
            'Syl_en':['en'],
            'Syl_er':['er'],
            'Syl_ey':['ey'],
            'Syl_ih':['ih'],
            'Syl_iy':['iy'],
            'Syl_ow':['ow'],
            'Syl_oy':['oy'],
            'Syl_uh':['uh'],
            'Syl_uw':['uw'],}
'''
QS_POS={'Word_GPOS==0':['0'],
        'Word_GPOS==x':['x'],
        'Word_GPOS==aux':['aux'],
        'Word_GPOS==cc':['cc'],
        'Word_GPOS==content':['content'],
        'Word_GPOS==det':['det'],
        'Word_GPOS==in':['in'],
        'Word_GPOS==md':['md'],
        'Word_GPOS==pps':['pps'],
        'Word_GPOS==punc':['punc'],
        'Word_GPOS==to':['to'],
        'Word_GPOS==wp':['wp']}
'''
QS_POS={'Word_GPOS==0':['0'], # 代表沒有GPOS
        'Word_GPOS==x':['x'], # x 代表 sil or sp 沒有GPOS
        'Word_GPOS==cc':['cc'],
        'Word_GPOS==cd':['cd'],
        'Word_GPOS==dt':['dt'],
        'Word_GPOS==ex':['ex'],
        'Word_GPOS==fw':['fw'],
        'Word_GPOS==in':['in'],
        'Word_GPOS==jj':['jj'],
        'Word_GPOS==jjr':['jjr'],
        'Word_GPOS==jjs':['jjs'],
        'Word_GPOS==ls':['ls'],
        'Word_GPOS==md':['md'],
        'Word_GPOS==nn':['nn'],
        'Word_GPOS==nns':['nns'],
        'Word_GPOS==nnp':['nnp'],
        'Word_GPOS==nnps':['nnps'],
        'Word_GPOS==pdt':['pdt'],
        'Word_GPOS==pos':['pos'],
        'Word_GPOS==prp':['prp'],
        'Word_GPOS==prp$':['prp$'],
        'Word_GPOS==rb':['rb'],
        'Word_GPOS==rbr':['rbr'],
        'Word_GPOS==rbs':['rbs'],
        'Word_GPOS==rp':['rp'],
        'Word_GPOS==sym':['sym'],
        'Word_GPOS==to':['to'],
        'Word_GPOS==uh':['uh'],
        'Word_GPOS==vb':['vb'],
        'Word_GPOS==vbd':['vbd'],
        'Word_GPOS==vbg':['vbg'],
        'Word_GPOS==vbn':['vbn'],
        'Word_GPOS==vbp':['vbp'],
        'Word_GPOS==vbz':['vbz'],
        'Word_GPOS==wdt':['wdt'],
        'Word_GPOS==wp':['wp'],
        'Word_GPOS==wp$':['wp$'],
        'Word_GPOS==wrb':['wrb'],
        }

QS_syl_stress={'Syl_Stress==2':['2'],
            'Syl_Stress==1':['1'],
            'Syl_Stress==0':['0'],
            'Syl_Stress==x':['x'],}
'''
qst_config = {"LLphone":r'\/A:\w+\^',"Lphone":r'\^\w+\-',"Cphone":r'\-\w+\+',"Rphone":r'\+\w+\+',"RRphone":r'\+\w+\/B\:',
                "phnum_in_presyl":r'\/B:\w+\^' , "phnum_in_cursyl":r'\^\w+\+' , "phnum_in_nextsyl":r'\+\w+\=' , "vowel_in_syl":r'\=\w+\/C\:' ,
                "sylnum_in_preword":r'\/C:\w+\^' , "sylnum_in_curword":r'\^\w+\=' , "sylnum_in_nextword":r'\=\w+\/D\:' ,
                "sylnum_in_prephrase":r'\/D:\w+\^' , "sylnum_in_curphrase":r'\^\w+\@' , "sylnum_in_nextphrase":r'\@\w+\-' , "wordnum_in_curphrase":r'\-\w+\=' , "wordnum_in_prephrase":r'\=\w+\^' , "wordnum_in_nextphrase":r'\^\w+\/E\:' ,
                "sylnum_in_sentense":r'\/E:\w+\$' , "wordnum_in_sentense":r'\$\w+\-' , "phrasenum_in_sentense":r'\-\w+\/F\:' ,
                "gpos_in_preword":r'\/F:\w+\$?\#' , "gpos_in_curword":r'\#\w+\$?\+' , "gpos_in_next_word":r'\+\w+\$?\/G\:' ,
                "ph_in_syl_fw":r'\/G:\w+\$' , "ph_in_syl_bw":r'\$\w+\@' , "syl_in_word_fw":r'\@\w+\@' , "syl_in_word_bw":r'\@\w+\$' , "syl_in_phrase_fw":r'\$\w+\&' , "syl_in_phrase_bw":r'\&\w+\-' ,
                "word_in_phrase_fw":r'\-\w+\&' , "word_in_phrase_bw":r'\&\w+\#' , "phrase_in_sentense_fw":r'\#\w+\#' , "phrase_in_sentense_bw":r'\#\w+\/H\:' ,
                "Lstress":r'\/H:\w+\-' , "Cstress":r'\-\w+\@' , "Rstress":r'\@\w+\#' ,
                "b7":r'\#\w+\-' , "b8":r'\-\w+\#' , "b9":r'\#\w+\^' , "b10":r'\^\w+\^' }

Group_onehot = ['LLphone','Lphone','Cphone','Rphone','RRphone','vowel_in_syl',
                'gpos_in_preword','gpos_in_curword','gpos_in_next_word',
                'Lstress','Cstress','Rstress']
Group_value = ['phnum_in_presyl','phnum_in_cursyl','phnum_in_nextsyl',
                'sylnum_in_preword','sylnum_in_curword','sylnum_in_nextword',
                'sylnum_in_prephrase','sylnum_in_curphrase','sylnum_in_nextphrase',
                'wordnum_in_prephrase','wordnum_in_curphrase','wordnum_in_nextphrase',
                'sylnum_in_sentense','wordnum_in_sentense','phrasenum_in_sentense',
                'ph_in_syl_fw','ph_in_syl_bw','syl_in_word_fw','syl_in_word_bw',
                'syl_in_phrase_fw','syl_in_phrase_bw','word_in_phrase_fw','word_in_phrase_bw',
                'phrase_in_sentense_fw','phrase_in_sentense_bw','b7','b8','b9','b10']
'''

qst_config = {"LLphone":r'\w+\;',"Lphone":r'\;\w+\-',"Cphone":r'\-\w+\+',
            "Rphone":r'\+\w+\;',"RRphone":r'\;\w+\!',"vowel":r'\!\w+\|',
            "Lstress":r'\|\w+\:',"Cstress":r'\:\w+\:',"Rstress":r'\:\w+\|',
            "Lpos":r'\|\w+\$?\#',"Cpos":r'\#\w+\$?\#',"Rpos":r'\#\w+\$?\|',
            "phone_syllable_fw":r'\|\w+\$',"phone_syllable_bw":r'\$\w+\$',"phones_syllable":r'\$\w+\|',
            "syllable_word_fw":r'\|\w+\@',"syllable_word_bw":r'\@\w+\@',"syllables_word":r'\@\w+\|',
            "word_sentence_fw":r'\|\w+\&',"word_sentence_bw":r'\&\w+\&',"words_sentence":r'\&\w+\|',
            "sentence_utterance_fw":r'\|\w+\^',"sentence_utterance_bw":r'\^\w+\^',"sentences_utterance":r'\^\w+\|',
            "phones_utterance":r'\|\w+\=',"syllables_utterance":r'\=\w+\=',"words_utterance":r'\=\w+\|',
            "stressed_syllables_sentence_before_syllable":r'\|\w+\+',"stressed_syllables_sentence_after_syllable":r'\+\w+\&',
            "syllables_previous_stressed_syllable_and_syllable":r'\&\w+\+',"syllables_syllable_and_next_stressed_syllable":r'\+\w+'
}

Group_onehot = ['LLphone','Lphone','Cphone','Rphone','RRphone','vowel',
                'Lstress','Cstress','Rstress','Lpos','Cpos','Rpos']

Group_value = ["phone_syllable_fw","phone_syllable_bw","phones_syllable",
                "syllable_word_fw","syllable_word_bw","syllables_word",
                "word_sentence_fw","word_sentence_bw","words_sentence",
                "sentence_utterance_fw","sentence_utterance_bw","sentences_utterance",
                "phones_utterance","syllables_utterance","words_utterance",
                "stressed_syllables_sentence_before_syllable","stressed_syllables_sentence_after_syllable",
                "syllables_previous_stressed_syllable_and_syllable","syllables_syllable_and_next_stressed_syllable"
]

# sub group
Group_phone = ['LLphone','Lphone','Cphone','Rphone','RRphone']
Group_syl_vowel = ['vowel']
Group_GPOS = ['Lpos','Cpos','Rpos']
Group_stress = ['Lstress','Cstress','Rstress']

pattern_phone = r'[a-z0-9]+'
pattern_syl_vowel = r'[a-zA-z0-9]+'
pattern_GPOS = r'[a-z0-9$]+'
pattern_stress = r'[a-z0-9]+'
pattern_value = r'\d+'

def read_hdf5(hdf5_name, hdf5_path):
    """READ HDF5 DATASET.

    Args:
        hdf5_name (str): Filename of hdf5 file.
        hdf5_path (str): Dataset name in hdf5 file.

    Return:
        any: Dataset values.

    """

    hdf5_file = h5py.File(hdf5_name, "r")
    hdf5_data = hdf5_file[hdf5_path][()]
    hdf5_file.close()

    return hdf5_data

def get_phone_vector(label):
    #label =' 2000000  2700000 /A:x^sil-ih+t+w/B:0^2+3=IH/C:0^1=1/D:0^6@0-0=5^0/E:6$5-1/F:0$0+0/G:0$0=0/H:1$2@1@1$1&6-1&5#1#1/I:0-3@3+1/J:'
    qst_list = list(qst_config.keys())
    pattern = []
    pattern_timestamp = r'\d+'
    for i in range(len(qst_list)):
        pattern.append(qst_config[qst_list[i]])

    # print("pattern :", len(pattern) ,label)
    result = []
    for i in range(len(pattern)):
        # tmp = re.search(pattern[i], label)
        # print(pattern[i], tmp)
        #print(pattern[i])
        result.append(re.search(pattern[i], label).group(0))

    # get durations
    time_stamp = re.findall(pattern_timestamp, label)
    duration = (int(time_stamp[1]) - int(time_stamp[0])) / float(10**7)
    err = 0
    if duration < 0 :
        duration = abs(duration)
        err = 1

    #print(result)
    ## result and qstlist mapping
    normalize_number = 1
    result_vec = []
    for i in range(len(result)) :
        vec = []
        if qst_list[i] in Group_onehot :
            if qst_list[i]  in Group_phone :
                match = re.search(pattern_phone, result[i]).group(0)
                for j in range(len(QS_phone)):
                    if match in list(QS_phone.values())[j]:
                        vec.append(1.0)
                    else :
                        vec.append(0.0)

            if qst_list[i] in Group_syl_vowel :
                match = re.search(pattern_syl_vowel, result[i]).group(0)
                for j in range(len(QS_syl_vowel)):
                    if match in list(QS_syl_vowel.values())[j]:
                        vec.append(1.0)
                    else :
                        vec.append(0.0)

            if qst_list[i] in Group_GPOS :
                match = re.search(pattern_GPOS, result[i]).group(0)
                for j in range(len(QS_POS)):
                    if match in list(QS_POS.values())[j]:
                        vec.append(1.0)
                    else :
                        vec.append(0.0)

            if qst_list[i] in Group_stress :
                match = re.search(pattern_stress, result[i]).group(0)
                for j in range(len(QS_syl_stress)):
                    if match in list(QS_syl_stress.values())[j]:
                        vec.append(1.0)
                    else :
                        vec.append(0.0)


        elif qst_list[i] in Group_value :
            if qst_list[i] in ["phone_syllable_fw","phone_syllable_bw","phones_syllable"]:
                normalize_number = 7
            elif qst_list[i] in ["syllable_word_fw","syllable_word_bw","syllables_word"]:
                normalize_number = 7
            elif qst_list[i] in ["word_sentence_fw","word_sentence_bw","words_sentence"]:
                normalize_number = 13
            elif qst_list[i] in ["sentence_utterance_fw","sentence_utterance_bw","sentences_utterance"]:
                normalize_number = 4
            elif qst_list[i] in ['phones_utterance']:
                normalize_number = 60
            elif qst_list[i] in ['syllables_utterance']:
                normalize_number = 28
            elif qst_list[i] in ['words_utterance']:
                normalize_number = 13
            elif qst_list[i] in ["stressed_syllables_sentence_before_syllable","stressed_syllables_sentence_after_syllable"]:
                normalize_number = 12
            elif qst_list[i] in ["syllables_previous_stressed_syllable_and_syllable","syllables_syllable_and_next_stressed_syllable"]:
                normalize_number = 5

            try :
                match = re.search(pattern_value, result[i]).group(0)
                match = int(match) / normalize_number
            except :
                match = 0.0
            vec.append(float(match))

        result_vec.append(vec)
    # print(result_vec)

    result_vec = list(itertools.chain.from_iterable(result_vec))
    # print(len(result_vec))

    return result_vec, duration, err

def Qstvector_Generation(htslabelIn_dir_path, VecOut_dir_path):

    if not os.path.isdir(VecOut_dir_path):
	    os.makedirs(VecOut_dir_path)

    for dirPath, dirNames, fileNames in os.walk(htslabelIn_dir_path):
        htslab_fileName = sorted(fileNames)

    for index, filename in enumerate(htslab_fileName):
        vec_all = []
        filepath = os.path.join(htslabelIn_dir_path, filename)
        vec_filename = 'label-{}.npy'.format(filename.replace(".lab",""))
        vec_filepath = os.path.join(VecOut_dir_path , vec_filename)

        with open(filepath, mode='r') as fin :
            for line in fin :
                result, duration, err = get_phone_vector(line)
                vec_all.append(result)

        np.save(vec_filepath,np.array(vec_all)) # (phone, 762)

        print("gen_qstvector_output", vec_filepath)




    return 0

if __name__ == '__main__':

    output_dir_path = os.path.join(os.getcwd(), "output")
    htslabelIn_dir_path = os.path.join(output_dir_path, "Hts_Label", "full")
    VecOut_dir_path = os.path.join(output_dir_path, "Qst_Vector")


    Qstvector_Generation(htslabelIn_dir_path, VecOut_dir_path)
