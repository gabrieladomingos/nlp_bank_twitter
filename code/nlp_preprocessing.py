import pandas as pd
from enelvo.normaliser import Normaliser
import re
import spacy
import nltk
import string

stopwords_to_add = ["na", "a", "o", "na", "tá", "lá", "com", "um", "ta","ai","aí", "bradesco","itau","nubank", "itaú", "inter","banco","bank","digio","meudigio",
                    "santander", "santander_br", "santanderbr", "neon", "timeneon", "bancointer", "meudigio", "falanext", "bancopan", "bancooriginal","bancodobrasil", "next",
                    "c6", "C6Bank", "c6bank", "netflixbrasil", "fazenda", "pra", "dia", "auroraalimentos", "tava", "porque", "alo", "oi", "gente", "deus", "po", "pan", " "]



def remove_links_and_usernames(original_text):
    clean_text = re.sub(r"\@", "",(re.sub(r"(?:https?\://)\S+", "", original_text)))
    return clean_text

def remove_extras(original_text):
    clean_text = re.sub(r"[,.;@#?!&$]+", ' ',original_text)
    clean_text = re.sub(r"\s+", ' ', clean_text)
    return clean_text

def remove_pontuaction(original_text):
    text_without_pontuaction = original_text.translate(str.maketrans('', '', string.punctuation))
    return text_without_pontuaction


def tokenization(original_text, nlp, stopwords):
    doc = nlp(original_text)
    list_tokens = []
    for token in doc:
        if token.text not in stopwords:
            if token.pos_ == "VERB":
                final = token.lemma_
            else:
                final = token.text
            list_tokens.append(final.lower())   
    return list_tokens


def preprocessing_text(df, tweet_col, clean_text_col):
    df[clean_text_col] = df[tweet_col].apply(lambda x: remove_links_and_usernames(x))
    df[clean_text_col] = df[clean_text_col].str.lower()
    df[clean_text_col] = df[clean_text_col].str.replace(" vc "," você ")
    df[clean_text_col] = df[clean_text_col].str.replace(" q "," que ")
    df[clean_text_col] = df[clean_text_col].str.replace(" pq "," por que ")
    df[clean_text_col] = df[clean_text_col].str.replace(" hj "," hoje ")
    df[clean_text_col] = df[clean_text_col].str.replace("\n"," ")
    df[clean_text_col] = df[clean_text_col].str.replace(" ñ "," não ")
    df[clean_text_col] = df[clean_text_col].str.replace(" pqp "," puta que pariu ")
    df[clean_text_col] = df[clean_text_col].str.replace(" sl "," sei lá ")
    df[clean_text_col] = df[clean_text_col].str.replace(" td "," tudo ")
    df[clean_text_col] = df[clean_text_col].str.replace(" pro "," para o ")
    df[clean_text_col] = df[clean_text_col].str.replace(" tão "," estão ") 
    df[clean_text_col] = df[clean_text_col].str.replace(" tempão "," tempo ") 
    df[clean_text_col] = df[clean_text_col].str.replace(" senão "," se não ")
    df[clean_text_col] = df[clean_text_col].str.replace(" app "," aplicativo ")
    df[clean_text_col] = df[clean_text_col].str.replace(" obg "," agradecimento ")
    return df

def preprocessing_tokens(clean_text, stopwords, nlp):
    text_without_pontuaction = remove_extras(clean_text)
    tokens = tokenization(text_without_pontuaction, nlp, stopwords)
    return tokens

def tokens(sentence):
    tokens =  sentence.split(" ")
    return tokens
            
def sentence(list_tokens):
    sentence_string  = " ".join(list_tokens)
    return sentence_string

def pos_cleaning(df, col_tokens, col_final):
    df["sentence"] = df[col_tokens].apply(lambda x: sentence(x))
    df["sentence"] = df["sentence"].str.replace("odeier", "odiar")
    df["sentence"] = df["sentence"].str.replace("odeior", "odiar")
    df["sentence"] = df["sentence"].str.replace("obrigar", "agradecimento")
    df[col_final] = df["sentence"].apply(lambda x: tokens(x))
    df = df.drop("sentence", axis = 1)
    return df 
