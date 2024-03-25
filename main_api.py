from httpx import get
import os
def get_response_for(keyword, amount, page=1):
    url = f'https://unsplash.com/napi/search/photos?page={page}&per_page={amount}&query={keyword}'
    resp = get(url)
    if resp.status_code==200:
        return resp.json()

def get_image_urls(data):
    results = data['results']
    img_urls = [x['urls']['raw'] for x in results if x['premium'] is False]
    img_urls = [x.split('?')[0] for x in img_urls]
    return img_urls

def download_images(img_urls, max_download, dest_dir='images',tag=''):
    success = 0
    for url in img_urls:
        if success < max_download:
            resp = get(url)
            file_name = url.split('/')[-1]
            
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            
            with open(f'{dest_dir}/{tag}{file_name}.jpeg', 'wb') as f:
                f.write(resp.content)
                success+=1
    return success

def scrape(keyword, num_of_results):
    start_page=1
    success_count=0
    while success_count<start_page:
        data = get_response_for(keyword,amount=20,page=start_page)
        
        max_downloads = num_of_results - success_count
        if data:
            img_urls =get_image_urls(data)
            downloads = download_images(img_urls, max_downloads, tag=keyword)
            success_count += downloads
            start_page+=1
        else:
            print('Error no data returned')
            break
        
    
if __name__ == '__main__':
    # data = get_response_for('dogs',3)
    # print(get_image_urls(data))
    scrape('valorant', 10)