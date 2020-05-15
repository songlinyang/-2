# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file
from qiniu import Zone, set_default
import sys
import os
basePath = os.path.dirname(os.path.abspath(__file__))

class QiniuUploader():

    def __init__(self):
        # 需要填写你的 Access Key 和 Secret Key
        self.access_key = 'Mdw2Q4oVkO3f8Ue-Ma5h_8idBr2WjLAtpq1Jhhnf'
        self.secret_key = 'op4PM_Bk97TXleBn4j8h7mGQFOITlN2gKizdFYNr'

        # 要上传的空间
        self.bucket_name = 'reportbucket'

    def upload_file(self,report_path,file_name):
        #name 是上传的文件名

        # 构建鉴权对象
        q = Auth(self.access_key,self.secret_key)

        # 上传到七牛后保存的文件名
        key = file_name

        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(self.bucket_name, key, 3600)

        # 要上传文件的本地路径
        localfile = os.path.join(report_path,file_name)
        #print(localfile)

        # 指定固定域名的zone,不同区域uphost域名见下文档
        # https://developer.qiniu.com/kodo/manual/1671/region-endpoint
        # 未指定或上传错误，sdk会根据token自动查询对应的上传域名
        # *.qiniup.com 支持https上传
        # 备用*.qiniu.com域名 不支持https上传
        # 要求https上传时，如果客户指定的两个host都错误，且sdk自动查询的第一个*.qiniup.com上传域名因意外不可用导致访问到备用*.qiniu.com会报ssl错误
        # 建议https上传时查看上面文档，指定正确的host

        # 设置七牛云上传文件服务器地址
        zone = Zone(
            up_host='https://up-z2.qiniup.com', # 上传文件的主机域名
            up_host_backup='https://upload.qiniup.com',
            io_host='http://iovip.qbox.me',
            scheme='https')
        set_default(default_zone=zone)

        try:
            ret, info = put_file(token, key, localfile)
        except Exception as err:
            print(info)
            print(ret)
            print(err)
        finally:
            return True
