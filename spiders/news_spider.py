import urllib.request
import json
from bs4 import BeautifulSoup

url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=antip&srv_id=pc&offset=0&limit=20&strategy=1&ext={%22pool%22:[%22high%22,%22top%22],%22is_filter%22:10,%22check_type%22:true}'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
req = urllib.request.Request(url)
resp = urllib.request.urlopen(req)
content = resp.read()
news_list = json.loads(str(content, 'utf-8'))['data']['list']
results = []


def is_Chinese(ch):
    if '\u4e00' <= ch <= '\u9fff':
        return True
    return False


def main():
    for news in news_list:
        if '美国' in news['title'] or '新加坡' in news['title'] or '英国' in news['title'] or '印' in news['title']:
            continue
        result = {'title': news['title'], 'img': news['img'], 'url': news['url'], 'media_name': news['media_name'], 'publish_time': news['publish_time']}
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

    with open('../spiders_data/news_data.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(results, ensure_ascii=False))


if __name__ == '__main__':
    main()
