import os
import re
import argparse
import random
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import numpy as np
import librosa
import librosa.filters
import wave

phone_dict = {}
vowel_dict = {}
consonant_dict = {}
others_dict = {}
file_nums = 1132

consonant = ['b','ch','d','dh','f','g','hh','jh',
            'k','l','m','n','ng','p','r','s','sh',
            't','th','v','w','y','z','zh']
vowel = ['aa','ae','ah','ao','aw','ay',
        'eh','er','ey',
        'ih','iy',
        'ow','oy',
        'uh','uw']
others = ['sil','sp']

_mel_basis = None
_inv_mel_basis = None

def _amp_to_db(x):
    min_level = np.exp(-100 / 20 * np.log(10))
    return 20 * np.log10(np.maximum(min_level, x))


def _stft(y):
    return librosa.stft(y=y, n_fft=2048, hop_length=160, win_length=800, pad_mode='constant')

def _linear_to_mel(spectogram):
    global _mel_basis
    if _mel_basis is None:
        _mel_basis = _build_mel_basis()
    return np.dot(_mel_basis, spectogram)

def _build_mel_basis():
    assert 7600 <= 16000 // 2
    return librosa.filters.mel(16000, 2048, n_mels=80,
							   fmin=55, fmax=7600)

def melspectrogram(wav):
    # D = _stft(preemphasis(wav, hparams.preemphasis, hparams.preemphasize), hparams)
    D = _stft(wav)
    S = _amp_to_db(_linear_to_mel(np.abs(D)**2.)) - 20
    return S

def phone_distribution(filenames, mul_dir_path,output_path):

    ## filename : arctic_a0001

    filepaths = [os.path.join(mul_dir_path, x + ".mul") for x in filenames]

    for filepath in filepaths :
        phones = []
        with open(filepath, mode="r") as fin : ## open each mul file
            for line in fin:
                line = line.split(" ")
                phones.append(line[2])
        for phone in phones: ## get phone in line
            if phone not in phone_dict.keys():
                phone_dict[phone] = 1
            else :
                phone_dict[phone] += 1

    ## calculate other distributions
    for i in range(len(phone_dict)):
        key = list(phone_dict.keys())[i]
        if key.lower() in vowel :
            vowel_dict[key] = phone_dict[key]
        elif key.lower() in consonant:
            consonant_dict[key] = phone_dict[key]
        else :
            others_dict[key] =  phone_dict[key]

    ## plot bar
    png_path = os.path.join(output_path, "distribution.png")
    plt.rcParams["figure.figsize"] = (16, 16)
    plt.bar(phone_dict.keys(),phone_dict.values())
    plt.bar(vowel_dict.keys(),vowel_dict.values())
    plt.bar(consonant_dict.keys(),consonant_dict.values())
    plt.xlabel("phone")
    plt.ylabel("phone count")
    plt.savefig(png_path)

    ## output txt
    txt_path = os.path.join(output_path, "distribution.txt")
    with open(txt_path, "w") as fout : ##
        for key, value in phone_dict.items():
            fout.write("%s: %d" % (key, value))
            if (value < 1000):
                fout.write(" * ")
            fout.write("\n")


    return 0 ;

def metadata_generate(filenames_target, dataset_dir_path, dataset, output_path):

    filenames = []
    sentenses = []
    sentenses_norm = []

    if dataset == 'arctic':
        filename_pattern = r'arctic_[ab]\d{4}'
        sentenses_pattern = r'\"(.*)+\"'
        text_path = os.path.join(dataset_dir_path, "arctic_sentense.txt")
        metadata_path = os.path.join(output_path, "metadata.csv")
        with open(text_path, mode='r') as fin :
            for line in fin:
                searchObj = re.search(filename_pattern, line)
                if searchObj:
                    filenames.append(searchObj.group())
                searchObj = re.search(sentenses_pattern, line)
                if searchObj:
                    sentenses.append(searchObj.group().strip('"'))

        with open(metadata_path, mode='w') as fout:
            for i in range(len(filenames)):
                if filenames[i] in filenames_target:
                    string = filenames[i]+"|"+sentenses[i]+"|"+sentenses[i]+"\n"
                    fout.write(string)

        #print("sentenses :", len(sentenses))
        #print("filenames", len(filenames))

    elif dataset == 'ljspeech':
        text_path = os.path.join(dataset_dir_path, "LJSpeech-1.1", "metadata.csv")
        metadata_path = os.path.join(output_path, "metadata.csv")

        with open(text_path, mode='r') as fin :
            for line in fin:
                line = line.split("|")
                filenames.append(line[0])
                sentenses.append(line[1].strip("\n"))
                sentenses_norm.append(line[2].strip("\n"))

        print(len(filenames_target))
        with open(metadata_path, mode='w') as fout:
            for i in range(len(filenames)):
                if filenames[i] in filenames_target:
                    string = filenames[i]+"|"+sentenses_norm[i]+"|"+sentenses[i]+"\n"
                    fout.write(string)

    return 0

def audiofile_move(filenames_target, audio_dir_path, raw_dir_path, output_path):


    print("audio_dir_path :", audio_dir_path)
    audio_files = []

    output_audio_dir = os.path.join(output_path, 'wavs')
    if os.path.exists(output_audio_dir):
        os.system("rm -r %s" % (output_audio_dir))
    if not os.path.exists(output_audio_dir):
        os.mkdir(output_audio_dir)

    for file in os.listdir(audio_dir_path):
        if file.endswith(".wav") and (file.rstrip(".wav") in filenames_target) :
            audio_files.append(os.path.join(audio_dir_path, file))

    for file in audio_files:
        if os.path.isfile(file):
            os.system("cp %s %s" % (file, output_audio_dir))
            print("cp %s %s done" % (file, output_audio_dir))

    raw_files = []

    output_raw_dir = os.path.join(output_path, 'raws')
    if os.path.exists(output_raw_dir):
        os.system("rm -r %s" % (output_raw_dir))
    if not os.path.exists(output_raw_dir):
        os.mkdir(output_raw_dir)

    for file in os.listdir(raw_dir_path):
        if file.endswith(".raw") and (file.rstrip(".raw") in filenames_target) :
            raw_files.append(os.path.join(raw_dir_path, file))

    for file in raw_files:
        if os.path.isfile(file):
            os.system("cp %s %s" % (file, output_raw_dir))
            print("cp %s %s done" % (file, output_raw_dir))


    return 0

def labelfile_move(filenames_target, label_dir_path, hts_label_dir_path, output_path):


    ## label file
    print("label_dir_path :", label_dir_path)



    htslabel_full_dir_path = os.path.join(hts_label_dir_path, "full")
    htslabel_mono_dir_path = os.path.join(hts_label_dir_path, "mono")

    output_label_dir = os.path.join(output_path, 'label')
    output_htslabel_dir = os.path.join(output_path, 'htslabel')
    output_label_mono_dir = os.path.join(output_htslabel_dir, 'mono')
    output_label_full_dir = os.path.join(output_htslabel_dir, 'full')
    if os.path.exists(output_label_dir):
        os.system("rm -r %s" % (output_label_dir))
    if not os.path.exists(output_label_dir):
        os.mkdir(output_label_dir)
    if not os.path.exists(output_label_mono_dir):
        os.mkdir(output_label_mono_dir)
    if not os.path.exists(output_label_full_dir):
        os.mkdir(output_label_full_dir)

    label_files = []
    filenames_target = [ ("label-"+x) for x in filenames_target]
    for file in os.listdir(label_dir_path):
        if file.endswith(".npy") and (file.rstrip(".npy") in filenames_target) :
            label_files.append(os.path.join(label_dir_path, file))
    print(label_files, len(label_files))
    #audio_files = random.sample(audio_files, file_nums)
    for file in label_files:
        if os.path.isfile(file):
            os.system("cp %s %s" % (file, output_label_dir))
            print("cp %s %s done" % (file, output_label_dir))


    print("hts_label_dir_path :", hts_label_dir_path)



    hstlabel_mono_files = []
    hstlabel_full_files = []
    ## mono

    for file in os.listdir(htslabel_mono_dir_path):
        if file.endswith(".lab") and (file.rstrip(".lab") in filenames_target) :
            hstlabel_mono_files.append(os.path.join(htslabel_mono_dir_path, file))

    # print(hstlabel_mono_files)


    for file in hstlabel_mono_files:
        if os.path.isfile(file) and os.path.isdir(output_label_mono_dir):
            os.system("cp %s %s" % (file, output_label_mono_dir))
            print("cp %s %s done" % (file, output_label_mono_dir))


    ## full
    for file in os.listdir(htslabel_full_dir_path):
        if file.endswith(".lab") and (file.rstrip(".lab") in filenames_target) :
            hstlabel_full_files.append(os.path.join(htslabel_full_dir_path, file))
    for file in hstlabel_full_files:
        if os.path.isfile(file) and os.path.isdir(output_label_full_dir):
            os.system("cp %s %s" % (file, output_label_full_dir))
            print("cp %s %s done" % (file, output_label_full_dir))

    #import pdb;pdb.set_trace()


def draw_png(data, x, y, filename):

    png_path = os.path.join(output_path, filename)
    plt.rcParams["figure.figsize"] = (16, 16)
    plt.bar(data.keys(),data.values())
    plt.xlabel(x)
    plt.ylabel(y)
    plt.savefig(png_path)
    plt.close()



def audiofile_pick(filenames, audio_dir_path, mul_dir_path):

    #filenames = random.sample(filenames, file_nums)
    picked_filenames = []
    audio_files = [os.path.join(audio_dir_path, x+".wav") for x in filenames]
    mul_files = [os.path.join(mul_dir_path, x+".mul") for x in filenames]

    second_cnt = 0.0;
    # global_max = [];
    # global_min = [];
    # global_mean = [];

    second_dict = {}
    phrases_utterance = {}
    phones_phrases = {}

    phones_in_phrase = [] # 2d
    phrase_in_utterance = [] # 1d

    for mulfile in mul_files:
        phone_cnt = 0;
        with open(mulfile, 'r') as fin:
            phones_in_phrase_1d = []
            phrase_in_utterance_1d = []

            for line in fin:
                line = line.split(" ")
                phone_cnt += 1;
                if (line[2] == "sp"):
                    phones_in_phrase_1d.append(phone_cnt)
                    phone_cnt = 0;

            phones_in_phrase.append(phones_in_phrase_1d)
            phrase_in_utterance.append(len(phones_in_phrase_1d))


    audio_length = []
    filenames = []
    for audiofile in audio_files:
        #data, samplerate = sf.read(audiofile)

        filename = os.path.basename(audiofile).rstrip(".wav")
        filenames.append(filename)
        f = wave.open(audiofile,'rb')
        params = f.getparams()
        nchannels, sampwidth, samplerate, nframes = params[:4]
        strData = f.readframes(nframes)#讀取音訊，字串格式
        data = np.fromstring(strData,dtype=np.int16)#將字串轉化為int
        f.close()

        second = int(len(data) / 16000) + 1;
        audio_length.append(second)


    #print(len(filenames), len(audio_length), len(phones_in_phrase), len(phrase_in_utterance))


    ## start to pick
    for i in range(len(filenames)):
        # print(filenames[i])
        # print(audio_length[i])
        # print(phones_in_phrase[i])
        # print(phrase_in_utterance[i])

        if second not in second_dict.keys():
            second_dict[second] = 1
        else :
            second_dict[second] += 1

        phrase = phrase_in_utterance[i]
        if phrase not in phrases_utterance.keys():
            phrases_utterance[phrase] = 1
        else :
            phrases_utterance[phrase] += 1

        for phones in phones_in_phrase[i]:
            if phones not in phones_phrases.keys():
                phones_phrases[phones] = 1
            else :
                phones_phrases[phones] += 1


        if (second >= 6 and second <= 10) and \
            (phrase >= 2 and phrase <=4):

            picked = True
            for phone_num in phones_in_phrase[i]:
                if phone_num < 5 or phone_num > 35 :
                    picked = False;

            if(picked == True):
                picked_filenames.append(filenames[i])

    print("picked filenames: ",len(picked_filenames))
    picked_filenames = random.sample(picked_filenames, 800)


    second = 0.0
    for filename in picked_filenames:
        #data, samplerate = sf.read(audiofile)

        audiofile = os.path.join(audio_dir_path, filename + ".wav")
        f = wave.open(audiofile,'rb')
        params = f.getparams()
        nchannels, sampwidth, samplerate, nframes = params[:4]
        strData = f.readframes(nframes)#讀取音訊，字串格式
        data = np.fromstring(strData,dtype=np.int16)#將字串轉化為int
        f.close()

        second += len(data) / 16000;

    print("average second :",second/len(picked_filenames))
    print("hours : ",second/3600)


    #filenames = random.sample(filenames, file_nums)

        #print(phrases_utterance)

        #import pdb; pdb.set_trace()

    # print(phrases_utterance)
    draw_png(second_dict, "seconds", "file_count", "audio_length.png")
    draw_png(phrases_utterance, "phrse_num", "file_count", "phrases_utterance.png")
    draw_png(phones_phrases, "phones_num", "count", "phones_phrases.png")

    # print(sorted(phones_phrases.items()))

    print("picked_filenames: ", len(picked_filenames))
    # import pdb; pdb.set_trace()

    return picked_filenames

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', '-d', type=str)
    parser.add_argument('--mul_dir_path', type=str, default=os.path.expanduser("/home/adamliu/Desktop/project/EA_V2/output_mul/"))
    parser.add_argument('--label_dir_path', type=str, default=os.path.expanduser("/home/adamliu/Desktop/project/EA_V2/output_vector/"))
    parser.add_argument('--dataset_dir_path', type=str, default=os.path.expanduser("/home/adamliu/Desktop/project/EA_V2/data/"))
    parser.add_argument('--hts_label_dir_path', type=str, default=os.path.expanduser("/home/adamliu/Desktop/project/EA_V2/output_htslabel/"))
    parser.add_argument('--raw_dir_path', type=str, default=os.path.expanduser("/home/adamliu/Desktop/project/EA_V2/output_16k/"))
    args = parser.parse_args()

    output_path = 'output_dataset'
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    dataset_dir_path = args.dataset_dir_path
    dataset = args.dataset
    if args.dataset == "arctic":
        mul_dir_path = os.path.join(args.mul_dir_path,"arctic")
        audio_dir_path = os.path.join(args.dataset_dir_path,"arctic")
        raw_dir_path = os.path.join(args.raw_dir_path,"arctic","raw")
        label_dir_path = os.path.join(args.label_dir_path,"arctic")
        hts_label_dir_path = os.path.join(args.hts_label_dir_path,"arctic")
        filenames = [x.rstrip(".wav") for x in sorted(os.listdir(audio_dir_path)) if x.endswith(".wav") ]
    elif args.dataset == "ljspeech":
        mul_dir_path = os.path.join(args.mul_dir_path,"ljspeech")
        audio_dir_path = os.path.join(args.dataset_dir_path,"ljspeech")
        raw_dir_path = os.path.join(args.raw_dir_path,"ljspeech","raw")
        label_dir_path = os.path.join(args.label_dir_path,"ljspeech")
        hts_label_dir_path = os.path.join(args.hts_label_dir_path,"ljspeech")
        filenames = [x.rstrip(".wav") for x in sorted(os.listdir(audio_dir_path)) if x.endswith(".wav") ]

    random.seed(12)
    #filenames = random.sample(filenames, file_nums)
    #print(filenames, len(filenames))

    filenames = audiofile_pick(filenames, audio_dir_path, mul_dir_path)
    print("picked filenames : ", len(filenames))

    labelfile_move(filenames, label_dir_path, hts_label_dir_path, output_path)
    phone_distribution(filenames, mul_dir_path, output_path)
    metadata_generate(filenames, dataset_dir_path, dataset, output_path)
    audiofile_move(filenames, audio_dir_path, raw_dir_path, output_path)

    #print(phone_dict)
