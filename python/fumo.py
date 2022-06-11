_FUMO_NAME_DICT = { 
                    '霊夢': 'Reimu', 'れいむ': 'Reimu', '魔理沙': 'Marisa', 'まりさ': 'Marisa', '蓮子': 'Renko', 'れんこ': 'Renko',
                    '神子': 'Toyosatomimi', 'みこ': 'Toyosatomimi', 'さとり': 'Satori', 'こいし': 'Koishi',
                    '早苗': 'Sanae', 'さなえ': 'Sanae', 'フランドール': 'Flandre', 'レミリア': 'Remilia', 'ふらん': 'Flandre', 'れみりあ': 'Remilia',
                    '咲夜': 'Sakuya', 'さくや': 'Sakuya', '鈴仙': 'Reisen', 'うどんげ': 'Reisen', '華扇': 'Kasen', 'かせん': 'Kasen',
                    '橙': 'Chen', 'ちぇん': 'Chen', '八雲藍': 'Ran', 'らん': 'Ran', '八雲紫': 'Yukari', 'ゆかり': 'Yukari',
                    'チルノ': 'Cirno', 'ちるの': 'Cirno', '幽香': 'Yuuka', 'ゆうか': 'Yuuka', '永琳': 'Eirin', 'えいりん': 'Eirin',
                    'ルーミア': 'Rumia', 'るーみあ': 'Rumia', '映姫': 'Eiki', 'えいき': 'Eiki', 'にとり': 'Nitori',
                    '女苑': 'Joon', 'じょおん': 'Joon', '輝夜': 'Kaguya', 'かぐや': 'Kaguya', '妹紅': 'Mokou', 'ふももこ': 'Mokou',     # Fumo moko cause just moko intercepts with fumo kokoro
                    'てゐ': 'Tewi', 'こころ': 'Kokoro', '射命丸': 'Aya', 'あや': 'Aya',
                    'はたて': 'Hatate', 'マーガトロイド': 'Alice', 'ありす': 'Alice', 'パチュリー': 'Patchouli', 'ぱちぇ': 'Patchouli', 'ぱちゅり': 'Patchouli',
                    '妖夢': 'Youmu', 'ようむ': 'Youmu', '幽々子': 'Yuyuko', 'ゆゆこ': 'Yuyuko', '比那名居': 'Tenshi', 'てんし': 'Tenshi',
                    '紫苑': 'Shion', 'しおん': 'Shion', '犬走椛': 'Momiji', 'もみじ。': 'Momiji', '紅美鈴': 'Meiling', 'めいりん': 'Meiling',
                    '諏訪子': 'Suwako', 'すわこ': 'Suwako'}


class FumoItem:
    @staticmethod
    def _getFumoType(title):
        for name in _FUMO_NAME_DICT:
            if name in title:
                return _FUMO_NAME_DICT[name]

        return "Other"

    
    def __init__(self, title, price, buyLink, imgLink):
        self.title = title
        self.price = price
        self.buyLink = buyLink
        self.imgLink = imgLink
        self.fumoType = self._getFumoType(title)


class FumoAuctionItem(FumoItem):
    def __init__(self, title, curPrice, buyoutPrice, buyLink, imgLink):
        super().__init__(title, curPrice, buyLink, imgLink)
        self.curPrice = curPrice
        self.buyoutPrice = buyoutPrice

    def __str__(self):
        s = ''
        s += 'Title: ' + self.title
        s += '\nFumo Type: ' + self.fumoType
        s += '\nCurrent Price: ' + str(self.curPrice)

        if self.buyoutPrice != 0:
            s += '\nBuyout Price: ' + str(self.buyoutPrice)
        
        s += '\nLink: ' + self.buyLink
        s += '\nThumbnail Link: ' + self.imgLink
        s += '\n'

        return s
