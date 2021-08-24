

import nltk

from nltk.corpus import PlaintextCorpusReader



if __name__ == "__main__":

    #corpus_root = '/data/arctic_sentense.txt'
    corpus_root = 'data'
    wordlists = PlaintextCorpusReader(corpus_root, 'arctic_sentense.txt')
    fileids = wordlists.fileids()
    raw = wordlists.raw()
    words = wordlists.words()
    sents = wordlists.sents()
    print("fileids :",fileids)
    print("raw :",raw)
    print("words :",words)
    print("sents :",sents[34])

    '''
    with open("data/arctic_sentense.txt","r") as texts :
        for line in texts:
            print(line)

    with open("data/bu_radio_dict_with_syl.txt","r") as texts:
        for line in texts :
            print(line)
    '''
