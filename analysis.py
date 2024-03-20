from textblob import TextBlob

import populate_dataframe

# ----------- Temporary Analysis! -----------

df = populate_dataframe.generate_dataframe()
#  columns=['week', 'title', 'content', 'author', 'file_id'])

# Create new columns for word count, sentiment polarity and sentiment subjectivity
df["word_count"] = df["content"].apply(lambda x: len(str(x).split(" ")))
df["sentiment_polarity"] = df["content"].apply(lambda x: TextBlob(x).sentiment[0])
df["sentiment_subjectivity"] = df["content"].apply(lambda x: TextBlob(x).sentiment[1])

# Group by author and calculate mean sentiment, total word count, average words per entry, and number of entries
grouped = (
    df.groupby("author")
    .agg(
        {
            "word_count": ["sum", "mean"],
            "sentiment_polarity": "mean",
            "sentiment_subjectivity": "mean",
            "content": "count",
        }
    )
    .reset_index()
)

# Flatten the MultiIndex in columns
grouped.columns = ["_".join(col).strip() for col in grouped.columns.values]

print(grouped.sort_values(by="content_count", ascending=False))
