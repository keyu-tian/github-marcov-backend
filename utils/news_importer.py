import urllib.request
import json
from bs4 import BeautifulSoup

from news.models import *


def is_Chinese(ch):
    if '\u4e00' <= ch <= '\u9fff':
        return True
    return False


def news_spider():
    results = []
    url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=antip&srv_id=pc&offset=0&limit=65&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    content = resp.read()
    news_list = json.loads(str(content, 'utf-8'))['data']['list']
    for news in news_list:
        result = {'title': news['title'],
                  'img': news['img'],
                  'url': news['url'],
                  'media_name': news['media_name'],
                  'publish_time': news['publish_time'],
                  'category_cn': news['category_cn'],
                  'sub_category_cn': news['sub_category_cn'],
                  }
        # print(result)
        url = result['url']
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        content = resp.read()
        soup = BeautifulSoup(content, 'html.parser')
        content = soup.find_all("p")
        article_contents = []
        for c in content:
            text = c.contents
            if is_Chinese(str(text[0])[0]):
                article_contents.append(text[0])
        result['context'] = '\n'.join(article_contents)
        if len(result['context']) == 0:
            continue
        results.append(result)

    with open('./spiders/spiders_data/news_data.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(results, ensure_ascii=False))
    return results


def news_importer():
    with open('./spiders/spiders_data/news_data.json', 'r+', encoding='utf-8') as f:
        data = json.loads(f.read())
    print(data)
    # 如果想要在存新的新闻之前删去旧的，可以去掉下面三行的注释
    # old_news = News.objects.all()
    # while old_news.count():
    #     old_news.delete()
    for line in data:
        # try:
        News.objects.get_or_create(title=line['title'], defaults={
            'img': line['img'],
            'url': line['url'],
            'media': line['media_name'],
            'publish_time': line['publish_time'],
            'context': line['context'],
            'category_cn': line['category_cn'],
            'sub_category_cn': line['sub_category_cn'],
        })
        # except:
        #     print('插入新闻数据错误')


if __name__ == '__main__':
    news_importer()
