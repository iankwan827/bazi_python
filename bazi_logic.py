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

    '太极贵人': lambda info:
        (info['dayGan'] in ['甲', '乙'] and info['zhi'] in ['子', '午']) or
        (info['yearGan'] in ['甲', '乙'] and info['zhi'] in ['子', '午']) or
        (info['dayGan'] in ['丙', '丁'] and info['zhi'] in ['酉', '卯']) or
        (info['yearGan'] in ['丙', '丁'] and info['zhi'] in ['酉', '卯']) or
        (info['dayGan'] in ['戊', '己'] and info['zhi'] in ['辰', '戌', '丑', '未']) or
        (info['yearGan'] in ['戊', '己'] and info['zhi'] in ['辰', '戌', '丑', '未']) or
        (info['dayGan'] in ['庚', '辛'] and info['zhi'] in ['寅', '亥']) or
        (info['yearGan'] in ['庚', '辛'] and info['zhi'] in ['寅', '亥']) or
        (info['dayGan'] in ['壬', '癸'] and info['zhi'] in ['巳', '申']) or
        (info['yearGan'] in ['壬', '癸'] and info['zhi'] in ['巳', '申']),

    '福星贵人': lambda info:
        (info['dayGan'] == '甲' and info['zhi'] in ['寅', '子']) or
        (info['yearGan'] == '甲' and info['zhi'] in ['寅', '子']) or
        (info['dayGan'] == '乙' and info['zhi'] in ['丑', '卯']) or
        (info['yearGan'] == '乙' and info['zhi'] in ['丑', '卯']) or
        (info['dayGan'] == '丙' and info['zhi'] == '子') or
        (info['yearGan'] == '丙' and info['zhi'] == '子') or
        (info['dayGan'] == '丁' and info['zhi'] == '酉') or
        (info['yearGan'] == '丁' and info['zhi'] == '酉') or
        (info['dayGan'] == '戊' and info['zhi'] == '申') or
        (info['yearGan'] == '戊' and info['zhi'] == '申') or
        (info['dayGan'] == '己' and info['zhi'] == '未') or
        (info['yearGan'] == '己' and info['zhi'] == '未') or
        (info['dayGan'] == '庚' and info['zhi'] in ['午', '巳']) or
        (info['yearGan'] == '庚' and info['zhi'] in ['午', '巳']) or
        (info['dayGan'] == '辛' and info['zhi'] == '巳') or
        (info['yearGan'] == '辛' and info['zhi'] == '巳') or
        (info['dayGan'] == '壬' and info['zhi'] == '辰') or
        (info['yearGan'] == '壬' and info['zhi'] == '辰') or
        (info['dayGan'] == '癸' and info['zhi'] in ['卯', '丑']) or
        (info['yearGan'] == '癸' and info['zhi'] in ['卯', '丑']),

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
            
            # An He (Secret Combinations) - Dynamic Check based on Hidden Stems
            # User rule: If hidden stems have He (Jia-Ji, Yi-Geng, etc.), it is An He.
            b1_hidden = HIDDEN_STEMS_MAP.get(b1, [])
            b2_hidden = HIDDEN_STEMS_MAP.get(b2, [])
            
            is_an_he = False
            for h1 in b1_hidden:
                for h2 in b2_hidden:
                    # Check if h1 and h2 combine
                    if gan_he_map.get(h1) == h2:
                        is_an_he = True
                        break
                if is_an_he: break
            
            if is_an_he:
                # Avoid duplicates if logic adds it multiple times or handled elsewhere
                # The prompt implies replacing the specific logic.
                res['branches'].append(f"{b1}{b2}暗合")

    # San He (Three Harmonies) - Whole Set check
    b_set = set(branches)
    san_he = [
         ('申子辰', '申子辰三合水局'), ('亥卯未', '亥卯未三合木局'),
         ('寅午戌', '寅午戌三合火局'), ('巳酉丑', '巳酉丑三合金局')
    ]
    for group, desc in san_he:
        if all(char in b_set for char in group):
            res['branches'].append(desc)

    # San Hui (Three Meetings) - Whole Set check
    san_hui = [
        ({'寅', '卯', '辰'}, '寅卯辰三会木方'),
        ({'巳', '午', '未'}, '巳午未三会火方'),
        ({'申', '酉', '戌'}, '申酉戌三会金方'),
        ({'亥', '子', '丑'}, '亥子丑三会水方')
    ]
    for group, desc in san_hui:
        if group.issubset(b_set):
            res['branches'].append(desc)

    # Ban He (Half Combinations) & Extra An He - Pairwise Check
    ban_he_pairs = {
        frozenset(['申', '子']): '申子半合(水局)',
        frozenset(['子', '辰']): '子辰半合(水局)',
        frozenset(['亥', '卯']): '亥卯半合(木局)',
        frozenset(['卯', '未']): '卯未半合(木局)',
        frozenset(['寅', '午']): '寅午半合(火局)',
        frozenset(['午', '戌']): '午戌半合(火局)',
        frozenset(['巳', '酉']): '巳酉半合(金局)',
        frozenset(['酉', '丑']): '酉丑半合(金局)'
    }
    
    for i in range(len(branches)):
        for j in range(i + 1, len(branches)):
            pair_set = frozenset([branches[i], branches[j]])
            
            if pair_set in ban_he_pairs:
                res['branches'].append(ban_he_pairs[pair_set])
            
            if pair_set in ban_he_pairs:
                res['branches'].append(ban_he_pairs[pair_set])
            
            # Missing An He - REMOVED (Covered by Dynamic Logic)
            
    # San Xing (Three Punishments) - Whole Set check
    if {'寅', '巳', '申'}.issubset(b_set):
        res['branches'].append('寅巳申三刑')
    if {'丑', '戌', '未'}.issubset(b_set):
        res['branches'].append('丑未戌三刑')
    
    # Unique filter
    res['stems'] = list(set(res['stems']))
    res['branches'] = list(set(res['branches']))
    
    res['stems'] = list(set(res['stems']))
    res['branches'] = list(set(res['branches']))
    
    return res

def get_kong_wang(gan, zhi):
    """根据干支计算空亡 (The void branches)"""
    if gan not in GAN or zhi not in ZHI:
        return ""
    gan_idx = GAN.index(gan)
    zhi_idx = ZHI.index(zhi)
    # 旬首 (Xun Shou) calculated relative to Jia (0)
    # The difference between Zhi and Gan index tells us which Xun it belongs to.
    # diff = 0 -> Jia Zi Xun -> Kong Wang: Xu(10), Hai(11) -> (diff-2), (diff-1)
    diff = (zhi_idx - gan_idx) % 12
    kw1 = ZHI[(diff - 2) % 12]
    kw2 = ZHI[(diff - 1) % 12]
    return f"{kw1}{kw2}"

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
    
    for i, p in enumerate(pillar_objs):
        gan = p['gan']
        zhi = p['zhi']
        
        ten_god = get_ten_god(day_gan, gan) if i != 2 else '元男' if gender == 'M' else '元女'
        
        hidden = []
        hidden_stems = HIDDEN_STEMS_MAP.get(zhi, [])
        for h in hidden_stems:
            hidden.append({
                'stem': h,
                'god': get_ten_god(day_gan, h)
            })
            
        shen_sha = get_shen_sha(year_gan, year_zhi, month_zhi, day_gan, day_zhi, gan, zhi, pillar_objs[0]['nayin'], pillar_objs[2]['nayin'])
        kong_wang = get_kong_wang(gan, zhi)
        
        processed_pillars.append({
            'gan': gan,
            'zhi': zhi,
            'ganColor': get_color(gan),
            'zhiColor': get_color(zhi),
            'naYin': p['nayin'],
            'tenGod': ten_god,
            'hidden': hidden,
            'shenSha': shen_sha,
            'kongWang': kong_wang
        })

    yun = bazi.getYun(1 if gender == 'M' else 0) 
    da_yun_arr = yun.getDaYun()
    
    da_yun_list = []
    for dy in da_yun_arr:
        start_age = dy.getStartAge()
        end_age = dy.getEndAge()
        start_year = dy.getStartYear()
        
        gz_str = dy.getGanZhi()
        if len(gz_str) >= 2:
            dy_gan = gz_str[0]
            dy_zhi = gz_str[1]
        else:
            dy_gan = ""
            dy_zhi = ""
            
        dy_nayin = NAYIN.get(gz_str, '')
        dy_ten_god = get_ten_god(day_gan, dy_gan) if dy_gan else ''
        
        dy_hidden = []
        if dy_zhi:
            for h in HIDDEN_STEMS_MAP.get(dy_zhi, []):
                dy_hidden.append({'stem': h, 'god': get_ten_god(day_gan, h)})
                
        dy_shen_sha = []
        dy_shen_sha = []
        if dy_gan and dy_zhi:
             dy_shen_sha = get_shen_sha(year_gan, year_zhi, month_zhi, day_gan, day_zhi, dy_gan, dy_zhi, pillar_objs[0]['nayin'], pillar_objs[2]['nayin'])
        
        dy_kong_wang = get_kong_wang(dy_gan, dy_zhi)
        
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
            
            ln_kong_wang = get_kong_wang(ln_gan, ln_zhi)
            
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
                'shenSha': ln_shen_sha,
                'kongWang': ln_kong_wang
            })
            
        # Robust Check for Da Yun
        c1 = '#333'
        c2 = '#333'
        if dy_gan: c1 = get_color(dy_gan)
        if dy_zhi: c2 = get_color(dy_zhi)

        da_yun_list.append({
            'ganZhi': gz_str,
            'gan': dy_gan, 'zhi': dy_zhi,
            'ganColor': c1,
            'zhiColor': c2,
            'naYin': dy_nayin,
            'tenGod': dy_ten_god,
            'hidden': dy_hidden,
            'shenSha': dy_shen_sha,
            'kongWang': dy_kong_wang,
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
    
    return {
        'pillars': processed_pillars,
        'daYunList': da_yun_list,
        'currentDaYun': current_dy,
        'interactions': interactions,
        'solarDate': f"{solar.getYear()}-{solar.getMonth()}-{solar.getDay()} {solar.getHour()}:00:00 (公历)",
        'lunarDate': f"{lunar.getYearInGanZhi()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()} (农历)",
        'gender': gender
    }

def get_dynamic_interactions(pillars, dynamic_indices):
    """
    Calculate interactions but ONLY return those that involve pillars at dynamic_indices.
    pillars: list of all pillars (e.g. 4 original + 1 DY + 1 LN)
    dynamic_indices: list of indices considered 'dynamic' (e.g. [4, 5])
    """
    stems = [p['gan'] for p in pillars]
    branches = [p['zhi'] for p in pillars]
    
    res = {'stems': [], 'branches': []}
    
    # --- Stems ---
    gan_he_map = {'甲': '己', '己': '甲', '乙': '庚', '庚': '乙', '丙': '辛', '辛': '丙', '丁': '壬', '壬': '丁', '戊': '癸', '癸': '戊'}
    gan_he_result = {'甲己': '合土', '乙庚': '合金', '丙辛': '合水', '丁壬': '合木', '戊癸': '合火'}
    gan_chong_pairs = [{'甲', '庚'}, {'乙', '辛'}, {'丙', '壬'}, {'丁', '癸'}]
    
    for i in range(len(stems)):
        for j in range(i + 1, len(stems)):
            if i not in dynamic_indices and j not in dynamic_indices:
                continue # Skip pure internal interactions
                
            s1, s2 = stems[i], stems[j]
            pair_key = "".join(sorted([s1, s2], key=lambda x: GAN.index(x) if x in GAN else -1))
            
            if gan_he_map.get(s1) == s2:
                desc = gan_he_result.get(pair_key, '')
                if desc: res['stems'].append(f"{pair_key}{desc}")
            if {s1, s2} in gan_chong_pairs:
                res['stems'].append(f"{s1}{s2}冲")

    # --- Branches ---
    liu_chong_pairs = [{'子', '午'}, {'丑', '未'}, {'寅', '申'}, {'卯', '酉'}, {'辰', '戌'}, {'巳', '亥'}]
    liu_he_pairs = {frozenset(['子', '丑']): '化土', frozenset(['寅', '亥']): '化木', frozenset(['卯', '戌']): '化火', frozenset(['辰', '酉']): '化金', frozenset(['巳', '申']): '化水', frozenset(['午', '未']): '化土'}
    liu_hai_pairs = [{'子', '未'}, {'丑', '午'}, {'寅', '巳'}, {'卯', '辰'}, {'申', '亥'}, {'酉', '戌'}]
    ban_he_pairs = {
        frozenset(['申', '子']): '申子半合(水局)', frozenset(['子', '辰']): '子辰半合(水局)',
        frozenset(['亥', '卯']): '亥卯半合(木局)', frozenset(['卯', '未']): '卯未半合(木局)',
        frozenset(['寅', '午']): '寅午半合(火局)', frozenset(['午', '戌']): '午戌半合(火局)',
        frozenset(['巳', '酉']): '巳酉半合(金局)', frozenset(['酉', '丑']): '酉丑半合(金局)'
    }

    for i in range(len(branches)):
        for j in range(i + 1, len(branches)):
            if i not in dynamic_indices and j not in dynamic_indices:
                continue

            b1, b2 = branches[i], branches[j]
            pair_set = {b1, b2}
            
            if pair_set in liu_chong_pairs: res['branches'].append(f"{b1}{b2}冲")
            he_desc = liu_he_pairs.get(frozenset(pair_set))
            if he_desc: res['branches'].append(f"{b1}{b2}六合{he_desc}")
            if pair_set in liu_hai_pairs: res['branches'].append(f"{b1}{b2}相害")
            if pair_set == {'子', '卯'}: res['branches'].append('子卯相刑')
            if b1 == b2 and b1 in ['辰', '午', '酉', '亥']: res['branches'].append(f"{b1}{b2}自刑")
            if pair_set == {'寅', '巳'}: res['branches'].append('寅巳相刑')
            if pair_set == {'巳', '申'}: res['branches'].append('巳申相刑')
            if pair_set == {'寅', '申'}: res['branches'].append('寅申相刑')
            if pair_set == {'丑', '戌'}: res['branches'].append('丑戌相刑')
            if pair_set == {'戌', '未'}: res['branches'].append('戌未相刑')
            if pair_set == {'丑', '未'}: res['branches'].append('丑未相刑')
            
            # An He
            b1_hidden = HIDDEN_STEMS_MAP.get(b1, [])
            b2_hidden = HIDDEN_STEMS_MAP.get(b2, [])
            is_an_he = False
            for h1 in b1_hidden:
                for h2 in b2_hidden:
                    if gan_he_map.get(h1) == h2:
                        is_an_he = True
                        break
                if is_an_he: break
            if is_an_he: res['branches'].append(f"{b1}{b2}暗合")
            
            fz = frozenset(pair_set)
            if fz in ban_he_pairs: res['branches'].append(ban_he_pairs[fz])


    # San He / San Hui Check
    b_indices = {b: [] for b in set(branches)} # map branch to list of indices
    for idx, b in enumerate(branches):
        if b not in b_indices: b_indices[b] = []
        b_indices[b].append(idx)
        
    san_he = [('申子辰', '申子辰三合水局'), ('亥卯未', '亥卯未三合木局'), ('寅午戌', '寅午戌三合火局'), ('巳酉丑', '巳酉丑三合金局')]
    san_hui = [({'寅', '卯', '辰'}, '寅卯辰三会木方'), ({'巳', '午', '未'}, '巳午未三会火方'), ({'申', '酉', '戌'}, '申酉戌三会金方'), ({'亥', '子', '丑'}, '亥子丑三会水方')]
    
    def check_group(group, desc):
        present = True
        involved_indices = []
        for char in group:
            if char not in b_indices:
                present = False
                break
            involved_indices.extend(b_indices[char])
        if present:
            if any(idx in dynamic_indices for idx in involved_indices):
                res['branches'].append(desc)
                
    for g, d in san_he: check_group(g, d)
    for g, d in san_hui: check_group(g, d)
    
    if {'寅', '巳', '申'}.issubset(set(branches)):
        check_group({'寅', '巳', '申'}, '寅巳申三刑')
    if {'丑', '戌', '未'}.issubset(set(branches)):
        check_group({'丑', '戌', '未'}, '丑未戌三刑')
        
    res['stems'] = list(set(res['stems']))
    res['branches'] = list(set(res['branches']))
    return res
