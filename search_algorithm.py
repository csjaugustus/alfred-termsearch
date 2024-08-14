import json
import re
import pinyin
from thefuzz import fuzz
import string
import os

fuzz_value = int(os.environ["fuzz_value"])

def preprocess_text(text):
    # Remove punctuation and convert to lower case
    return text.translate(str.maketrans('', '', string.punctuation)).lower()

def contains_chinese(s):
    return re.findall(r'[\u4e00-\u9fff]+', s)

def pinyin_matched(query, target):
    if not contains_chinese(target):
        return False
    # explicitly replace some known errors in pinyin transcription
    with open("replace_d.json", "r", encoding="utf-8") as f:
        replace_d = json.load(f)

    for k, v in replace_d.items():
        target = target.replace(k, v)

    target_py = pinyin.get(target, format="strip", delimiter="")
    if len(query) > 1 and query in target_py:
        return len(query) / len(target_py) * 100
    return 0

def fuzzy_search(query, target, threshold=fuzz_value):
    """
    Perform a fuzzy search on a single target string to find the highest matching score
    between any word in the query and the target string, with higher scores for multiple word matches.

    Args:
    query (str): The query string containing words to search for.
    target (str): The single target string to be searched.
    threshold (int): The score threshold for considering a match.

    Returns:
    int: The highest score for any word in the query that meets or exceeds the threshold,
         possibly enhanced by multiple word matches.
    """
    # Preprocess the query and target
    query_words = preprocess_text(query).split()
    processed_target = preprocess_text(target)
    
    # Find the highest score above the threshold and count matches
    max_score = 0
    match_count = 0
    total_score = 0

    for word in query_words:
        score = fuzz.ratio(word, processed_target)
        if score >= threshold:
            match_count += 1
            total_score += score
            if score > max_score:
                max_score = score

    # If multiple words match, enhance the max score
    if match_count > 1:
        max_score = total_score / match_count  # Average score from all matches
        # Bonus proportional to the number of matching words
        max_score += (match_count - 1) * 10  # Adding 10 points per additional word

    return max_score