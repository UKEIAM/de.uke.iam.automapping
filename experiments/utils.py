import pandas as pd


def make_dataframe(dict_similar_concept, dictionary, data_frame):
    """
    Function for creating new DataFrame

    Variables
    -------------
    dict_similar_concept - {term: (concept_name, concept_id, similarity_score); (..)}
    dictinoary - {'term': terms, 'concepts': concepts}
    data_frame - init dataframe
    """
    compare_df=data_frame.copy()
    concepts=[]
    similarities=[]
    ids=[]
    for term in dictionary['terms']:
        number_of_concepts=len(dict_similar_concept[term][0][0])
        concepts+=(dict_similar_concept[term][0][0])
        ids+=(dict_similar_concept[term][0][1])
        similarities+=(dict_similar_concept[term][0][2])
    try:
        compare_df['Concept']=concepts
        compare_df['Concept_id']=ids
        compare_df['Similarity']=similarities

    except ValueError:
        compare_df=pd.DataFrame()
        compare_df['Term']=make_flatten_list_of_terms(dictionary['terms'], number_of_concepts)
        compare_df['Concept']=concepts
        compare_df['Concept_id']=ids
        compare_df['Similarity']=similarities
    return compare_df

def comparing_dataframes(df_old, df_new, num_guesses):
    """
    Function for comparing DataFrames

    Variables
    ------------
    df_old - df init, or what we got in previous chunk
    df_new - result of new chunk
    num_guesses - number of guesses 
    """
    df_together=pd.concat([df_old, df_new])
    df_together=df_together.set_index(['Concept', 'Concept_id']).groupby('Term')['Similarity'].nlargest(num_guesses).reset_index()#TODO Concept, Term make variables
    return df_together


def make_flatten_list_of_terms(terms, num_guesses):
    """
    Function from make list over list

    Variables
    ------------
    terms - list of terms
    num_guesses - number of guesses 
    """
    list_of_terms =[[i]*num_guesses for i in terms]
    flatten_list_of_terms=[]
    for i in list_of_terms:
        for ii in i:
            flatten_list_of_terms.append(ii)
    return flatten_list_of_terms