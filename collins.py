from bs4 import BeautifulSoup
import requests
import sys


def download_page(word):
    """
    从有道词典中下载对应单词的页面
    :param word: 指定的单词
    :return: str, 有道词典中单词的对应页面
    """
    t = requests.get('http://dict.youdao.com/w/{}/#keyfrom=dict2.top'.format(word))
    return t.text


def parse_page(html_str):
    """
    解析html页面，提取出柯林斯词典的部分
    :param html_str:
    :return:
    """
    soup = BeautifulSoup(html_str, features='html.parser')
    return str(soup.find(id='authTransToggle'))


def append_to_file(s, filename):
    """
    追加内容s到文件filename中
    :param s: str
    :param filename: str
    :return:
    """
    if s == 'None':
        return

    with open(filename, 'a', encoding='utf-8') as f:
        f.write(s)


def download_and_append_the_description_of_one_word_to_file(word, filename):
    tmp = download_page(word)
    append_to_file(parse_page(tmp), filename)


def write_head_tag_to_file(filename):
    """
    写入<head>标签到文件filename中，用于css能够正常工作并使排版美观
    :param filename:
    :return:
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(
            '<head>\n'
            '<meta content="b3b78fbb4a7fb8c99ada6de72aac8a0e" name="baidu_union_verify"/>\n'
            '<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>\n'
            '<meta content="illuminate" name="keywords">\n'
            '<title>{}</title>\n'
            '<link href="https://shared-https.ydstatic.com/images/favicon.ico" rel="shortcut icon" type="image/x-icon"/>\n'
            '<link href="https://shared.ydstatic.com/dict/v2016/result/160621/result-min.css" rel="stylesheet" type="text/css"/>\n'
            '<link href="https://shared.ydstatic.com/dict/v2016/result/pad.css" media="screen and (orientation: portrait), screen and (orientation: landscape)" rel="stylesheet" type="text/css"/>\n'
            '<link href="http://dict.youdao.com/w/illuminate/" rel="canonical">\n'
            '<link href="plugins/search-provider.xml" rel="search" title="Yodao Dict" type="application/opensearchdescription+xml"/>\n<script src="https://shared.ydstatic.com/js/jquery/jquery-1.8.2.min.js" type="text/javascript"></script>\n'
            '</link></meta></head>'.format(filename.replace('.html', '')))


def download_words_to_file(words_file_name, target_file_name):
    """
    指定一个单词集文件(words_file)，下载页面到target_file中去
    :param words_file_name: 单词集文件，每个单词换行
    :param target_file_name: 目标页面的文件名
    :return: None
    """
    write_head_tag_to_file(target_file_name)
    with open(words_file_name, 'r', encoding='utf-8') as words_file:
        words = words_file.read()
        words = words.split('\n')
        for word in words:
            print('Downloading ' + word + '...')
            download_and_append_the_description_of_one_word_to_file(word, target_file_name)
        print('Done.')


if __name__ == '__main__':
    words_file_name_ = sys.argv[1]
    target_file_name_ = sys.argv[2]
    download_words_to_file(words_file_name_, target_file_name_)
