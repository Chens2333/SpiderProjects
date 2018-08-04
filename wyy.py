# import time
# import urllib.request
# from urllib.request import urlretrieve
# import requests
# from bs4 import BeautifulSoup
#
#
# def get_page(url):
#     headers = {
#         'Host': 'music.163.com',
#         'Referer': 'https://music.163.com/',
#         'User-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36'
#     }
#     res = urllib.request.Request(url, headers=headers)
#
#     r = BeautifulSoup(res,'lxml')
#
#     music_dict = {}
#     # result = r.select('span[class="icn icn-dl"]')
#     result = r.find("ul",{'class': 'f-hide'}).find_all('a')
#     for music in result:
#         music_id = music.get('href').strip("/song?id=")
#         music_name = music.text
#         music_dict[music_id] = music_name
#     return music_dict
#
# def download_song(music_dict):
#     for song_id in music_dict:
#         song_url = "http://music.163.com/song/media/outer/url?id=%s.mp3" % song_id
#         path = "./网易云音乐/%s.mp3" % music_dict[song_id]
#         time.sleep(1)
#         urlretrieve(song_url, path)
#         print("正在下载%s" % music_dict[song_id])
#
# def main():
#     id = int(input('请输入歌单id：'))
#     url = 'https://music.163.com/playlist?id={}'.format(id)
#     music_dict = get_page(url)
#     download_song(music_dict)
#
# if __name__ == '__main__':
#     main()
from urllib import request

import requests,os,time,sys,re
from scrapy.selector import Selector

class wangyiyun():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Referer': 'http://music.163.com/'}
        self.main_url='http://music.163.com/'
        self.session = requests.Session()
        self.session.headers=self.headers

    def get_songurls(self,playlist):
        '''进入所选歌单页面，得出歌单里每首歌各自的ID 形式就是“song?id=64006"'''
        url=self.main_url+'playlist?id=%d'% playlist
        re= self.session.get(url)   #直接用session进入网页，懒得构造了
        sel=Selector(text=re.text)   #用scrapy的Selector，懒得用BS4了
        songurls=sel.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        return songurls   #所有歌曲组成的list
        ##['/song?id=64006', '/song?id=63959', '/song?id=25642714', '/song?id=63914', '/song?id=4878122', '/song?id=63650']

    def get_songinfo(self,songurl):
        '''根据songid进入每首歌信息的网址，得到歌曲的信息
        return：'64006'，'陈小春-失恋王'''
        url=self.main_url+songurl
        re=self.session.get(url)
        sel=Selector(text=re.text)
        song_id = url.split('=')[1]
        song_name = sel.xpath("//em[@class='f-ff2']/text()").extract_first()
        singer= '&'.join(sel.xpath("//p[@class='des s-fc4']/span/a/text()").extract())
        songname=singer+'-'+song_name
        return str(song_id),songname

    def download_song(self, songurl, dir_path):
        '''根据歌曲url，下载mp3文件'''
        song_id, songname = self.get_songinfo(songurl)  # 根据歌曲url得出ID、歌名
        song_url = 'http://music.163.com/song/media/outer/url?id=%s.mp3'%song_id
        path = dir_path + os.sep + songname + '.mp3'  # 文件路径
        request.urlretrieve(song_url, path)  # 下载文件

    def work(self, playlist):
        songurls = self.get_songurls(playlist)  # 输入歌单编号，得到歌单所有歌曲的url
        dir_path = r'C:\Users\Administrator\Desktop'
        for songurl in songurls:
            self.download_song(songurl, dir_path)  # 下载歌曲

if __name__ == '__main__':
    d = wangyiyun()
    d.work(2307923934)