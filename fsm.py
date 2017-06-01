from transitions.extensions import GraphMachine
import datetime

class TocMachine(GraphMachine):
    portion = 0
    price = 0
    people = 0
    initial = False
    today = datetime.date.today()
    

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )
    
    def select_order(self, update):
        text = update.message.text
        return text.lower() == 'order'

    def on_enter_orderS(self, update):
        update.message.reply_text("A餐:100元\nB餐:120元\nC餐:150元\n請問想選擇哪一種餐點?")

    def select_book(self, update):
        text = update.message.text
        return text.lower() == 'book'

    def on_enter_bookS(self, update):
        update.message.reply_text("起問想訂幾人位?")

    def select_recommend(self, update):
        text = update.message.text
        return text.lower() == 'recommend'

    def on_enter_recommendS(self, update):
        TocMachine.today = datetime.date.today()
        if TocMachine.today.day % 3 == 0:
            update.message.reply_text("今日推薦A餐")
        if TocMachine.today.day % 3 == 1:
            update.message.reply_text("今日推薦B餐")
        if TocMachine.today.day % 3 == 2:
            update.message.reply_text("今日推薦C餐")
        self.go_back(update)

    def select_A(self, update):
        text = update.message.text
        TocMachine.price=100
        return text.lower() == 'a'

    def select_B(self, update):
        text = update.message.text
        TocMachine.price=120
        return text.lower() == 'b'

    def select_C(self, update):
        text = update.message.text
        TocMachine.price=150
        return text.lower() == 'c'

    def on_enter_OAS(self, update):
        update.message.reply_photo("http://ext.pimg.tw/nixojov/1468201784-201305714_n.jpg?v=1468202151")
        update.message.reply_text("起問想訂幾份A餐?")

    def on_enter_OBS(self, update):
        update.message.reply_photo("http://0426310836.tw.tranews.com/Show/images/News/3290907_1.jpg")
        update.message.reply_text("起問想訂幾份B餐?")

    def on_enter_OCS(self, update):
        update.message.reply_photo("http://tw1001k.tw.tranews.com/images/Link/TW1001K000001_4_3.jpg")
        update.message.reply_text("起問想訂幾份C餐?")

    def select_check(self, update):
        text = update.message.text
        if text.isdigit():
            TocMachine.portion=int(text)
        return text.isdigit()

    def on_enter_OcheckS(self, update):
        update.message.reply_text("總價{0}元".format(TocMachine.price * TocMachine.portion))
        self.go_back(update)

    def on_enter_severType(self, update):
        if TocMachine.initial == True:
            update.message.reply_text("請問還需要什麼服務嗎?\n我們有提供:\nOrder(點餐)\nBook(訂位)\nRecommend(推薦)\n三種服務")
        TocMachine.initial=True

    def select_bookcheck(self, update):
        text = update.message.text
        if text.isdigit():
            if int(text)<=4:
                TocMachine.people=int(text)
                return True
        return False

    def select_bookcheck2(self, update):
        text = update.message.text
        if text.isdigit():
            if int(text)>4:
                return True
        return False

    def on_enter_BcheckS(self, update):
        update.message.reply_text("訂位成功\n共{0}人訂位".format(TocMachine.people))
        self.go_back(update)

    def on_enter_BrefuseS(self, update):
        update.message.reply_text("網路訂位最多4人\n訂位失敗")
        self.go_back(update)

    def on_enter_Start(self, update):
        update.message.reply_text("我是餐廳服務系統Chatbot\n我們有提供:\nOrder(點餐)\nBook(訂位)\nRecommend(推薦)\n三種服務\n請問你想選哪一種呢?")
        self.go_back(update)

    def start_chat(self, update):
        text = update.message.text
        return text == "/start"
