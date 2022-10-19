import pandas as pd
import os


def create_raw_dataset(path_to_search_files, starts_with_filename, path_to_save_csv):
    df_tweets = pd.DataFrame()
    list_files = os.listdir(path_to_search_files)
    for file in list_files:
        if file.startswith(starts_with_filename):
            df = pd.read_csv(os.path.join(path_to_search_files, file), sep = ";")
            df_tweets = pd.concat([df_tweets,df])
        
    df_tweets = df_tweets[["id","created_at","bank","text"]].drop_duplicates().reset_index(drop = True)
    df_tweets.columns = ["tweet_id","tweet_created_at","bank","tweet_original_text"]
    df_tweets.to_csv(path_to_save_csv, sep = ";", header = True, index = False)
    print("CSV file saved in path!")
    return df_tweets

def clean_raw_dataset(df, col):
    df = df[~df[col].str.contains("#AFazenda")]
    df = df[~df[col].str.contains("#Fazenda")]
    df = df[~df[col].str.contains("#fazenda")]
    df = df[~df[col].str.contains("#FAZENDA")]
    df = df[~df[col].str.contains("@AuroraAlimentos ")]
    df = df[~df[col].str.contains("#VCTGameChangers")]
    df = df[~df[col].str.contains("#eSports")]
    df = df[~df[col].str.contains("#LigaGamersClub")]
    df = df[~df[col].str.contains("Hathor")]
    df = df[~df[col].str.contains("patrocinadores")]
    df = df[~df[col].str.contains("patrocinador")]
    df = df[~df[col].str.contains("éxito")]
    df = df[~df[col].str.contains("worlds2022")]
    df = df[~df[col].str.contains("agressão")]
    df = df[~df[col].str.contains(" estoy ")]
    df = df[~df[col].str.contains(" gamer ")]
    df = df[~df[col].str.contains(" gamers ")]
    df = df[~df[col].str.contains(" worlds ")]
    df = df[~df[col].str.contains(" partida ")]
    df = df[~df[col].str.contains(" ao vivo ")]
    df = df[~df[col].str.contains("lollapaloozabr")]
    df = df[~df[col].str.contains("iampauloandre")]
    df = df[~df[col].str.contains(" bgs ")]
    return df