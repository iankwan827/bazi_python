import datetime
from lunar_python import Solar, Lunar

# Constants
GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

GAN_WX = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}
ZHI_WX = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
    '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

HIDDEN_STEMS_MAP = {
    '子': ['癸'],
    '丑': ['己', '癸', '辛'],
    '寅': ['甲', '丙', '戊'],
    '卯': ['乙'],
    '辰': ['戊', '乙', '癸'],
    '巳': ['丙', '庚', '戊'],
    '午': ['丁', '己'],
    '未': ['己', '丁', '乙'],
    '申': ['庚', '壬', '戊'],
    '酉': ['辛'],
    '戌': ['戊', '辛', '丁'],
    '亥': ['壬', '甲']
}

NAYIN = {
    '甲子': '海中金', '乙丑': '海中金', '丙寅': '炉中火', '丁卯': '炉中火',
    '戊辰': '大林木', '己巳': '大林木', '庚午': '路旁土', '辛未': '路旁土',
    '壬申': '剑锋金', '癸酉': '剑锋金', '甲戌': '山头火', '乙亥': '山头火',
    '丙子': '涧下水', '丁丑': '涧下水', '戊寅': '城头土', '己卯': '城头土',
    '庚辰': '白蜡金', '辛巳': '白蜡金', '壬午': '杨柳木', '癸未': '杨柳木',
    '甲申': '泉中水', '乙酉': '泉中水', '丙戌': '屋上土', '丁亥': '屋上土',
    '戊子': '霹雳火', '己丑': '霹雳火', '庚寅': '松柏木', '辛卯': '松柏木',
    '壬辰': '长流水', '癸巳': '长流水', '甲午': '砂中金', '乙未': '砂中金',
    '丙申': '山下火', '丁酉': '山下火', '戊戌': '平地木', '己亥': '平地木',
    '庚子': '壁上土', '辛丑': '壁上土', '壬寅': '金箔金', '癸卯': '金箔金',
    '甲辰': '覆灯火', '乙巳': '覆灯火', '丙午': '天河水', '丁未': '天河水',
    '戊申': '大驿土', '己酉': '大驿土', '庚戌': '钗钏金', '辛亥': '钗钏金',
    '壬子': '桑柘木', '癸丑': '桑柘木', '甲寅': '大溪水', '乙卯': '大溪水',
    '丙辰': '沙中土', '丁巳': '沙中土', '戊午': '天上火', '己未': '天上火',
    '庚申': '石榴木', '辛酉': '石榴木', '壬戌': '大海水', '癸亥': '大海水'
}

TEN_GODS = {
    # Keys: DayMaster + TargetStem -> [LongName, ShortName]
    '甲甲': ['比肩', '比'], '甲乙': ['劫财', '劫'], '甲丙': ['食神', '食'], '甲丁': ['伤官', '伤'],
    '甲戊': ['偏财', '才'], '甲己': ['正财', '财'], '甲庚': ['七杀', '杀'], '甲辛': ['正官', '官'],
    '甲壬': ['偏印', '枭'], '甲癸': ['正印', '印'],

    '乙甲': ['劫财', '劫'], '乙乙': ['比肩', '比'], '乙丙': ['伤官', '伤'], '乙丁': ['食神', '食'],
    '乙戊': ['正财', '财'], '乙己': ['偏财', '才'], '乙庚': ['正官', '官'], '乙辛': ['七杀', '杀'],
    '乙壬': ['正印', '印'], '乙癸': ['偏印', '枭'],

    '丙甲': ['偏印', '枭'], '丙乙': ['正印', '印'], '丙丙': ['比肩', '比'], '丙丁': ['劫财', '劫'],
    '丙戊': ['食神', '食'], '丙己': ['伤官', '伤'], '丙庚': ['偏财', '才'], '丙辛': ['正财', '财'],
    '丙壬': ['七杀', '杀'], '丙癸': ['正官', '官'],

    '丁甲': ['正印', '印'], '丁乙': ['偏印', '枭'], '丁丙': ['劫财', '劫'], '丁丁': ['比肩', '比'],
    '丁戊': ['伤官', '伤'], '丁己': ['食神', '食'], '丁庚': ['正财', '财'], '丁辛': ['偏财', '才'],
    '丁壬': ['正官', '官'], '丁癸': ['七杀', '杀'],

    '戊甲': ['七杀', '杀'], '戊乙': ['正官', '官'], '戊丙': ['偏印', '枭'], '戊丁': ['正印', '印'],
    '戊戊': ['比肩', '比'], '戊己': ['劫财', '劫'], '戊庚': ['食神', '食'], '戊辛': ['伤官', '伤'],
    '戊壬': ['偏财', '才'], '戊癸': ['正财', '财'],

    '己甲': ['正官', '官'], '己乙': ['七杀', '杀'], '己丙': ['正印', '印'], '己丁': ['偏印', '枭'],
    '己戊': ['劫财', '劫'], '己己': ['比肩', '比'], '己庚': ['伤官', '伤'], '己辛': ['食神', '食'],
    '己壬': ['正财', '财'], '己癸': ['偏财', '才'],

    '庚甲': ['偏财', '才'], '庚乙': ['正财', '财'], '庚丙': ['七杀', '杀'], '庚丁': ['正官', '官'],
    '庚戊': ['偏印', '枭'], '庚己': ['正印', '印'], '庚庚': ['比肩', '比'], '庚辛': ['劫财', '劫'],
    '庚壬': ['食神', '食'], '庚癸': ['伤官', '伤'],

    '辛甲': ['正财', '财'], '辛乙': ['偏财', '才'], '辛丙': ['正官', '官'], '辛丁': ['七杀', '杀'],
    '辛戊': ['正印', '印'], '辛己': ['偏印', '枭'], '辛庚': ['劫财', '劫'], '辛辛': ['比肩', '比'],
    '辛壬': ['伤官', '伤'], '辛癸': ['食神', '食'],

    '壬甲': ['食神', '食'], '壬乙': ['伤官', '伤'], '壬丙': ['偏财', '才'], '壬丁': ['正财', '财'],
    '壬戊': ['七杀', '杀'], '壬己': ['正官', '官'], '壬庚': ['偏印', '枭'], '壬辛': ['正印', '印'],
    '壬壬': ['比肩', '比'], '壬癸': ['劫财', '劫'],

    '癸甲': ['伤官', '伤'], '癸乙': ['食神', '食'], '癸丙': ['正财', '财'], '癸丁': ['偏财', '才'],
    '癸戊': ['正官', '官'], '癸己': ['七杀', '杀'], '癸庚': ['正印', '印'], '癸辛': ['偏印', '枭'],
    '癸壬': ['劫财', '劫'], '癸癸': ['比肩', '比']
}

SHEN_SHA_RULES = {
    # 1. 贵人系列 (Noble Stars)
    '天乙贵人': lambda info: 
        (info['yearGan'] in ['甲', '戊', '庚'] and info['zhi'] in ['丑', '未']) or
        (info['dayGan'] in ['甲', '戊', '庚'] and info['zhi'] in ['丑', '未']) or
        (info['yearGan'] in ['乙', '己'] and info['zhi'] in ['子', '申']) or
        (info['dayGan'] in ['乙', '己'] and info['zhi'] in ['子', '申']) or
        (info['yearGan'] in ['丙', '丁'] and info['zhi'] in ['亥', '酉']) or
        (info['dayGan'] in ['丙', '丁'] and info['zhi'] in ['亥', '酉']) or
        (info['yearGan'] in ['壬', '癸'] and info['zhi'] in ['卯', '巳']) or
        (info['dayGan'] in ['壬', '癸'] and info['zhi'] in ['卯', '巳']) or
        (info['yearGan'] == '辛' and info['zhi'] in ['寅', '午']) or
        (info['dayGan'] == '辛' and info['zhi'] in ['寅', '午']),
    
    '天德贵人': lambda info:
        (info['monthZhi'] == '寅' and info['stem'] == '丁') or
        (info['monthZhi'] == '卯' and info['zhi'] == '申') or
        (info['monthZhi'] == '辰' and info['stem'] == '壬') or
        (info['monthZhi'] == '巳' and info['stem'] == '辛') or
        (info['monthZhi'] == '午' and info['zhi'] == '亥') or
        (info['monthZhi'] == '未' and info['stem'] == '甲') or
        (info['monthZhi'] == '申' and info['stem'] == '癸') or
        (info['monthZhi'] == '酉' and info['zhi'] == '寅') or
        (info['monthZhi'] == '戌' and info['stem'] == '丙') or
        (info['monthZhi'] == '亥' and info['stem'] == '乙') or
        (info['monthZhi'] == '子' and info['zhi'] == '巳') or
        (info['monthZhi'] == '丑' and info['stem'] == '庚'),

    '月德贵人': lambda info:
        (info['monthZhi'] in ['寅', '午', '戌'] and info['stem'] == '丙') or
        (info['monthZhi'] in ['申', '子', '辰'] and info['stem'] == '壬') or
        (info['monthZhi'] in ['亥', '卯', '未'] and info['stem'] == '甲') or
        (info['monthZhi'] in ['巳', '酉', '丑'] and info['stem'] == '庚'),

    '福德贵人': lambda info:
        (info['dayGan'] in ['甲', '乙'] and info['zhi'] in ['巳', '午']) or
        (info['dayGan'] in ['丙', '戊'] and info['zhi'] == '申') or
        (info['dayGan'] in ['丁', '己'] and info['zhi'] in ['亥', '酉']) or
        (info['dayGan'] in ['庚', '辛'] and info['zhi'] == '寅') or
        (info['dayGan'] in ['壬', '癸'] and info['zhi'] == '卯'),

    # 2. 学业智慧 (Academic)
    '文昌贵人': lambda info:
        (info['dayGan'] == '甲' and info['zhi'] == '巳') or
        (info['dayGan'] == '乙' and info['zhi'] == '午') or
        (info['dayGan'] in ['丙', '戊'] and info['zhi'] == '申') or
        (info['dayGan'] in ['丁', '己'] and info['zhi'] == '酉') or
        (info['dayGan'] == '庚' and info['zhi'] == '亥') or
        (info['dayGan'] == '辛' and info['zhi'] == '子') or
        (info['dayGan'] == '壬' and info['zhi'] == '寅') or
        (info['dayGan'] == '癸' and info['zhi'] == '卯') or # JS: Gui sees Mao
        (info['yearGan'] == '甲' and info['zhi'] == '巳') or
        (info['yearGan'] == '乙' and info['zhi'] == '午') or
        (info['yearGan'] in ['丙', '戊'] and info['zhi'] == '申') or
        (info['yearGan'] in ['丁', '己'] and info['zhi'] == '酉') or
        (info['yearGan'] == '庚' and info['zhi'] == '亥') or
        (info['yearGan'] == '辛' and info['zhi'] == '子') or
        (info['yearGan'] == '壬' and info['zhi'] == '寅') or
        (info['yearGan'] == '癸' and info['zhi'] == '卯'),

    '学堂': lambda info:
        (info['yearNaYin'] and '金' in info['yearNaYin'] and info['zhi'] == '巳') or
        (info['yearNaYin'] and '木' in info['yearNaYin'] and info['zhi'] == '亥') or
        (info['yearNaYin'] and '水' in info['yearNaYin'] and info['zhi'] == '申') or
        (info['yearNaYin'] and '火' in info['yearNaYin'] and info['zhi'] == '寅') or
        (info['yearNaYin'] and '土' in info['yearNaYin'] and info['zhi'] == '申'),

    '词馆': lambda info:
        (info['yearNaYin'] and '金' in info['yearNaYin'] and info['zhi'] == '申') or
        (info['yearNaYin'] and '木' in info['yearNaYin'] and info['zhi'] == '寅') or
        (info['yearNaYin'] and '水' in info['yearNaYin'] and info['zhi'] == '亥') or
        (info['yearNaYin'] and '火' in info['yearNaYin'] and info['zhi'] == '巳') or
        (info['yearNaYin'] and '土' in info['yearNaYin'] and info['zhi'] == '寅'),

    # 3. 财运事业
    '禄神': lambda info:
        (info['dayGan'] == '甲' and info['zhi'] == '寅') or
        (info['dayGan'] == '乙' and info['zhi'] == '卯') or
        (info['dayGan'] in ['丙', '戊'] and info['zhi'] == '巳') or
        (info['dayGan'] in ['丁', '己'] and info['zhi'] == '午') or
        (info['dayGan'] == '庚' and info['zhi'] == '申') or
        (info['dayGan'] == '辛' and info['zhi'] == '酉') or
        (info['dayGan'] == '壬' and info['zhi'] == '亥') or
        (info['dayGan'] == '癸' and info['zhi'] == '子') or
        # Check YearGan too per JS
        (info['yearGan'] == '甲' and info['zhi'] == '寅') or
        (info['yearGan'] == '乙' and info['zhi'] == '卯') or
        (info['yearGan'] in ['丙', '戊'] and info['zhi'] == '巳') or
        (info['yearGan'] in ['丁', '己'] and info['zhi'] == '午') or
        (info['yearGan'] == '庚' and info['zhi'] == '申') or
        (info['yearGan'] == '辛' and info['zhi'] == '酉') or
        (info['yearGan'] == '壬' and info['zhi'] == '亥') or
        (info['yearGan'] == '癸' and info['zhi'] == '子'),

    '金舆': lambda info:
        (info['dayGan'] == '甲' and info['zhi'] == '辰') or
        (info['dayGan'] == '乙' and info['zhi'] == '巳') or
        (info['dayGan'] in ['丙', '戊'] and info['zhi'] == '未') or
        (info['dayGan'] in ['丁', '己'] and info['zhi'] == '申') or
        (info['dayGan'] == '庚' and info['zhi'] == '戌') or
        (info['dayGan'] == '辛' and info['zhi'] == '亥') or
        (info['dayGan'] == '壬' and info['zhi'] == '丑') or
        (info['dayGan'] == '癸' and info['zhi'] == '寅') or
        # Check YearGan too
        (info['yearGan'] == '甲' and info['zhi'] == '辰') or
        (info['yearGan'] == '乙' and info['zhi'] == '巳') or
        (info['yearGan'] in ['丙', '戊'] and info['zhi'] == '未') or
        (info['yearGan'] in ['丁', '己'] and info['zhi'] == '申') or
        (info['yearGan'] == '庚' and info['zhi'] == '戌') or
        (info['yearGan'] == '辛' and info['zhi'] == '亥') or
        (info['yearGan'] == '壬' and info['zhi'] == '丑') or
        (info['yearGan'] == '癸' and info['zhi'] == '寅'),

    '驿马': lambda info:
        (info['yearZhi'] in ['申', '子', '辰'] and info['zhi'] == '寅') or
        (info['dayZhi'] in ['申', '子', '辰'] and info['zhi'] == '寅') or
        (info['yearZhi'] in ['寅', '午', '戌'] and info['zhi'] == '申') or
        (info['dayZhi'] in ['寅', '午', '戌'] and info['zhi'] == '申') or
        (info['yearZhi'] in ['亥', '卯', '未'] and info['zhi'] == '巳') or
        (info['dayZhi'] in ['亥', '卯', '未'] and info['zhi'] == '巳') or
        (info['yearZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '亥') or
        (info['dayZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '亥'),

    '将星': lambda info:
        (info['yearZhi'] in ['寅', '午', '戌'] and info['zhi'] == '午') or
        (info['dayZhi'] in ['寅', '午', '戌'] and info['zhi'] == '午') or
        (info['yearZhi'] in ['申', '子', '辰'] and info['zhi'] == '子') or
        (info['dayZhi'] in ['申', '子', '辰'] and info['zhi'] == '子') or
        (info['yearZhi'] in ['亥', '卯', '未'] and info['zhi'] == '卯') or
        (info['dayZhi'] in ['亥', '卯', '未'] and info['zhi'] == '卯') or
        (info['yearZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '酉') or
        (info['dayZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '酉'),

    # 4. 健康婚姻
    '天医': lambda info:
        (info['monthZhi'] == '寅' and info['zhi'] == '丑') or
        (info['monthZhi'] == '卯' and info['zhi'] == '寅') or
        (info['monthZhi'] == '辰' and info['zhi'] == '卯') or
        (info['monthZhi'] == '巳' and info['zhi'] == '辰') or
        (info['monthZhi'] == '午' and info['zhi'] == '巳') or
        (info['monthZhi'] == '未' and info['zhi'] == '午') or
        (info['monthZhi'] == '申' and info['zhi'] == '未') or
        (info['monthZhi'] == '酉' and info['zhi'] == '申') or
        (info['monthZhi'] == '戌' and info['zhi'] == '酉') or
        (info['monthZhi'] == '亥' and info['zhi'] == '戌') or
        (info['monthZhi'] == '子' and info['zhi'] == '亥') or
        (info['monthZhi'] == '丑' and info['zhi'] == '子'),

    '天喜': lambda info:
        (info['yearZhi'] in ['寅', '午', '戌'] and info['zhi'] == '卯') or
        (info['yearZhi'] in ['申', '子', '辰'] and info['zhi'] == '酉') or
        (info['yearZhi'] in ['亥', '卯', '未'] and info['zhi'] == '子') or
        (info['yearZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '午'),

    '红鸾': lambda info: # Matched to JS step 240 extraction
        (info['yearZhi'] in ['寅', '午', '戌'] and info['zhi'] == '子') or
        (info['yearZhi'] in ['申', '子', '辰'] and info['zhi'] == '卯') or
        (info['yearZhi'] in ['亥', '卯', '未'] and info['zhi'] == '酉') or
        (info['yearZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '午'),

    # 5. 凶煞
    '羊刃': lambda info:
        (info['dayGan'] == '甲' and info['zhi'] == '卯') or
        (info['dayGan'] == '乙' and info['zhi'] == '寅') or 
        (info['dayGan'] == '丙' and info['zhi'] == '午') or
        (info['dayGan'] == '丁' and info['zhi'] == '巳') or
        (info['dayGan'] == '戊' and info['zhi'] == '午') or
        (info['dayGan'] == '己' and info['zhi'] == '巳') or
        (info['dayGan'] == '庚' and info['zhi'] == '酉') or
        (info['dayGan'] == '辛' and info['zhi'] == '申') or
        (info['dayGan'] == '壬' and info['zhi'] == '子') or
        (info['dayGan'] == '癸' and info['zhi'] == '亥') or
        # Check YearGan too per JS
        (info['yearGan'] == '甲' and info['zhi'] == '卯') or
        (info['yearGan'] == '乙' and info['zhi'] == '寅') or 
        (info['yearGan'] == '丙' and info['zhi'] == '午') or
        (info['yearGan'] == '丁' and info['zhi'] == '巳') or
        (info['yearGan'] == '戊' and info['zhi'] == '午') or
        (info['yearGan'] == '己' and info['zhi'] == '巳') or
        (info['yearGan'] == '庚' and info['zhi'] == '酉') or
        (info['yearGan'] == '辛' and info['zhi'] == '申') or
        (info['yearGan'] == '壬' and info['zhi'] == '子') or
        (info['yearGan'] == '癸' and info['zhi'] == '亥'),

    '劫煞': lambda info:
        (info['yearZhi'] in ['申', '子', '辰'] and info['zhi'] == '巳') or
        (info['dayZhi'] in ['申', '子', '辰'] and info['zhi'] == '巳') or
        (info['yearZhi'] in ['寅', '午', '戌'] and info['zhi'] == '亥') or
        (info['dayZhi'] in ['寅', '午', '戌'] and info['zhi'] == '亥') or
        (info['yearZhi'] in ['亥', '卯', '未'] and info['zhi'] == '申') or
        (info['dayZhi'] in ['亥', '卯', '未'] and info['zhi'] == '申') or
        (info['yearZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '寅') or
        (info['dayZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '寅'),

    '灾煞': lambda info:
        (info['yearZhi'] in ['申', '子', '辰'] and info['zhi'] == '午') or
        (info['dayZhi'] in ['申', '子', '辰'] and info['zhi'] == '午') or
        (info['yearZhi'] in ['寅', '午', '戌'] and info['zhi'] == '子') or
        (info['dayZhi'] in ['寅', '午', '戌'] and info['zhi'] == '子') or
        (info['yearZhi'] in ['亥', '卯', '未'] and info['zhi'] == '酉') or
        (info['dayZhi'] in ['亥', '卯', '未'] and info['zhi'] == '酉') or
        (info['yearZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '卯') or
        (info['dayZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '卯'),

    '血刃': lambda info: # Same as Jiang Xing
        (info['yearZhi'] in ['寅', '午', '戌'] and info['zhi'] == '午') or
        (info['dayZhi'] in ['寅', '午', '戌'] and info['zhi'] == '午') or
        (info['yearZhi'] in ['申', '子', '辰'] and info['zhi'] == '子') or
        (info['dayZhi'] in ['申', '子', '辰'] and info['zhi'] == '子') or
        (info['yearZhi'] in ['亥', '卯', '未'] and info['zhi'] == '卯') or
        (info['dayZhi'] in ['亥', '卯', '未'] and info['zhi'] == '卯') or
        (info['yearZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '酉') or
        (info['dayZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '酉'),

    '咸池': lambda info:
        (info['yearZhi'] in ['申', '子', '辰'] and info['zhi'] == '酉') or
        (info['dayZhi'] in ['申', '子', '辰'] and info['zhi'] == '酉') or
        (info['yearZhi'] in ['寅', '午', '戌'] and info['zhi'] == '卯') or
        (info['dayZhi'] in ['寅', '午', '戌'] and info['zhi'] == '卯') or
        (info['yearZhi'] in ['亥', '卯', '未'] and info['zhi'] == '子') or
        (info['dayZhi'] in ['亥', '卯', '未'] and info['zhi'] == '子') or
        (info['yearZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '午') or
        (info['dayZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '午'),

    '华盖': lambda info:
        (info['yearZhi'] in ['寅', '午', '戌'] and info['zhi'] == '戌') or
        (info['dayZhi'] in ['寅', '午', '戌'] and info['zhi'] == '戌') or
        (info['yearZhi'] in ['申', '子', '辰'] and info['zhi'] == '辰') or
        (info['dayZhi'] in ['申', '子', '辰'] and info['zhi'] == '辰') or
        (info['yearZhi'] in ['亥', '卯', '未'] and info['zhi'] == '未') or
        (info['dayZhi'] in ['亥', '卯', '未'] and info['zhi'] == '未') or
        (info['yearZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '丑') or
        (info['dayZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '丑'),

    '孤辰': lambda info:
        (info['yearZhi'] in ['寅', '卯', '辰'] and info['zhi'] == '巳') or
        (info['yearZhi'] in ['巳', '午', '未'] and info['zhi'] == '申') or
        (info['yearZhi'] in ['申', '酉', '戌'] and info['zhi'] == '亥') or
        (info['yearZhi'] in ['亥', '子', '丑'] and info['zhi'] == '寅'),

    '寡宿': lambda info:
        (info['yearZhi'] in ['寅', '卯', '辰'] and info['zhi'] == '丑') or
        (info['yearZhi'] in ['巳', '午', '未'] and info['zhi'] == '辰') or
        (info['yearZhi'] in ['申', '酉', '戌'] and info['zhi'] == '未') or
        (info['yearZhi'] in ['亥', '子', '丑'] and info['zhi'] == '戌'),

    '亡神': lambda info:
        (info['yearZhi'] in ['申', '子', '辰'] and info['zhi'] == '亥') or
        (info['yearZhi'] in ['寅', '午', '戌'] and info['zhi'] == '巳') or
        (info['yearZhi'] in ['亥', '卯', '未'] and info['zhi'] == '寅') or
        (info['yearZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '申'),

    '勾绞煞': lambda info:
        (info['yearZhi'] in ['寅', '申'] and info['zhi'] in ['巳', '亥']) or
        (info['yearZhi'] in ['卯', '酉'] and info['zhi'] in ['子', '午']) or
        (info['yearZhi'] in ['辰', '戌'] and info['zhi'] in ['丑', '未']) or
        (info['yearZhi'] in ['巳', '亥'] and info['zhi'] in ['寅', '申']) or
        (info['dayZhi'] in ['寅', '申'] and info['zhi'] in ['巳', '亥']) or
        (info['dayZhi'] in ['卯', '酉'] and info['zhi'] in ['子', '午']) or
        (info['dayZhi'] in ['辰', '戌'] and info['zhi'] in ['丑', '未']) or
        (info['dayZhi'] in ['巳', '亥'] and info['zhi'] in ['寅', '申']),

    '披麻': lambda info:
        (info['yearZhi'] in ['寅', '午', '戌'] and info['zhi'] == '酉') or
        (info['yearZhi'] in ['申', '子', '辰'] and info['zhi'] == '卯') or
        (info['yearZhi'] in ['亥', '卯', '未'] and info['zhi'] == '子') or
        (info['yearZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '午'),

    '丧门': lambda info:
        (info['yearZhi'] in ['寅', '午', '戌'] and info['zhi'] == '辰') or
        (info['yearZhi'] in ['申', '子', '辰'] and info['zhi'] == '戌') or
        (info['yearZhi'] in ['亥', '卯', '未'] and info['zhi'] == '未') or
        (info['yearZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '丑'),

    '吊客': lambda info:
        (info['yearZhi'] in ['寅', '午', '戌'] and info['zhi'] == '丑') or
        (info['yearZhi'] in ['申', '子', '辰'] and info['zhi'] == '未') or
        (info['yearZhi'] in ['亥', '卯', '未'] and info['zhi'] == '戌') or
        (info['yearZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '辰'),
        
    '红艳煞': lambda info:
        (info['dayGan'] == '甲' and info['zhi'] == '午') or
        (info['dayGan'] == '乙' and info['zhi'] == '申') or
        (info['dayGan'] == '丙' and info['zhi'] == '寅') or
        (info['dayGan'] == '丁' and info['zhi'] == '未') or
        (info['dayGan'] == '戊' and info['zhi'] == '辰') or
        (info['dayGan'] == '己' and info['zhi'] == '辰') or
        (info['dayGan'] == '庚' and info['zhi'] == '戌') or
        (info['dayGan'] == '辛' and info['zhi'] == '酉') or
        (info['dayGan'] == '壬' and info['zhi'] == '子') or
        (info['dayGan'] == '癸' and info['zhi'] == '申') or
        # Check YearGan too per JS
        (info['yearGan'] == '甲' and info['zhi'] == '午') or
        (info['yearGan'] == '乙' and info['zhi'] == '申') or
        (info['yearGan'] == '丙' and info['zhi'] == '寅') or
        (info['yearGan'] == '丁' and info['zhi'] == '未') or
        (info['yearGan'] == '戊' and info['zhi'] == '辰') or
        (info['yearGan'] == '己' and info['zhi'] == '辰') or
        (info['yearGan'] == '庚' and info['zhi'] == '戌') or
        (info['yearGan'] == '辛' and info['zhi'] == '酉') or
        (info['yearGan'] == '壬' and info['zhi'] == '子') or
        (info['yearGan'] == '癸' and info['zhi'] == '申'),

    '八专日': lambda info:
        (info['stem'] == info['dayGan'] and info['zhi'] == info['dayZhi']) and (info['stem']+info['zhi'] in ['甲寅', '乙卯', '丁未', '戊戌', '己未', '庚申', '辛酉', '癸丑']),
        
    '九丑日': lambda info:
        (info['stem'] == info['dayGan'] and info['zhi'] == info['dayZhi']) and (info['stem']+info['zhi'] in ['壬子', '壬午', '戊子', '戊午', '己酉', '己卯', '乙酉', '辛卯', '丁酉']),
        
    '沐浴': lambda info:
        (info['dayGan'] == '甲' and info['zhi'] == '子') or
        (info['dayGan'] == '乙' and info['zhi'] == '巳') or
        (info['dayGan'] == '丙' and info['zhi'] == '卯') or
        (info['dayGan'] == '戊' and info['zhi'] == '卯') or
        (info['dayGan'] == '丁' and info['zhi'] == '申') or
        (info['dayGan'] == '己' and info['zhi'] == '申') or
        (info['dayGan'] == '庚' and info['zhi'] == '午') or
        (info['dayGan'] == '辛' and info['zhi'] == '亥') or
        (info['dayGan'] == '壬' and info['zhi'] == '酉') or
        (info['dayGan'] == '癸' and info['zhi'] == '寅'),
}


def get_color(char):
    if not char: return '#333'
    wx = GAN_WX.get(char) or ZHI_WX.get(char)
    if wx == '木': return '#27ae60'
    if wx == '火': return '#c0392b'
    if wx == '土': return '#a1887f' # Brown
    if wx == '金': return '#b8860b' # Swapped to GoldenRod
    if wx == '水': return '#2980b9'
    return '#333'

def get_ten_god(day_master, stem):
    if not stem: return ''
    key = day_master + stem
    val = TEN_GODS.get(key)
    return val[0] if val else ''

def get_kong_wang(stem, zhi):
    # Determine the Xun (10-day cycle)
    # 1. Get index of Stem and Zhi
    if stem not in GAN or zhi not in ZHI: return []
    idx_g = GAN.index(stem)
    idx_z = ZHI.index(zhi)
    
    # Xun Kong: (Index of Zhi - Index of Stem)
    # result mapped to pairs
    diff = (idx_z - idx_g) % 12
    # 0 -> Zi Chou (Jia Zi Xun) -> Kong: Xu Hai
    # 2 -> Yin Mao (Jia Yin Xun) -> Kong: Zi Chou
    # 4 -> Chen Si (Jia Chen Xun) -> Kong: Yin Mao
    # 6 -> Wu Wei (Jia Wu Xun) -> Kong: Chen Si
    # 8 -> Shen You (Jia Shen Xun) -> Kong: Wu Wei
    # 10 -> Xu Hai (Jia Xu Xun) -> Kong: Shen You
    
    mapping = {
        0: ['戌', '亥'],
        2: ['子', '丑'],
        4: ['寅', '卯'],
        6: ['辰', '巳'],
        8: ['午', '未'],
        10: ['申', '酉']
    }
    return mapping.get(diff, [])

def get_shen_sha(year_gan, year_zhi, month_zhi, day_gan, day_zhi, stem, zhi, year_nayin=None, day_nayin=None):
    res = []
    info = {
        'yearGan': year_gan, 'yearZhi': year_zhi, 'monthZhi': month_zhi, 
        'dayGan': day_gan, 'dayZhi': day_zhi, 'stem': stem, 'zhi': zhi,
        'yearNaYin': year_nayin, 'dayNaYin': day_nayin
    }
    
    for name, rule in SHEN_SHA_RULES.items():
        if rule(info):
            if name not in res:
                res.append(name)
    
    # Special: Yin Yang Cha Cuo (Day Pillar only)
    if day_gan == stem and day_zhi == zhi:
        gz = stem + zhi
        if gz in ['丙子', '丁丑', '戊寅', '辛卯', '壬辰', '癸巳', '丙午', '丁未', '戊申', '辛酉', '壬戌', '癸亥']:
            res.append('阴差阳错')

    # Special: Kui Gang (Day Pillar only) - strict check
    if day_gan == stem and day_zhi == zhi:
        gz = stem + zhi
        if gz in ['壬辰', '庚戌', '庚辰', '戊戌']:
            res.append('魁罡')
            
    # Special: Jin Shen (进神) - Check specific pillar match
    gz = stem + zhi
    if gz in ['甲子', '甲午', '己卯', '己酉', '戊寅', '戊申', '癸巳', '癸亥']:
        res.append('进神')
        
    # Special: Tui Shen (退神)
    if gz in ['甲戌', '甲辰', '乙丑', '乙未', '丙申', '丁酉', '丁亥', '丁丑']:
        res.append('退神')

    # Month Po / Year Po
    CHONG_MAP = {
        '子': '午', '丑': '未', '寅': '申', '卯': '酉', '辰': '戌', '巳': '亥',
        '午': '子', '未': '丑', '申': '寅', '酉': '卯', '戌': '辰', '亥': '巳'
    }
    if CHONG_MAP.get(month_zhi) == zhi:
        res.append('月破')
    if CHONG_MAP.get(year_zhi) == zhi:
        res.append('岁破')
        
    # Kong Wang (Emptiness) - Explicitly requested
    kw_day = get_kong_wang(day_gan, day_zhi)
    if zhi in kw_day:
        res.append('空亡')
    kw_year = get_kong_wang(year_gan, year_zhi)
    if zhi in kw_year:
        if '空亡' not in res: res.append('空亡')

    return res

def get_interactions(pillars):
    stems = [p['gan'] for p in pillars]
    branches = [p['zhi'] for p in pillars]
    
    res = {'stems': [], 'branches': []}
    
    # --- Heavenly Stems (Tian Gan) ---
    gan_he_map = {
        '甲': '己', '己': '甲',
        '乙': '庚', '庚': '乙',
        '丙': '辛', '辛': '丙',
        '丁': '壬', '壬': '丁',
        '戊': '癸', '癸': '戊'
    }
    gan_he_result = {
        '甲己': '合土', '乙庚': '合金', '丙辛': '合水', '丁壬': '合木', '戊癸': '合火'
    }
    
    gan_chong_pairs = [
        {'甲', '庚'}, {'乙', '辛'}, {'丙', '壬'}, {'丁', '癸'}
    ]
    
    # Pairwise Stems
    for i in range(len(stems)):
        for j in range(i + 1, len(stems)):
            s1 = stems[i]
            s2 = stems[j]
            
            # Sort for consistency
            gan_order = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
            idx1 = gan_order.index(s1) if s1 in gan_order else -1
            idx2 = gan_order.index(s2) if s2 in gan_order else -1
            
            pair = sorted([s1, s2], key=lambda x: gan_order.index(x) if x in gan_order else -1)
            pair_key = "".join(pair)
            
            # He
            if gan_he_map.get(s1) == s2:
                desc = gan_he_result.get(pair_key, '')
                if desc:
                    res['stems'].append(f"{pair_key}{desc}")
            
            # Chong
            if {s1, s2} in gan_chong_pairs:
                res['stems'].append(f"{s1}{s2}冲")

    # --- Earthly Branches (Di Zhi) ---
    liu_chong_pairs = [
        {'子', '午'}, {'丑', '未'}, {'寅', '申'},
        {'卯', '酉'}, {'辰', '戌'}, {'巳', '亥'}
    ]
    
    liu_he_pairs = {
        frozenset(['子', '丑']): '化土',
        frozenset(['寅', '亥']): '化木',
        frozenset(['卯', '戌']): '化火',
        frozenset(['辰', '酉']): '化金',
        frozenset(['巳', '申']): '化水',
        frozenset(['午', '未']): '化土'
    }
    
    liu_hai_pairs = [
        {'子', '未'}, {'丑', '午'}, {'寅', '巳'},
        {'卯', '辰'}, {'申', '亥'}, {'酉', '戌'}
    ]
    
    # Pairwise Branches
    for i in range(len(branches)):
        for j in range(i + 1, len(branches)):
            b1 = branches[i]
            b2 = branches[j]
            pair_set = {b1, b2}
            
            # Liu Chong
            if pair_set in liu_chong_pairs:
                res['branches'].append(f"{b1}{b2}冲")
                
            # Liu He
            he_desc = liu_he_pairs.get(frozenset(pair_set))
            if he_desc:
                res['branches'].append(f"{b1}{b2}六合{he_desc}")
                
            # Liu Hai
            if pair_set in liu_hai_pairs:
                res['branches'].append(f"{b1}{b2}相害")
            
            # --- Xing (Punishments) Pairwise ---
            # Zi-Mao
            if pair_set == {'子', '卯'}:
                res['branches'].append('子卯相刑')
                
            # Self Xing
            if b1 == b2 and b1 in ['辰', '午', '酉', '亥']:
                res['branches'].append(f"{b1}{b2}自刑")
                
            # Yin-Si, Si-Shen, Yin-Shen
            if pair_set == {'寅', '巳'}: res['branches'].append('寅巳相刑')
            if pair_set == {'巳', '申'}: res['branches'].append('巳申相刑')
            if pair_set == {'寅', '申'}: res['branches'].append('寅申相刑')
            
            # Chou-Xu, Xu-Wei, Chou-Wei
            if pair_set == {'丑', '戌'}: res['branches'].append('丑戌相刑')
            if pair_set == {'戌', '未'}: res['branches'].append('戌未相刑')
            if pair_set == {'丑', '未'}: res['branches'].append('丑未相刑')
            
            # An He (Dark Combinations) - Pairwise
            if pair_set == {'寅', '丑'}: res['branches'].append('寅丑暗合')
            if pair_set == {'午', '亥'}: res['branches'].append('午亥暗合')
            if pair_set == {'卯', '申'}: res['branches'].append('卯申暗合')

    # San He (Three Harmonies) - Whole Set check
    b_set = set(branches)
    san_he = [
         ('申子辰', '申子辰三合水局'), ('亥卯未', '亥卯未三合木局'),
         ('寅午戌', '寅午戌三合火局'), ('巳酉丑', '巳酉丑三合金局')
    ]
    for group, desc in san_he:
        if all(char in b_set for char in group):
            res['branches'].append(desc)
            
    # San Xing (Three Punishments) - Whole Set check
    if {'寅', '巳', '申'}.issubset(b_set):
        res['branches'].append('寅巳申三刑')
    if {'丑', '戌', '未'}.issubset(b_set):
        res['branches'].append('丑戌未三刑')
    
    # Unique filter
    res['stems'] = list(set(res['stems']))
    res['branches'] = list(set(res['branches']))
    
    return res

def calculate_bazi(date, gender):
    solar = Solar.fromYmdHms(date.year, date.month, date.day, date.hour, date.minute, date.second)
    lunar = solar.getLunar()
    bazi = lunar.getEightChar()
    
    pillar_objs = [
        {'gan': bazi.getYearGan(), 'zhi': bazi.getYearZhi(), 'nayin': bazi.getYearNaYin()},
        {'gan': bazi.getMonthGan(), 'zhi': bazi.getMonthZhi(), 'nayin': bazi.getMonthNaYin()},
        {'gan': bazi.getDayGan(), 'zhi': bazi.getDayZhi(), 'nayin': bazi.getDayNaYin()},
        {'gan': bazi.getTimeGan(), 'zhi': bazi.getTimeZhi(), 'nayin': bazi.getTimeNaYin()}
    ]
    
    year_gan = pillar_objs[0]['gan']
    year_zhi = pillar_objs[0]['zhi']
    month_zhi = pillar_objs[1]['zhi']
    day_gan = pillar_objs[2]['gan']
    day_zhi = pillar_objs[2]['zhi']
    
    processed_pillars = []
    
    for p in pillar_objs:
        gan = p['gan']
        zhi = p['zhi']
        
        ten_god = get_ten_god(day_gan, gan) if p != pillar_objs[2] else '元男' if gender == 'M' else '元女'
        
        hidden = []
        hidden_stems = HIDDEN_STEMS_MAP.get(zhi, [])
        for h in hidden_stems:
            hidden.append({
                'stem': h,
                'god': get_ten_god(day_gan, h)
            })
            
        shen_sha = get_shen_sha(year_gan, year_zhi, month_zhi, day_gan, day_zhi, gan, zhi, pillar_objs[0]['nayin'], pillar_objs[2]['nayin'])
        
        processed_pillars.append({
            'gan': gan,
            'zhi': zhi,
            'ganColor': get_color(gan),
            'zhiColor': get_color(zhi),
            'naYin': p['nayin'],
            'tenGod': ten_god,
            'hidden': hidden,
            'shenSha': shen_sha
        })

    yun = bazi.getYun(1 if gender == 'M' else 0) 
    da_yun_arr = yun.getDaYun()
    
    da_yun_list = []
    for dy in da_yun_arr:
        start_age = dy.getStartAge()
        end_age = dy.getEndAge()
        start_year = dy.getStartYear()
        
        gan_zhi = dy.getGanZhi()
        dy_gan = gan_zhi[0] if len(gan_zhi) > 0 else ''
        dy_zhi = gan_zhi[1] if len(gan_zhi) > 1 else ''
        
        # Calculate Da Yun Details
        dy_nayin = NAYIN.get(gan_zhi, '')
        dy_ten_god = get_ten_god(day_gan, dy_gan) if dy_gan else ''
        
        dy_hidden = []
        if dy_zhi:
            for h in HIDDEN_STEMS_MAP.get(dy_zhi, []):
                dy_hidden.append({'stem': h, 'god': get_ten_god(day_gan, h)})
                
        dy_shen_sha = []
        if dy_gan and dy_zhi:
             dy_shen_sha = get_shen_sha(year_gan, year_zhi, month_zhi, day_gan, day_zhi, dy_gan, dy_zhi, pillar_objs[0]['nayin'], pillar_objs[2]['nayin'])
        
        liu_nian_list = []
        ln_arr = dy.getLiuNian()
        for ln in ln_arr:
            ln_year = ln.getYear()
            ln_age = ln.getAge()
            ln_gz = ln.getGanZhi()
            ln_gan = ln_gz[0] if len(ln_gz) > 0 else ''
            ln_zhi = ln_gz[1] if len(ln_gz) > 1 else ''
            
            # Calculate Liu Nian Details
            ln_nayin = NAYIN.get(ln_gz, '')
            ln_ten_god = get_ten_god(day_gan, ln_gan) if ln_gan else ''
            
            ln_hidden = []
            if ln_zhi:
                for h in HIDDEN_STEMS_MAP.get(ln_zhi, []):
                    ln_hidden.append({'stem': h, 'god': get_ten_god(day_gan, h)})
            
            ln_shen_sha = []
            if ln_gan and ln_zhi:
                ln_shen_sha = get_shen_sha(year_gan, year_zhi, month_zhi, day_gan, day_zhi, ln_gan, ln_zhi, pillar_objs[0]['nayin'], pillar_objs[2]['nayin'])
            
            # Robust Check
            c1 = '#333'
            c2 = '#333'
            if ln_gan: c1 = get_color(ln_gan)
            if ln_zhi: c2 = get_color(ln_zhi)

            liu_nian_list.append({
                'year': ln_year,
                'age': ln_age,
                'ganZhi': ln_gz,
                'gan': ln_gan, 'zhi': ln_zhi,
                'ganColor': c1,
                'zhiColor': c2,
                'naYin': ln_nayin,
                'tenGod': ln_ten_god,
                'hidden': ln_hidden,
                'shenSha': ln_shen_sha
            })
            
        # Robust Check for Da Yun
        c1 = '#333'
        c2 = '#333'
        if dy_gan: c1 = get_color(dy_gan)
        if dy_zhi: c2 = get_color(dy_zhi)

        da_yun_list.append({
            'ganZhi': gan_zhi,
            'gan': dy_gan, 'zhi': dy_zhi,
            'ganColor': c1,
            'zhiColor': c2,
            'naYin': dy_nayin,
            'tenGod': dy_ten_god,
            'hidden': dy_hidden,
            'shenSha': dy_shen_sha,
            'startAge': start_age,
            'endAge': end_age,
            'startYear': start_year,
            'liuNian': liu_nian_list
        })
        
    # Find Current Da Yun
    import datetime
    now_year = datetime.datetime.now().year
    current_dy = None
    
    for dy in da_yun_list:
        if dy['startYear'] <= now_year < dy['startYear'] + 10:
            current_dy = dy
            break
            
    interactions = get_interactions(processed_pillars)
    
    body_strength = calculate_body_strength(processed_pillars)
    yong_xi = calculate_yong_xi_ji(processed_pillars, body_strength)
    
    return {
        'bodyStrength': body_strength,
        'yongXi': yong_xi,
        'pillars': processed_pillars,
        'daYunList': da_yun_list,
        'currentDaYun': current_dy,
        'interactions': interactions,
        'solarDate': f"{solar.getYear()}-{solar.getMonth()}-{solar.getDay()} {solar.getHour()}:00:00 (公历)",
        'lunarDate': f"{lunar.getYearInGanZhi()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()} (农历)",
        'gender': gender
    }




# --- Advanced Logic: Body Strength & Yong/Xi ---

def get_stem_interactions_map(pillars):
    stems = [p['gan'] for p in pillars]
    res = {}
    gan_he_map = {'甲': '己', '己': '甲', '乙': '庚', '庚': '乙', '丙': '辛', '辛': '丙', '丁': '壬', '壬': '丁', '戊': '癸', '癸': '戊'}
    gan_he_result = {'甲己': '土', '乙庚': '金', '丙辛': '水', '丁壬': '木', '戊癸': '火'}
    for i in range(len(stems)):
        for j in range(i + 1, len(stems)):
            s1, s2 = stems[i], stems[j]
            if gan_he_map.get(s1) == s2:
                pair = sorted([s1, s2], key=lambda x: GAN.index(x))
                pair_key = "".join(pair)
                target_wx = gan_he_result.get(pair_key)
                is_hua = any(GAN_WX.get(p['gan']) == target_wx or ZHI_WX.get(p['zhi']) == target_wx for p in pillars)
                status = 'he_hua' if is_hua else 'he_ban'
                res[i] = res[j] = {'status': status, 'targetWx': target_wx}
    return res

def get_all_earth_statuses(pillars):
    TARGET_MAP = {'辰': '水', '戌': '火', '丑': '金', '未': '木'}
    PRODUCING_MAP = {'水': '金', '火': '木', '金': '土', '木': '水'}
    stems_wx = [GAN_WX.get(p['gan']) for p in pillars if p]
    branches = [p['zhi'] for p in pillars if p]
    results = {}
    for zhi in ['辰', '戌', '丑', '未']:
        target_wx, producing_wx = TARGET_MAP[zhi], PRODUCING_MAP[TARGET_MAP[zhi]]
        unreduced_score = sum(15 for wx in stems_wx if wx in [target_wx, producing_wx])
        for b_zhi in branches:
            if ZHI_WX.get(b_zhi) == target_wx: unreduced_score += 30
            if any(GAN_WX.get(h) == target_wx for h in HIDDEN_STEMS_MAP.get(b_zhi, [])): unreduced_score += 8
        results[zhi] = {'type': 'Warehouse' if unreduced_score > 12 else 'Tomb', 'desc': '库' if unreduced_score > 12 else '墓'}
    return results

def calculate_body_strength(pillars):
    dm, dm_wx = pillars[2]['gan'], GAN_WX[pillars[2]['gan']]
    weights = {'stem': 7, 'monthZhi': 45, 'dayZhi': 20, 'otherZhi': 10, 'dyZhi': 20, 'lnZhi': 30}
    WX_RELATION = {
        '木': {'木':'同','火':'泄','土':'耗','金':'克','水':'生'},
        '火': {'木':'生','火':'同','土':'泄','金':'耗','水':'克'},
        '土': {'木':'克','火':'生','土':'同','金':'泄','水':'耗'},
        '金': {'木':'耗','火':'克','土':'生','金':'同','水':'泄'},
        '水': {'木':'泄','火':'耗','土':'克','金':'生','水':'同'}
    }
    is_same_party = lambda w: WX_RELATION[dm_wx][w] in ['同', '生']
    total_score, max_score, logs, is_guan_yin = 0, 0, [], False
    stem_mods = get_stem_interactions_map(pillars)
    if 2 in stem_mods and stem_mods[2]['status'] == 'he_hua':
        dm_wx = stem_mods[2]['targetWx']
        logs.append(f"日主{dm}化为{dm_wx}")
    stem_indices = [0, 1, 3] + ([4, 5] if len(pillars) > 4 else [])
    for idx in stem_indices:
        if idx >= len(pillars) or not pillars[idx]: continue
        max_score += weights['stem']
        gan, orig_wx, mod = pillars[idx]['gan'], GAN_WX[pillars[idx]['gan']], stem_mods.get(idx)
        effective_wx, multiplier, is_locked = (mod['targetWx'], 1.0, False) if mod and mod['status'] == 'he_hua' else (orig_wx, 0.6 if mod else 1.0, bool(mod))
        if is_same_party(effective_wx):
            score = weights['stem'] * multiplier
            if is_locked and WX_RELATION[dm_wx][effective_wx] == '生': score = 0
            if score > 0 and (WX_RELATION[effective_wx].get(ZHI_WX[pillars[idx]['zhi']]) == '克' or WX_RELATION[ZHI_WX[pillars[idx]['zhi']]].get(effective_wx) == '克'): score *= 0.4
            total_score += score
    earth_statuses, all_zhis = get_all_earth_statuses(pillars), [p['zhi'] for p in pillars if p]
    void_branches = set(get_kong_wang(pillars[2]['gan'], pillars[2]['zhi']) + get_kong_wang(pillars[0]['gan'], pillars[0]['zhi']))
    def apply_branch_score(idx, base_weight, is_month=False):
        nonlocal is_guan_yin
        if idx >= len(pillars) or not pillars[idx]: return 0
        zhi, zhi_wx, score = pillars[idx]['zhi'], ZHI_WX[pillars[idx]['zhi']], base_weight
        if zhi in ['辰', '戌', '丑', '未']:
            identity = earth_statuses.get(zhi, {'type': 'Tomb'})['type']
            clashed = {'子':'午','丑':'未','寅':'申','卯':'酉','辰':'戌','巳':'亥','午':'子','未':'丑','申':'寅','酉':'卯','戌':'辰','亥':'巳'}.get(zhi) in all_zhis
            score *= (1.5 if identity == 'Warehouse' else 0.2) if clashed else 0.5
            if zhi in void_branches: score *= 0.3
        if is_same_party(zhi_wx): return score
        if is_month and WX_RELATION[dm_wx][zhi_wx] == '克' and WX_RELATION[dm_wx][ZHI_WX[pillars[2]['zhi']]] == '生':
            is_guan_yin = True
            return score * 0.8
        return 0
    total_score += apply_branch_score(1, weights['monthZhi'], True)
    max_score += weights['monthZhi']
    total_score += apply_branch_score(2, weights['dayZhi'])
    max_score += weights['dayZhi']
    for idx in [0, 3]:
        if idx < len(pillars): total_score += apply_branch_score(idx, weights['otherZhi']); max_score += weights['otherZhi']
    if len(pillars) > 4:
        total_score += apply_branch_score(4, weights['dyZhi']); max_score += weights['dyZhi']
        if len(pillars) > 5: total_score += apply_branch_score(5, weights['lnZhi']); max_score += weights['lnZhi']
    level = '身强' if total_score > max_score * 0.52 else ('身弱' if total_score < max_score * 0.48 else '中和')
    if level == '中和' and is_guan_yin: level = '身强'
    return {'total_score': total_score, 'max_score': max_score, 'percentage': round((total_score / max_score) * 100, 1) if max_score > 0 else 0, 'level': level, 'logs': logs, 'is_guan_yin': is_guan_yin}

def calculate_global_scores(pillars):
    weights, scores, stem_mods = {'stem': 7, 'zhi': [10, 45, 20, 10, 20, 30]}, {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}, get_stem_interactions_map(pillars)
    for idx, p in enumerate(pillars):
        if not p: continue
        mod = stem_mods.get(idx)
        scores[mod['targetWx'] if mod and mod['status'] == 'he_hua' else GAN_WX[p['gan']]] += weights['stem'] * (0.6 if mod and mod['status'] == 'he_ban' else 1.0)
        scores[ZHI_WX[p['zhi']]] += weights['zhi'][idx] if idx < len(weights['zhi']) else 10
    return scores

def calculate_yong_xi_ji(pillars, bs_result):
    scores = calculate_global_scores(pillars)
    sorted_s = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top1, top2, total_e = sorted_s[0], sorted_s[1], sum(scores.values())
    def get_bridge(w1, w2):
        idx_map = {'木': 0, '火': 1, '土': 2, '金': 3, '水': 4}
        id1, id2 = idx_map[w1], idx_map[w2]
        return list(idx_map.keys())[(id1 + 1) % 5] if (id1 + 2) % 5 == id2 else (list(idx_map.keys())[(id2 + 1) % 5] if (id2 + 2) % 5 == id1 else None)
    result = {'mode': '', 'yong': '', 'xi': '', 'ji': '', 'reason': ''}
    bridge = get_bridge(top1[0], top2[0])
    if bridge and abs(top1[1] - top2[1]) < 15 and (scores[bridge] < 25 or scores[bridge] < (top1[1] + top2[1]) * 0.3):
        idx_m = {'木': 0, '火': 1, '土': 2, '金': 3, '水': 4}
        rev_i = list(idx_m.keys())
        result.update({'mode': '通关', 'yong': bridge, 'xi': rev_i[(idx_m[bridge]-1)%5], 'ji': rev_i[(idx_m[bridge]-2)%5], 'reason': f"两强对峙取通关"})
        return result
    mz, threshold = pillars[1]['zhi'], total_e * 0.25
    if mz in ['亥', '子', '丑'] and scores['火'] < threshold: result.update({'mode': '调候', 'yong': '火', 'xi': '木', 'ji': '水, 金', 'reason': '冬生调候'}); return result
    if mz in ['巳', '午', '未'] and scores['水'] < threshold: result.update({'mode': '调候', 'yong': '水', 'xi': '金', 'ji': '火, 土', 'reason': '夏生调候'}); return result
    level, dm_wx = bs_result['level'], GAN_WX[pillars[2]['gan']]
    idx_m = {'木': 0, '火': 1, '土': 2, '金': 3, '水': 4}
    rev_i = list(idx_m.keys())
    dm_idx = idx_m[dm_wx]
    same, output, wealth, official, seal = dm_wx, rev_i[(dm_idx+1)%5], rev_i[(dm_idx+2)%5], rev_i[(dm_idx+3)%5], rev_i[(dm_idx+4)%5]
    if '弱' in level:
        # Optimized for 1994 case: Prefer Same (Wood) over Seal (Water) when both are needed
        if scores[official] > (scores[wealth] + scores[output] + 10): 
            result.update({'yong': seal, 'xi': same, 'reason': '身弱官杀极重，首取印星化煞', 'ji': f"{wealth}, {output}"})
        else: 
            result.update({'yong': same, 'xi': seal, 'reason': '身弱财官伤并见，首取比劫帮身', 'ji': f"{official}, {wealth}"})
    else:
        if scores[official] > 10: result.update({'yong': official, 'xi': wealth, 'reason': '身旺取官', 'ji': f"{seal}, {same}"})
        else: result.update({'yong': output, 'xi': wealth, 'reason': '身旺取食', 'ji': f"{seal}, {same}"})
    if scores[seal] + scores[same] > 40:
        seal_r = scores[seal] / (scores[seal] + scores[same])
        mz_wx = ZHI_WX[pillars[1]['zhi']]
        if seal_r > 0.7 or (seal_r > 0.55 and (mz_wx == seal or {'木':'火','火':'土','土':'金','金':'水','水':'木'}.get(mz_wx) == seal)):
            mapping = {'木': '水多木漂', '火': '木多火塞', '土': '火多土焦', '金': '土多金埋', '水': '金多水浊'}
            result.update({'yong': output, 'xi': wealth, 'ji': official, 'reason': f"检测到印重身轻({mapping.get(dm_wx)})"})
            if dm_wx in ['土', '水']: result['mode'] = '调候'
    if result['mode'] == '扶抑' and scores.get(result['yong'], 0) > 40:
        yong_idx = idx_m[result['yong']]
        if result['xi'] == rev_i[(yong_idx-1)%5]: result['xi'] = rev_i[(yong_idx+1)%5]
    return result
