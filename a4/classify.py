"""
classify.py
classify the sentiments of each tweet

"""
import numpy as np
import pickle
import re


def read_afinn():
    
    afinn = dict()
    with open('sentiment.txt', 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                afinn[parts[0]] = int(parts[1])

    print('read %d AFINN terms.\nE.g.: %s' % (len(afinn), str(list(afinn.items())[:10])))

    return afinn



# rate message score
def afinn_sentiment(terms, afinn):
    total = 0
    for t in terms:
        if t in afinn:
            # print('\t%s=%d' % (t, afinn[t]))
            total += afinn[t]
    return total
"""
read twitters.txt and rate each tweet, then output sentiment 
result into emotion.txt
"""
def rate_tweets(filename, afinn):
    total = 0
    good = 0
    neutral = 0
    bad = 0
    text_file1 = open("good.txt", "w")
    text_file2 = open("neutral.txt", "w")
    text_file3 = open("bad.txt", "w")
    text_file4 = open("summary.txt", "w")

    for line in open(filename):
        l = line.rstrip('\n')
        if len(l) > 0:
            score = afinn_sentiment(line.split(), afinn)
            total += 1
            if score > 0:
                good += 1
                text_file1.write('%s = %d\n' % (line, score))
            elif score < 0:
                bad += 1
                text_file3.write('%s = %d\n' % (line, score))
            else:
                neutral += 1
                text_file2.write('%s = %d\n' % (line, score))
    text_file4.write('Emotion Summary of Tweets\n')
    text_file4.write('Total number of tweets: %d\n' % total)
    text_file4.write('Good : %d\n' % good)
    text_file4.write('Neutral : %d\n' % neutral)
    text_file4.write('Bad : %d' % bad)
    text_file1.close()
    text_file2.close()
    text_file3.close()
    text_file4.close()


def main():
	afinn = read_afinn()
	rate_tweets('twitters.txt', afinn)


if __name__ == '__main__':
    main()
