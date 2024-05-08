# SJCScraper
A Google Drive scraper for The Sunday Journal Club (SJC). Used for analysis and future maintenance.

# Background on The Sunday Journal Club

The Sunday Journal Club started in November 2023, and its members produce a (mostly) written form of media each week. Entries include a variety of forms such as poems, essays, drawings, casual rambles, opinion pieces, stories, and videos. It's currently organised through Google Drive, allowing people to share their thoughts when reading eachothers submissions.

It's a relaxed environment, and a great place to practice your prose! If you are interested in joining, please contact me! - James

Okay, now onto the boring stuff...

# Pre-requisites:
```
git clone https://github.com/jamespilcher/SJCScraper
```

1. Get added to the `sunday-journal-club` project in Google Cloud Console, and also be added as a Test User for the OAuth consent screen. Those in the sunday-journal-club@googlegroups.com already have access.
2. Navigate to APIs & Services -> Credentials. Under OAuth 2.0 Client IDs, download the SJCScraper as a JSON.
3. Place that JSON in the root of your SJCScraper directory, and rename it to `credentials.json`.
    - Alternatively you can set the `GOOGLE_OAUTH_CREDENTIALS_PATH` environment variable.

Python 3.10+

# Setup

Setup a python virtual environment, and install the requirements:

```bash
python -m venv env

source env/bin/activate

python -m pip install -r ./requirements.txt
```

Pre-commit set up:
```
pre-commit install
```

Add the SJC Folder ID to `generate_basic_dataframe.py`. You can get this from its URL
```
SJC_FOLDER_ID = "XXXXXXXXX"
```

# Running

For a rudementary analysis, please run:
```
python ./analysis.py
```

Example output:
```
              author  word_count_sum  word_count_mean  sentiment_polarity_mean  sentiment_subjectivity_mean
0   britta@gmail.com           23792      1113.588235                 0.190861                     0.499228           
1     troy@gmail.com            9521       521.000000                -0.056213                     0.574097            
2     jeff@gmail.com            2458       729.000000                 0.107223                     0.496752             
3  shirley@gmail.com            1693       564.333333                 0.076805                     0.550391             
4   pierce@gmail.com           18505      1184.473684                 0.108346                     0.426565            
5    annie@gmail.com            3158       519.750000                 0.191276                     0.516971             
6     abed@gmail.com            4246      1082.000000                 0.056805                     0.506592        
7    chang@gmail.com               5         5.000000                -0.973414                     0.806592         
```
