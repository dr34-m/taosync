import json

from common.LNG import language
from common.config import getConfig
from controller.baseController import BaseHandler, handle_request, cookieName
from service.system import userService


class Login(BaseHandler):
    @handle_request
    def post(self, req):
        cfg = getConfig()
        user = userService.checkPwd(None, req['passwd'], req['userName'])
        self.set_signed_cookie(cookieName, json.dumps(user),
                               expires_days=cfg['server']['expires'])
        userReturn = user.copy()
        del userReturn['passwd']
        del userReturn['sqlVersion']
        return userReturn

    @handle_request
    def put(self, req):
        return userService.resetPasswd(req['userName'], req['key'], req.get('passwd', None))

    @handle_request
    def delete(self, req):
        self.clear_cookie(cookieName)


class User(BaseHandler):
    @handle_request
    def get(self, req):
        user = req['__user']
        return user

    @handle_request
    def put(self, req):
        user = json.loads(self._get_signed_user_cookie())
        userService.editPasswd(user['id'], req['passwd'], req['oldPasswd'])


class Language(BaseHandler):
    @handle_request
    def get(self, req):
        return language()

    @handle_request
    def post(self, req):
        language(req['language'])
        return language()
