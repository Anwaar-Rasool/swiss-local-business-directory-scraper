def fix_mojibake(text):
    try:
        return text.encode("latin1").decode("utf-8")
    except:
        return text

import pandas as pd

df = pd.read_csv(r"D:\Crawling\TravelSaaS\Operators\Operators total final.csv", encoding='latin-1', low_memory=False)

df = df.map(lambda x: fix_mojibake(x) if isinstance(x, str) else x)

df.to_csv(r"D:\Crawling\TravelSaaS\Operators\Operators total final-encoded.csv", encoding="utf-8-sig", index=False)