import datetime, time, jwt

from studyDJ.settings import SECRET_KEY
from user.models import user


class MyAuth():
    # 签发token
    @staticmethod
    def encode_auth_token(user_tel_eamil, login_time):
        """
        生成认证Token
        :param user_tel_eamil:  telephone or email
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                # 过期时间 1个小时
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=3, seconds=0),
                # 发行时间
                'iat': datetime.datetime.utcnow(),
                # token签发者
                'iss': 'study',
                'data': {
                    'tel_email': user_tel_eamil,
                    'login_time': login_time
                }
            }
            return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        except Exception as e:
            return e

    # 验证token
    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        res = None
        payload = None
        try:
            # 取消过期时间验证  将True改为False
            payload = jwt.decode(auth_token, SECRET_KEY, options={'verify_exp': True})
            if ('data' in payload and 'tel_email' in payload['data']):
                res = 'Token验证通过'
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            res = 'Token过期'
        except jwt.InvalidTokenError:
            res = '无效Token'
        finally:
            return {"res": res, "payload": payload}

    # 用户登录
    def authenticate(self, tel_email, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param password:
        :return: json
        """
        token = None
        res = {}
        if str(tel_email).find('@') != -1:
            # 邮箱登录
            uu = user.objects.filter(email=tel_email).first()
        else:
            # 电话号码登录
            uu = user.objects.filter(telephone=tel_email).first()
        if uu:
            if uu.password == password:
                login_time = int(time.time())
                res['token'] = self.encode_auth_token(tel_email, login_time).decode()
                res['res'] = '登录成功'
            else:
                res['res'] = '用户名或密码错误'
        else:
            res['res'] = '该用户未注册'
        return res

    # 用户鉴权
    def identify(self, token):
        """
        用户鉴权
        :return: list
        """
        payload = None
        if (token):
            payload = self.decode_auth_token(token)
        return payload
