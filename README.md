# arxivDaily

## email configuration

this env variable should be set in arxiv.py

```python
email_from = os.getenv('EMAIL_FROM')
email_to = os.getenv('EMAIL_TO')
smtp_username = os.getenv('EMAIL_USERNAME')
smtp_password = os.getenv('EMAIL_PASSWD')
```

## translation configuration

get these keys from youdao translation service if you need a translation for convenience.

```python
# 您的应用ID
APP_KEY = os.getenv("YOUDAO_TRANSLATE_APP_KEY") 
# 您的应用密钥
APP_SECRET = os.getenv("YOUDAO_TRANSLATE_APP_SECRET")
```

## run daily for linux


```shell
crontab -e
```

```shell
* * * * * python /path/to/your/arxiv.py
```

`*` stands for minute, hour, date, month, week respectively.