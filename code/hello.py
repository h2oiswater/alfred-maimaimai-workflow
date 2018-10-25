#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

# Workflow3 supports Alfred 3's new features. The `Workflow` class
# is also compatible with Alfred 2.
from workflow import Workflow3, web
from bs4 import BeautifulSoup

def parseContent(content):
    label = content.find("div", "card-label")
    title = content.find("div", "zm-card-title")
    price = content.find("div", "card-price")
    a = content.find("a")
    if label != None and label.get_text().encode('utf8') == '国内':
        return {
            "title": price.get_text().strip(),
            "price": title.get_text(),
            "url": a.attrs['href']
        }
    else:
        return None
        

def parseHtml(html):
    list = []
    #转换为BeautifulSoup对象
    bsObj = BeautifulSoup(html)
    contentArray = bsObj.findAll("li", "card-group-list")
    for content in contentArray:
        result = parseContent(content)
        if result != None:
            list.append(result)
    return list


def main(wf):
    # The Workflow3 instance will be passed to the function
    # you call from `Workflow3.run`.
    # Not super useful, as the `wf` object created in
    # the `if __name__ ...` clause below is global...
    #
    # Your imports go here if you want to catch import errors, which
    # is not a bad idea, or if the modules/packages are in a directory
    # import here
    # added via `Workflow3(libraries=...)`
    # import urllib

    # Get args from Workflow3, already in normalized Unicode.
    # This is also necessary for "magic" arguments to work.
    args = wf.args
    
    # Do stuff here ...
    searchKey = args[0]

    data = web.get(url="https://search.m.smzdm.com", params={
        "s": searchKey,
        "v": "b"
    }, headers={
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Mobile Safari/537.36",
        "Host": "search.m.smzdm.com",
        "Referer": "https://search.m.smzdm.com/"
    }, cookies=None, auth=None,
        timeout=60, allow_redirects=True, stream=False)
    
    if data.status_code == 200:
        list = parseHtml(data.text)
        for item in list:
            wf.add_item(title=item['title'],
                    subtitle=item['price'],
                    valid=True,
                    arg='https://' + item['url'][4:])
        # Add an item to Alfred feedback
        # wf.add_item(title=searchKey,
        #             subtitle='subtitle1',
        #             valid=True,
        #             arg='https://www.baidu.com')
    else:
        # Add an item to Alfred feedback
        wf.add_item(title='failed',
                    subtitle='subtitle1',
                    valid=True,
                    arg='https://www.baidu.com')

    

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but subsequent calls
    # are ignored (otherwise the JSON sent to Alfred would be invalid).
    wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3()
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))