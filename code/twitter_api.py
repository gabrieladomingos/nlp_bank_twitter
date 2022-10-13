import os
import json
import requests
import pandas as pd

def make_api_request(endpoint, **kwargs):
    raw_response = requests.get(endpoint, **kwargs)
    response = raw_response.json()
    return response


def get_bank_tweets_search_api(bank, num_tweets=10):
    bearer_token = os.environ.get("BEARER_TOKEN")
    endpoint = "https://api.twitter.com/2/tweets/search/recent"
    query = f"""-is:retweet -is:reply -reality -Reality -patocinador -patrocinadores -Eleição -eleição 
    -Patrocinadores -Patrocinador -fazenda -Fazenda -#VCTGameChangers -#eSports -#LigaGamersClub -VALORANT -#AFazenda {bank}"""
    total_results = 0

    if num_tweets <= 100:
        params = {'query': query, 'tweet.fields': 'created_at,id,text', 'max_results': num_tweets}
    else:
        params = {'query': query, 'tweet.fields': 'created_at,id,text', 'max_results': 100}
    
    headers = {"Authorization": f"Bearer {bearer_token}","User-Agent": "v2RecentSearchPython"}
    response = make_api_request(endpoint, headers=headers, params=params)
    result = response['data']
    result_count = response['meta']['result_count']
    total_results = total_results + result_count

    while 'next_token' in response['meta']:
        if total_results >= num_tweets:
            return result

        params["next_token"] = response["meta"]["next_token"]
        response = make_api_request(endpoint, headers=headers, params=params)

        result = result + response['data']
        result_count = response['meta']['result_count']
        total_results = total_results + result_count
    return result


def get_multiple_banks_tweets_search_api(banks_list, num_tweets, path_to_save_csv):
    tweets_per_bank = {}
    for bank in banks_list:
        tweets = get_bank_tweets_search_api(bank, num_tweets)
        tweets_per_bank[bank] = tweets
    
    all_banks_tweets = pd.DataFrame()
    for key, value in tweets_per_bank.items():
        bank_tweets = pd.DataFrame.from_dict(value)
        bank_tweets['bank'] = key
        all_banks_tweets = pd.concat([all_banks_tweets, bank_tweets])

    all_banks_tweets.to_csv(path_to_save_csv, header = True, sep = ";", index = False, encoding="utf8")
    print("CSV file saved in path!")
    
    return all_banks_tweets

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