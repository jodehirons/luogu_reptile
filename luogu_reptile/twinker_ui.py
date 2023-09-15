import tkinter as tk
from tkinter import ttk
import get_article_list
import get_MD
import sys
import time

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


# 定义重定向的方法，将终端输出的内容存到GUI页面
def redirect_print_to_text_widget(text_widget):
    class PrintRedirector:
        def __init__(self, text_widget):
            self.text_widget = text_widget

        def write(self, text):
            self.text_widget.insert(tk.END, text)
            self.text_widget.see(tk.END)

    sys.stdout = PrintRedirector(text_widget)


# d定义主要爬取方法
def search_and_crawl():
    keyword = keyword_entry.get()
    tag = tag_entry.get()
    difficult = difficult_combobox.get()

    if len(tag) > 0:
        tag = [tag_item for tag_item in tag.split("，")]

        # 清除之前的结果
    result_label.config(text="")

    # 调用get_article_list.py中的函数进行搜索
    total_count, article_list = get_article_list.get_infomation_list(
        difficult, tag, keyword
    )
    print(f"搜索得到的文章总数有{total_count}篇，爬取前50篇文章")
    start_time = time.time()  # 记录开始时间

    # 遍历搜索结果，调用get_MD.py中的函数进行爬取
    for article in article_list:
        get_MD.download_article_and_solution(
            article["pid"], article["title"], article["difficulty"], keyword
        )
        # 在这里可以将problemMD保存到文件或进行其他操作

    # 提示爬取完成
    end_time = time.time()  # 记录结束时间
    elapsed_time = end_time - start_time  # 计算时间差
    # 更新总共花费时间的文本框
    time_entry.delete(0, tk.END)  # 清空文本框内容
    time_entry.insert(tk.END, f"{elapsed_time:.2f}秒")  # 插入花费的时间

    result_label.config(text=f"爬取完成！总共花费时间：{elapsed_time:.2f}秒")  # 更新标签文本内容为花费的时间
    root.update()


# 创建GUI界面
root = tk.Tk()
root.title("洛谷题库搜索和爬取")
root.geometry("600x400")

# 创建输入框和标签
keyword_label = ttk.Label(root, text="关键词：")
keyword_label.pack()
keyword_entry = ttk.Entry(root, width=30)
keyword_entry.pack()

tag_label = ttk.Label(root, text="标签：")
tag_label.pack()
tag_entry = ttk.Entry(root, width=30)
tag_entry.pack()

difficult_label = ttk.Label(root, text="难度：")
difficult_label.pack()
difficult_combobox = ttk.Combobox(root, values=list(difficultymap.keys()), width=27)
difficult_combobox.pack()

# 创建样式对象
style = ttk.Style()

# 定义按钮样式
style.configure(
    "Custom.TButton", background="#4CAF50", foreground="blue", font=("Helvetica", 10)
)

# 创建搜索和爬取按钮
search_button = ttk.Button(
    root, text="搜索和爬取", command=search_and_crawl, style="Custom.TButton",width=20
)
search_button.pack()

time_label = ttk.Label(root, text="总共花费时间：")
time_label.pack()
time_entry = ttk.Entry(root)
time_entry.pack()

# 创建文本框
text_widget = tk.Text(root, width=80, height=20)
text_widget.pack()
# 重定向print语句的输出到文本框
redirect_print_to_text_widget(text_widget)
# 创建结果标签
result_label = ttk.Label(root, text="")
result_label.pack()


root.mainloop()
