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

exact_match_found = False

for p in paired:
    with open(p[1], "r", encoding="utf-8") as f:
        tb = json.load(f)

    for k, v in tb.items():
        if query == k:
            exact_match_found = True
        if contains_chinese(query):
            if query in k:
                formatted_lst.append({
                        "title": k,
                        "subtitle" : " | ".join(v),
                        "arg" : f"{p[1]}||{k}|{' | '.join(v)}",
                        "mods": {
                            "cmd" : {
                                "valid": True,
                                "arg": f"{p[1]}||{k}|{' | '.join(v)}",
                                "subtitle": p[0]
                            }
                        },
                        "score": len(query) / len(k) * 100
                    })
            elif any(query in tt for tt in v):
                for tt in v:
                    if query in tt:
                        formatted_lst.append({
                                "title": k,
                                "subtitle": f'✅ {" | ".join(v)}',
                                "arg": f"{p[1]}||{k}||{' | '.join(v)}",
                                "mods": {
                                    "cmd" : {
                                        "valid": True,
                                        "arg": f"{p[1]}||{k}||{' | '.join(v)}",
                                        "subtitle": p[0]
                                    }
                                },
                                "score": len(query) / len(tt) * 100 # need update to return highest match score instead of first
                            })
        else:
            if fuzzy_search(query, k) or pinyin_matched(query, k):
                formatted_lst.append({
                        "title": k,
                        "subtitle" : " | ".join(v),
                        "arg" : f"{p[1]}||{k}||{' | '.join(v)}",
                        "mods": {
                            "cmd" : {
                                "valid": True,
                                "arg": f"{p[1]}||{k}||{' | '.join(v)}",
                                "subtitle": p[0]
                            }
                        },
                        "score": max(fuzzy_search(query, k), pinyin_matched(query, k))
                    })
                
            elif any(fuzzy_search(query, tt) or pinyin_matched(query, tt) for tt in v):
                for tt in v:
                    if fuzzy_search(query, tt) or pinyin_matched(query, tt):
                        to_add = {
                                "title": k,
                                "subtitle": f'✅ {" | ".join(v)}',
                                "arg": f"{p[1]}||{k}||{' | '.join(v)}",
                                "mods": {
                                    "cmd" : {
                                        "valid": True,
                                        "arg": f"{p[1]}||{k}||{' | '.join(v)}",
                                        "subtitle": p[0]
                                    }
                                },
                                "score": max(fuzzy_search(query, tt), pinyin_matched(query, tt))
                            }
                        if to_add not in formatted_lst:
                            formatted_lst.append(to_add)



formatted_lst.sort(key=lambda x: x['score'], reverse=True)

if not exact_match_found:
    formatted_lst.insert(0, {
            "title" : query,
            "subtitle" : "This will be added as a new entry.",
            "arg" : f"new||{query}",
            "icon" : {"path" : "addnewentry.png"}
        })
    
formatted_d = {"items" : formatted_lst}

data = json.dumps(formatted_d)

sys.stdout.write(data)
