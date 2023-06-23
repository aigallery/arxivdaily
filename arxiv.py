import smtplib
import feedparser
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from TranslateDemo import createRequest
import time
import os


# Email configuration
email_from = os.getenv('EMAIL_FROM')
email_to = os.getenv('EMAIL_TO')
smtp_server = "smtp.163.com"
smtp_port = 25
smtp_username = os.getenv('EMAIL_USERNAME')
smtp_password = os.getenv('EMAIL_PASSWD')

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

def get_new_papers(feed_url,args):
    new_papers = []
    filtered_papers = []

    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        for it in ["cs.AI", "cs.CV"]:
            if it in entry.title:
                filtered_papers.append(entry)
    for interesting in args.keywords:
        record = []
        for idx in range(len(filtered_papers)):
            if interesting in filtered_papers[idx].title + filtered_papers[idx].summary.replace("\n", " "):
                record.append(idx)
                new_papers.append({
                    'title': filtered_papers[idx].title,
                    'authors': filtered_papers[idx].author,
                    'summary': filtered_papers[idx].summary.replace("\n", " "),
                    'link': filtered_papers[idx].link
                })
        if len(record) > 0:
            record.sort(reverse=True)
            [filtered_papers.pop(i) for i in record]
            

    return new_papers

def main(args):
    # Arxiv RSS feed URL
    feed_url = "http://arxiv.org/rss/cs"
    new_papers = get_new_papers(feed_url,args)
    num_papers = len(new_papers)
    body = ""
    subject = ""
    if num_papers > 0:
        subject += "Arxiv New Papers - {}".format(datetime.date.today())
        body += "There are {} new papers available:\n\n".format(num_papers)

        for i, paper in enumerate(new_papers, start=1):
            body += "Paper {}\n".format(i)
            body += "Title: {}\n".format(paper['title'])
            body += "Authors: {}\n".format(paper['authors'])
            body += "Summary: {}\n".format(paper['summary'])
            time.sleep(1)
            body += "SummaryChinese: {}\n".format(createRequest(paper['summary']))
            body += "Link: {}\n\n".format(paper['link'])
            body += "---------------------------------------------------------------\n"

        print("body in email:", body)
    else:
        body += "no papers found today!"
        body += "no papers found today!"

    send_email(subject, body)

if __name__ == '__main__':
    import argparse

    # 创建ArgumentParser对象
    parser = argparse.ArgumentParser(description='arxiv daily')

    # 添加命令行参数
    parser.add_argument('--keywords', type=str, nargs='+', default=['reinforcement', 'deep', 'learning', 'deep reinforcement learning', 'diffusion', 'autonomous','vehicle','driving','transformer','Image','image','Video','video'], help='interesting keywords')

    # 解析命令行参数
    args = parser.parse_args()
    main(args)

