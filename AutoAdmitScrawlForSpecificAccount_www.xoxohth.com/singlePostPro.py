from requests import get as requests_get
from bs4 import BeautifulSoup
import re
from pandas import DataFrame

"""
**************************
// 汇总各楼层的信息，包括每层楼：【回帖人编号、被回帖人编号、回帖信息】
"""
def floor_info_collect(soup):
    
    #楼层信息，一个楼层编号，紧接该楼层信息，依次排列
    floor_info = soup.find_all("p")
    name_p = floor_info[1]
    floor_table = name_p.find_next_sibling("table")

    floor_list = [];

    while floor_table:

        reply_number = "#" + name_p.a["name"] # 评论账号
        
        if ( floor_table.find("a", href = re.compile("#\d+")) ):  # 被评论帐号
            beReplied_number = floor_table.find("a", href = re.compile("#\d+"))["href"]
        else:
            beReplied_number = "0"
        
        #print(floor_table.prettify())

        # 评论
        reply_content = ""
        strings_table = list(floor_table.stripped_strings)
        for ii in range( 4, len(strings_table) -1 ):
            reply_content += strings_table[ii]
            
        #for string in floor_table.stripped_strings:
            #print(string)

        floor_list.append([reply_number, beReplied_number, reply_content])
            
        
        name_p = floor_table.find_next_sibling("p")
        floor_table = name_p.find_next_sibling("table")


    return floor_list


"""
**************************
// 根据键值返回键
"""
def get_keys(dic, value):
    return [k for k,v in dic.items() if v == value]



def accountQueryInSinglePost(pageLinker, account_query):

    res = requests_get(pageLinker, timeout=(20, 60))
    soup = BeautifulSoup(res.text, 'lxml')

    """
    **************************
    """

    # 帖子全部内容，包括楼层索引部分和楼层信息部分
    post_content = soup.find("font", size="1", face="MS Sans Serif")


    """
    **************************
    """

    #帖子的标题
    post_title = post_content.b.string

    #楼层索引
    floor_index = post_content.find("table")


    """
    **************************
    // 一切以返回结果为准，网页元素可能有误
    // target: 通过索引部分，将楼层的编号和账号一一对应，保存在字典floor_number_account中
    """
    floor_number_account = {};

    #floor_index的每条索引以三条td保存
    floor_index_td_all = floor_index.find_all("td", recursive = False) # 只寻找直接子节点

    # 发帖人账号
    poster = ""

    td_index = 0
    while td_index < len(floor_index_td_all):
        
        # 每条索引以三条td保存，第一个td标签里存有楼层编号，第二个td标签里存有账号

        floor_number = floor_index_td_all[td_index].a["href"]
        
        floor_account = floor_index_td_all[td_index + 1].find("font", size="1", face="MS Sans Serif").string

        if(td_index == 0):
            poster = floor_account

        floor_number_account[floor_number] = floor_account

        td_index += 3



    """
    **************************
    //查询该帖子中是否出现过查询账号
    """

    if account_query in floor_number_account.values():
        #print("查询账号在该帖子中留下过痕迹！")
        
        floor_list = floor_info_collect(soup)


        # 查询账号是发帖人
        if account_query == poster:

            # 去除标题中的特殊字符
            with open("./poster/" + "".join(list(filter(str.isalnum, post_title))) + ".txt", "w", encoding='utf-8') as txt_file:

                print("post website: " + pageLinker + "\n", file = txt_file)
            
                print("post title: " + post_title + "\n\n", file = txt_file)

                indent = ""

                for floor_index in range(len(floor_list)):

                    if ( floor_index > 0 and floor_list[floor_index][1] == floor_list[floor_index - 1][0] ):
                        indent += "\t"
                        print(indent + "account: " + floor_number_account[floor_list[floor_index][0]], file = txt_file)
                        print(indent + floor_list[floor_index][2] + "\n\n", file = txt_file)

                    else:
                        indent = ""
                        print("account: " + floor_number_account[floor_list[floor_index][0]], file = txt_file)
                        print(floor_list[floor_index][2] + "\n\n", file = txt_file)


        # 查询账号是跟帖人
        else:       
            # 去除标题中的特殊字符
            with open("./replier/" + "".join(list(filter(str.isalnum, post_title))) + ".txt", "w", encoding='utf-8') as txt_file:

                # 跟帖的楼层
                account_query_reply_floor_numbers = get_keys(floor_number_account, account_query)
                
                print("post website: " + pageLinker + "\n", file = txt_file)          
                print("post title: " + post_title + "\n\n", file = txt_file)

                for floor_index in range(len(floor_list)):
                    if( floor_list[floor_index][0] in account_query_reply_floor_numbers):
                        print("reply to the account: " + floor_number_account[floor_list[floor_index][1]], file = txt_file)
                        print(floor_list[floor_index][2] + "\n\n", file = txt_file)
                    
               
            

    """    
    else:
        print("查询账号未在该帖子中留下过痕迹！")

    for xx, yy in floor_number_account.items():
        print(xx, "\t", yy)

    for xx in floor_list:
        print(xx)

    """



"""
// 测试与样例
"""
if __name__ == "__main__":

    account_query = "Muscadine wine"
    pageLinker_trunct = "http://www.xoxohth.com/thread.php?thread_id=4001814&mc=39&forum_id=2"

    accountQueryInSinglePost(pageLinker, account_query)
    





    
