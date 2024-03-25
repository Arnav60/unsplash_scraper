from httpx import get
from selectolax.parser import HTMLParser
import os

def get_img_tags_for(term=None):
    if not term:
        raise Exception('No search term provided')
    
    url=f'https://unsplash.com/s/photos/{term}'
    resp = get(url)
    
    if resp.status_code != 200:
        raise Exception('Error getting response')
    
    tree = HTMLParser(resp.text)
    imgs = tree.css('figure a img')
    return imgs

def img_filter(url: str, keywords: list) -> bool:
    return not any(x in url for x in keywords)

# img_filter(src, ['premium', 'profile'])

def get_high_res_img_url(img_node):
    srcset = img_node.attrs.get("srcset")
    if srcset:
        srcset_list = srcset.split(", ")
        url_res = [src.split(" ") for src in srcset_list if img_filter(src, ['plus', 'profile', 'premium'])]
        if not url_res:
            return None
        
        return url_res[0][0].split("?")[0]
    else:
        return []
    
def save_images(img_urls, dest_dir='images', tag=''):
    for url in img_urls:
        resp= get(url)
        file_name = url.split('/')[-1]
        
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            
        with open(f"{dest_dir}/{tag}{file_name}.jpeg", 'wb') as f:
            f.write(resp.content)
        
    

if __name__ == '__main__':
    img_nodes = get_img_tags_for('cats')
    all_img_urls = [get_high_res_img_url(i) for i in img_nodes]
    img_urls = [u for u in all_img_urls if u]
    save_images(img_urls, 'images', 'cats')
    print(img_urls)