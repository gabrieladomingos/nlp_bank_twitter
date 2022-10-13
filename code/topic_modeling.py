from wordcloud import WordCloud
import matplotlib.pyplot as plt
import gensim
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
from pprint import pprint


def join_words(list_words):
    sentence = ' '.join(list_words)
    return sentence

def creat_wordcloud(df, bank, sentiment, colormap, stopwords, lexical):
    df = df[df['sentiment'] == sentiment]
    df = df[df['bank'] == bank]
    df["sentence"] = df["clean_tokens"].apply(lambda x: join_words(x))
    text = " ".join(sentence for sentence in df['sentence'])
    wordcloud = WordCloud(background_color="white", stopwords = stopwords,
                          colormap = colormap).generate(text)
    plt.figure(figsize=[10,10])
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    title = bank + " " + sentiment + " " + lexical
    plt.title(title)
    plt.savefig(f'wordcloud_{bank}_{sentiment}_{lexical}.png')
    plt.show()

        
def gensim_preprocess(list_tokens):
    for token in list_tokens:
        yield(gensim.utils.simple_preprocess(str(token)))                
       
    
def topic_modeling(df, bank, sentiment, num_topics):
    lda_models = dict()
    df = df[df['bank'] == bank]
    df = df[df["sentiment"] == sentiment]
    clean_tokens = list(gensim_preprocess(df["clean_tokens"]))
    id2word = corpora.Dictionary(clean_tokens)
    corpus = [id2word.doc2bow(text) for text in clean_tokens]
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=num_topics)
    print(bank + ":" + sentiment)
    print(" ")
    pprint(lda_model.print_topics())
    lda_models[bank] = lda_model[corpus]
    return lda_models