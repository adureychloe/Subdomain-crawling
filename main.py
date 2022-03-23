
# baidu搜索引擎搜索子域名的语法为：site:[域名]
import requests  # 用于请求网页
from bs4 import BeautifulSoup  # 用于处理获取的到的网页源码数据
from urllib.parse import urlparse  # 用于处理url
# 忽略requests证书警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 定义一个采用baidu搜索的方法
def subdomain_search(domain_url:str, flag:int, pagenum:int):
    Subdomain = []  # 定义一个空列表用于存储收集到的子域名
    # 选择搜索引擎
    search_dict = {0: "https://cn.bing.com/search?q=domain%3A", 1: "https://www.baidu.com/s?ie=utf-8&wd=site%3A"}
    # 不同的页码标识
    page_dict = {0:"&first=", 1:"&pn="}
    num = 0 # 计数爬取子域名数量
    # 定义请求头，绕过反爬机制
    hearders = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',
        'accept': '*/*',
        #'referer': 'https://cn.bing.com/search?q=domain%3abaidu.com&qs=HS&pq=domain%3a&sc=10-7&cvid=B99CC286861647E79EF504A4D5B819F1&FORM=QBLH&sp=1',
        'referer': 'https://www.baidu.com/s?wd=site:qq.com&pn=0',
        'cookie': 'MUID=15F7A3347F9B66091BBBAC017EB56733'
    }
    if flag == 0:
        for i in range(pagenum):
            # 翻页处理，pagenum表示页码
            i = i * 10  # pn=0是第一页，pn=10是第二页，以此类推
            # 定义请求url
            url = search_dict[flag] + domain_url + page_dict[flag] + str(10 * i)
            resp = requests.get(url, headers=hearders, verify=False)  # 访问url，获取网页源码
            soup = BeautifulSoup(resp.content,
                                 'html.parser')  # 创建一个BeautifulSoup对象，第一个参数是网页源码，第二个参数是Beautiful Soup 使用的 HTML 解析器，
            job_bt = soup.find_all('h2')  # find_all()查找源码中所有<h2>元素的内容
            for item in job_bt:
                link = item.a.get('href')  # 循环获取元素<a>的属性href的内容
                title = item.a.contents  # 获取标签<a>的内容
                # urlparse是一个解析url的工具，scheme获取url的协议名，netloc获取url的网络位置
                domain = str(urlparse(link).scheme + "://" + urlparse(link).netloc)
                if domain in Subdomain:  # 如果解析后的domain存在于Subdomain中则跳过，否则将domain存入子域名表中
                    pass
                else:
                    Subdomain.append(domain)
                    num += 1
                    print(domain)

    elif flag==1:
        # 定义请求url
        for i in range(pagenum):
            # 翻页处理，pagenum表示页码
            i = i*10 #pn=0是第一页，pn=10是第二页，以此类推
            url = search_dict[flag] + domain_url + page_dict[flag] + str(i)
            resp = requests.get(url, headers=hearders, verify=False)  # 访问url，获取网页源码
            # print(resp.content)
            soup = BeautifulSoup(resp.content,
                                'html.parser')  # 创建一个BeautifulSoup对象，第一个参数是网页源码，第二个参数是Beautiful Soup 使用的 HTML 解析器，
            job_bt = soup.find_all('h3')  # find_all()查找源码中所有<h3>标签的内容
            for i in job_bt:
                link = i.a.get('href')  # 循环获取‘href’的内容
                domain = find_domain(link)
                # urlparse是一个解析url的工具，scheme获取url的协议名，netloc获取url的网络位置
                domain = str(urlparse(domain).scheme + "://" + urlparse(domain).netloc)
                if domain in Subdomain:  # 如果解析后的domain存在于Subdomain中则跳过，否则将domain存入子域名表中
                    pass
                else:
                    Subdomain.append(domain)
                    num += 1
                    print(domain)

    print("子域名爬取完成，一共{}个".format(num))

def find_domain(url):
    hearders = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',
        'accept': '*/*',
        # 'referer': 'https://cn.bing.com/search?q=domain%3abaidu.com&qs=HS&pq=domain%3a&sc=10-7&cvid=B99CC286861647E79EF504A4D5B819F1&FORM=QBLH&sp=1',
        'referer': 'https://www.baidu.com/s?wd=site:qq.com&pn=0',
        'cookie': 'MUID=15F7A3347F9B66091BBBAC017EB56733'
    }
    try:
        link = requests.get(url, headers=hearders, verify=False, timeout = 10).url  # 访问url，获取网页源码
    except:
        link = ""
        print("{} 无法访问或访问超时".format(url))  # 输出错误信息
    return link


if __name__=="__main__":
    domain = input("请输入需要查找的域名：")
    flag = int(input("请输入要用的搜索引擎（0：bing，1：百度）："))
    pagenum = int(input("请输入要查找的页数："))
    subdomain_search(domain,flag,pagenum)