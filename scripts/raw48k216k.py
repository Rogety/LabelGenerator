import os
import argparse



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', '-d', type=str)
    #parser.add_argument('--dataset_dir_path', type=str, default=os.path.expanduser("~/Desktop/project/EA_V2/"))
    args = parser.parse_args()

    if args.dataset == "arctic":
        input_path = r"dataset/arctic/raw/";
        output_raw_path = r"output_16k/arctic/raw/";
        output_wav_path = r"output_16k/arctic/wav/";
    elif args.dataset == "ljspeech":
        input_path = r"dataset/ljspeech/wavs/";
        output_raw_path = r"output_16k/ljspeech/raw/";
        output_wav_path = r"output_16k/ljspeech/wav/";

    if not os.path.exists(output_raw_path):
        os.mkdir(output_raw_path);
    if not os.path.exists(output_wav_path):
        os.mkdir(output_wav_path);

    if args.dataset == "ljspeech":
        for _ , _ ,filename in os.walk(input_path):
            wav_name = sorted(filename)
            raw_name = sorted([ x.replace(".wav" , ".raw") for x in filename ])

        for i in range(len(raw_name)):
            cmd = "sox " + " -v 0.8 "+ input_path+wav_name[i] + " -r 16000 -c 1 -b 16 -e signed-integer " + output_raw_path+raw_name[i]
            os.system(cmd)

        for i in range(len(raw_name)):
            cmd = "sox " + " -v 0.8 "+ input_path+wav_name[i] + " -r 16000 -c 1 -b 16 -e signed-integer " + output_wav_path+wav_name[i]
            os.system(cmd)


    ## /home/adamliu/Desktop/project/EA_V2/output_16k/

    if args.dataset == "arctic":

        for _ , _ ,filename in os.walk(input_path):
            raw_name = sorted(filename)
            wav2_name = sorted([ x.replace(".raw" , ".wav") for x in filename ])
            wav2_name = sorted([ x.replace("cmu_us_arctic_slt" , "cmu_arctic") for x in wav2_name ])
            raw2_name = sorted(filename)
            raw2_name = sorted([ x.replace("cmu_us_arctic_slt" , "cmu_arctic") for x in filename ])

        for i in range(len(raw_name)):
            cmd = "sox -r 48000 -t raw -b 16 -e signed-integer "+ input_path + raw_name[i] + " -r 16000 " + output_raw_path +raw2_name[i]
            os.system(cmd)

        for i in range(len(raw_name)):
            cmd = "sox -r 48000 -t raw -b 16 -e signed-integer "+ input_path + raw_name[i] + " -r 16000 " + output_wav_path +wav2_name[i]
            os.system(cmd)



    ## 22050 -> 16000

    '''
    ljspeech_dir_path = os.path.join(os.getcwd(), "data/ljspeech")
    if not os.path.isdir(ljspeech_dir_path):
	    os.mkdir(ljspeech_dir_path)

    for _ , _ ,filename in os.walk("data/LJSpeech-1.1/wavs"):
        wav_name = sorted(filename)


    for i in range(len(wav_name)):
        print(wav_name[i])
        input_path = "data/LJSpeech-1.1/wavs/" + wav_name[i]
        output_path = "data/ljspeech/"+ wav_name[i]
        cmd = "sox" + " -r 22050 -v 0.8 "+ input_path + " -b 16 -c 1 -r 16000 -e signed-integer " + output_path
        # cmd = "sox  "data/LJSpeech-1.1/wavs/"+ wav_name[i] -b 16 -e signed-integer "+  " -r 16000 "
        os.system(cmd)
    print("transform wav done")

    for i in range(len(wav_name)):
        print(wav_name[i])
        input_path = "data/LJSpeech-1.1/wavs/" + wav_name[i]
        output_path = "data/ljspeech_raw/"+ wav_name[i].replace(".wav",".raw")
        cmd = "sox" + " -r 22050 -v 0.8 "+ input_path + " -b 16 -c 1 -r 16000 -e signed-integer " + output_path
        os.system(cmd)
    print("transform raw done")
    '''
