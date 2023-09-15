import re
import urllib.request, urllib.error
import requests
import bs4
from fake_useragent import UserAgent
import json
import os

reverserd_difficulty_map = {
    -1: "无选择",
    0: "暂无评定",
    1: "入门",
    2: "普及-",
    3: "普及/提高-",
    4: "普及+/提高",
    5: "提高+/省选-",
    6: "省选/NOI-",
    7: "NOI/NOI+/CTSC",
}


baseUrl = "https://www.luogu.com.cn/problem/"
solutionUrl = "https://www.luogu.com.cn/problem/solution/"
savePath = "C:\\Users\\10196\\Desktop\\软件工程\\"

# request访问头部的构成
cookie = "__client_id=fe3875329dc1c1f5866f30eacb344db8db1c74eb;_uid=1095262"
headers = {"User-Agent": str(UserAgent().random), "cookie": cookie}


def download_article_and_solution(pid, title, difficult, keywords):
    # delay = random.randint(1, 5)
    # time.sleep(delay)#随机睡眠一段时间避免被反爬
    print(f"当前在爬取题目{pid}-{title}")
    article_html = getHTML(baseUrl + str(pid))
    solution_html = getHTML(solutionUrl + str(pid))
    if article_html == "error":
        print("爬取失败，可能是不存在该题或无权查看")
    else:
        problemMD = get_article_MD(article_html)
        print("爬取题目成功！正在保存...", end="")
        save_article_Data(problemMD, title, difficult, keywords, pid)
        print("题目保存成功!")
        solutionMD = get_solution_MD(solution_html)
        print("题解爬取成功，正在保存...", end="")
        save_soltion_Data(solutionMD, title, difficult, keywords, pid)
        print("题解保存成功")
    print("爬取完毕")


def getHTML(url):
    """传入URL地址获取response


    Args:
        url (str): URL地址

    Returns:
        _request.get_: _request的回复_
    """
    res = requests.get(url=url, headers=headers)
    res.encoding = "utf-8"
    html = res.text
    if str(html).find("Exception") == -1:  # 洛谷中没找到该题目或无权查看的提示网页中会有该字样
        return html
    else:
        return "error"


def get_article_MD(html):
    """_传入html网页内容处理得到markdown的字符串_

    Args:
        html (_request.txt_): _传入html网页的内容进行处理_

    Returns:
        _str_: _返回markdown文件的字符串_
    """
    bs = bs4.BeautifulSoup(html, "html.parser")
    core = bs.select("article")[0]
    md = str(core)
    # 按照标题层次写为markdown的形式，然后去除多余元素保存
    md = re.sub("<h1>", "# ", md)
    md = re.sub("<h2>", "## ", md)
    md = re.sub("<h3>", "#### ", md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
    return md


def get_solution_MD(html):
    """_传入html网页内容处理得到markdown的字符串_

    Args:
        html (_request.txt_): _传入html网页的内容进行处理_

    Returns:
        _str_: _返回markdown文件的字符串_
    """
    # 使用正则表达式提取json字符串
    match = re.search(
        r'window\._feInjection = JSON\.parse\(decodeURIComponent\("(.+?)"\)\);', html
    )
    if match:
        json_str = match.group(1)
        # 将url编码的json字符串解码
        decoded_json_str = urllib.parse.unquote(json_str)

        # 将json字符串转换为Python的字典对象
        data = json.loads(decoded_json_str)
        solutions = data["currentData"]["solutions"]["result"]  # 获取题解内容
        # 判断题解存不存在
        if len(solutions) > 0:
            bestSolution = solutions[0]
            md = bestSolution["content"]
            return md
        return "Sorry, there is no solution"
    else:
        return "No match found"


# 保存文章到指定路径
def save_article_Data(data, title, difficult, keywords, pid):
    invalid_chars = r'\/:*?"<>|'
    trimmed_filename = title.strip()
    for char in invalid_chars:
            trimmed_filename = trimmed_filename.replace(char, '_')
    title = trimmed_filename[:255]
    
    
    filename = f"{pid}-{title}.md"


    # 限制文件名长度为255个字符

    
    if "，" in keywords:
        keywords = keywords.replace("，", "-")
    father_path = savePath + reverserd_difficulty_map[difficult] + "-" + keywords
    file_path = father_path + "\\" + pid + "-" + title
    cfilename = file_path + "\\" + filename
    # 判断路径存不存在，如果不存在则创建路径
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file = open(cfilename, "w", encoding="utf-8")

    for d in data:
        file.writelines(d)
    file.close()


# 保存题解到指定路径
def save_soltion_Data(data, title, difficult, keywords, pid):
    invalid_chars = r'\/:*?"<>|'
    trimmed_filename = title.strip()
    for char in invalid_chars:
            trimmed_filename = trimmed_filename.replace(char, '_')
    title = trimmed_filename[:255]

    filename = f"{pid}-{title}-题解.md"

    # 限制文件名长度为255个字符

    if "，" in keywords:
        keywords = keywords.replace("，", "-")
    father_path = savePath + reverserd_difficulty_map[difficult] + "-" + keywords
    file_path = father_path + "\\" + pid + "-" + title
    cfilename = file_path + "\\" + filename
    
    
    
    # 判断路径存不存在，如果不存在则创建路径
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file = open(cfilename, "w", encoding="utf-8")

    for d in data:
        file.writelines(d)
    file.close()


if __name__ == "__main__":
    #测试爬取功能是否能正常进行
    download_article_and_solution("P1316", "数独", 1, "字符串，P")
    
