import requests
from urllib3 import encode_multipart_formdata


def go_upload(img_path):
    url = 'https://wechat.53iq.com/tmp/kitchen/api/upload_img'
    # files={'image":':('1.jpeg',open('1.jpeg','rb'),'images/png',{})}
    # files = {'upload': ('image.png', open(os.path.join(os.getcwd(), '1.jpeg'), 'rb').read(), 'multipart/form-data'),
    #          'type': photo_type}
    #
    # encode_data = encode_multipart_formdata(files)
    res = None
    with  open(img_path, 'rb') as f:
        file = {"image": ("filename", f.read()), 'watermark': 'yes'}
        encode_data = encode_multipart_formdata(file)
        file_data = encode_data[0]
        header = {'Content-Type': encode_data[1], }
        res = requests.post(url, headers=header, data=file_data).json()
    print("上传文件结果", res)
    return res


if __name__ == '__main__':
    go_upload()
