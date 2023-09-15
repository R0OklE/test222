#顽症体
import tkinter as tk
from tkinter import ttk
import re
from bs4 import BeautifulSoup
import requests
import os
import urllib.parse
import threading
from tkinter import filedialog
import tkinter.messagebox
import concurrent.futures
import time
import profile
#常用网址
baseUrl = "https://www.luogu.com.cn/problem/P"
queUrl = "https://www.luogu.com.cn/problem/solution/P"
solUrl = "https://www.luogu.com.cn/blog/_post/"
urlUrl = "https://www.luogu.com.cn/problem/list"
#文件保存的头路径
savePath = "E:\\pachong\\"
Path = "E:\\pachong\\"

#URL池
def fetch_url(url):
   headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76",
      "Cookie": "__client_id=383641e8eb3654287f93d5612bfe6e423cbda2fa; _uid=667359; C3VK=f7b0e2",
   }
   response = requests.get(url, headers=headers).text
   return {url: response}
#多线程爬取
def multi_threaded_crawler(urls, max_workers):
   html_data = []
   with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
      # 使用Executor.map方法保持URL顺序
      results = executor.map(fetch_url, urls)
      # 迭代结果并按顺序存储HTML数据
      for result in results:
         html_data.append(result)
   return html_data

#获取一组标题
def get_title(html,c):
   soup = BeautifulSoup(html, "html.parser")
   a = soup.findAll("li")
   for aa in a:
      b = aa.find("a")
      c.append((b.string))
   return c

#获取一组标签
def get_label(html):
   label = urllib.parse.unquote(html)
   number = extract_numbers(label)
   return number

#获取难度
def get_difficulty(number):
   if (number == "1"):
      difficulty = "入门"
   elif (number == "2"):
      difficulty = "普及-"
   elif (number == "3"):
      difficulty = "普及&提高-"
   elif (number == "4"):
      difficulty = "普及+&提高"
   elif (number == "5"):
      difficulty = "提高+&省选-"
   elif (number == "6"):
      difficulty = "省选&NOI-"
   elif (number == "7"):
      difficulty = "NOI/NOI+/CTSC"
   return difficulty

#获取题目
def get_html(url):
   headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76",
      "Cookie": "__client_id=383641e8eb3654287f93d5612bfe6e423cbda2fa; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2Fproblem%2FP1000; _uid=667359; SpilopeliaState=q6onssjuh2ich8muq6k3o1484u",
   }
   content = requests.get(url, headers=headers).text
   return content

#将题目保存
def get_MM(content):
   soup = BeautifulSoup(content,"html.parser")
   if soup.select("article"):
       core = soup.select("article")[0]
   else : core = content
   md = str(core)
   md = re.sub("<h1>", "# ", md)
   md = re.sub("<h2>", "## ", md)
   md = re.sub("<h3>", "#### ", md)
   md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
   md = re.sub("\*\*广告\*\*.*", '', md, flags=re.DOTALL)
   return md


#获取小马
def get_key(url):
   headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76",
      "Cookie": "__client_id=383641e8eb3654287f93d5612bfe6e423cbda2fa; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2Fproblem%2FP1000; _uid=667359; SpilopeliaState=q6onssjuh2ich8muq6k3o1484u",
   }
   content = requests.get(url, headers=headers)
   key = extract_number(content.text)
   return key
def get_horse(url):
   key = extract_number(url)
   return key

#利用获取到的key,再次爬取blog中的solution，return题解的主体
def get_solution(key):
   headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76",
      "Cookie": "__client_id=383641e8eb3654287f93d5612bfe6e423cbda2fa; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2Fproblem%2FP1000; _uid=667359; SpilopeliaState=q6onssjuh2ich8muq6k3o1484u",
   }
   content = requests.get(solUrl+str(key), headers=headers).text
   soup = BeautifulSoup(content, "html.parser")
   a = soup.findAll("div", attrs={"id": "article-content"})
   return a

#实现HTML转MD
def get_MD(a):
   md = str(a)
   md = re.sub("<h1>", "# ", md)
   md = re.sub("<h2>", "## ", md)
   md = re.sub("<h3>", "#### ", md)
   md = re.sub("<code>(.*?)</code>","'''",md)
   return md

#将题解保存
def save_file(data,filename):
    file = open(filename,"w",encoding="utf-8")
    file.write(data)
    check_new_folders()
    text.update()
    text.yview_moveto(1.0)
#   file.close()
#正则转换
def extract_number(text):
   pattern = r"%22id%22%3A(\d+)"#从题解爬出的html中，找出第一个题解的博客后缀
   match = re.search(pattern, text)
   if match:
      return match.group(1)
   return None
def extract_numbers(text):
   pattern = r"difficulty\D+(\d+)"#获取题单界面爬取到的html文件中的”difficulty“系数
   numbers = re.findall(pattern, text)
   return numbers

#提取标签
def match(label):
   match = re.search(r'\[([^\[\]]+)\]', label)#得到”2000“和”NOIP普及组”的标签
   if match:
      extracted_parts = match.group(1).split()
      a = extracted_parts[0][4:]
      extracted_parts[0] = extracted_parts[0][:4]+extracted_parts[1]
      extracted_parts[1] = a
      return extracted_parts

#根据要求创建文件夹
def set_folder(name):
   if not os.path.exists(name):
      os.mkdir(name)
 #  else:
    #print("Folder already exists")
#实现打包爬取前50
def packet():
    list = get_html(urlUrl)
    print("启动！ε=ε=ε=(~￣▽￣)~")
    result_text.insert(tk.END, "启动！ε=ε=ε=(~￣▽￣)~\n")
    result_text.update()
    # 空列表存放title
    c = []
    get_title(list, c)
    num = get_label(list)
    for i in range(1000,1050):
      #难度标签
      dif = get_difficulty(num[i-1000])
      print("正在获取第",i-999,"个文件")
      result_text.insert(tk.END, "正在获取文件...\n")
      result_text.yview_moveto(1.0)
      result_text.update()
      #题目
      title = c[i-1000]
      v = match(title)
      html = get_html(baseUrl + str(i))
      print("...")
      result_text.insert(tk.END, "...\n")
      result_text.update()
      #print(html)
      mm = get_MM(html)
      key = get_key(queUrl+str(i))
   #   print(key)
      solution = get_solution(key)
   #   print(solution)
      md = get_MD(solution)
      print("...")
      result_text.insert(tk.END, "...\n")
      result_text.yview_moveto(1.0)
      result_text.update()
      if v:
         set_folder(savePath+"\\"+dif+"-"+v[0]+"-"+v[1])
         set_folder(savePath+"\\"+dif+"-"+v[0]+"-"+v[1]+"\\"+"P"+str(i)+"——"+title)
         save_file(mm, savePath+"\\"+dif+"-"+v[0]+"-"+v[1]+"\\"+"P"+str(i)+"——"+title+"\\"+"P"+str(i)+"——"+title+".md")
         save_file(md, savePath+"\\"+dif+"-"+v[0]+"-"+v[1]+"\\"+"P"+str(i)+"——"+title+"\\"+"P"+str(i)+"——"+title+"题解"+".md")
      else:
         set_folder(savePath+"\\"+dif)
         set_folder(savePath+"\\"+dif+"\\"+"P"+str(i)+"——"+title)
         save_file(mm, savePath+"\\"+dif+"\\"+"P"+str(i)+"——"+title+"\\"+"P"+str(i)+"——"+title+".md")
         save_file(md, savePath+"\\"+dif+"\\"+"P"+str(i)+"——"+title+"\\"+"P"+str(i)+"——"+title+"题解"+".md")
    show_message_box()
    result_text.yview_moveto(1.0)
    result_text.update()
#实现急速？（也许）打包爬取前50
def packets():
    ll = get_html(urlUrl)
    print("启动！ε=ε=ε=(~￣▽￣)~")
    result_text.insert(tk.END, "启动！ε=ε=ε=(~￣▽￣)~\n")
    result_text.update()
    # 空列表存放title
    c = []
    d = []
    get_title(ll, c)
    num = get_label(ll)
    for i in range(1000,1050):
      #难度标签
      dif = get_difficulty(num[i-1000])
      print("正在获取第",i-999,"个文件")
      result_text.insert(tk.END, "正在获取文件...\n")
      result_text.yview_moveto(1.0)
      result_text.update()
      #题目
      title = c[i-1000]
      v = match(title)
      html = get_html(baseUrl + str(i))
      print("...")
      result_text.insert(tk.END, "...\n")
      result_text.update()
      #print(html)
      mm = get_MM(html)
      if i%5 ==0:
         urls = [
            queUrl + str(i),
            queUrl + str(i+1),
            queUrl + str(i+2),
            queUrl + str(i+3),
            queUrl + str(i+4)
         ]
         datas=multi_threaded_crawler(urls, 5)
         for data in datas:
            url, html = list(data.items())[0]
            key = get_horse(html)
            d.append(key)
      keys = d[i%5]
      solution = get_solution(keys)
   #   print(solution)
      md = get_MD(solution)
      print("...")
      result_text.insert(tk.END, "...\n")
      result_text.yview_moveto(1.0)
      result_text.update()
      if v:
         set_folder(savePath+"\\"+dif+"-"+v[0]+"-"+v[1])
         set_folder(savePath+"\\"+dif+"-"+v[0]+"-"+v[1]+"\\"+"P"+str(i)+"——"+title)
         save_file(mm, savePath+"\\"+dif+"-"+v[0]+"-"+v[1]+"\\"+"P"+str(i)+"——"+title+"\\"+"P"+str(i)+"——"+title+".md")
         save_file(md, savePath+"\\"+dif+"-"+v[0]+"-"+v[1]+"\\"+"P"+str(i)+"——"+title+"\\"+"P"+str(i)+"——"+title+"题解"+".md")
      else:
         set_folder(savePath+"\\"+dif)
         set_folder(savePath+"\\"+dif+"\\"+"P"+str(i)+"——"+title)
         save_file(mm, savePath+"\\"+dif+"\\"+"P"+str(i)+"——"+title+"\\"+"P"+str(i)+"——"+title+".md")
         save_file(md, savePath+"\\"+dif+"\\"+"P"+str(i)+"——"+title+"\\"+"P"+str(i)+"——"+title+"题解"+".md")
    show_message_box()
    result_text.yview_moveto(1.0)
    result_text.update()
#防止tkinter界面卡死
def execute_thread():
    # 创建子线程执行程序
    thread = threading.Thread(target=packet)
    thread.start()
#根据要求搜索并爬取
def search():
    difficulty = difficulty_var.get()
    difficulty = re.sub(r"/", "&", difficulty)
    keyword = keyword_entry.get()
    year = year_var.get()
    year = year.ljust(4)[:4]
    list = get_html(urlUrl)
    c = []
    b = []
    get_title(list, c)
    num = get_label(list)

    for i in range(1000, 1050):
        dif = get_difficulty(num[i - 1000])
        title = c[i - 1000]
        v = match(title)
        bo1 = (dif == difficulty) | (difficulty == "所有难度")
        if year!="全部年份":
            if v:
                bo2 = (v[1] == year)
            else :continue
        else: bo2=1
        if keyword:
            bo3 = (keyword == "P" + str(i))
        else: bo3=1
        if bo1 & bo2 & bo3:
            b.append(i)
    if b:
        for i in b:
            dif = get_difficulty(num[i - 1000])
            # 题目
            title = c[i - 1000]
            v = match(title)
            html = get_html(baseUrl + str(i))
            # print(html)
            mm = get_MM(html)
            key = get_key(queUrl + str(i))
            #   print(key)
            solution = get_solution(key)
            #   print(solution)
            md = get_MD(solution)
            if v:
                set_folder(savePath + "\\" + dif + "-" + v[0] + "-" + v[1])
                set_folder(savePath +"\\"  + dif + "-" + v[0] + "-" + v[1] + "\\" + "P" + str(i) + "——" + title)
                save_file(mm,
                          savePath +"\\"  + dif + "-" + v[0] + "-" + v[1] + "\\" + "P" + str(i) + "——" + title + "\\" + "P" + str(
                              i) + "——" + title + ".md")
                save_file(md,
                          savePath +"\\" + dif + "-" + v[0] + "-" + v[1] + "\\" + "P" + str(i) + "——" + title + "\\" + "P" + str(
                              i) + "——" + title + "题解" + ".md")
            else:
                set_folder(savePath +"\\" + dif)
                set_folder(savePath +"\\" + dif + "\\" + "P" + str(i) + "——" + title)
                save_file(mm,
                          savePath +"\\" + dif + "\\" + "P" + str(i) + "——" + title + "\\" + "P" + str(i) + "——" + title + ".md")
                save_file(md, savePath +"\\" + dif + "\\" + "P" + str(i) + "——" + title + "\\" + "P" + str(
                    i) + "——" + title + "题解" + ".md")

    else:print("404 Not Found!!!")
    result_text.insert(tk.END, "文件全部已经获取完成~（￣︶￣）↗\n")
    show_message_box()
    result_text.yview_moveto(1.0)
    result_text.update()
def searchs():
    difficulty = difficulty_var.get()
    difficulty = re.sub(r"/", "&", difficulty)
    keyword = keyword_entry.get()
    year = year_var.get()
    year = year.ljust(4)[:4]
    list = get_html(urlUrl)
    c = []
    b = []
    get_title(list, c)
    num = get_label(list)

    for i in range(1000, 1050):
        dif = get_difficulty(num[i - 1000])
        title = c[i - 1000]
        v = match(title)
        bo1 = (dif == difficulty) | (difficulty == "所有难度")
        if year!="全部年份":
            if v:
                bo2 = (v[1] == year)
            else :continue
        else: bo2=1
        if keyword:
            bo3 = (keyword == "P" + str(i))
        else: bo3=1
        if bo1 & bo2 & bo3:
            b.append(i)
    if b:
        for i in b:
            dif = get_difficulty(num[i - 1000])
            # 题目
            title = c[i - 1000]
            v = match(title)
            html = get_html(baseUrl + str(i))
            # print(html)
            mm = get_MM(html)
            key = get_key(queUrl + str(i))
            solution = get_solution(key)
            md = get_MD(solution)
            if v:
                set_folder(Path + dif + "-" + v[0] + "-" + v[1])
                set_folder(Path + dif + "-" + v[0] + "-" + v[1] + "\\" + "P" + str(i) + "——" + title)
                save_file(mm,
                          Path + dif + "-" + v[0] + "-" + v[1] + "\\" + "P" + str(i) + "——" + title + "\\" + "P" + str(
                              i) + "——" + title + ".md")
                save_file(md,
                          Path + dif + "-" + v[0] + "-" + v[1] + "\\" + "P" + str(i) + "——" + title + "\\" + "P" + str(
                              i) + "——" + title + "题解" + ".md")
            else:
                set_folder(Path + dif)
                set_folder(Path + dif + "\\" + "P" + str(i) + "——" + title)
                save_file(mm,
                          Path + dif + "\\" + "P" + str(i) + "——" + title + "\\" + "P" + str(i) + "——" + title + ".md")
                save_file(md, Path + dif + "\\" + "P" + str(i) + "——" + title + "\\" + "P" + str(
                    i) + "——" + title + "题解" + ".md")

    else:print("404 Not Found!!!")
    result_text.insert(tk.END, "文件全部已经获取完成~（￣︶￣）↗\n")
    show_message_box()
    result_text.yview_moveto(1.0)
    result_text.update()
#防止tkinter卡死
def execute_threads():
    # 创建子线程执行程序
    thread = threading.Thread(target=search)
    thread.start()
#GUI鼠标右键菜单栏
def do_copy():
    # 复制操作的代码
    pass
def do_paste():
    # 粘贴操作的代码
    pass
def do_cut():
    # 剪切操作的代码
    pass
def show_context_menu(event):
    menu.post(event.x_root, event.y_root)
#修改保存路径
def select_save_folder():
    global savePath
    savePath = filedialog.askdirectory()
    if savePath:
        Path_label.configure(text=savePath)
        root.mainloop()
        return savePath

    else:
        return None
#提示窗口
def show_message_box():
    tkinter.messagebox.showinfo("提示", "文件下载完成！(￣o￣) . z Z")

def check_new_folders():

    entry.delete(0, "end")
    entry.insert(0, savePath)

    folder_list = []
    for item in os.listdir(savePath):
        item_path = os.path.join(savePath, item)
        if os.path.isdir(item_path):
            folder_list.append(item)

    new_folders = []
    updated_folders = []

    for folder in folder_list:
        if folder not in existing_folders:
            new_folders.append(folder)
        else:
            folder_path = os.path.join(savePath, folder)
            subfolder_list = []
            for subitem in os.listdir(folder_path):
                subitem_path = os.path.join(folder_path, subitem)
                if os.path.isdir(subitem_path):
                    subfolder_list.append(subitem)
            for subfolder in subfolder_list:
                if subfolder not in existing_subfolders[folder]:
                    updated_folders.append(subfolder)

    if new_folders:
        text.insert("end", "新增文件夹及其内部文件夹名:\n")
        for folder in new_folders:
            text.insert("end", folder + "\n")
            folder_path = os.path.join(savePath, folder)
            for subitem in os.listdir(folder_path):
                subitem_path = os.path.join(folder_path, subitem)
                if os.path.isdir(subitem_path):
                    text.insert("end", " - " + subitem + "\n")
        text.insert("end", "\n")

    if updated_folders:
        text.insert("end", "更新的文件夹内部新增文件夹名:\n")
        for folder in updated_folders:
            text.insert("end", folder + "\n")
        text.insert("end", "\n")

    existing_folders.update(folder_list)
    for folder in folder_list:
        if folder not in existing_subfolders:
            existing_subfolders[folder] = set()
        folder_path = os.path.join(savePath, folder)
        subfolder_list = []
        for subitem in os.listdir(folder_path):
            subitem_path = os.path.join(folder_path, subitem)
            if os.path.isdir(subitem_path):
                subfolder_list.append(subitem)
        existing_subfolders[folder].update(subfolder_list)

    root.after(1000, check_new_folders)

#tkinter的body部分
savePath="E:\\pachong"
root = tk.Tk()
root.geometry("650x500")
root.title("题目筛选器")
root.resizable(0,0)

# 设置标签背景颜色为白色
style = ttk.Style()
style.configure("White.TLabel", background="white")

# 创建右键菜单
menu = tk.Menu(root, tearoff=0)
menu.add_command(label="复制", command=do_copy)
menu.add_command(label="粘贴", command=do_paste)
menu.add_command(label="剪切", command=do_cut)

# 绑定右键点击事件
root.bind("<Button-3>", show_context_menu)

# 难度选择
difficulty_label = ttk.Label(root, text="难度：")
difficulty_label.grid(row=1, column=0,pady=15)
difficulty_var = tk.StringVar(root)
difficulty_var.set("所有难度")
difficulty_options = [
    "所有难度",
    "入门",
    "普及-",
    "普及/提高-",
    "普及+/提高",
    "提高+/省选-",
    "省选/NOI-",
    "NOI/NOI+/CTSC",
    "所有难度"
]
difficulty_menu = ttk.OptionMenu(root, difficulty_var, *difficulty_options)
difficulty_menu.grid(row=1, column=1, columnspan=2,pady=15)

#年份输入
year_var = tk.StringVar(root)
year_var.set("全部年份")
year_options = [
    "全部年份",
 "1997".ljust(9)[:9],"1998".ljust(9)[:9],"1999".ljust(9)[:9],"2000".ljust(9)[:9],"2001".ljust(9)[:9],"2002".ljust(9)[:9],"2003".ljust(9)[:9],
"2004".ljust(9)[:9],"2005".ljust(9)[:9],"2006".ljust(9)[:9],"2007".ljust(9)[:9],"2008".ljust(9)[:9],"2009".ljust(9)[:9],
"2011".ljust(9)[:9],"2012".ljust(9)[:9],"2013".ljust(9)[:9],"2014".ljust(9)[:9],"2015".ljust(9)[:9],"2016".ljust(9)[:9],"2017".ljust(9)[:9],
"2018".ljust(9)[:9],"2019".ljust(9)[:9],"2020".ljust(9)[:9],"2021".ljust(9)[:9],"2022".ljust(9)[:9],"2023".ljust(9)[:9],
    "全部年份"
]
year_menu = ttk.OptionMenu(root, year_var, *year_options)
year_menu.grid(row=1, column=3, columnspan = 1,pady=15)

# 关键词输入
keyword_label = ttk.Label(root, text="关键词：")
keyword_label.grid(row=1, column=4, sticky="",pady=15)
keyword_entry = ttk.Entry(root)
keyword_entry.grid(row=1, column=5, padx=5, pady=15)

# 筛选按钮
filter_button = tk.Button(root, text="筛选", command=execute_threads)
filter_button.grid(row=1, column=6, columnspan=1, padx=5, pady=15)

# 打包下载
bag_label = ttk.Label(root, text="批量下载：")
bag_label.grid(row=3, column=0, padx=5, pady=15)
bag_button = ttk.Button(root, text="打包下载前50题", command=execute_thread)
bag_button.grid(row=3, column=1, columnspan=2, padx=5, pady=15)
bag_button = ttk.Button(root, text="急速下载前50题", command=packets)
bag_button.grid(row=3, column=3, columnspan=2, padx=5, pady=15)

#保存路径
save_path = ttk.Label(root, text="保存路径：")
save_path.grid(row=2, column=0, padx=5, pady=15)
Path_label = ttk.Label(root, text=savePath, style="White.TLabel")
Path_label.grid(row=2, column=1, padx=5, pady=15)
select_button = ttk.Button(root, text="选择保存路径", command=select_save_folder)
select_button.grid(row=2, column=5, padx=0, pady=15,sticky=tk.E)

# 结果输出文本框
result_text = tk.Text(root, height=12, width=40)
result_text.grid(row=4, column=0, columnspan=4, padx=5, pady=5)


entry = tk.Entry(root)
entry.grid(row=3, column=5, padx=5, pady=15)
# 创建文本控件
text = tk.Text(root, height=12,width=40)
text.grid(row=4,column=5,columnspan=4,padx=5,pady=5)

existing_folders = set()
existing_subfolders = {}
root.mainloop()
