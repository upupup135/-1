import requests
from bs4 import BeautifulSoup
from time import sleep  #引入时间
import threading     #引入多线程模块
import queue   #队列
import fake_useragent
import os


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Referer": ""
}
origin_url = "https://pic.netbian.com"


def huoquurl(url, xiangyin_result):
    res = requests.get(url=url, headers=headers)
    xiangyin_result.put(res.text)


def huoquimg(url01):  # url01现在是一个未知的参数，图片的URL链接
#拿网页的内容
#先拿图片的响应
    img_res = requests.get(url=url01, headers=headers)
    #拿到图片的响应体后，拿图片的二进制数据
    img_data = img_res.content
    #可以使用os模块建立文件夹
    if not os.path.exists("./img"):
        os.mkdir("./img")
    #写入文件夹中
    with open("./img/" + url01.split("/")[-1], mode="wb") as f:
        f.write(img_data)
        print("正在下载图片：{}".format(url01.split("/")[-1]))


#对拿到的响应进行处理，使用BeautifulSoup
def chulires(url03):    #url03只是一个形参，没实际作用
    soup = BeautifulSoup(url03, "lxml")
    # 先通过class找一下
    div01 = soup.find("div", class_="slist")
    #直接找img，因为每个里面都有img。
    img01 = div01.find_all("img")
    for img02 in img01:
        img_url = "{}{}".format(origin_url, img02["src"])  #得到完整的图片地址
        #调用函数huoquimg ，把图片地址传过去下载，放入文件夹里
        huoquimg(img_url)



def duoxiancheng():
    # 创建队列
    xiangyin_result = queue.Queue()    #xiangyin_result是xiangyin_result这个列表的队列，用来接收响应值的内容
    q = queue.Queue()         #q是url的数据队列，这个队列用来存储url地址
    for i in range(15, 25):
        q.put("https://pic.netbian.com/4k/index_{}.html".format(i))
    # 创建线程,发网页请求，请求多个页面的内容
    threads = []     #建立一个空列表
    threads01 = []   #建立一个接收图片url数据的空列表
    #range里面的值就是查看多少页的数据
    for i in range(10):
        #创建多线程
        t = threading.Thread(target=huoquurl, args=(q.get(), xiangyin_result))  #把这个xiangyin_result列表一同传入获取响应的方法中，把响应值添加到列表里
        threads.append(t)  #把通过huoquurl方法返回的响应添加到列表里面
    for i in range(10):
        threads[i].start()
    #这段代码的作用是启动11个线程。使用range(11)生成一个从0到10的数字序列，通过threads[i].start()启动对应索引的线程.
    for i in range(10):
        threads[i].join()
    #该代码片段是用于等待多个线程完成执行的。
    #同样创建关于xiangyin_result这个列表的多线程
    for i in range(xiangyin_result.qsize()):  #获取队列中响应值内容的个数  Queue.qsize() 返回队列的大小
        t1 = threading.Thread(target=chulires, args=(xiangyin_result.get(),))   #t1这只是一个组，通过循环把这些组传入threads01列表里面
        threads01.append(t1)
    for i in range(10):
        threads01[i].start()
    #这段代码的作用是启动11个线程。使用range(11)生成一个从0到10的数字序列，通过threads01[i].start()启动对应索引的线程.
    for i in range(10):
        threads[i].join()
    ##该代码片段是用于等待多个线程完成执行的。
    return xiangyin_result


duoxiancheng()










