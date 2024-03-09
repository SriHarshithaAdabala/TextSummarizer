import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
 

text="""A college (Latin: collegium) is an educational institution or a constituent part of one. A college may be a degree-awarding tertiary educational institution, a part of a collegiate or federal university, an institution offering vocational education, a further education institution, or a secondary school.

In most of the world, a college may be a high school or secondary school, a college of further education, a training institution that awards trade qualifications, a higher-education provider that does not have university status (often without its own degree-awarding powers), or a constituent part of a university. In the United States, a college may offer undergraduate programs – either as an independent institution or as the undergraduate program of a university – or it may be a residential college of a university or a community college, referring to (primarily public) higher education institutions that aim to provide affordable and accessible education, usually limited to two-year associate degrees.[1] The word is generally also used as a synonym for a university in the US.[2] Colleges in countries such as France, Belgium, and Switzerland provide secondary education."""

def summarizer(rawdocs):
    stopwords=list(STOP_WORDS)
    #print(stopwords)

    nlp=spacy.load('en_core_web_sm')
    doc=nlp(rawdocs)
    #print(doc)

    tokens=[token.text for token in doc]
    #print(tokens)

    word_fre={}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_fre.keys():
                    word_fre[word.text]=1
                else:
                    word_fre[word.text]+=1
    #print(word_fre)
    max_freq=max(word_fre.values())
    #print(max_freq)
    for word in word_fre.keys():
        word_fre[word]=word_fre[word]/max_freq
    #print(word_fre)

    sent_tokens=[sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores={}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_fre.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent]=word_fre[word.text]
                else:
                    sent_scores[sent]+=word_fre[word.text]
    #print(sent_scores)
                    
    select_len=int(len(sent_tokens)*0.3)
    #print(select_len)

    summary=nlargest(select_len,sent_scores,key=sent_scores.get)
    #print(summary)

    final_summary=[word.text for word in summary]
    summary=' '.join(final_summary)
    #print(text)
    #print(summary)
    #print("length of original text",len(text.split(' ')))
    #print("length of summarized text",len(summary.split(' ')))
    return summary,doc,len(rawdocs.split(' ')),len(summary.split(' '))