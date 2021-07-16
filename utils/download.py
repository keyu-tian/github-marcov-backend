import os
import requests
from tqdm import tqdm
from retrying import retry

from meta_config import SPIDER_DATA_DIRNAME


@retry(stop_max_attempt_number=5, wait_random_min=100, wait_random_max=1000)
def download_from_url(url, fpath):
    """
    :example:
    >>> url = 'https://github.com.cnpmjs.org/BlankerL/DXY-COVID-19-Data/releases/download/2021.07.06/DXYArea.csv'
    >>> input_file = os.path.join(SPIDER_DATA_DIRNAME, 'epidemic_domestic_data', 'DXYArea.csv')
    >>> download_from_url(url, input_file)
    """
    
    requests.packages.urllib3.disable_warnings()
    
    response = requests.get(url, stream=True, verify=False)
    print('[responsed!]')
    if response.ok:
        file_size = int(response.headers['Content-Length'])
        
        if os.path.exists(fpath):
            first_byte = os.path.getsize(fpath)
        else:
            first_byte = 0
        if first_byte >= file_size:
            return file_size
        header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
        pbar = tqdm(
            total=file_size, initial=0, dynamic_ncols=True,
            unit='B', unit_scale=True, desc=os.path.split(fpath)[-1]
        )
        req = requests.get(url, headers=header, stream=True, verify=False)
        with(open(fpath, 'ab')) as f:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    pbar.update(1024)
        pbar.close()
        return file_size
    else:
        print(os.path.split(fpath)[-1] + ' 获取失败！')
        return 0
