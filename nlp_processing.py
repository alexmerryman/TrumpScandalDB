import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
from nltk import word_tokenize, pos_tag, pos_tag_sents
from nltk.corpus import stopwords
stop = stopwords.words('english')

catalog_df = pd.read_csv("data/cleaned/catalog_cleaned.csv")
catalog_df_sample = catalog_df.sample(n=100)

# print(catalog_df_sample['entry_text_split'])


def tokenize_POS_tag(df):
    df = df[~df['entry_text_split'].isnull()]  # TODO: Do this in preprocess?
    df['entry_no_stopwords'] = df['entry_text_split'].apply(lambda x: ' '.join([word for word in str(x).split() if word not in (stop)]))
    df['tokenized_text'] = df['entry_no_stopwords'].apply(word_tokenize)
    df['bigrams'] = df['tokenized_text'].apply(lambda row: list(nltk.ngrams(row, 2)))
    df['POS_tagged_text'] = pos_tag_sents(df['entry_text_split'].apply(word_tokenize))

    return df


tokenized_tagged_df = tokenize_POS_tag(catalog_df_sample)


def bigrams_hashmap(df):
    flat_list = [item for sublist in df['bigrams'].tolist() for item in sublist]
    bigrams_hashmap_dict = {f'{k}': flat_list.count(k) for k in flat_list}
    print(bigrams_hashmap_dict)
    bigrams_hashmap_df = pd.DataFrame.from_dict(data=bigrams_hashmap_dict, orient='index', columns=['bigram', 'corpus_count'])

    return bigrams_hashmap_df


# https://scikit-learn.org/stable/modules/feature_extraction.html#feature-hashing
def POS_hashmap(df):
    unique_tokens = df['tokenized_text'].unique().tolist()
    # TODO: token_hash_dict


bigrams_hashmap_df = bigrams_hashmap(tokenized_tagged_df)
print(bigrams_hashmap_df)

tokenized_tagged_df.to_csv("nlp_df.csv", index=False)
print(tokenized_tagged_df)
