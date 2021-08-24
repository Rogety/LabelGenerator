import os
import argparse
import soundfile as sf

def dataset_word_count(filenames):

    phrase_cnt, word_cnt, syl_cnt, phone_cnt = 0,0,0,0
    wav_seconds = 0.0

    for filename in filenames:
        mul_filename = filename + ".mul"
        mul_filename_path = os.path.join(mul_dir_path, mul_filename)
        with open(mul_filename_path, "r") as fin:
            for line in fin:
                line = line.split(" ")
                line.pop()
                if len(line) > 4: ## 代表這一行包含 word
                    word_cnt += 1
                if len(line) > 3: ##
                    syl_cnt += 1
                if line[2] != 'sp' or line[2] != 'sil':
                    phone_cnt += 1
                if len(line) > 7: ##
                    if line[-1] == '.' or line[-1] == ',':
                        phrase_cnt += 1

            #print(phrase_cnt, word_cnt, syl_cnt, phone_cnt)
            #import pdb;pdb.set_trace()

        audio_filename = filename + ".wav"
        audio_filename_path = os.path.join(audio_dir_path, audio_filename)
        data, samplerate = sf.read(audio_filename_path)
        wav_seconds += len(data)/samplerate




    return phrase_cnt, word_cnt, syl_cnt, phone_cnt, wav_seconds


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', '-d', type=str)
    parser.add_argument('--mul_dir_path', type=str, default=os.path.expanduser("/home/adamliu/Desktop/project/EA_V2/output_mul/"))
    parser.add_argument('--label_dir_path', type=str, default=os.path.expanduser("/home/adamliu/Desktop/project/EA_V2/output_vector/"))
    parser.add_argument('--dataset_dir_path', type=str, default=os.path.expanduser("/home/adamliu/Desktop/project/EA_V2/data/"))
    args = parser.parse_args()

    output_path = 'output_dataset'
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    dataset_dir_path = args.dataset_dir_path
    dataset = args.dataset
    if args.dataset == "arctic":
        mul_dir_path = os.path.join(args.mul_dir_path,"arctic")
        audio_dir_path = os.path.join(args.dataset_dir_path,"arctic")
        label_dir_path = os.path.join(args.label_dir_path,"arctic")
        filenames = [x.rstrip(".wav") for x in sorted(os.listdir(audio_dir_path)) if x.endswith(".wav") ]
    elif args.dataset == "ljspeech":
        mul_dir_path = os.path.join(args.mul_dir_path,"ljspeech")
        audio_dir_path = os.path.join(args.dataset_dir_path,"ljspeech")
        label_dir_path = os.path.join(args.label_dir_path,"ljspeech")
        filenames = [x.rstrip(".wav") for x in sorted(os.listdir(audio_dir_path)) if x.endswith(".wav") ]



    phrase_cnt, word_cnt, syl_cnt, phone_cnt, wav_seconds = dataset_word_count(filenames)


    print("audio files: ", len(filenames))
    print("phrase_cnt count: ", phrase_cnt)
    print("word count: ", word_cnt)
    print("syl_cnt count: ", syl_cnt)
    print("phone_cnt count: ", phone_cnt)
    print("wav_seconds: ", wav_seconds)
