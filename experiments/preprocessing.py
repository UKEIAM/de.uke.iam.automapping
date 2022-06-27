"""
 A step for deleting unnecessery information using Spacy tagging
 
"""

def delete_extra(data_list, spacy_voc):
    """
    data_list: data which we need to clean
    """
    ready_sent=[]
    for sentence in data_list:
        token_list=[]
        doc=spacy_voc(sentence)
        token_list=[token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        text = " ".join(token_list)
        ready_sent.append(text)
    return ready_sent