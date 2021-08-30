import html, requests, time

def scrape_page(url):
    time.sleep(0.4)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(url, headers=headers)
    cntnt = result.content.decode('utf-8')
    return html.unescape(cntnt)

def get_link(div):
    start_index = div.find('href="') + 6
    end_index = div.find('"', start_index)
    link = div[start_index:end_index]
    return link

def get_div_text(div, tag = "div", contains_div = False):
    start_index = div.find('>') + 1
    end_index = div.find('</{}>'.format(tag), start_index) if not contains_div else div.find("<",start_index)

    #Sanity check for if end tag is not included, above line assumes it is but for now it isnt being
    end_index = end_index if end_index > 0 else len(div)

    text = div[start_index:end_index]
    return text

def get_div_by_class(page, class_name, tag = "div"):
    div = ''
    start_index = get_start_index(page,class_name,tag) if class_name is not None else page.find('<{}>'.format(tag))
    is_entire_div = False
    offset = 0
    levels = 1
    while not is_entire_div:
        end_index = page.find('</{}>'.format(tag), start_index + offset) + len(tag) + 3
        offset = end_index - start_index + 4
        div = page[start_index:end_index]
        is_entire_div = div.count('<{}'.format(tag)) == levels
        levels = levels + 1
        if levels > 100:             #Sanity check, divs should never be bigger than this
            break
    return div

def get_div_text_by_class(page, class_name, tag = "div", contains_div = False):
    div = get_div_by_class(page,class_name,tag)
    return get_div_text(div,tag,contains_div)


def get_all_divs_by_class(page, class_name):
    divs = []
    div = ''
    
    while '<div class="{}"'.format(class_name) in page:
        start_index = page.find('<div class="{}"'.format(class_name))
        is_entire_div = False
        offset = 0
        levels = 1
        end_index = 0
        while not is_entire_div:
            end_index = page.find('</div>', start_index + offset)
            offset = end_index - start_index + 4
            div = page[start_index:end_index]
            is_entire_div = div.count('<div') == levels
            levels = levels + 1
            if levels > 100:  #Sanity check
                break
        divs.append(div)
        page = page[end_index:]
    return divs

def get_sections_in_div(div,tag = "span"):
    sections = []
    while '<{}'.format(tag) in div:
        section = ''
        start_index = div.find('<{}'.format(tag))
        is_entire_div = False
        offset = 0
        levels = 1
        end_index = 0
        while not is_entire_div:
            end_index = div.find('</{}>'.format(tag), start_index + offset) + len(tag) + 3
            offset = end_index - start_index + 4
            section = div[start_index:end_index]
            is_entire_div = div[:end_index].count('<{}'.format(tag)) == levels
            levels = levels + 1
        sections.append(section)
        div = div[end_index:]
    return sections

def get_img_from_div(div):
    start_index = div.find("<img")
    end_index = div.find(">", start_index)
    img = div[start_index:end_index]
    return img

def get_img_src(img):
    start_index = img.find('src="') + 5
    end_index = img.find('"',start_index + 5)
    link = img[start_index:end_index]
    return link

def get_button_by_title(page, title, tag="a"):
    return get_div_by_class(page,title,tag)


    
def get_start_index(page, class_name, tag = 'div'):
    start_index = 0
    offset = 0
    while start_index > -1:
        start_index = page.find('<{}'.format(tag))
        end_index = page.find('>', start_index)
        if class_name in page[start_index:end_index]:
            return start_index + offset
        offset += end_index
        page = page[end_index + 1:]
    return start_index
