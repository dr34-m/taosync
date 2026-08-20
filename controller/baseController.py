import json
import logging

from tornado.web import RequestHandler

from common import commonService
from common.LNG import G, set_context_lang
from common.config import getConfig
from service.system import userService

cookieName = 'tao_sync'


class BaseHandler(RequestHandler):
    def _get_signed_user_cookie(self):
        # 登录时和校验时必须使用同一个有效期，否则浏览器仍保留 Cookie 时，
        # 服务端会回退到 Tornado 默认的 31 天有效期。
        return self.get_signed_cookie(
            cookieName,
            max_age_days=getConfig()['server']['expires']
        )

    def get_current_user(self):
        return json.loads(self._get_signed_user_cookie())


def handle_request(func):
    def wrapper(self):
        uri = self.request.uri
        lang = self.request.headers.get("Accept-Language", None)
        set_context_lang(lang)
        user = self._get_signed_user_cookie()
        trueUser = None
        if not uri.startswith('/svr/noAuth'):
            if user is None:
                self.clear_cookie(cookieName)
                msg = commonService.result_map(G('sign_in'), 401)
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(msg)
                return
            else:
                cUser = json.loads(user)
                trueUser = userService.getUser(cUser['id'], None)
                if ('passwd' not in cUser
                        or 'userName' not in cUser
                        or trueUser['passwd'] != cUser['passwd']
                        or trueUser['userName'] != cUser['userName']):
                    msg = commonService.result_map(G('login_expired'), 401)
                    self.clear_cookie(cookieName)
                    self.set_header('Content-Type', 'application/json; charset=UTF-8')
                    self.write(msg)
                    return
        try:
            req = commonService.get_post_data(self)
            req['__lang'] = set_context_lang(lang)
            if trueUser:
                req['__user'] = trueUser.copy()
                del req['__user']['passwd']
                del req['__user']['sqlVersion']
            msg = commonService.result_map(func(self, req))
        except Exception as e:
            msg = commonService.result_map(str(e), 500)
            logger = logging.getLogger()
            logger.exception(e)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(msg)

    return wrapper
