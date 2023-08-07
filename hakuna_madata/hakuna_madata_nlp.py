# LIBRARIES
import pandas as pd
import emoji
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from textblob import Word

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# STYLING
plt.style.use('dark_background')
sns.set_palette("dark")

# READ CSV
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)

df = pd.read_csv('hakuna_madata/hakuna_madata.csv')

# FIRST LOOK
df.tail()
df.name.nunique()
df.name.value_counts().reset_index()
top10 = df.name.value_counts()[:10]
sns.barplot(y=top10.index, x=top10.values)

# FEATURE ENGINEERING
for col in df.columns:
    df[col] = df[col].str.strip()


# DATE
df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y %H:%M', errors='coerce')
df.groupby(df['date'].dt.day).message.count()
daily_message_count = df.resample('D', on='date').size()
sns.lineplot(x=daily_message_count.index, y=daily_message_count)

# EMOJI
message = "Bravoo 👏"

[c for c in message if emoji.is_emoji(c)]

df['emojis'] = df['message'].apply(lambda message: [c for c in message if emoji.is_emoji(c)])
df[df['emojis'].apply(lambda x: True if len(x) else False)]
df['emoji_count'] = df['emojis'].apply(lambda x: len(x))

df.tail()

emoji_counts = df['emojis'].apply(pd.Series).stack().value_counts()
df.groupby("name").agg({'emoji_count':'sum'}).sort_values(by='emoji_count', ascending=False)

emoji_counts.head(10)

# NLP STEPS

# normalizing case
df['message'] = df['message'].str.lower()
df.tail(10)

# numbers
df['message'] = df['message'].str.replace('\d', '', regex=True)
df.tail(10)

# stopwords
sw = stopwords.words('turkish')
df['message'] = df['message'].apply(lambda x: " ".join(w for w in x.split() if w not in sw))

# punctuations
pattern = r'[^\w\s]'
df['message'] = df['message'].str.replace(r'[^\w\s]', '', regex=True)
df.tail()

# rare words
temp_df = pd.Series(' '.join(df['message']).split()).value_counts()
drops = temp_df[temp_df <= 1]

# word cloud
message_with_media = df[df['message'] == 'medya dahil edilmedi'].index

text = " ".join(i for i in df['message'].drop(message_with_media))

wordcloud = WordCloud(width=800, height=400,).generate(text)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()