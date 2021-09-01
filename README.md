# LabelGenerator

![image](https://user-images.githubusercontent.com/37763987/130551477-5b62002d-81ea-45df-b3a6-9b4f9b9da7c4.png)

## Directory
- EA_V2
    - dataset
        - bu_radio_dict_with_syl.txt
        - arctic 
        - ljspeech
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
    - Makefile
