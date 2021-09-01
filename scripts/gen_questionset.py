import os
import re
import json
import re
'''
label = []
with open("./output/full/cmu_us_arctic_slt_a0005.lab") as fin :
    for line in fin :
        label.append(line)

#print(label)
print(label[1])
pattern = re.compile(r'\W\w+\W')
match = pattern.findall(label[0])
print(match)
'''

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
        'aa':['aa'],'ae':['ae'],'ah':['ah'],'ao':['ao'],'aw':['aw'],
        'ay':['ay'],'b':['b'],'ch':['ch'],'d':['d'],'dh':['dh'],'eh':['eh'],
        'er':['er'],'ey':['ey'],'f':['f'],'g':['g'],'hh':['hh'],'ih':['ih'],'iy':['iy'],
        'jh':['jh'],'k':['k'],'l':['l'],'m':['m'],'n':['n'],'ng':['ng'],'ow':['ow'],'oy':['oy'],'p':['p'],
        'r':['r'],'s':['s'],'sh':['sh'],'t':['t'],'th':['th'],'uh':['uh'],'uw':['uw'],'v':['v'],'w':['w'],'y':['y'],
        'z':['z'],'zh':['zh'],'pau':['pau'],'sil':['sil'],'sp':['sp'],'0':['0']}

QS_phones_in_syl={
            'Syl_Num-Segs==0':['0'],
            'Syl_Num-Segs==1':['1'],
            'Syl_Num-Segs==2':['2'],
            'Syl_Num-Segs==3':['3'],
            'Syl_Num-Segs==4':['4'],
            'Syl_Num-Segs==5':['5'],
            'Syl_Num-Segs==6':['6'],
            'Syl_Num-Segs==7':['7'],
            'Syl_Num-Segs<=2':['1','2'],
            'Syl_Num-Segs<=3':['1','2','3'],
            'Syl_Num-Segs<=4':['1','2','3','4'],
            'Syl_Num-Segs<=5':['1','2','3','4','5'],
            'Syl_Num-Segs<=6':['1','2','3','4','5','6'],
            'Syl_Num-Segs<=7':['1','2','3','4','5','6','7'],}

QS_syl_vowel={
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
            'Syl_ay':['ay'],
            'Syl_eh':['eh'],
            'Syl_er':['er'],
            'Syl_ey':['ey'],
            'Syl_ih':['ih'],
            'Syl_iy':['iy'],
            'Syl_ow':['ow'],
            'Syl_oy':['oy'],
            'Syl_uh':['uh'],
            'Syl_uw':['uw'],
            'Syl_no_vowel':['0'],
            }

QS_syls_in_word={
                'Word_Num-Syls==0':['0'],
                'Word_Num-Syls==1':['1'],
                'Word_Num-Syls==2':['2'],
                'Word_Num-Syls==3':['3'],
                'Word_Num-Syls==4':['4'],
                'Word_Num-Syls==5':['5'],
                'Word_Num-Syls==6':['6'],
                'Word_Num-Syls==7':['7'],
                'Word_Num-Syls<=2':['1','2'],
                'Word_Num-Syls<=3':['1','2','3'],
                'Word_Num-Syls<=4':['1','2','3','4'],
                'Word_Num-Syls<=5':['1','2','3','4','5'],
                'Word_Num-Syls<=6':['1','2','3','4','5','6'],
                'Word_Num-Syls<=7':['1','2','3','4','5','6','7'],}

QS_syls_in_phrase={
                'Phrase_Num-Syls==0':['0'],
                'Phrase_Num-Syls==1':['1'],
                'Phrase_Num-Syls==2':['2'],
                'Phrase_Num-Syls==3':['3'],
                'Phrase_Num-Syls==4':['4'],
                'Phrase_Num-Syls==5':['5'],
                'Phrase_Num-Syls==6':['6'],
                'Phrase_Num-Syls==7':['7'],
                'Phrase_Num-Syls==8':['8'],
                'Phrase_Num-Syls==9':['9'],
                'Phrase_Num-Syls==10':['10'],
                'Phrase_Num-Syls==11':['11'],
                'Phrase_Num-Syls==12':['12'],
                'Phrase_Num-Syls==13':['13'],
                'Phrase_Num-Syls==14':['14'],
                'Phrase_Num-Syls==15':['15'],
                'Phrase_Num-Syls==16':['16'],
                'Phrase_Num-Syls==17':['17'],
                'Phrase_Num-Syls==18':['18'],
                'Phrase_Num-Syls==19':['19'],
                'Phrase_Num-Syls==20':['20'],
                'Phrase_Num-Syls<=2':['1','2'],
                'Phrase_Num-Syls<=3':['1','2','3'],
                'Phrase_Num-Syls<=4':['1','2','3','4'],
                'Phrase_Num-Syls<=5':['1','2','3','4','5'],
                'Phrase_Num-Syls<=6':['1','2','3','4','5','6'],
                'Phrase_Num-Syls<=7':['1','2','3','4','5','6','7'],
                'Phrase_Num-Syls<=8':['1','2','3','4','5','6','7','8'],
                'Phrase_Num-Syls<=9':['1','2','3','4','5','6','7','8','9'],
                'Phrase_Num-Syls<=10':['1','2','3','4','5','6','7','8','9','10'],
                'Phrase_Num-Syls<=11':['1','2','3','4','5','6','7','8','9','10','11'],
                'Phrase_Num-Syls<=12':['1','2','3','4','5','6','7','8','9','10','11','12'],
                'Phrase_Num-Syls<=13':['1','2','3','4','5','6','7','8','9','10','11','12','13'],
                'Phrase_Num-Syls<=14':['1','2','3','4','5','6','7','8','9','10','11','12','13','14'],
                'Phrase_Num-Syls<=15':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'],
                'Phrase_Num-Syls<=16':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'],
                'Phrase_Num-Syls<=17':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'],
                'Phrase_Num-Syls<=18':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18'],
                'Phrase_Num-Syls<=19':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19'],
                'Phrase_Num-Syls<=20':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'],}

QS_words_in_phrase={
                    'Phrase_Num-Words==0':['0'],
                    'Phrase_Num-Words==1':['1'],
                    'Phrase_Num-Words==2':['2'],
                    'Phrase_Num-Words==3':['3'],
                    'Phrase_Num-Words==4':['4'],
                    'Phrase_Num-Words==5':['5'],
                    'Phrase_Num-Words==6':['6'],
                    'Phrase_Num-Words==7':['7'],
                    'Phrase_Num-Words==8':['8'],
                    'Phrase_Num-Words==9':['9'],
                    'Phrase_Num-Words==10':['10'],
                    'Phrase_Num-Words==11':['11'],
                    'Phrase_Num-Words==12':['12'],
                    'Phrase_Num-Words==13':['13'],

                    'Phrase_Num-Words<=2':['1','2'],
                    'Phrase_Num-Words<=3':['1','2','3'],
                    'Phrase_Num-Words<=4':['1','2','3','4'],
                    'Phrase_Num-Words<=5':['1','2','3','4','5'],
                    'Phrase_Num-Words<=6':['1','2','3','4','5','6'],
                    'Phrase_Num-Words<=7':['1','2','3','4','5','6','7'],
                    'Phrase_Num-Words<=8':['1','2','3','4','5','6','7','8'],
                    'Phrase_Num-Words<=9':['1','2','3','4','5','6','7','8','9'],
                    'Phrase_Num-Words<=10':['1','2','3','4','5','6','7','8','9','10'],
                    'Phrase_Num-Words<=11':['1','2','3','4','5','6','7','8','9','10','11'],
                    'Phrase_Num-Words<=12':['1','2','3','4','5','6','7','8','9','10','11','12'],
                    'Phrase_Num-Words<=13':['1','2','3','4','5','6','7','8','9','10','11','12','13'],}

QS_syls_in_sentense={
                    'Num-Syls_in_Utterance==0':['0'],
                    'Num-Syls_in_Utterance==1':['1'],
                    'Num-Syls_in_Utterance==2':['2'],
                    'Num-Syls_in_Utterance==3':['3'],
                    'Num-Syls_in_Utterance==4':['4'],
                    'Num-Syls_in_Utterance==5':['5'],
                    'Num-Syls_in_Utterance==6':['6'],
                    'Num-Syls_in_Utterance==7':['7'],
                    'Num-Syls_in_Utterance==8':['8'],
                    'Num-Syls_in_Utterance==9':['9'],
                    'Num-Syls_in_Utterance==10':['10'],
                    'Num-Syls_in_Utterance==11':['11'],
                    'Num-Syls_in_Utterance==12':['12'],
                    'Num-Syls_in_Utterance==13':['13'],
                    'Num-Syls_in_Utterance==14':['14'],
                    'Num-Syls_in_Utterance==15':['15'],
                    'Num-Syls_in_Utterance==16':['16'],
                    'Num-Syls_in_Utterance==17':['17'],
                    'Num-Syls_in_Utterance==18':['18'],
                    'Num-Syls_in_Utterance==19':['19'],
                    'Num-Syls_in_Utterance==20':['20'],
                    'Num-Syls_in_Utterance==21':['21'],
                    'Num-Syls_in_Utterance==22':['22'],
                    'Num-Syls_in_Utterance==23':['23'],
                    'Num-Syls_in_Utterance==24':['24'],
                    'Num-Syls_in_Utterance==25':['25'],
                    'Num-Syls_in_Utterance==26':['26'],
                    'Num-Syls_in_Utterance==27':['27'],
                    'Num-Syls_in_Utterance==28':['28'],

                    'Num-Syls_in_Utterance<=2':['1','2'],
                    'Num-Syls_in_Utterance<=3':['1','2','3'],
                    'Num-Syls_in_Utterance<=4':['1','2','3','4'],
                    'Num-Syls_in_Utterance<=5':['1','2','3','4','5'],
                    'Num-Syls_in_Utterance<=6':['1','2','3','4','5','6'],
                    'Num-Syls_in_Utterance<=7':['1','2','3','4','5','6','7'],
                    'Num-Syls_in_Utterance<=8':['1','2','3','4','5','6','7','8'],
                    'Num-Syls_in_Utterance<=9':['1','2','3','4','5','6','7','8','9'],
                    'Num-Syls_in_Utterance<=10':['1','2','3','4','5','6','7','8','9','10'],
                    'Num-Syls_in_Utterance<=11':['1','2','3','4','5','6','7','8','9','10','11'],
                    'Num-Syls_in_Utterance<=12':['1','2','3','4','5','6','7','8','9','10','11','12'],
                    'Num-Syls_in_Utterance<=13':['1','2','3','4','5','6','7','8','9','10','11','12','13'],
                    'Num-Syls_in_Utterance<=14':['1','2','3','4','5','6','7','8','9','10','11','12','13','14'],
                    'Num-Syls_in_Utterance<=15':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'],
                    'Num-Syls_in_Utterance<=16':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'],
                    'Num-Syls_in_Utterance<=17':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'],
                    'Num-Syls_in_Utterance<=18':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18'],
                    'Num-Syls_in_Utterance<=19':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19'],
                    'Num-Syls_in_Utterance<=20':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'],
                    'Num-Syls_in_Utterance<=21':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21'],
                    'Num-Syls_in_Utterance<=22':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22'],
                    'Num-Syls_in_Utterance<=23':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23'],
                    'Num-Syls_in_Utterance<=24':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24'],
                    'Num-Syls_in_Utterance<=25':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25'],
                    'Num-Syls_in_Utterance<=26':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26'],
                    'Num-Syls_in_Utterance<=27':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27'],
                    'Num-Syls_in_Utterance<=28':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28'],}

QS_phones_in_sentense={
                    'Num-Phones_in_Utterance==0':['0'],
                    'Num-Phones_in_Utterance==1':['1'],
                    'Num-Phones_in_Utterance==2':['2'],
                    'Num-Phones_in_Utterance==3':['3'],
                    'Num-Phones_in_Utterance==4':['4'],
                    'Num-Phones_in_Utterance==5':['5'],
                    'Num-Phones_in_Utterance==6':['6'],
                    'Num-Phones_in_Utterance==7':['7'],
                    'Num-Phones_in_Utterance==8':['8'],
                    'Num-Phones_in_Utterance==9':['9'],
                    'Num-Phones_in_Utterance==10':['10'],
                    'Num-Phones_in_Utterance==11':['11'],
                    'Num-Phones_in_Utterance==12':['12'],
                    'Num-Phones_in_Utterance==13':['13'],
                    'Num-Phones_in_Utterance==14':['14'],
                    'Num-Phones_in_Utterance==15':['15'],
                    'Num-Phones_in_Utterance==16':['16'],
                    'Num-Phones_in_Utterance==17':['17'],
                    'Num-Phones_in_Utterance==18':['18'],
                    'Num-Phones_in_Utterance==19':['19'],
                    'Num-Phones_in_Utterance==20':['20'],
                    'Num-Phones_in_Utterance==21':['21'],
                    'Num-Phones_in_Utterance==22':['22'],
                    'Num-Phones_in_Utterance==23':['23'],
                    'Num-Phones_in_Utterance==24':['24'],
                    'Num-Phones_in_Utterance==25':['25'],
                    'Num-Phones_in_Utterance==26':['26'],
                    'Num-Phones_in_Utterance==27':['27'],
                    'Num-Phones_in_Utterance==28':['28'],

                    'Num-Phones_in_Utterance<=2':['1','2'],
                    'Num-Phones_in_Utterance<=3':['1','2','3'],
                    'Num-Phones_in_Utterance<=4':['1','2','3','4'],
                    'Num-Phones_in_Utterance<=5':['1','2','3','4','5'],
                    'Num-Phones_in_Utterance<=6':['1','2','3','4','5','6'],
                    'Num-Phones_in_Utterance<=7':['1','2','3','4','5','6','7'],
                    'Num-Phones_in_Utterance<=8':['1','2','3','4','5','6','7','8'],
                    'Num-Phones_in_Utterance<=9':['1','2','3','4','5','6','7','8','9'],
                    'Num-Phones_in_Utterance<=10':['1','2','3','4','5','6','7','8','9','10'],
                    'Num-Phones_in_Utterance<=11':['1','2','3','4','5','6','7','8','9','10','11'],
                    'Num-Phones_in_Utterance<=12':['1','2','3','4','5','6','7','8','9','10','11','12'],
                    'Num-Phones_in_Utterance<=13':['1','2','3','4','5','6','7','8','9','10','11','12','13'],
                    'Num-Phones_in_Utterance<=14':['1','2','3','4','5','6','7','8','9','10','11','12','13','14'],
                    'Num-Phones_in_Utterance<=15':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'],
                    'Num-Phones_in_Utterance<=16':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'],
                    'Num-Phones_in_Utterance<=17':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'],
                    'Num-Phones_in_Utterance<=18':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18'],
                    'Num-Phones_in_Utterance<=19':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19'],
                    'Num-Phones_in_Utterance<=20':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'],
                    'Num-Phones_in_Utterance<=21':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21'],
                    'Num-Phones_in_Utterance<=22':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22'],
                    'Num-Phones_in_Utterance<=23':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23'],
                    'Num-Phones_in_Utterance<=24':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24'],
                    'Num-Phones_in_Utterance<=25':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25'],
                    'Num-Phones_in_Utterance<=26':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26'],
                    'Num-Phones_in_Utterance<=27':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27'],
                    'Num-Phones_in_Utterance<=28':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28'],}


QS_words_in_sentense={
                    'Num-Words_in_Utterance==0':['0'],
                    'Num-Words_in_Utterance==1':['1'],
                    'Num-Words_in_Utterance==2':['2'],
                    'Num-Words_in_Utterance==3':['3'],
                    'Num-Words_in_Utterance==4':['4'],
                    'Num-Words_in_Utterance==5':['5'],
                    'Num-Words_in_Utterance==6':['6'],
                    'Num-Words_in_Utterance==7':['7'],
                    'Num-Words_in_Utterance==8':['8'],
                    'Num-Words_in_Utterance==9':['9'],
                    'Num-Words_in_Utterance==10':['10'],
                    'Num-Words_in_Utterance==11':['11'],
                    'Num-Words_in_Utterance==12':['12'],
                    'Num-Words_in_Utterance==13':['13'],

                    'Num-Words_in_Utterance<=2':['1','2'],
                    'Num-Words_in_Utterance<=3':['1','2','3'],
                    'Num-Words_in_Utterance<=4':['1','2','3','4'],
                    'Num-Words_in_Utterance<=5':['1','2','3','4','5'],
                    'Num-Words_in_Utterance<=6':['1','2','3','4','5','6'],
                    'Num-Words_in_Utterance<=7':['1','2','3','4','5','6','7'],
                    'Num-Words_in_Utterance<=8':['1','2','3','4','5','6','7','8'],
                    'Num-Words_in_Utterance<=9':['1','2','3','4','5','6','7','8','9'],
                    'Num-Words_in_Utterance<=10':['1','2','3','4','5','6','7','8','9','10'],
                    'Num-Words_in_Utterance<=11':['1','2','3','4','5','6','7','8','9','10','11'],
                    'Num-Words_in_Utterance<=12':['1','2','3','4','5','6','7','8','9','10','11','12'],
                    'Num-Words_in_Utterance<=13':['1','2','3','4','5','6','7','8','9','10','11','12','13'],}

QS_phrases_in_sentense={
                        'Num-Phrases_in_Utterance==0':['0'],
                        'Num-Phrases_in_Utterance==1':['1'],
                        'Num-Phrases_in_Utterance==2':['2'],
                        'Num-Phrases_in_Utterance==3':['3'],
                        'Num-Phrases_in_Utterance==4':['4'],

                        'Num-Phrases_in_Utterance<=2':['1','2'],
                        'Num-Phrases_in_Utterance<=3':['1','2','3'],
                        'Num-Phrases_in_Utterance<=4':['1','2','3','4'],}
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
        'Word_GPOS==wp':['wp'],}
'''
QS_POS={'Word_GPOS==0':['0'], # 代表沒有GPOS
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
            'Syl_Stress==0':['0'],}

QS_b7={
    'Num-StressedSyl_before_C-Syl_in_C-Phrase==0':['0'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase==1':['1'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase==2':['2'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase==3':['3'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase==4':['4'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase==5':['5'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase==6':['6'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase==7':['7'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase==8':['8'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase==9':['9'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase==10':['10'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase==11':['11'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase==12':['12'],

    'Num-StressedSyl_before_C-Syl_in_C-Phrase<=1':['0','1'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase<=2':['0','1','2'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase<=3':['0','1','2','3'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase<=4':['0','1','2','3','4'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase<=5':['0','1','2','3','4','5'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase<=6':['0','1','2','3','4','5','6'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase<=7':['0','1','2','3','4','5','6','7'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase<=8':['0','1','2','3','4','5','6','7','8'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase<=9':['0','1','2','3','4','5','6','7','8','9'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase<=10':['0','1','2','3','4','5','6','7','8','9','10'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase<=11':['0','1','2','3','4','5','6','7','8','9','10','11'],
    'Num-StressedSyl_before_C-Syl_in_C-Phrase<=12':['0','1','2','3','4','5','6','7','8','9','10','11','12'],}

QS_b8={
    'Num-StressedSyl_after_C-Syl_in_C-Phrase==0':['0'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase==1':['1'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase==2':['2'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase==3':['3'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase==4':['4'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase==5':['5'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase==6':['6'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase==7':['7'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase==8':['8'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase==9':['9'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase==10':['10'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase==11':['11'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase==12':['12'],

    'Num-StressedSyl_after_C-Syl_in_C-Phrase<=1':['0','1'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase<=2':['0','1','2'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase<=3':['0','1','2','3'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase<=4':['0','1','2','3','4'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase<=5':['0','1','2','3','4','5'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase<=6':['0','1','2','3','4','5','6'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase<=7':['0','1','2','3','4','5','6','7'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase<=8':['0','1','2','3','4','5','6','7','8'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase<=9':['0','1','2','3','4','5','6','7','8','9'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase<=10':['0','1','2','3','4','5','6','7','8','9','10'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase<=11':['0','1','2','3','4','5','6','7','8','9','10','11'],
    'Num-StressedSyl_after_C-Syl_in_C-Phrase<=12':['0','1','2','3','4','5','6','7','8','9','10','11','12'],}

QS_b9={
    'Num-Syl_from_prev-StressedSyl==0':['0'],
    'Num-Syl_from_prev-StressedSyl==1':['1'],
    'Num-Syl_from_prev-StressedSyl==2':['2'],
    'Num-Syl_from_prev-StressedSyl==3':['3'],
    'Num-Syl_from_prev-StressedSyl==4':['4'],
    'Num-Syl_from_prev-StressedSyl==5':['5'],

    'Num-Syl_from_prev-StressedSyl<=0':['0'],
    'Num-Syl_from_prev-StressedSyl<=1':['0','1'],
    'Num-Syl_from_prev-StressedSyl<=2':['0','1','2'],
    'Num-Syl_from_prev-StressedSyl<=3':['0','1','2','3'],
    'Num-Syl_from_prev-StressedSyl<=4':['0','1','2','3','4'],
    'Num-Syl_from_prev-StressedSyl<=5':['0','1','2','3','4','5'],}

QS_b10={
        'Num-Syl_from_next-StressedSyl==0':['0'],
        'Num-Syl_from_next-StressedSyl==1':['1'],
        'Num-Syl_from_next-StressedSyl==2':['2'],
        'Num-Syl_from_next-StressedSyl==3':['3'],
        'Num-Syl_from_next-StressedSyl==4':['4'],
        'Num-Syl_from_next-StressedSyl==5':['5'],

        'Num-Syl_from_next-StressedSyl<=0':['0'],
        'Num-Syl_from_next-StressedSyl<=1':['0','1'],
        'Num-Syl_from_next-StressedSyl<=2':['0','1','2'],
        'Num-Syl_from_next-StressedSyl<=3':['0','1','2','3'],
        'Num-Syl_from_next-StressedSyl<=4':['0','1','2','3','4'],
        'Num-Syl_from_next-StressedSyl<=5':['0','1','2','3','4','5'],}

'''
QS_e5={'Num-ContWord_before_C-Word_in_C-Phrase==x':['x'],
    'Num-ContWord_before_C-Word_in_C-Phrase==0':['0'],
    'Num-ContWord_before_C-Word_in_C-Phrase==1':['1'],
    'Num-ContWord_before_C-Word_in_C-Phrase==2':['2'],
    'Num-ContWord_before_C-Word_in_C-Phrase==3':['3'],
    'Num-ContWord_before_C-Word_in_C-Phrase==4':['4'],
    'Num-ContWord_before_C-Word_in_C-Phrase==5':['5'],
    'Num-ContWord_before_C-Word_in_C-Phrase==6':['6'],
    'Num-ContWord_before_C-Word_in_C-Phrase==7':['7'],
    'Num-ContWord_before_C-Word_in_C-Phrase==8':['8'],
    'Num-ContWord_before_C-Word_in_C-Phrase==9':['9'],

    'Num-ContWord_before_C-Word_in_C-Phrase<=1':['0','1'],
    'Num-ContWord_before_C-Word_in_C-Phrase<=2':['0','1','2'],
    'Num-ContWord_before_C-Word_in_C-Phrase<=3':['0','1','2','3'],
    'Num-ContWord_before_C-Word_in_C-Phrase<=4':['0','1','2','3','4'],
    'Num-ContWord_before_C-Word_in_C-Phrase<=5':['0','1','2','3','4','5'],
    'Num-ContWord_before_C-Word_in_C-Phrase<=6':['0','1','2','3','4','5','6'],
    'Num-ContWord_before_C-Word_in_C-Phrase<=7':['0','1','2','3','4','5','6','7'],
    'Num-ContWord_before_C-Word_in_C-Phrase<=8':['0','1','2','3','4','5','6','7','8'],
    'Num-ContWord_before_C-Word_in_C-Phrase<=9':['0','1','2','3','4','5','6','7','8','9'],}

QS_e6={'Num-ContWord_after_C-Word_in_C-Phrase==x':['x'],
    'Num-ContWord_after_C-Word_in_C-Phrase==0':['0'],
    'Num-ContWord_after_C-Word_in_C-Phrase==1':['1'],
    'Num-ContWord_after_C-Word_in_C-Phrase==2':['2'],
    'Num-ContWord_after_C-Word_in_C-Phrase==3':['3'],
    'Num-ContWord_after_C-Word_in_C-Phrase==4':['4'],
    'Num-ContWord_after_C-Word_in_C-Phrase==5':['5'],
    'Num-ContWord_after_C-Word_in_C-Phrase==6':['6'],
    'Num-ContWord_after_C-Word_in_C-Phrase==7':['7'],
    'Num-ContWord_after_C-Word_in_C-Phrase==8':['8'],

    'Num-ContWord_after_C-Word_in_C-Phrase<=0':['0'],
    'Num-ContWord_after_C-Word_in_C-Phrase<=1':['0','1'],
    'Num-ContWord_after_C-Word_in_C-Phrase<=2':['0','1','2'],
    'Num-ContWord_after_C-Word_in_C-Phrase<=3':['0','1','2','3'],
    'Num-ContWord_after_C-Word_in_C-Phrase<=4':['0','1','2','3','4'],
    'Num-ContWord_after_C-Word_in_C-Phrase<=5':['0','1','2','3','4','5'],
    'Num-ContWord_after_C-Word_in_C-Phrase<=6':['0','1','2','3','4','5','6'],
    'Num-ContWord_after_C-Word_in_C-Phrase<=7':['0','1','2','3','4','5','6','7'],
    'Num-ContWord_after_C-Word_in_C-Phrase<=8':['0','1','2','3','4','5','6','7','8'],}

QS_e7={'Num-Words_from_prev-ContWord==x':['x'],
    'Num-Words_from_prev-ContWord==0':['0'],
    'Num-Words_from_prev-ContWord==1':['1'],
    'Num-Words_from_prev-ContWord==2':['2'],
    'Num-Words_from_prev-ContWord==3':['3'],
    'Num-Words_from_prev-ContWord==4':['4'],
    'Num-Words_from_prev-ContWord==5':['5'],

    'Num-Words_from_prev-ContWord<=0':['0'],
    'Num-Words_from_prev-ContWord<=1':['0','1'],
    'Num-Words_from_prev-ContWord<=2':['0','1','2'],
    'Num-Words_from_prev-ContWord<=3':['0','1','2','3'],
    'Num-Words_from_prev-ContWord<=4':['0','1','2','3','4'],
    'Num-Words_from_prev-ContWord<=5':['0','1','2','3','4','5'],}

QS_e8={'Num-Words_from_next-ContWord==x':['x'],
    'Num-Words_from_next-ContWord==0':['0'],
    'Num-Words_from_next-ContWord==1':['1'],
    'Num-Words_from_next-ContWord==2':['2'],
    'Num-Words_from_next-ContWord==3':['3'],
    'Num-Words_from_next-ContWord==4':['4'],
    'Num-Words_from_next-ContWord==5':['5'],

    'Num-Words_from_next-ContWord<=0':['0'],
    'Num-Words_from_next-ContWord<=1':['0','1'],
    'Num-Words_from_next-ContWord<=2':['0','1','2'],
    'Num-Words_from_next-ContWord<=3':['0','1','2','3'],
    'Num-Words_from_next-ContWord<=4':['0','1','2','3','4'],
    'Num-Words_from_next-ContWord<=5':['0','1','2','3','4','5'],}
'''
QS_p6={
    'Seg_Fw==1':['1'],
    'Seg_Fw==2':['2'],
    'Seg_Fw==3':['3'],
    'Seg_Fw==4':['4'],
    'Seg_Fw==5':['5'],
    'Seg_Fw==6':['6'],
    'Seg_Fw==7':['7'],

    'Seg_Fw<=2':['1','2'],
    'Seg_Fw<=3':['1','2','3'],
    'Seg_Fw<=4':['1','2','3','4'],
    'Seg_Fw<=5':['1','2','3','4','5'],
    'Seg_Fw<=6':['1','2','3','4','5','6'],
    'Seg_Fw<=7':['1','2','3','4','5','6','7'],}

QS_p7={
    'Seg_Bw==1':['1'],
    'Seg_Bw==2':['2'],
    'Seg_Bw==3':['3'],
    'Seg_Bw==4':['4'],
    'Seg_Bw==5':['5'],
    'Seg_Bw==6':['6'],
    'Seg_Bw==7':['7'],

    'Seg_Bw<=0':['0'],
    'Seg_Bw<=1':['0','1'],
    'Seg_Bw<=2':['0','1','2'],
    'Seg_Bw<=3':['0','1','2','3'],
    'Seg_Bw<=4':['0','1','2','3','4'],
    'Seg_Bw<=5':['0','1','2','3','4','5'],
    'Seg_Bw<=6':['0','1','2','3','4','5','6'],
    'Seg_Bw<=7':['0','1','2','3','4','5','6','7'],}

QS_b3={
    'Pos_C-Syl_in_C-Word(Fw)==1':['1'],
    'Pos_C-Syl_in_C-Word(Fw)==2':['2'],
    'Pos_C-Syl_in_C-Word(Fw)==3':['3'],
    'Pos_C-Syl_in_C-Word(Fw)==4':['4'],
    'Pos_C-Syl_in_C-Word(Fw)==5':['5'],
    'Pos_C-Syl_in_C-Word(Fw)==6':['6'],
    'Pos_C-Syl_in_C-Word(Fw)==7':['7'],

    'Pos_C-Syl_in_C-Word(Fw)<=1':['1'],
    'Pos_C-Syl_in_C-Word(Fw)<=2':['1','2'],
    'Pos_C-Syl_in_C-Word(Fw)<=3':['1','2','3'],
    'Pos_C-Syl_in_C-Word(Fw)<=4':['1','2','3','4'],
    'Pos_C-Syl_in_C-Word(Fw)<=5':['1','2','3','4','5'],
    'Pos_C-Syl_in_C-Word(Fw)<=6':['1','2','3','4','5','6'],
    'Pos_C-Syl_in_C-Word(Fw)<=7':['1','2','3','4','5','6','7'],}

QS_b4={
    'Pos_C-Syl_in_C-Word(Bw)==1':['1'],
    'Pos_C-Syl_in_C-Word(Bw)==2':['2'],
    'Pos_C-Syl_in_C-Word(Bw)==3':['3'],
    'Pos_C-Syl_in_C-Word(Bw)==4':['4'],
    'Pos_C-Syl_in_C-Word(Bw)==5':['5'],
    'Pos_C-Syl_in_C-Word(Bw)==6':['6'],
    'Pos_C-Syl_in_C-Word(Bw)==7':['7'],


    'Pos_C-Syl_in_C-Word(Bw)<=2':['1','2'],
    'Pos_C-Syl_in_C-Word(Bw)<=3':['1','2','3'],
    'Pos_C-Syl_in_C-Word(Bw)<=4':['1','2','3','4'],
    'Pos_C-Syl_in_C-Word(Bw)<=5':['1','2','3','4','5'],
    'Pos_C-Syl_in_C-Word(Bw)<=6':['1','2','3','4','5','6'],
    'Pos_C-Syl_in_C-Word(Bw)<=7':['1','2','3','4','5','6','7'],}

QS_b5={
    'Pos_C-Syl_in_C-Phrase(Fw)==1':['1'],
    'Pos_C-Syl_in_C-Phrase(Fw)==2':['2'],
    'Pos_C-Syl_in_C-Phrase(Fw)==3':['3'],
    'Pos_C-Syl_in_C-Phrase(Fw)==4':['4'],
    'Pos_C-Syl_in_C-Phrase(Fw)==5':['5'],
    'Pos_C-Syl_in_C-Phrase(Fw)==6':['6'],
    'Pos_C-Syl_in_C-Phrase(Fw)==7':['7'],
    'Pos_C-Syl_in_C-Phrase(Fw)==8':['8'],
    'Pos_C-Syl_in_C-Phrase(Fw)==9':['9'],
    'Pos_C-Syl_in_C-Phrase(Fw)==10':['10'],
    'Pos_C-Syl_in_C-Phrase(Fw)==11':['11'],
    'Pos_C-Syl_in_C-Phrase(Fw)==12':['12'],
    'Pos_C-Syl_in_C-Phrase(Fw)==13':['13'],
    'Pos_C-Syl_in_C-Phrase(Fw)==14':['14'],
    'Pos_C-Syl_in_C-Phrase(Fw)==15':['15'],
    'Pos_C-Syl_in_C-Phrase(Fw)==16':['16'],
    'Pos_C-Syl_in_C-Phrase(Fw)==17':['17'],
    'Pos_C-Syl_in_C-Phrase(Fw)==18':['18'],
    'Pos_C-Syl_in_C-Phrase(Fw)==19':['19'],
    'Pos_C-Syl_in_C-Phrase(Fw)==20':['20'],


    'Pos_C-Syl_in_C-Phrase(Fw)<=2':['1','2'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=3':['1','2','3'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=4':['1','2','3','4'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=5':['1','2','3','4','5'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=6':['1','2','3','4','5','6'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=7':['1','2','3','4','5','6','7'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=8':['1','2','3','4','5','6','7','8'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=9':['1','2','3','4','5','6','7','8','9'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=10':['1','2','3','4','5','6','7','8','9','10'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=11':['1','2','3','4','5','6','7','8','9','10','11'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=12':['1','2','3','4','5','6','7','8','9','10','11','12'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=13':['1','2','3','4','5','6','7','8','9','10','11','12','13'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=14':['1','2','3','4','5','6','7','8','9','10','11','12','13','14'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=15':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=16':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=17':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=18':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=19':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19'],
    'Pos_C-Syl_in_C-Phrase(Fw)<=20':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'],}

QS_b6={
     'Pos_C-Syl_in_C-Phrase(Bw)==1':['1'],
     'Pos_C-Syl_in_C-Phrase(Bw)==2':['2'],
     'Pos_C-Syl_in_C-Phrase(Bw)==3':['3'],
     'Pos_C-Syl_in_C-Phrase(Bw)==4':['4'],
     'Pos_C-Syl_in_C-Phrase(Bw)==5':['5'],
     'Pos_C-Syl_in_C-Phrase(Bw)==6':['6'],
     'Pos_C-Syl_in_C-Phrase(Bw)==7':['7'],
     'Pos_C-Syl_in_C-Phrase(Bw)==8':['8'],
     'Pos_C-Syl_in_C-Phrase(Bw)==9':['9'],
     'Pos_C-Syl_in_C-Phrase(Bw)==10':['10'],
     'Pos_C-Syl_in_C-Phrase(Bw)==11':['11'],
     'Pos_C-Syl_in_C-Phrase(Bw)==12':['12'],
     'Pos_C-Syl_in_C-Phrase(Bw)==13':['13'],
     'Pos_C-Syl_in_C-Phrase(Bw)==14':['14'],
     'Pos_C-Syl_in_C-Phrase(Bw)==15':['15'],
     'Pos_C-Syl_in_C-Phrase(Bw)==16':['16'],
     'Pos_C-Syl_in_C-Phrase(Bw)==17':['17'],
     'Pos_C-Syl_in_C-Phrase(Bw)==18':['18'],
     'Pos_C-Syl_in_C-Phrase(Bw)==19':['19'],
     'Pos_C-Syl_in_C-Phrase(Bw)==20':['20'],

     'Pos_C-Syl_in_C-Phrase(Bw)<=2':['1','2'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=3':['1','2','3'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=4':['1','2','3','4'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=5':['1','2','3','4','5'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=6':['1','2','3','4','5','6'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=7':['1','2','3','4','5','6','7'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=8':['1','2','3','4','5','6','7','8'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=9':['1','2','3','4','5','6','7','8','9'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=10':['1','2','3','4','5','6','7','8','9','10'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=11':['1','2','3','4','5','6','7','8','9','10','11'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=12':['1','2','3','4','5','6','7','8','9','10','11','12'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=13':['1','2','3','4','5','6','7','8','9','10','11','12','13'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=14':['1','2','3','4','5','6','7','8','9','10','11','12','13','14'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=15':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=16':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=17':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=18':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=19':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19'],
     'Pos_C-Syl_in_C-Phrase(Bw)<=20':['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'],}

QS_e3={
     'Pos_C-Word_in_C-Phrase(Fw)==1':['1'],
     'Pos_C-Word_in_C-Phrase(Fw)==2':['2'],
     'Pos_C-Word_in_C-Phrase(Fw)==3':['3'],
     'Pos_C-Word_in_C-Phrase(Fw)==4':['4'],
     'Pos_C-Word_in_C-Phrase(Fw)==5':['5'],
     'Pos_C-Word_in_C-Phrase(Fw)==6':['6'],
     'Pos_C-Word_in_C-Phrase(Fw)==7':['7'],
     'Pos_C-Word_in_C-Phrase(Fw)==8':['8'],
     'Pos_C-Word_in_C-Phrase(Fw)==9':['9'],
     'Pos_C-Word_in_C-Phrase(Fw)==10':['10'],
     'Pos_C-Word_in_C-Phrase(Fw)==11':['11'],
     'Pos_C-Word_in_C-Phrase(Fw)==12':['12'],
     'Pos_C-Word_in_C-Phrase(Fw)==13':['13'],

     'Pos_C-Word_in_C-Phrase(Fw)<=2':['1','2'],
     'Pos_C-Word_in_C-Phrase(Fw)<=3':['1','2','3'],
     'Pos_C-Word_in_C-Phrase(Fw)<=4':['1','2','3','4'],
     'Pos_C-Word_in_C-Phrase(Fw)<=5':['1','2','3','4','5'],
     'Pos_C-Word_in_C-Phrase(Fw)<=6':['1','2','3','4','5','6'],
     'Pos_C-Word_in_C-Phrase(Fw)<=7':['1','2','3','4','5','6','7'],
     'Pos_C-Word_in_C-Phrase(Fw)<=8':['1','2','3','4','5','6','7','8'],
     'Pos_C-Word_in_C-Phrase(Fw)<=9':['1','2','3','4','5','6','7','8','9'],
     'Pos_C-Word_in_C-Phrase(Fw)<=10':['1','2','3','4','5','6','7','8','9','10'],
     'Pos_C-Word_in_C-Phrase(Fw)<=11':['1','2','3','4','5','6','7','8','9','10','11'],
     'Pos_C-Word_in_C-Phrase(Fw)<=12':['1','2','3','4','5','6','7','8','9','10','11','12'],
     'Pos_C-Word_in_C-Phrase(Fw)<=13':['1','2','3','4','5','6','7','8','9','10','11','12','13'],}

QS_e4={
     'Pos_C-Word_in_C-Phrase(Bw)==1':['1'],
     'Pos_C-Word_in_C-Phrase(Bw)==2':['2'],
     'Pos_C-Word_in_C-Phrase(Bw)==3':['3'],
     'Pos_C-Word_in_C-Phrase(Bw)==4':['4'],
     'Pos_C-Word_in_C-Phrase(Bw)==5':['5'],
     'Pos_C-Word_in_C-Phrase(Bw)==6':['6'],
     'Pos_C-Word_in_C-Phrase(Bw)==7':['7'],
     'Pos_C-Word_in_C-Phrase(Bw)==8':['8'],
     'Pos_C-Word_in_C-Phrase(Bw)==9':['9'],
     'Pos_C-Word_in_C-Phrase(Bw)==10':['10'],
     'Pos_C-Word_in_C-Phrase(Bw)==11':['11'],
     'Pos_C-Word_in_C-Phrase(Bw)==12':['12'],
     'Pos_C-Word_in_C-Phrase(Bw)==13':['13'],

     'Pos_C-Word_in_C-Phrase(Bw)<=2':['0','1','2'],
     'Pos_C-Word_in_C-Phrase(Bw)<=3':['0','1','2','3'],
     'Pos_C-Word_in_C-Phrase(Bw)<=4':['0','1','2','3','4'],
     'Pos_C-Word_in_C-Phrase(Bw)<=5':['0','1','2','3','4','5'],
     'Pos_C-Word_in_C-Phrase(Bw)<=6':['0','1','2','3','4','5','6'],
     'Pos_C-Word_in_C-Phrase(Bw)<=7':['0','1','2','3','4','5','6','7'],
     'Pos_C-Word_in_C-Phrase(Bw)<=8':['0','1','2','3','4','5','6','7','8'],
     'Pos_C-Word_in_C-Phrase(Bw)<=9':['0','1','2','3','4','5','6','7','8','9'],
     'Pos_C-Word_in_C-Phrase(Bw)<=10':['0','1','2','3','4','5','6','7','8','9','10'],
     'Pos_C-Word_in_C-Phrase(Bw)<=11':['0','1','2','3','4','5','6','7','8','9','10','11'],
     'Pos_C-Word_in_C-Phrase(Bw)<=12':['0','1','2','3','4','5','6','7','8','9','10','11','12'],
     'Pos_C-Word_in_C-Phrase(Bw)<=13':['0','1','2','3','4','5','6','7','8','9','10','11','12','13'],}

QS_h3={
     'Pos_C-Phrase_in_Utterance(Fw)==1':['1'],
     'Pos_C-Phrase_in_Utterance(Fw)==2':['2'],
     'Pos_C-Phrase_in_Utterance(Fw)==3':['3'],
     'Pos_C-Phrase_in_Utterance(Fw)==4':['4'],

     'Pos_C-Phrase_in_Utterance(Fw)<=2':['1','2'],
     'Pos_C-Phrase_in_Utterance(Fw)<=3':['1','2','3'],
     'Pos_C-Phrase_in_Utterance(Fw)<=4':['1','2','3','4'],}

QS_h4={
 'Pos_C-Phrase_in_Utterance(Bw)==1':['1'],
 'Pos_C-Phrase_in_Utterance(Bw)==2':['2'],
 'Pos_C-Phrase_in_Utterance(Bw)==3':['3'],
 'Pos_C-Phrase_in_Utterance(Bw)==4':['4'],

 'Pos_C-Phrase_in_Utterance(Bw)<=2':['1','2'],
 'Pos_C-Phrase_in_Utterance(Bw)<=3':['1','2','3'],
 'Pos_C-Phrase_in_Utterance(Bw)<=4':['1','2','3','4'],}

'''
questionset.append(get_QS(QS_phones_in_syl,"L-",symbol_syllable[0],symbol_syllable[1],type))
questionset.append(get_QS(QS_syls_in_word,"L-",symbol_word[0],symbol_word[1],type))
questionset.append(get_QS(QS_syls_in_phrase,"R-",symbol_phrase[2],symbol_phrase[3],type))
questionset.append(get_QS(QS_words_in_phrase,"L-",symbol_phrase[3],symbol_phrase[4],type))
questionset.append(get_QS(QS_syls_in_sentense,"",symbol_sentense[0],symbol_sentense[1],type))
questionset.append(get_QS(QS_words_in_sentense,"",symbol_sentense[1],symbol_sentense[2],type))
questionset.append(get_QS(QS_phrases_in_sentense,"",symbol_sentense[2],symbol_sentense[3],type)) # 15
questionset.append(get_QS(QS_p6,"",symbol_position[0],symbol_position[1],type))
questionset.append(get_QS(QS_p7,"",symbol_position[1],symbol_position[2],type))
questionset.append(get_QS(QS_b3,"",symbol_position[2],symbol_position[3],type))
questionset.append(get_QS(QS_b4,"",symbol_position[3],symbol_position[4],type))
questionset.append(get_QS(QS_b5,"",symbol_position[4],symbol_position[5],type))
questionset.append(get_QS(QS_b6,"",symbol_position[5],symbol_position[6],type))
questionset.append(get_QS(QS_e3,"",symbol_position[6],symbol_position[7],type))
questionset.append(get_QS(QS_e4,"",symbol_position[7],symbol_position[8],type))
questionset.append(get_QS(QS_h3,"",symbol_position[8],symbol_position[9],type))
questionset.append(get_QS(QS_h4,"",symbol_position[9],symbol_position[10],type)) # 10
questionset.append(get_QS(QS_b7,"",symbol_tone[3],symbol_tone[4],type))
questionset.append(get_QS(QS_b8,"",symbol_tone[4],symbol_tone[5],type))
questionset.append(get_QS(QS_b9,"",symbol_tone[5],symbol_tone[6],type))
questionset.append(get_QS(QS_b10,"",symbol_tone[6],symbol_tone[7],type)) # 4
'''

QS_value = {


}

QS_onehot = {

}

def get_QS( qs_dict, qs_prefix="", prefix="", suffix="", type="HTS"):
    qs = []
    if type == "HTS" :
        for key , value in qs_dict.items():
            value = map(lambda x: '*'+prefix+x+suffix+'*' , value)
            str1 = "QS "+'"'+ qs_prefix + key + '"' +'\t'
            str2 = "{" + ','.join(value) + "}"
            string = str1 + str2 + "\n"
            qs.append(string)
    elif type == "DNN" :
        for key , value in qs_dict.items():
            value = map(lambda x: '*'+prefix+x+suffix+'*' , value)
            str1 = qs_prefix + key +' '
            str2 = "{" + ','.join(value) + "}"
            string = str1 + str2 + "\n"
            qs.append(string)
    return qs

symbol_phone=['/A:','^','-','+','+','/B:']
symbol_syllable=['/B:','^','+','=','/C:']
symbol_word=['/C:','^','=','/D:']
symbol_phrase=['/D:','^','@','-','=','^','/E:']
symbol_sentense=['/E:','$','-','/F:']
symbol_pos=['/F:','#','+','/G:']
#symbol_stress=['/G:','$','=','/H:']
symbol_position=['/G:','$','@','@','$','&','-','&','#','#','/H']
#symbol_tone=['/I:','-','@','+','@','=','+','$']
symbol_tone=['/H:','-','@','#','-','#','^','^']

def gen_qst(type="HTS"):
    symbol = [';','-','+',';','!','|',':',':','|','#','#',
            '|','$','$','|','@','@','|','&','&','|','^','^','|','=','=',
            '|','+','&','+']
    questionset = []
    questionset_utt  = []


    ## test1 12_19
    # categorical
    questionset.append(get_QS(QS_phone,"LL-","",symbol[0],type))
    questionset.append(get_QS(QS_phone,"L-",symbol[0],symbol[1],type))
    questionset.append(get_QS(QS_phone,"C-",symbol[1],symbol[2],type))
    questionset.append(get_QS(QS_phone,"R-",symbol[2],symbol[3],type))
    questionset.append(get_QS(QS_phone,"RR-",symbol[3],symbol[4],type))
    questionset.append(get_QS(QS_syl_vowel,"C-",symbol[4],symbol[5],type))
    questionset.append(get_QS(QS_POS,"L-",symbol[5],symbol[6],type))
    questionset.append(get_QS(QS_POS,"C-",symbol[6],symbol[7],type))
    questionset.append(get_QS(QS_POS,"R-",symbol[7],symbol[8],type))
    questionset.append(get_QS(QS_syl_stress,"L-",symbol[8],symbol[9],type))
    questionset.append(get_QS(QS_syl_stress,"C-",symbol[9],symbol[10],type))
    questionset.append(get_QS(QS_syl_stress,"R-",symbol[10],symbol[11],type))
    ## numerical
    questionset.append(get_QS(QS_p6,"",symbol[11],symbol[12],type))
    questionset.append(get_QS(QS_p7,"",symbol[12],symbol[13],type))
    questionset.append(get_QS(QS_phones_in_syl,"C-",symbol[13],symbol[14],type))
    questionset.append(get_QS(QS_b3,"",symbol[14],symbol[15],type))
    questionset.append(get_QS(QS_b4,"",symbol[15],symbol[16],type))
    questionset.append(get_QS(QS_syls_in_word,"C-",symbol[16],symbol[17],type))
    questionset.append(get_QS(QS_e3,"",symbol[17],symbol[18],type))
    questionset.append(get_QS(QS_e4,"",symbol[18],symbol[19],type))
    questionset.append(get_QS(QS_words_in_phrase,"C-",symbol[19],symbol[20],type))
    questionset.append(get_QS(QS_h3,"",symbol[20],symbol[21],type))
    questionset.append(get_QS(QS_h4,"",symbol[21],symbol[22],type))
    questionset.append(get_QS(QS_phrases_in_sentense,"",symbol[22],symbol[23],type))
    questionset.append(get_QS(QS_phones_in_sentense,"",symbol[23],symbol[24],type))
    questionset.append(get_QS(QS_syls_in_sentense,"",symbol[24],symbol[25],type))
    questionset.append(get_QS(QS_words_in_sentense,"",symbol[25],symbol[26],type))
    questionset.append(get_QS(QS_b7,"",symbol[26],symbol[27],type))
    questionset.append(get_QS(QS_b8,"",symbol[27],symbol[28],type))
    questionset.append(get_QS(QS_b9,"",symbol[28],symbol[29],type))
    questionset.append(get_QS(QS_b10,"",symbol[29],"",type))


    questionset_utt.append(get_QS(QS_syls_in_sentense,"",symbol[24],symbol[25],type))
    questionset_utt.append(get_QS(QS_words_in_sentense,"",symbol[25],"",type))
    questionset_utt.append(get_QS(QS_phrases_in_sentense,"",symbol[22],symbol[23],type))


    ## test2 12_29
    '''
    # phone
    questionset.append(get_QS(QS_phone,"LL-",symbol_phone[0],symbol_phone[1],type))
    questionset.append(get_QS(QS_phone,"L-",symbol_phone[1],symbol_phone[2],type))
    questionset.append(get_QS(QS_phone,"C-",symbol_phone[2],symbol_phone[3],type))
    questionset.append(get_QS(QS_phone,"R-",symbol_phone[3],symbol_phone[4],type))
    questionset.append(get_QS(QS_phone,"RR-",symbol_phone[4],symbol_phone[5],type))

    # syllable
    ## num
    questionset.append(get_QS(QS_phones_in_syl,"L-",symbol_syllable[0],symbol_syllable[1],type))
    questionset.append(get_QS(QS_phones_in_syl,"C-",symbol_syllable[1],symbol_syllable[2],type))
    questionset.append(get_QS(QS_phones_in_syl,"R-",symbol_syllable[2],symbol_syllable[3],type))
    ## Vowel
    questionset.append(get_QS(QS_syl_vowel,"C-",symbol_syllable[3],symbol_syllable[4],type))


    # word
    ## num
    questionset.append(get_QS(QS_syls_in_word,"L-",symbol_word[0],symbol_word[1],type))
    questionset.append(get_QS(QS_syls_in_word,"C-",symbol_word[1],symbol_word[2],type))
    questionset.append(get_QS(QS_syls_in_word,"R-",symbol_word[2],symbol_word[3],type))


    #phrase
    ## num
    questionset.append(get_QS(QS_syls_in_phrase,"L-",symbol_phrase[0],symbol_phrase[1],type))
    questionset.append(get_QS(QS_syls_in_phrase,"C-",symbol_phrase[1],symbol_phrase[2],type))
    questionset.append(get_QS(QS_syls_in_phrase,"R-",symbol_phrase[2],symbol_phrase[3],type))
    questionset.append(get_QS(QS_words_in_phrase,"L-",symbol_phrase[3],symbol_phrase[4],type))
    questionset.append(get_QS(QS_words_in_phrase,"C-",symbol_phrase[4],symbol_phrase[5],type))
    questionset.append(get_QS(QS_words_in_phrase,"R-",symbol_phrase[5],symbol_phrase[6],type))

    #sentense
    ## num
    questionset.append(get_QS(QS_syls_in_sentense,"",symbol_sentense[0],symbol_sentense[1],type))
    questionset.append(get_QS(QS_words_in_sentense,"",symbol_sentense[1],symbol_sentense[2],type))
    questionset.append(get_QS(QS_phrases_in_sentense,"",symbol_sentense[2],symbol_sentense[3],type))

    #pos
    questionset.append(get_QS(QS_POS,"L-",symbol_pos[0],symbol_pos[1],type))
    questionset.append(get_QS(QS_POS,"C-",symbol_pos[1],symbol_pos[2],type))
    questionset.append(get_QS(QS_POS,"R-",symbol_pos[2],symbol_pos[3],type))

    # position
    questionset.append(get_QS(QS_p6,"",symbol_position[0],symbol_position[1],type))
    questionset.append(get_QS(QS_p7,"",symbol_position[1],symbol_position[2],type))
    questionset.append(get_QS(QS_b3,"",symbol_position[2],symbol_position[3],type))
    questionset.append(get_QS(QS_b4,"",symbol_position[3],symbol_position[4],type))
    questionset.append(get_QS(QS_b5,"",symbol_position[4],symbol_position[5],type))
    questionset.append(get_QS(QS_b6,"",symbol_position[5],symbol_position[6],type))
    questionset.append(get_QS(QS_e3,"",symbol_position[6],symbol_position[7],type))
    questionset.append(get_QS(QS_e4,"",symbol_position[7],symbol_position[8],type))
    questionset.append(get_QS(QS_h3,"",symbol_position[8],symbol_position[9],type))
    questionset.append(get_QS(QS_h4,"",symbol_position[9],symbol_position[10],type))

    ## tone
    questionset.append(get_QS(QS_syl_stress,"L-",symbol_tone[0],symbol_tone[1],type))
    questionset.append(get_QS(QS_syl_stress,"C-",symbol_tone[1],symbol_tone[2],type))
    questionset.append(get_QS(QS_syl_stress,"R-",symbol_tone[2],symbol_tone[3],type))
    questionset.append(get_QS(QS_b7,"",symbol_tone[3],symbol_tone[4],type))
    questionset.append(get_QS(QS_b8,"",symbol_tone[4],symbol_tone[5],type))
    questionset.append(get_QS(QS_b9,"",symbol_tone[5],symbol_tone[6],type))
    questionset.append(get_QS(QS_b10,"",symbol_tone[6],symbol_tone[7],type))
    #questionset.append(get_QS(QS_e5,"",symbol_tone[4],symbol_tone[5],type))
    #questionset.append(get_QS(QS_e6,"",symbol_tone[5],symbol_tone[6],type))
    #questionset.append(get_QS(QS_e7,"",symbol_tone[6],symbol_tone[7],type))
    #questionset.append(get_QS(QS_e8,"",symbol_tone[7],"",type))

    questionset_utt.append(get_QS(QS_syls_in_sentense,"",symbol_sentense[0],symbol_sentense[1],type))
    questionset_utt.append(get_QS(QS_words_in_sentense,"",symbol_sentense[1],symbol_sentense[2],type))
    questionset_utt.append(get_QS(QS_phrases_in_sentense,"",symbol_sentense[2],symbol_sentense[3],type))

    '''
    '''
    ## test3 12
    # categorical
    questionset.append(get_QS(QS_phone,"LL-","",symbol[0],type))
    questionset.append(get_QS(QS_phone,"L-",symbol[0],symbol[1],type))
    questionset.append(get_QS(QS_phone,"C-",symbol[1],symbol[2],type))
    questionset.append(get_QS(QS_phone,"R-",symbol[2],symbol[3],type))
    questionset.append(get_QS(QS_phone,"RR-",symbol[3],symbol[4],type))
    questionset.append(get_QS(QS_syl_vowel,"C-",symbol[4],symbol[5],type))
    questionset.append(get_QS(QS_POS,"L-",symbol[5],symbol[6],type))
    questionset.append(get_QS(QS_POS,"C-",symbol[6],symbol[7],type))
    questionset.append(get_QS(QS_POS,"R-",symbol[7],symbol[8],type))
    questionset.append(get_QS(QS_syl_stress,"L-",symbol[8],symbol[9],type))
    questionset.append(get_QS(QS_syl_stress,"C-",symbol[9],symbol[10],type))
    questionset.append(get_QS(QS_syl_stress,"R-",symbol[10],"",type))
    #print(len(questionset))
    '''

    return questionset, questionset_utt

def get_QS_DNN():
    qs = []


    return qs

def gen_qst_DNN(type="DNN"):

    questionset = []

    '''
    ## test_2 12_29
    # categorical
    questionset.append(get_QS(QS_phone,"LL-",symbol_phone[0],symbol_phone[1],type))
    questionset.append(get_QS(QS_phone,"L-",symbol_phone[1],symbol_phone[2],type))
    questionset.append(get_QS(QS_phone,"C-",symbol_phone[2],symbol_phone[3],type))
    questionset.append(get_QS(QS_phone,"R-",symbol_phone[3],symbol_phone[4],type))
    questionset.append(get_QS(QS_phone,"RR-",symbol_phone[4],symbol_phone[5],type))
    questionset.append(get_QS(QS_syl_vowel,"C-",symbol_syllable[3],symbol_syllable[4],type))
    questionset.append(get_QS(QS_POS,"L-",symbol_pos[0],symbol_pos[1],type))
    questionset.append(get_QS(QS_POS,"C-",symbol_pos[1],symbol_pos[2],type))
    questionset.append(get_QS(QS_POS,"R-",symbol_pos[2],symbol_pos[3],type))
    questionset.append(get_QS(QS_syl_stress,"L-",symbol_tone[0],symbol_tone[1],type))
    questionset.append(get_QS(QS_syl_stress,"C-",symbol_tone[1],symbol_tone[2],type))
    questionset.append(get_QS(QS_syl_stress,"R-",symbol_tone[2],symbol_tone[3],type))

    QS_numerical = [
    # B3
    'L-Syl_Num-Segs {*/B:%d^*} MIN=0 MAX=7\n',
    'C-Syl_Num-Segs {*^%d+*} MIN=0 MAX=7\n',
    'R-Syl_Num-Segs {*+%d=*} MIN=0 MAX=7\n',
    # C3
    'L-Word_Num-Syls {*/C:%d^*} MIN=0 MAX=7\n',
    'C-Word_Num-Syls {*^%d=*} MIN=0 MAX=7\n',
    'R-Word_Num-Syls {*=%d/D:*} MIN=0 MAX=7\n',
    # D6
    'L-Phrase_Num-Syls {*/D:%d^*} MIN=0 MAX=20\n',
    'C-Phrase_Num-Syls {*^%d@*} MIN=0 MAX=20\n',
    'R-Phrase_Num-Syls {*@%d-*} MIN=0 MAX=20\n',
    'L-Sentence_Num-Words {*-%d=*} MIN=0 MAX=13\n',
    'C-Sentence_Num-Words {*=%d^*} MIN=0 MAX=13\n',
    'R-Sentence_Num-Words {*^%d/E:*} MIN=0 MAX=13\n',
    # E3
    'Num-Syls_in_Utterance {*/E:%d$*} MIN=0 MAX=28\n',
    'Num-Words_in_Utterance {*$%d-*} MIN=0 MAX=13\n',
    'Num-Sentences_in_Utterance {*-%d/F:*} MIN=0 MAX=4\n',
    # G10
    'Seg_Fw {*/G:%d$*} MIN=0 MAX=7\n',
    'Seg_Bw {*$%d@*} MIN=0 MAX=7\n',
    'Pos_C-Syl_in_C-Word(Fw) {*@%d@*} MIN=0 MAX=7\n',
    'Pos_C-Syl_in_C-Word(Bw) {*@%d$*} MIN=0 MAX=7\n',
    'Pos_C-Syl_in_C-Phrase(Fw) {*$%d&*} MIN=0 MAX=20\n',
    'Pos_C-Syl_in_C-Phrase(Bw) {*&%d-*} MIN=0 MAX=20\n',
    'Pos_C-Word_in_C-Sentence(Fw) {*-%d&*} MIN=0 MAX=13\n',
    'Pos_C-Word_in_C-Sentence(Bw) {*&%d#*} MIN=0 MAX=13\n',
    'Pos_C-Sentence_in_Utterance(Fw) {*#%d#*} MIN=0 MAX=4\n',
    'Pos_C-Sentence_in_Utterance(Bw) {*#%d/H:*} MIN=0 MAX=13\n',
    # H4
    'Num-StressedSyl_before_C-Syl_in_C-Phrase {*#%d-*} MIN=0 MAX=12\n',
    'Num-StressedSyl_after_C-Syl_in_C-Phrase {*-%d#*} MIN=0 MAX=12\n',
    'Num-Syl_from_prev-StressedSyl {*#%d^*} MIN=0 MAX=5\n',
    'Num-Syl_from_next-StressedSyl {*^%d^} MIN=0 MAX=5\n'
    ]
    '''


    ## test1 12_19
    symbol = [';','-','+',';','!','|',':',':','|','#','#',
            '|','$','$','|','@','@','|','&','&','|','^','^','|','=','=',
            '|','+','&','+']
    # categorical
    questionset.append(get_QS(QS_phone,"LL-","",symbol[0],type))
    questionset.append(get_QS(QS_phone,"L-",symbol[0],symbol[1],type))
    questionset.append(get_QS(QS_phone,"C-",symbol[1],symbol[2],type))
    questionset.append(get_QS(QS_phone,"R-",symbol[2],symbol[3],type))
    questionset.append(get_QS(QS_phone,"RR-",symbol[3],symbol[4],type))
    questionset.append(get_QS(QS_syl_vowel,"C-",symbol[4],symbol[5],type))
    questionset.append(get_QS(QS_POS,"L-",symbol[5],symbol[6],type))
    questionset.append(get_QS(QS_POS,"C-",symbol[6],symbol[7],type))
    questionset.append(get_QS(QS_POS,"R-",symbol[7],symbol[8],type))
    questionset.append(get_QS(QS_syl_stress,"L-",symbol[8],symbol[9],type))
    questionset.append(get_QS(QS_syl_stress,"C-",symbol[9],symbol[10],type))
    questionset.append(get_QS(QS_syl_stress,"R-",symbol[10],symbol[11],type))

    ## test3 remove temporary

    # numerical
    QS_numerical = [
    'Pos_C-Syl_in_C-Word(Fw) {*|%d$*} MIN=0 MAX=7\n',
    'Pos_C-Syl_in_C-Word(Bw) {*$%d$*} MIN=0 MAX=7\n',
    'C-Syl_Num-Segs {*$%d|*} MIN=0 MAX=7\n',
    'Seg_Fw {*|%d@*} MIN=0 MAX=7\n',
    'Seg_Bw {*@%d@*} MIN=0 MAX=7\n',
    'C-Word_Num-Syls {*@%d|*} MIN=0 MAX=7\n',
    'Pos_C-Word_in_C-Sentence(Fw) {*|%d&*} MIN=0 MAX=13\n',
    'Pos_C-Word_in_C-Sentence(Bw) {*&%d&*} MIN=0 MAX=13\n',
    'C-Sentence_Num-Words {*&%d|*} MIN=0 MAX=13\n',
    'Pos_C-Sentence_in_Utterance(Fw) {*|%d^*} MIN=0 MAX=4\n',
    'Pos_C-Sentence_in_Utterance(Bw) {*^%d^*} MIN=0 MAX=13\n',
    'Num-Sentences_in_Utterance {*^%d|*} MIN=0 MAX=4\n',
    'Num-Phones_in_Utterance {*|%d=*} MIN=0 MAX=60\n',
    'Num-Syls_in_Utterance {*=%d=*} MIN=0 MAX=28\n',
    'Num-Words_in_Utterance {*=%d|*} MIN=0 MAX=13\n',
    'Num-StressedSyl_before_C-Syl_in_C-Phrase {*|%d+*} MIN=0 MAX=12\n',
    'Num-StressedSyl_after_C-Syl_in_C-Phrase {*+%d&*} MIN=0 MAX=12\n',
    'Num-Syl_from_prev-StressedSyl {*&%d+*} MIN=0 MAX=5\n',
    'Num-Syl_from_next-StressedSyl {*+%d*} MIN=0 MAX=5\n'
    ]



    for qes in QS_numerical:
        questionset.append(qes)


    QS_additional = [
        'Pos_C-State_in_Phone(Fw) MIN=2 MAX=6\n',
        'Pos_C-State_in_Phone(Bw) MIN=2 MAX=6\n',
        'Pos_C-Frame_in_State(Fw) MIN=1 MAX=90\n',
        'Pos_C-Frame_in_State(Bw) MIN=1 MAX=90\n',
        'Pos_C-Frame_in_Phone(Fw) MIN=1 MAX=150\n',
        'Pos_C-Frame_in_Phone(Bw) MIN=1 MAX=150\n'
    ]

    for qes in QS_additional:
        questionset.append(qes)


    return questionset

if __name__ == '__main__':
    qst_HTS, qst_utt_HTS, qst_DNN = [], [], []
    qst_HTS, qst_utt_HTS = gen_qst("HTS")
    qst_DNN =  gen_qst_DNN("DNN")

    input_dir_path = os.path.expanduser("~/Desktop/project/EA_V2/input/")
    qes_dir_path = os.path.join(input_dir_path, "Questionset")
    if not os.path.isdir(qes_dir_path):
	    os.mkdir(qes_dir_path)

    ## calculate length
    count=0
    for items in qst_HTS:
        for item in items:
            count += 1


    with open(os.path.join(qes_dir_path, "questions_qst001.hed"),'w') as fout:
        for items in qst_HTS:
            for item in items:
                fout.write(item)

    with open(os.path.join(qes_dir_path, "questions_utt_qst001.hed"),'w') as fout:
        for items in qst_utt_HTS:
            for item in items:
                fout.write(item)

    with open(os.path.join(qes_dir_path, "questions_qst001.conf"),'w') as fout:
        for items in qst_DNN:
            for item in items:
                fout.write(item)

    #symbol_phone=['/A:','^','-','+','+','/B:']
    qst_config_path = os.path.join(qes_dir_path,"qstConfigs.json")
    qst_config = {"LLphone":r'\/A:\w+\^',"Lphone":r'\^\w+\-',"Cphone":r'\-\w+\+',"Rphone":r'\+\w+\+',"RRphone":r'\+\w+\/B\:',
                "phnum_in_presyl":r'\/B:\w+\^' , "phnum_in_cursyl":r'\^\w+\+' , "phnum_in_nextsyl":r'\+\w+\=' , "vowel_in_syl":r'\=\w+\/C\:' ,
                "sylnum_in_preword":r'\/C:\w+\^' , "sylnum_in_curword":r'\^\w+\=' , "sylnum_in_nextword":r'\=\w+\/D\:' ,
                "sylnum_in_prephrase":r'\/D:\w+\^' , "sylnum_in_curphrase":r'\^\w+\@' , "sylnum_in_nextphrase":r'\@\w+\-' , "wordnum_in_curphrase":r'\-\w+\=' , "wordnum_in_prephrase":r'\=\w+\^' , "wordnum_in_nextphrase":r'\^\w+\/E\:' ,
                "sylnum_in_sentense":r'\/E:\w+\$' , "wordnum_in_sentense":r'\$\w+\-' , "phrasenum_in_sentense":r'\-\w+\/F\:' ,
                "gpos_in_preword":r'\/F:\w+\$?\#' , "gpos_in_curword":r'\#\w+\$?\+' , "gpos_in_next_word":r'\+\w+\$?\/G\:' ,
                "ph_in_syl_fw":r'\/G:\w+\$' , "ph_in_syl_bw":r'\$\w+\@' , "syl_in_word_fw":r'\@\w+\@' , "syl_in_word_bw":r'\@\w+\$' , "syl_in_phrase_fw":r'\$\w+\&' , "syl_in_phrase_bw":r'\&\w+\-' ,
                "word_in_phrase_fw":r'\-\w+\&' , "word_in_phrase_bw":r'\&\w+\#' , "phrase_in_sentense_fw":r'\#\w+\#' , "phrase_in_sentense_bw":r'\#\w+\/H\:' ,
                "Lstress":r'\/H:\w+\-' , "Cstress":r'\-\w+\@' , "Rstress":r'\@\w+\#' ,
                "b7":r'\#\w+\-' , "b8":r'\-\w+\#' , "b9":r'\#\w+\^' , "b10":r'\^\w+\^' ,
                    "length":count}
    with open(qst_config_path, mode = "w") as qst_configs_file:
        json.dump(qst_config, qst_configs_file, indent ="",sort_keys=True)

    with open(qst_config_path, mode = "r") as qst_configs_file:
        qst_configs = json.load(qst_configs_file)

    QS_group = ['QS_phone',
                'QS_phones_in_syl','QS_syl_vowel',
                'QS_syls_in_word',
                'QS_syls_in_phrase','QS_words_in_phrase',
                'QS_syls_in_sentense','QS_words_in_sentense','QS_phrases_in_sentense',
                'QS_POS',
                'QS_syl_stress',
                'QS_p6','QS_p7','QS_b3','QS_b4','QS_b5','QS_b6','QS_e3','QS_e4','QS_h3','QS_h4',
                'QS_b7','QS_b8','QS_b9','QS_b10'
                ]
