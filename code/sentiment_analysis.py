import pandas as pd
from leia import SentimentIntensityAnalyzer


def polarity_leiA(text, sentiment_analyser):
    polarity = sentiment_analyser.polarity_scores(text)['compound']
    return polarity

def get_sentiment(polarity):
    if polarity >= 0.05:
        sentiment = "positivo"
    elif polarity <= -0.05:
        sentiment = "negativo"
    else:
        sentiment = "neutro"
    return sentiment

def read_oplexicon(path):
    oplexicon = pd.read_csv(path, sep=",", header=None)
    oplexicon.columns = ["token", "class", "polarity", "classification_method"]
    oplexicon = oplexicon[['token','polarity']]
    oplexicon = oplexicon.drop_duplicates().reset_index(drop = True)
    return oplexicon

def polarity_oplexicon(path, df, tokens_col, group_cols):
    oplexicon = read_oplexicon(path)
    df_explode = df.copy()
    df_explode["clean_tokens_explode"]  = df_explode[tokens_col]
    df_explode = df_explode.explode("clean_tokens_explode")
    df_explode = df_explode.merge(oplexicon, how = 'left', left_on = "clean_tokens_explode", right_on = 'token')
    df_explode = df_explode.groupby(group_cols).mean().reset_index()
    df = df.merge(df_explode, on = group_cols, how = "left")
    return df


def groups_analysis(df, cols, group_cols):
    df_sentiment = df[cols].groupby(group_cols).count().reset_index()
    df_sentiment.columns = ['bank','sentiment','quantity']
    df_total = df_sentiment.groupby('bank').sum().reset_index()
    df_total.columns = ["bank","total"]
    df_sentiment = df_sentiment.merge(df_total, on = 'bank')
    df_sentiment["percentage"]= (df_sentiment["quantity"]/df_sentiment["total"])*100
    df_sentiment_pivot = df_sentiment.pivot(index = "bank", columns = "sentiment", values = "percentage")
    df_sentiment_pivot
    return df_sentiment_pivot

def calculate_bank_score(df):
    df["bank_score"] = df["positivo"] - df["negativo"]
    return df

    