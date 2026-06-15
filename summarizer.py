# this file contains NLP logic 
import spacy 
import numpy as np 
from collections import Counter # counter is a subclass of dictionary that helps count hashable objects, it is used to count the frequency of words in the text and it provides a convenient way to create a frequency distribution of words in the text
nlp = spacy.load("en_core_web_sm") # en = english, core = core NLP features, web = trained on web text, sm = small model
def summarize_text(text, percentage=0.3): # text = user's article and percentage = summary size
    if not text.strip(): # check if the text is empty or contains only whitespace, if it does return an empty string as the summary
        return ""
    doc = nlp(text) # process the text with spacy 
    word_frequencies = {} # create a dictionary to store word frequency
    for token in doc:
        if (
            not token.is_stop and not token.is_punct and not token.is_space
            # ignore useless tokens that are stop words, punctuation and spaces
        ):
            word = token.lemma_.lower() # returns root form and converts everything to lowercase
            if word in word_frequencies: 
                word_frequencies[word] += 1 # if the word is already in the dictionary, increment its frequency
            else:
                word_frequencies[word] = 1 # if the word is not in the dictionary, add it with frequency 1
    if not word_frequencies: 
        return text # if there are no valid words in the text return the original text as the summary
    max_freq = max(word_frequencies.values()) # find the maximum frequency of any word in the dictionary
    for word in word_frequencies:
        word_frequencies[word] /= max_freq # normalize the frequencies by dividing each frequency by the maximum frequency
                    # scales everything between 0 and 1 
    sentence_scores = {} # create a dictionary to store sentence scores 
    sentences = list(doc.sents) # doc.sents is a generator used to extract the sentences and list is used access the individual sentences by index
    for sent in sentences: # processes one sentence at a time 
        for token in sent: # checks every word inside that sentence
            word = token.lemma_.lower()
            if word in word_frequencies: # check if it is important word 
                if sent in sentence_scores:
                    sentence_scores[sent] += word_frequencies[word] 
                else:
                    sentence_scores[sent] = word_frequencies[word] 
    summary_length = max(1, int(len(sentences) * percentage)) # calculates the number of sentences to be chosen for the summary based on the percentage specified by the user, max ensures atleast one sentence is selected
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:summary_length] # this sorts the sentences based on highest score in descending order and selects the top sentences based on the calculated summary length
    top_sentences = sorted(top_sentences, key=lambda s: sentences.index(s)) # this sorts the selected sentences back to their original order in the text using their index in the sentences list and it uses lambda function to get the index of each sentence
    summary = " ".join([sent.text for sent in top_sentences]) # this joins the text of the selected sentences together to form the final summary and it uses a space as a separator between sentences and it uses a list comprehension to extract the text of each selected sentence                            return summary
    return summary
def get_word_frequencies(text): # returns word frequencies for keyword visualization
    doc = nlp(text) # process the text with spacy
    words=[] # create a list to store the words in the text
    for token in doc:
        if(
            not token.is_stop and not token.is_punct and not token.is_space
        ):
            words.append(token.lemma_.lower())
    return Counter(words) # return a counter object that counts the frequency of each word in the list and it is a subclass of dictionary that provides a convenient way to create a frequency distribution of words in the text
def get_top_keywords(text, n=10): # returns the top n keywords for keyword visualization
    frequencies = get_word_frequencies(text) # get the word frequencies using the previous function
    return frequencies.most_common(n) # return the n most common words and their frequencies as a list of tuples, where each tuple contains n word and its frequency, it uses the most_common method of the Counter class to get the top n words based on their frequency
def get_text_statistics(text, summary):
    original_words = len(text.split()) # count the number of words in the original text by splitting the text
    summary_words = len(summary.split()) # count the number of words in the summary by splitting the summary
    original_sentences = len(list(nlp(text).sents)) # count the number of sentences in the original text by processing it with spacy and using doc.sents to get the sentences and then counting them 
    summary_sentences = len(list(nlp(summary).sents)) # count the number of sentences in the memory by processing it with spacy and using doc.sents to get the sentences and then counting them
    compression_ratio = round(
        (
            (original_words-summary_words) / original_words 
        ) *100, 
        2
    ) # calculate the compression ratio as the percentage of words reduced from the original text to the summary and it rounds the result to 2 decimal places
    stats = {
        "original_words": original_words,
        "summary_words": summary_words,
        "original_sentences": original_sentences,
        "summary_sentences": summary_sentences,
        "compression_ratio": compression_ratio
    }
    return stats



    