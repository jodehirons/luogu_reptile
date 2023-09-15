#根据需要进行搜索的关键词，难度种类等对洛谷的题目进行搜索，并返回所有文章的概况信息
import urllib.request, urllib.error
import requests
from fake_useragent import UserAgent
import json

listUrl = "https://www.luogu.com.cn/problem/list"

#使用fake_useragent构建虚拟头部
cookie ="__client_id=fe3875329dc1c1f5866f30eacb344db8db1c74eb;_uid=1095262"
headers= {'User-Agent':str(UserAgent().random),
          'cookie':cookie}
#初始化一个params用于传递查询信息
_contentOnly = 1
params = {"_contentOnly": _contentOnly}

#初始化一个词典用于存放所有的key以及对应的标签
tags={}

difficultymap = {
    "无选择": -1,
    "暂无评定": 0,
    "入门": 1,
    "普及-": 2,
    "普及/提高-": 3,
    "普及+/提高": 4,
    "提高+/省选-": 5,
    "省选/NOI-": 6,
    "NOI/NOI+/CTSC": 7,
}

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

def load_tags(tags):
    """将已经保存好的包含tags的JSON文件读入，存为字典

    Args:
        tags (dict): 空字典
    """
    if len(tags) != 0:
        return
    with open('keys.json','r',encoding='utf-8') as file:
        data = json.load(file)
        tags_list = data['tags']
        for tag in tags_list:
            tags[tag['name']] = tag['id']
    return tags


def get_infomation_list(difficult,user_tags,keywords):
    """通过难度，标签和关键词对题目进行搜索输入

    Args:
        difficult (str): 题目难度
        user_tags (list): _题目标签
        keywords (str): 搜索关键词

    Raises:
        Exception: _description_

    Returns:
       int and dict: 返回搜索到的文章数以及前五十篇（第一页）文章的信息
    """
    tags_list ={}
    tags_list = load_tags(tags_list)
    real_tags =[]
    print(f"正在搜索难度为{difficult},标签为{user_tags},关键词为{keywords}的文章")
    if len(difficult) >0 and difficult != "无选择"  :
        difficult = difficultymap[difficult]
        
    params["difficulty"] = difficult
    if len(user_tags) != 0:
        for tag in user_tags:
            if tag in tags_list.keys():
                tag_value = tags_list[tag]
                real_tags.append(tag_value)
            else:
                return "Error: Tag '{}' not found".format(tag)

        if len(real_tags) != 0:
            params['tag'] = real_tags
            
    if len(keywords) != 0:
        params['keyword'] = keywords
        
    print(params)
    res = requests.get(listUrl, headers=headers, params=params)
    
    #判断res是否获得正常的返回，如果返回失败则报错
    if res.status_code != 200:
        raise Exception("Error: Failed to get a successful response from the server")

    infomation = res.text
    json_load = json.loads(infomation)
    article_info = json_load["currentData"]["problems"]
    #获取搜索得到的文章数目以及文章信息
    totalCount = article_info["count"]
    problems = article_info["result"]
    print("文章搜索成功，返回搜索信息")
    return totalCount, problems   

if __name__ == '__main__':
    total_count,article = get_infomation_list("","","")
    print(article)
    pass