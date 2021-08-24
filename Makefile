all : train_dict ea hts_label hts_qst vector 
source : ea hts_label hts_qst vector
LabGen : dataset_preprocess MFA_pretrained 

train_dict :
	/home/adamliu/Desktop/project/hts_tool/montreal-forced-aligner/bin/mfa_train_and_align -j 16 data/arctic data/bu_radio_dict.txt data/aligned_arctic/
	#/home/adamliu/Desktop/project/hts_tool/montreal-forced-aligner/bin/mfa_train_and_align -j 16 data/ljspeech data/bu_radio_dict.txt data/aligned_ljspeech/
dict :
	python scripts/convert_dict_with_syl.py


lab :
	#python scripts/convert2lab.py
	python scripts/convert2lab_v2.py --dataset=arctic
	#python scripts/convert2lab_v2.py --dataset=ljspeech

ea :
	#python scripts/ea.py --dataset=arctic 
	python scripts/ea.py --dataset=ljspeech 

corpus :
	python scripts/corpus.py

hts_label :
	#python scripts/mul_lab_v3.py
	#python scripts/mul_lab_v3.py --dataset=arctic
	#python scripts/mul_lab_v3.py --dataset=ljspeech
	#python scripts/mul_lab_v4.py --dataset=arctic
	python scripts/mul_lab_v4.py --dataset=ljspeech

hts_qst :
	#python scripts/qst_gen.py
	python scripts/qst_gen_v2.py

vector :
	#python scripts/lab2vector.py --dataset=arctic
	python scripts/lab2vector.py --dataset=ljspeech

mvf_test:
	cp -r output_htslabel/full/* /home/adamliu/Desktop/project/HTS_2.2_test/data/labels/full/
	cp -r output_htslabel/mono/* /home/adamliu/Desktop/project/HTS_2.2_test/data/labels/mono/
	##cp -r output/full/cmu_us_arctic_slt_b053?.lab /home/adamliu/Desktop/project/HTS_2.2/data/labels/full/
	cp -r output_htslabel/full/* /home/adamliu/Desktop/project/HTS_2.2_test/data/labels/gen/
	cp output_questionst/questions_qst001.hed /home/adamliu/Desktop/project/HTS_2.2_test/data/questions/
	##cp output/questions_utt_qst001.hed /home/adamliu/Desktop/project/HTS_2.2_test/data/questions/
	cp output_questionst/questions_qst001.conf /home/adamliu/Desktop/project/dnn_tts/data/questions/
	cp output_questionst/questions_qst001.hed /home/adamliu/Desktop/project/dnn_tts/data/questions/
	cp output_questionst/qstConfigs.json /home/adamliu/Desktop/project/dnn_tts/configs/

test_g2p:
	python scripts/test.py

mvf_0801:
	cp -r output_htslabel/full/* /home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0801/data/labels/full/
	cp -r output_htslabel/mono/* /home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0801/data/labels/mono/
	cp -r output_htslabel/full/* /home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0801/data/labels/gen/
	cp output_questionst/questions_qst001.hed /home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0801/data/questions/

mvf_0803:
	#cp -r output_htslabel/ljspeech/full/* /home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0803/data/labels/full/
	#cp -r output_htslabel/ljspeech/mono/* /home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0803/data/labels/mono/
	#cp -r output_htslabel/ljspeech/full/* /home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0803/data/labels/gen/
	cp -r output_htslabel/arctic/full/* /home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0803/data/labels/full/
	cp -r output_htslabel/arctic/mono/* /home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0803/data/labels/mono/
	cp -r output_htslabel/arctic/full/* /home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0803/data/labels/gen/
	cp output_questionset/questions_qst001.conf /home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0803/data/questions/
	cp output_questionset/questions_qst001.hed /home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0803/data/questions/
	cp output_questionset/questions_qst001.conf /home/adamliu/Desktop/project/dnn_tts/data/questions/
	cp output_questionset/questions_qst001.hed /home/adamliu/Desktop/project/dnn_tts/data/questions/
	cp output_questionset/qstConfigs.json /home/adamliu/Desktop/project/dnn_tts/configs/
	cp output_questionset/questions_qst001.conf /home/adamliu/Desktop/DNN-TTS-V5_MINE/data/questions/
	cp output_questionset/questions_qst001.hed /home/adamliu/Desktop/DNN-TTS-V5_MINE/data/questions/
	cp output_questionset/questions_qst001.conf /home/adamliu/Desktop/project/DNN-TTS-V5/data/questions/
	cp output_questionset/questions_qst001.conf /home/adamliu/Desktop/DNN-TTS-V5_1002/data/questions/
	#cp output_questionset/questions_qst001.hed /home/adamliu/Desktop/DNN-TTS-V5_1002/data/questions/
	
mv2tacotron:
	cp -r output_vector/arctic/*.npy /home/adamliu/Desktop/project/tacotron1027_label/training/
	
raw_16k:
	python scripts/raw48k216k.py --dataset=arctic
	python scripts/raw48k216k.py --dataset=ljspeech
	
verification_input : 
	python scripts/verification.py
	
split_dict : 
	python scripts/split_dictionary.py
	
dictionary_check : 
	python scripts/dictionary_check.py

hdf5_transform : 
#	python scripts/hdf5_transform.py \
#	--lf0_dir=/home/adamliu/Desktop/WOLRD_VOCODING_TUTORIAL/vocoding_scripts/feat_extraction/lf0/world/ARCTIC/ \
#	--mgc_dir=/home/adamliu/Desktop/WOLRD_VOCODING_TUTORIAL/vocoding_scripts/feat_extraction/mgc/world/ARCTIC/ \
#	--out_dir=/home/adamliu/Desktop/project/EA_V2/output_hdf5/world/hdf5/
	python scripts/hdf5_transform.py \
	--lf0_dir=/home/adamliu/Desktop/WOLRD_VOCODING_TUTORIAL/vocoding_scripts/feat_extraction/lf0/world/ljspeech/ \
	--mgc_dir=/home/adamliu/Desktop/WOLRD_VOCODING_TUTORIAL/vocoding_scripts/feat_extraction/mgc/world/ljspeech/ \
	--out_dir=/home/adamliu/Desktop/project/EA_V2/output_hdf5/world/hdf5/
	python scripts/hdf5_transform.py \
	--lf0_dir=/home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0803/gen/qst001/ver1/1mix/lf0/ \
	--mgc_dir=/home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0803/gen/qst001/ver1/1mix/mgc/ \
	--out_dir=/home/adamliu/Desktop/project/EA_V2/output_hdf5/hts/1mix/hdf5/
	python scripts/hdf5_transform.py \
	--lf0_dir=/home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0803/gen/qst001/ver1/2mix/lf0/ \
	--mgc_dir=/home/adamliu/Desktop/HTS-demo_CMU-ARCTIC-SLT_0803/gen/qst001/ver1/2mix/mgc/ \
	--out_dir=/home/adamliu/Desktop/project/EA_V2/output_hdf5/hts/2mix/hdf5/
	
	
phone_distribution:
	#python scripts/phone_distribution.py --dataset arctic
	python scripts/phone_distribution.py --dataset ljspeech
	
database_info:
	#python scripts/database_info.py --dataset arctic
	python scripts/database_info.py --dataset ljspeech

clean : 
	#rm -r output_htslabel output_mul output_questionset output_vector 
	#rm data/arctic/*.lab data/ljspeech/*.lab
	rm -r input/
	# rm -r output/

	
tmp : 
	python scripts/tmp.py
	
tmp2 : 
	python scripts/tmp2.py
	
all2:
	dataset_preprocess MFA_pretrained

dataset_preprocess:
	python scripts/dataset_preprocess.py
	
MFA:
	~/Desktop/project/hts_tool/montreal-forced-aligner/bin/mfa_train_and_align -j 16 \
	input/Mfa_Label/ \
	input/data/bu_radio_dict.txt \
	input/Mfa_TextGrid/
	
MFA_pretrained: 
	~/Desktop/project/hts_tool/montreal-forced-aligner/bin/mfa_align -j 16 \
	input/Mfa_Label/ \
	input/data/bu_radio_dict.txt english \
	input/Mfa_TextGrid/
	
	
convert2mul:
	python scripts/convert2mul.py
	
convert2htslabel:
	python scripts/convert2htslabel.py


#mfa align /path/to/librispeech/dataset /path/to/librispeech/lexicon.txt english ~/Documents/aligned_librispeech