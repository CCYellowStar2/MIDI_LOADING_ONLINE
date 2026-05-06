import logging
from datetime import datetime

class AppLogger:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(f"log_{datetime.now().strftime('%Y%m%d')}.txt"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("AIPiano")

    def info(self, msg): self.logger.info(msg)
    def error(self, msg): self.logger.error(msg)
    def warning(self, msg): self.logger.warning(msg)



# 程序出Bug了？
# 　　　∩∩
# 　　（´･ω･）
# 　 ＿|　⊃／(＿＿_
# 　／ └-(＿＿＿／
# 　￣￣￣￣￣￣￣
# 算了反正不是我写的
# 　　 ⊂⌒／ヽ-、＿
# 　／⊂_/＿＿＿＿ ／
# 　￣￣￣￣￣￣￣
# 万一是我写的呢
# 　　　∩∩
# 　　（´･ω･）
# 　 ＿|　⊃／(＿＿_
# 　／ └-(＿＿＿／
# 　￣￣￣￣￣￣￣
# 算了反正改了一个又出三个
# 　　 ⊂⌒／ヽ-、＿
# 　／⊂_/＿＿＿＿ ／
# 　￣￣￣￣￣￣￣


#
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |# '.
#                 / \\|||  :  |||# \
#                / _||||| -:- |||||- \
#               |   | \\\  -  #/ |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#               佛祖保佑         永无BUG
#
#
#