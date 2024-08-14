import sys
import json
import os
from search_algorithm import contains_chinese, pinyin_matched, fuzzy_search

query = sys.argv[1]
fuzz_value = int(os.environ["fuzz_value"])
termbase_dir = os.environ["termbase_dir"]
termbase_names = [p for p in os.listdir(termbase_dir) if p.endswith(".json")]
termbase_paths = [os.path.join(termbase_dir, fn) for fn in termbase_names]
paired = list(zip(termbase_names, termbase_paths))

formatted_lst = []

for p in paired:
    with open(p[1], "r", encoding="utf-8") as f:
        tb = json.load(f)

    for k, v in tb.items():
        fuzzy_score = fuzzy_search(query, k)
        pinyin_score = pinyin_matched(query, k)

        if contains_chinese(query):
            if query in k:
                formatted_lst.append({
                        "title": k,
                        "subtitle" : " | ".join(v),
                        "arg" : f"{p[1]}||{k}||{' | '.join(v)}",
                        "mods" : {
                            "cmd" : {
                                "valid" : True,
                                "arg" : f"{p[1]}||{k}||{' | '.join(v)}",
                                "subtitle" : p[0]
                            }
                        },
                        "score": len(query) / len(k) * 100
                    })
            elif any(query in tt for tt in v):
                for tt in v:
                    if query in tt:
                        formatted_lst.append({
                                "title": f"{tt} 🔁",
                                "subtitle": k,
                                "arg": f"rev||{k}||{tt}",
                                "mods": {
                                    "cmd" : {
                                        "valid" : True,
                                        "arg" : f"rev||{k}||{tt}",
                                        "subtitle" : p[0]
                                    }
                                },
                                "score": len(query) / len(tt) * 100
                                  # this part needs to be updated so that instead of returning the first matched tt, it should return the one with the highest score
                            })
        else:
            if fuzzy_score or pinyin_score:
                formatted_lst.append({
                        "title": k,
                        "subtitle" : " | ".join(v),
                        "arg" : f"{p[1]}||{k}||{' | '.join(v)}",
                        "mods": {
                            "cmd" : {
                                "valid" : True,
                                "arg" : f"{p[1]}||{k}||{' | '.join(v)}",
                                "subtitle" : p[0]
                            }
                        },
                        "score": max(fuzzy_score, pinyin_score)
                    })
                
            # for reverse searches
            elif any(fuzzy_search(query, tt) or pinyin_matched(query, tt) for tt in v):
                for tt in v:
                    if fuzzy_search(query, tt) or pinyin_matched(query, tt):
                        formatted_lst.append({
                                "title": f"{tt} 🔁",
                                "subtitle": k,
                                "arg": f"rev||{k}||{tt}",
                                "mods": {
                                    "cmd" : {
                                        "valid" : True,
                                        "arg" : f"rev||{k}||{tt}",
                                        "subtitle" : p[0]
                                    }
                                },
                                "score": max(fuzzy_search(query, tt), pinyin_matched(query, tt)) # may need to simplify syntax
                            })

formatted_lst.sort(key=lambda x: x['score'], reverse=True)
formatted_d = {"items" : formatted_lst}

data = json.dumps(formatted_d)

sys.stdout.write(data)

