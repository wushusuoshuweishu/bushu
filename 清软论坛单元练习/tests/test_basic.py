import unittest

from app.checkers.user import register_params_check


class BasicTestCase(unittest.TestCase):
    '''
    TODO: 在这里补充注册相关测试用例
    '''
    def test_register_params_check(self):
        self.assertEqual(('username', False), register_params_check(None))

        content = {'username': 'djk2'}                                      # 测试username
        self.assertEqual(('username', False), register_params_check(content))
        content['username'] = 'djkdjk'
        self.assertEqual(('username', False), register_params_check(content))

        content = {'username': 'djk20', 'password': 'ufe'}                  # 测试password
        self.assertEqual(('password', False), register_params_check(content))
        content['password'] = 'djnwijeij~~'
        self.assertEqual(('password', False), register_params_check(content))

        content['password'] = 'djdjj*^-_'                                   # 测试nickname
        self.assertEqual(('nickname', False), register_params_check(content))

        content['nickname'] = 'dd'                                          # 测试url
        self.assertEqual(('url', False), register_params_check(content))
        content['url'] = "hyyp://wo.zi.ji.bian.de"
        self.assertEqual(('url', False), register_params_check(content))
        content['url'] = "https://w.o.z.i.j.i.b.i.a.n.l.e.y.i.g.e.h.e.n.c.h.a.n.g.d.e.y.u.m.i.n.g"
        self.assertEqual(('url', False), register_params_check(content))
        content['url'] = "http://wozijibiande"
        self.assertEqual(('url', False), register_params_check(content))
        content['url'] = "https://wozijibiande.123"
        self.assertEqual(('url', False), register_params_check(content))
        content['url'] = "https://;.;"
        self.assertEqual(('url', False), register_params_check(content))
        content['url'] = "https://123.-com"
        self.assertEqual(('url', False), register_params_check(content))
        content['url'] = 'https:/www.baidu.com'
        self.assertEqual(('url', False), register_params_check(content))

        content['url'] = 'https://wushusuoshuweishu.github.io'              # 测试mobile
        self.assertEqual(('mobile', False), register_params_check(content))
        content['mobile'] = '+867323286862386625658265368532'
        self.assertEqual(('mobile', False), register_params_check(content))

        content['mobile'] = '+86.137675480410'                               # 测试magic_number
        self.assertEqual(('ok', True), register_params_check(content))
        content['magic_number'] = -1
        self.assertEqual(('magic_number', False), register_params_check(content))
        content['magic_number'] = 1.6
        self.assertEqual(('magic_number', False), register_params_check(content))

        content['magic_number'] = 0
        self.assertEqual(('ok', True), register_params_check(content))      # 测试成功案例


if __name__ == '__main__':
    unittest.main()
