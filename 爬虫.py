import os
import requests
from lxml import etree


def get_movies_data(url, headers):
    try:
        # 获取页面的响应内容
        db_response = requests.get(url, headers=headers)
        # 检查响应状态
        db_response.raise_for_status()  # Raise an error for bad responses
        # 将获得的源码转化为 etree
        db_response_etree = etree.HTML(db_response.content)

        # 提取所有电影数据
        db_movie_items = db_response_etree.xpath('//*[@id="content"]/div/div[1]/ol/li/div[@class="item"]')

        # 遍历电影数据列表
        for db_movie_item in db_movie_items:
            # 获取电影ID
            db_id = db_movie_item.xpath('div[@class="pic"]/em/text()')
            # 获取电影标题
            db_title = db_movie_item.xpath('div[@class="info"]/div[@class="hd"]/a/span[1]/text()')
            # 获取电影分数
            db_score = db_movie_item.xpath('div[@class="info"]/div[@class="bd"]/div/span[@class="rating_num"]/text()')
            # 获取电影评论
            db_des = db_movie_item.xpath('div[@class="info"]/div[@class="bd"]/p/text()[1]')
            # 获取电影图片
            db_pic = db_movie_item.xpath('div[@class="pic"]/a/img/@src')

            # 处理可能返回的空值
            print(f"ID: {db_id[0] if db_id else 'N/A'}, "
                  f"Title: {db_title[0] if db_title else 'N/A'}, "
                  f"Score: {db_score[0] if db_score else 'N/A'}, "
                  f"Description: {db_des[0].strip() if db_des else 'N/A'}, "
                  f"Image: {db_pic[0] if db_pic else 'N/A'}")

            with open(r"D:\img\v.txt","ab") as f:
                tmp_data = '编号：'+str(db_id)+'标题：'+str(db_title)+'评分：'+str(db_score)+'电影描述：'+str(db_des)+'\n'
                f.write(tmp_data.encode('utf-8'))
            db_pic = str(db_pic[0].replace("\'",""))
            download_img(db_id, db_title,db_pic,headers)
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_img(db_id, db_title,db_pic,headers):
    img_path =r"D:\img"
    if os.path.exists(img_path):
        pass
    else:
        os.mkdir(img_path)
    #获取图片二进制数据
    img_dada = requests.get(db_pic, headers=headers).content
    #设置图片存储的路径和名称
    image_path = os.path.join(img_path, f'{db_id[0]}_{db_title[0]}.jpg')
    #存储海报
    with open(image_path, 'wb') as f:
        f.write(img_dada)

def main():
    urls = ['https://movie.douban.com/top250?start='+str(i*25)+'&filter=' for i in range(10) ]
    #设置表头请求
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
}
    txt_path = r"D:\img\v.txt"
    if os.path.isfile(txt_path):
        os.remove(txt_path)

    #从列表取出url进行爬取
    for url in urls:
        get_movies_data(url, headers)

if __name__ == '__main__':
    main()
