# LabelGenerator

![image](https://user-images.githubusercontent.com/37763987/130551477-5b62002d-81ea-45df-b3a6-9b4f9b9da7c4.png)

## Directory
- EA_V2
    - dataset
        - bu_radio_dict_with_syl.txt
        - arctic 
            - raw
            - arctic_sentence.txt
        - ljspeech
            - wavs
            - metadata.csv
    - input
        - data
            - bu_radio_dict.txt
            - sentence.txt
            - wavs_16kHz
                - xxx.wav ~ xxx.wav
        - Mfa_Label
            - xxx.lab ~ xxx.lab
            - xxx.wav ~ xxx.wav
        - Mfa_TextGrid
            - xxx.TextGrid ~ xxx.TextGrid
        - Gen_Questionset
            - qstConfigs.json
            - questions_qst001.conf
            - questions_qst001.hed
            - questions_utt_qst001.hed
        - Gen_Mul
            - xxx.mul ~ xxx.mul
    - output
        - Hts_Label
            - full
                - xxx.lab ~ xxx.lab
            - mono
                - xxx.lab ~ xxx.lab
        - Qst_Vector
            - label-xxx.npy ~ label-xxx.npy
    - scripts 
        - dataset_preprocess.py
        - convert2mul.py
        - convert2htslabel.py
        - convert2qstvector.py
        - gen_questionset.py
    - tool
        - montreal-forced-aligner
    - Makefile

## Note
1. 下載語料庫 arctic 或者 ljspeech 放到 dataset資料夾
2. 安裝montreal forced aligner 到 tool資料夾
3. 語料庫ljspeech 不可以用 MFA pretrained model 要重新訓練 acousitc model
4. arctic database 使用 US_English_slt (female) 
5. 下載完 database 要改檔案名稱對應到我的目錄

## 下載連結
Montreal-Forced-Aligner : https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner
arctic database : http://www.festvox.org/cmu_arctic/
ljspeech database : https://keithito.com/LJ-Speech-Dataset/

