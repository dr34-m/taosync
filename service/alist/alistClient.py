"""
@Author：dr34m
@Date  ：2024/7/4 13:57 
"""
import requests


class AlistClient:
    def __init__(self, url, token, alistId=None):
        """
        初始化
        :param url: 请求地址，例如'http://localhost:5244'，注意结尾不要/
        :param alistId: 存在数据库中的id
        :param token: 登录鉴权信息
        """
        self.url = url
        self.user = None
        self.alistId = alistId
        self.token = token
        self.getUser()

    def req(self, method, url, data=None, params=None):
        """
        通用请求
        :param method: get/post
        :param url: 请求地址，/api/xxx
        :param data: 需要放在请求体中用json传的数据
        :param params: 在url中的请求参数
        :return: 200返回res['data']，401自动登录后重试，失败抛出异常
        """
        res = {
            'code': 500,
            'message': None,
            'data': None
        }
        headers = None
        if self.token is not None:
            headers = {
                'Authorization': self.token
            }
        try:
            r = requests.request(method, self.url + url, json=data, params=params, headers=headers, timeout=(10, 300))
            if r.status_code == 200:
                res = r.json()
            else:
                res['code'] = r.status_code
                res['message'] = '状态码非200_/_Code not 200'
        except Exception as e:
            if 'Invalid URL' in str(e):
                raise Exception("alist地址格式有误_/_The alist address format is incorrect")
            elif 'Max retries' in str(e):
                raise Exception("alist连接失败，请检查是否填写正确_/_"
                                "Alist connection failed, please check whether it is filled in correctly")
            raise Exception(e)
        if res['code'] != 200:
            if res['code'] == 401:
                raise Exception("AList鉴权失败，可能是令牌已失效_/_AList authentication failed"
                                ", possibly because the token has expired")
            raise Exception(f"AList返回{res['code']}错误，原因为：{res['message']}_/_"
                            f"AList returns {res['code']}, reason: {res['message']}")
        return res['data']

    def post(self, url, data=None, params=None):
        """
        发送post请求
        :param url: 请求地址，/api/xxx
        :param data: 需要放在请求体中用json传的数据
        :param params: 放在url中的请求参数
        :return: 200返回res['data']，401自动登录后重试，失败抛出异常
        """
        return self.req('post', url, data, params)

    def get(self, url, params=None):
        """
        发送get请求
        :param url: 请求地址，/api/xxx
        :param params: 放在url中的请求参数
        :return: 200返回res['data']，401自动登录后重试，失败抛出异常
        """
        return self.req('get', url, params=params)

    def getUser(self):
        """
        获取当前用户
        :return:
        """
        self.user = self.get('/api/me')['username']

    def updateAlistId(self, alistId):
        """
        更新alistId
        :param alistId:
        :return:
        """
        self.alistId = alistId

    def fileListApi(self, path, refresh=True):
        """
        目录列表
        :param path: 目录
        :param refresh: 强制刷新，true/false
        :return: {
            "test1-1/": {},  # key以/结尾表示目录
            "test1.txt": 4  # 不以/结尾，表示文件，存文件大小
        }
        """
        res = self.post('/api/fs/list', data={
            'path': path,
            'refresh': refresh
        })['content']
        if res is not None:
            return {
                f"{item['name']}/" if item['is_dir'] else item['name']: {} if item['is_dir']
                else item['size'] for item in res
            }
        else:
            return {}

    def filePathList(self, path):
        """
        通过路径获取其下路径列表
        :param path:
        :return:
        """
        res = self.post('/api/fs/list', data={
            'path': path,
            'refresh': True
        })['content']
        if res is not None:
            return [{'path': item['name']} for item in res if item['is_dir']]
        else:
            return []

    def allFileList(self, path, refresh=True):
        """
        递归获取文件列表
        :param path: 根路径
        :param refresh: 强制刷新，true/false
        :return: {
            "test1-1/": {
                "test1-3/": {
                    "test1.txt": 4
                },
                "test1.txt": 4
            },
            "test1.txt": 4
        }
        """
        fList = self.fileListApi(path, refresh)
        for key in fList.keys():
            if key.endswith('/'):
                fList[key] = self.allFileList(f"{path}/{key[:-1]}", refresh)
        return fList

    def deleteFile(self, path, names=None):
        """
        删除文件或目录
        :param path: 路径
        :param names: 文件/目录名，列表
        """
        self.post('/api/fs/remove', data={
            'names': names,
            'dir': path
        })

    def copyFile(self, srcDir, dstDir, name):
        """
        复制文件
        :param srcDir: 源目录
        :param dstDir: 目标目录
        :param name: 文件名
        :return: 任务id
        """
        tasks = self.post('/api/fs/copy', data={
            'src_dir': srcDir,
            'dst_dir': dstDir,
            'names': [
                name
            ]
        })['tasks']
        if tasks:
            return tasks[0]['id']
        else:
            return None

    def taskInfo(self, taskId):
        """
        任务详情
        :param taskId: 任务id
        :return: {
            "id": "26GQSD1mZHDlDq1V1Lf7G",
            "name": "copy [/test1](/test1/test1.txt) to [/test2](/)",
            "state": 2, # 0-等待中，1-进行中，2-成功
            "status": "getting src object",
            "progress": 0, # 进度
            "error": ""
        }
        """
        return self.post('/api/admin/task/copy/info', params={
            'tid': taskId
        })

    def copyTaskDone(self):
        """
        已完成的复制任务
        :return: [{
            "id": "26GQSD1mZHDlDq1V1Lf7G",
            "name": "copy [/test1](/test1/test1.txt) to [/test2](/)",
            "state": 2, # 0-等待中，1-进行中，2-成功
            "status": "getting src object",
            "progress": 0, # 进度
            "error": ""
        }]
        """
        return self.get('/api/admin/task/copy/done')

    def copyTaskUnDone(self):
        """
        未完成的复制任务
        :return: [{
            "id": "26GQSD1mZHDlDq1V1Lf7G",
            "name": "copy [/test1](/test1/test1.txt) to [/test2](/)",
            "state": 1, # 0-等待中，1-进行中，2-成功
            "status": "getting src object",
            "progress": 0, # 进度
            "error": ""
        }]
        """
        return self.get('/api/admin/task/copy/undone')

    def copyTaskRetry(self, taskId):
        """
        重试复制任务
        :param taskId: 任务id
        """
        self.post('/api/admin/task/copy/retry', params={
            'tid': taskId
        })

    def copyTaskClearSucceeded(self):
        """
        清除已成功的复制任务
        """
        self.post('/api/admin/task/copy/clear_succeeded')

    def copyTaskDelete(self, taskId):
        """
        删除复制任务
        :param taskId: 任务id
        """
        self.post('/api/admin/task/copy/delete', params={
            'tid': taskId
        })

    def copyTaskCancel(self, taskId):
        """
        取消复制任务
        :param taskId: 任务id
        """
        self.post('/api/admin/task/copy/cancel', params={
            'tid': taskId
        })
