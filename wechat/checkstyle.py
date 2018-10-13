from bs4 import BeautifulSoup
import requests
import sys

def get_content(url):
    soup = BeautifulSoup(requests.get(url).text,'lxml')
    return soup.find(class_='rich_media_content').find_all('p')

def str_2_dic(style):
    dic = {}
    styles = [s.split(":") for s in style.split(";") if len(s) > 0]
    for s in styles:
        dic[s[0]] = s[1]
    return dic

def right_styles():
    #正文
    style1 = {
        'text-align' : ' left',
        'line-height' : ' 1.75em',
        'letter-spacing': ' 1px',
        'font-size': ' 15px'
        }
    #图片备注
    style2 = {
        'text-align': ' center',
        'line-height': ' 1.75em',
        'font-size': ' 14px',
        'color': ' rgb(178, 178, 178)',
        'letter-spacing': ' 1px'
    }
    #引言
    style3 = {
        'text-align': ' left',
        'line-height': ' 1.75em',
        'color': ' rgb(136, 136, 136)',
        'letter-spacing': ' 1px',
        'font-size': ' 14px'
    }
    #标题
    style4 = {
        'text-align': ' center',
        'line-height': ' 1.75em',
        'letter-spacing': ' 1px',
        'font-size': ' 16px'
    }

    return [style1, style2, style3, style4]
    
def check_style(url):
    content = get_content(url)
    for p in content:
        if not p.find("br") and not p.find("img"):
            style = p.get("style") if p.get("style") else ""
            if len(p.find_all("span")) > 0:
                style += ''.join(span.get("style") if span.get("style") else "" \
                         for span in p.find_all("span"))
            if len(style) > 0:
                style = str_2_dic(style)
                for right_style in right_styles():
                    if all(0 if key not in style or right_style[key] != style[key] \
                           else 1 for key in right_style):
                        break
                else:
                    print("[-] Incorrect: {}".format(p))



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[-] Error : Without URL as input \nExample: python chechstyle.py 'http://tmp_url.com'")
        sys.exit(0)
    tmp_url = sys.argv[1]
    check_style(tmp_url)