# -*- coding: UTF-8 -*-
__author__ = "tianhuilin"

import requests
import math
import json
import re
from bs4 import BeautifulSoup


class TfIdf(object):
    """
    爬取多篇英文新闻，统计TF-IDF TOP10 高频词，存储为json文件
    """

    def __init__(self):
        pass

    def crawl_news(self, url):
        """
        提取指定网页链接的新闻标题和正文，去掉正文中的特殊符号，返回标题的字符串和一个由正文各个单词组成的列表
        :param url: str
        :return: (str, List[unicode])
        """
        if "foxnews.com" not in url and "chinadaily.com" not in url:
            print "Can't process url:", url
            return None
        else:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "lxml")
            try:
                if "foxnews.com" in url:
                    title = soup.find(itemprop="headline").get_text()
                    contents = soup.find("div", {"class": "article-text"}).get_text().lower()
                else:
                    title = soup.find(id="Title_e").find("h1").get_text()
                    contents = soup.find(id="Content").get_text().lower()
            except AttributeError, e:
                print "Can't find text in url:", url, e
                return None
            title, contents = self.remove_punc(title, contents)
            return title, contents

    def remove_punc(self, my_str1, my_str2):
        """
        去除标题的特殊字符，正文中的标点符号和特殊字符
        :param my_str1: unicode
        :param my_str2: unicode
        :return: str, List[unicode]
        """
        r1 = '[!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~]+'
        r2 = u"“|”|-|‘|’|：|'s|→|–| |\n|，"
        my_str1 = re.sub(r2, ' ', my_str1)
        my_str2 = re.sub(r1, "", my_str2)
        my_str2 = (re.sub(r2, ' ', my_str2)).split(" ")
        my_str2 = filter(lambda x: x != u'', my_str2)
        return my_str1, my_str2

    def tf_idf_10(self, urls):
        """
        统计TF-IDF词频，存储每篇新闻的TOP10 高频词。
        :param urls: List[str]
        :return: 写入json文件
        """
        articles_title = []
        articles_content = []
        for url in urls:
            if self.crawl_news(url):
                title, contents = self.crawl_news(url)
                articles_title.append(title)
                articles_content.append(contents)

        dict_df = {}
        dict_tf_list = []
        for content in articles_content:
            dict_tf = {}
            for term in content:
                if term in dict_tf:
                    dict_tf[term] += 1.0
                else:
                    dict_tf[term] = 1.0
                    if term in dict_df:
                        dict_df[term] += 1.0
                    else:
                        dict_df[term] = 1.0

            for term, times in dict_tf.items():
                dict_tf[term] = times / len(content)
            dict_tf_list.append(dict_tf)

        for term, times in dict_df.items():
            dict_df[term] = math.log(float(len(articles_title)) / times)

        for pos, content in enumerate(dict_tf_list):
            for term, tf in content.items():
                content[term] = tf * dict_df[term]
            dict_tf_list[pos] = sorted(content.items(), key=lambda d: d[1], reverse=True)

        out_put_data = []
        for i in range(len(articles_title)):
            data = []
            data.append("article_title:")
            data.append(articles_title[i])
            data.append([{"term": k, "value": round(v, 4)} for k, v in dict_tf_list[i][:10]])
            out_put_data.append(data)

        with open('TF_IDF_top10.json', 'w') as f:
            json.dump(out_put_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    url_list = [
        'http://www.foxnews.com/politics/2016/08/02/trump-calls-obama-worst-president-disaster-after-unfit-to-serve-slam.html',
        'http://www.foxnews.com/entertainment/2016/08/03/people-kiss-strangers-in-attempt-to-find-love-on-love-at-first-kiss.html',
        'http://www.foxnews.com/health/2016/08/03/does-jet-lag-make-hungry.html',
        'http://www.foxnews.com/travel/2016/08/03/rangers-advise-americans-to-stay-safe-as-record-numbers-flock-to-national-parks.html',
        'http://www.foxnews.com/sports/2016/08/02/brandon-marshall-made-bold-claims-about-ryan-fitzpatrick-and-jay-cutler.html',
        'http://www.foxnews.com/politics/2016/08/02/khan-and-smith-how-media-are-treating-two-grieving-parents.html',
        'http://www.foxnews.com/entertainment/2016/03/09/pawn-stars-figure-jailed-in-vegas-on-weapon-drug-charges.html',
        'http://www.foxnews.com/entertainment/2016/02/02/virginia-man-known-for-his-role-on-television-show-moonshiners-has-been.html',
        'http://www.foxnews.com/politics/2016/08/02/in-twist-environmentalists-fight-proposed-carbon-tax-because-it-doesnt-grow-govt.html',
        'http://www.foxnews.com/opinion/2016/08/02/teen-singers-honor-fallen-soldier-aboard-jetliner.html',
        'www.baidu.com',
        'http://www.chinadaily.com.cn/china/2016-08/03/content_26321051.htm',
        'http://www.chinadaily.com.cn/china/2016-08/03/content_26324333.htm',
        'http://www.chinadaily.com.cn/china/2016-08/03/content_26322896.htm',
        'http://www.chinadaily.com.cn/china/2016-08/02/content_26308237.htm',
        'http://www.chinadaily.com.cn/china/2016-08/03/content_26322807.htm',
        'http://www.chinadaily.com.cn/china/2016-08/03/content_26322443.htm',
        'http://www.chinadaily.com.cn/china/2016-08/01/content_26304735.htm',
        'http://www.chinadaily.com.cn/china/2016-08/03/content_26324677.htm',
        'http://www.chinadaily.com.cn/china/2016-08/03/content_26324.htm',
        'http://www.chinadaily.com.cn/china/2016-08/02/content_26308238.htm'
        ]
    TfIdf().tf_idf_10(url_list)
