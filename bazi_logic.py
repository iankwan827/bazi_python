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

WX_RELATION = {
    '木': { '木': '同', '火': '泄', '土': '耗', '金': '克', '水': '生' },
    '火': { '木': '生', '火': '同', '土': '泄', '金': '耗', '水': '克' },
    '土': { '木': '克', '火': '生', '土': '同', '金': '泄', '水': '耗' },
    '金': { '木': '耗', '火': '克', '土': '生', '金': '同', '水': '泄' },
    '水': { '木': '泄', '火': '耗', '土': '克', '金': '生', '水': '同' }
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
        (info['yearZhi'] == '子' and info['zhi'] == '酉') or
        (info['yearZhi'] == '丑' and info['zhi'] == '申') or
        (info['yearZhi'] == '寅' and info['zhi'] == '未') or
        (info['yearZhi'] == '卯' and info['zhi'] == '午') or
        (info['yearZhi'] == '辰' and info['zhi'] == '巳') or
        (info['yearZhi'] == '巳' and info['zhi'] == '辰') or
        (info['yearZhi'] == '午' and info['zhi'] == '卯') or
        (info['yearZhi'] == '未' and info['zhi'] == '寅') or
        (info['yearZhi'] == '申' and info['zhi'] == '丑') or
        (info['yearZhi'] == '酉' and info['zhi'] == '子') or
        (info['yearZhi'] == '戌' and info['zhi'] == '亥') or
        (info['yearZhi'] == '亥' and info['zhi'] == '戌'),

    '红鸾': lambda info:
        (info['yearZhi'] == '子' and info['zhi'] == '卯') or
        (info['yearZhi'] == '丑' and info['zhi'] == '寅') or
        (info['yearZhi'] == '寅' and info['zhi'] == '丑') or
        (info['yearZhi'] == '卯' and info['zhi'] == '子') or
        (info['yearZhi'] == '辰' and info['zhi'] == '亥') or
        (info['yearZhi'] == '巳' and info['zhi'] == '戌') or
        (info['yearZhi'] == '午' and info['zhi'] == '酉') or
        (info['yearZhi'] == '未' and info['zhi'] == '申') or
        (info['yearZhi'] == '申' and info['zhi'] == '未') or
        (info['yearZhi'] == '酉' and info['zhi'] == '午') or
        (info['yearZhi'] == '戌' and info['zhi'] == '巳') or
        (info['yearZhi'] == '亥' and info['zhi'] == '辰'),

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
    
    '驿马': lambda info:
        (info['yearZhi'] in ['寅', '午', '戌'] and info['zhi'] == '申') or
        (info['dayZhi'] in ['寅', '午', '戌'] and info['zhi'] == '申') or
        (info['yearZhi'] in ['申', '子', '辰'] and info['zhi'] == '寅') or
        (info['dayZhi'] in ['申', '子', '辰'] and info['zhi'] == '寅') or
        (info['yearZhi'] in ['亥', '卯', '未'] and info['zhi'] == '巳') or
        (info['dayZhi'] in ['亥', '卯', '未'] and info['zhi'] == '巳') or
        (info['yearZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '亥') or
        (info['dayZhi'] in ['巳', '酉', '丑'] and info['zhi'] == '亥'),

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

    '孤鸾煞': lambda info:
        (info['stem'] == info['dayGan'] and info['zhi'] == info['dayZhi']) and (info['stem']+info['zhi'] in ['乙巳', '丁巳', '辛亥', '戊申', '壬子']),

    '童子煞': lambda info:
        # 1. Season Check (Month Zhi)
        (info['monthZhi'] in ['寅', '卯', '辰'] and info['zhi'] in ['寅', '子']) or # Spring
        (info['monthZhi'] in ['申', '酉', '戌'] and info['zhi'] in ['寅', '子']) or # Autumn
        (info['monthZhi'] in ['巳', '午', '未'] and info['zhi'] in ['卯', '未', '辰']) or # Summer
        (info['monthZhi'] in ['亥', '子', '丑'] and info['zhi'] in ['卯', '未', '辰']) or # Winter
        # 2. Na Yin Check (Year Na Yin)
        (info['yearNaYin'] and '土' in info['yearNaYin'] and info['zhi'] in ['辰', '巳']) or
        (info['yearNaYin'] and ('金' in info['yearNaYin'] or '木' in info['yearNaYin']) and info['zhi'] in ['午', '卯']) or
        (info['yearNaYin'] and ('水' in info['yearNaYin'] or '火' in info['yearNaYin']) and info['zhi'] in ['酉', '戌']),
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

def get_stem_interactions_map(pillars):
    """
    Returns a map of stem index to its interaction status (He Hua or He Ban).
    """
    stems = [p['gan'] for p in pillars]
    gan_he_map = {
        '甲': '己', '己': '甲',
        '乙': '庚', '庚': '乙',
        '丙': '辛', '辛': '丙',
        '丁': '壬', '壬': '丁',
        '戊': '癸', '癸': '戊'
    }
    gan_he_result = {
        '甲己': '土', '乙庚': '金', '丙辛': '水', '丁壬': '木', '戊癸': '火'
    }
    
    mz = pillars[1]['zhi'] if len(pillars) > 1 else None
    mz_wx = ZHI_WX.get(mz) if mz else None
    
    mods = {} # idx -> {'status': 'he_hua'/'he_ban', 'target_wx': element, 'multiplier': 0.6}
    
    for i in range(len(stems)):
        for j in range(i + 1, len(stems)):
            s1 = stems[i]
            s2 = stems[j]
            
            # Spatial Distance Rule:
            # - Within 4 pillars (0-3): only adjacent (dist=1) interact.
            # - Da Yun / Liu Nian (4, 5): treated as always adjacent to all.
            is_valid_dist = False
            if i >= 4 or j >= 4:
                is_valid_dist = True
            elif abs(i - j) == 1:
                is_valid_dist = True
                
            if is_valid_dist and gan_he_map.get(s1) == s2:
                # Get Result Element
                pair = sorted([s1, s2], key=lambda x: GAN.index(x) if x in GAN else -1)
                pair_key = "".join(pair)
                target_wx = gan_he_result.get(pair_key)
                
                if mz != None and mz_wx == target_wx:
                    # Success (He Hua)
                    if i not in mods: mods[i] = {'status': 'he_hua', 'target_wx': target_wx, 'multiplier': 1.0}
                    if j not in mods: mods[j] = {'status': 'he_hua', 'target_wx': target_wx, 'multiplier': 1.0}
                else:
                    # Failure (He Ban)
                    if i not in mods: mods[i] = {'status': 'he_ban', 'target_wx': None, 'multiplier': 0.6}
                    if j not in mods: mods[j] = {'status': 'he_ban', 'target_wx': None, 'multiplier': 0.6}
                    
    return mods

def get_interactions(pillars):
    stems = [p['gan'] for p in pillars]
    branches = [p['zhi'] for p in pillars]
    
    res = {'stems': [], 'branches': []}
    
    # --- Heavenly Stems (Tian Gan) ---
    res['judgments'] = [] # Initialize judgments list
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
                    # Strict He Hua Check: Month Zhi Element must match Result Element
                    # Get Month Zhi (Pillars[1])
                    if len(pillars) > 1:
                        mz = pillars[1]['zhi']
                        mz_wx = ZHI_WX.get(mz)
                        target_wx = desc[-1] # "合土" -> "土"
                        
                        if mz_wx == target_wx:
                            res['stems'].append(f"{pair_key}{desc}")
                            # Success Judgment
                            res['judgments'].append(f"{pair_key}{desc}成功：{pair[0]}与{pair[1]}均按{target_wx}五行论断。")
                        else:
                            res['stems'].append(f"{pair_key}{desc}(不化)")
                            # Failure Judgment
                            res['judgments'].append(f"{pair_key}合绊：{pair[0]}与{pair[1]}相互牵制，暂不生助克制其他天干。")
                    else:
                        # Fallback
                        res['stems'].append(f"{pair_key}{desc}")
                        res['judgments'].append(f"{pair_key}{desc}：{pair[0]}与{pair[1]}均按{target_wx}五行论断（无月令参考，暂按成功论）。")
            
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
            # Normalize Order for Deduplication (e.g. "子卯" vs "卯子")
            # Sort by ZHI order
            zhi_order = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
            pair_list = sorted([b1, b2], key=lambda x: zhi_order.index(x) if x in zhi_order else -1)
            b1, b2 = pair_list[0], pair_list[1]
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
    
    # --- Judgments (Double Clash) ---
    judgments = []
    
    def check_double_chong(idx1, idx2, pillars, gan_chong, zhi_chong_list):
        if idx1 >= len(pillars) or idx2 >= len(pillars): return False
        p1 = pillars[idx1]
        p2 = pillars[idx2]
        s1, s2 = p1['gan'], p2['gan']
        b1, b2 = p1['zhi'], p2['zhi']
        
        # Check Stem Chong
        is_stem_chong = {s1, s2} in gan_chong
        # Check Branch Chong
        is_branch_chong = {b1, b2} in zhi_chong_list
        
        return is_stem_chong and is_branch_chong

    # 0:Year, 1:Month, 2:Day, 3:Hour
    # Only check if we have enough pillars (at least 4 for original bazi)
    if len(pillars) >= 4:
        # 日、月干支双冲 (Day & Month)
        if check_double_chong(2, 1, pillars, gan_chong_pairs, liu_chong_pairs):
            judgments.append("日、月干支双冲，事业艰难。")
            
        # 年、日干支双冲 (Year & Day)
        if check_double_chong(0, 2, pillars, gan_chong_pairs, liu_chong_pairs):
            judgments.append("年、日干支双冲，主本不和，纵富贵也不久。")
            
        # 年、时干支双冲 (Year & Hour)
        if check_double_chong(0, 3, pillars, gan_chong_pairs, liu_chong_pairs):
            judgments.append("年、时干支双冲，乃别立根基之人。")
            
        # 月、时干支双冲 (Month & Hour)
        if check_double_chong(1, 3, pillars, gan_chong_pairs, liu_chong_pairs):
            judgments.append("月、时干支双冲，恐有多次起倒之遇。")

    res['judgments'].extend(judgments)
    # Deduplicate judgments
    res['judgments'] = list(dict.fromkeys(res['judgments']))

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
        'solarDate': f"{solar.getYear()}-{solar.getMonth():02d}-{solar.getDay():02d} {solar.getHour():02d}:{solar.getMinute():02d}:{solar.getSecond():02d} (公历)",
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

def get_gong_jia_relations(pillars):
    if not pillars or len(pillars) < 4:
        return {'adjacent': [], 'separated': []}

    # Standard Pillars: 0-Year, 1-Month, 2-Day, 3-Hour
    # indices in pillars list.
    adjacent_pairs = [(0, 1), (1, 2), (2, 3)]
    separated_pairs = [(0, 2), (0, 3), (1, 3)]

    p_names = ['年', '月', '日', '时']
    ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    gong_map = {
        '申辰': '子', '辰申': '子',
        '亥未': '卯', '未亥': '卯',
        '寅戌': '午', '戌寅': '午',
        '巳丑': '酉', '丑巳': '酉',
        '亥丑': '子', '丑亥': '子',
        '寅辰': '卯', '辰寅': '卯',
        '巳未': '午', '未巳': '午',
        '申戌': '酉', '戌申': '酉'
    }
    
    # Xing/Chong/He Helpers
    liu_chong_pairs = [{'子', '午'}, {'丑', '未'}, {'寅', '申'}, {'卯', '酉'}, {'辰', '戌'}, {'巳', '亥'}]
    liu_he_pairs = {'子丑': '六合', '寅亥': '六合', '卯戌': '六合', '辰酉': '六合', '巳申': '六合', '午未': '六合'}

    res = {'adjacent': [], 'separated': []}

    def process_pairs(pairs, is_sep):
        for i, j in pairs:
            p1 = pillars[i]
            p2 = pillars[j]
            b1 = p1['zhi']
            b2 = p2['zhi']
            name1 = p_names[i]
            name2 = p_names[j]
            
            relations = []

            # 1. Gong (Arch)
            key = b1 + b2
            key_rev = b2 + b1
            if key in gong_map:
                relations.append({'type': '拱', 'char': gong_map[key], 'desc': f"拱{gong_map[key]}"})
            elif key_rev in gong_map:
                relations.append({'type': '拱', 'char': gong_map[key_rev], 'desc': f"拱{gong_map[key_rev]}"})

            # 2. Jia (Squeeze)
            try:
                idx1 = ZHI.index(b1)
                idx2 = ZHI.index(b2)
                
                # Check Forward Squeeze: idx1 -> (mid) -> idx2
                if (idx1 + 2) % 12 == idx2:
                    mid_idx = (idx1 + 1) % 12
                    mid_char = ZHI[mid_idx]
                    relations.append({'type': '夹', 'char': mid_char, 'desc': f"夹{mid_char}"})

                # Check Reverse Squeeze
                elif (idx1 - 2 + 12) % 12 == idx2:
                    mid_idx = (idx1 - 1 + 12) % 12
                    mid_char = ZHI[mid_idx]
                    relations.append({'type': '倒夹', 'char': mid_char, 'desc': f"倒夹{mid_char}"})

            except ValueError:
                pass 

            # 3. Simple Xing/Chong/He
            # Chong
            pair_set = {b1, b2}
            if pair_set in liu_chong_pairs:
                relations.append({'type': '冲', 'char': '', 'desc': '相冲'})
            
            # He
            pair_str_sorted = "".join(sorted([b1, b2], key=lambda x: ZHI.index(x) if x in ZHI else -1))
            if pair_str_sorted in liu_he_pairs:
                 relations.append({'type': '合', 'char': '', 'desc': '六合'})
            
            # Xing
            if pair_set == {'子', '卯'}: relations.append({'type': '刑', 'char': '', 'desc': '相刑'})
            if b1 == b2 and b1 in ['辰', '午', '酉', '亥']: relations.append({'type': '刑', 'char': '', 'desc': '自刑'})

            if relations:
                item = {
                    'p1': name1, 'p2': name2,
                    'b1': b1, 'b2': b2,
                    'relations': relations
                }
                if is_sep:
                    res['separated'].append(item)
                else:
                    res['adjacent'].append(item)

    process_pairs(adjacent_pairs, False)
    process_pairs(separated_pairs, True)
    
    return res

def get_void_branches(day_gan, day_zhi):
    gan_idx = GAN.index(day_gan)
    zhi_idx = ZHI.index(day_zhi)
    xun_offset = (zhi_idx - gan_idx) % 12
    if xun_offset == 0: return ['戌', '亥'] # Jia Zi
    if xun_offset == 10: return ['子', '丑'] # Jia Yin
    if xun_offset == 8: return ['寅', '卯'] # Jia Chen
    if xun_offset == 6: return ['辰', '巳'] # Jia Wu
    if xun_offset == 4: return ['午', '未'] # Jia Shen
    if xun_offset == 2: return ['申', '酉'] # Jia Xu
    return []

def check_is_clashed(target_zhi, all_zhis):
    # Standard Clash Map
    clash_map = {
        '子': '午', '午': '子',
        '丑': '未', '未': '丑',
        '寅': '申', '申': '寅',
        '卯': '酉', '酉': '卯',
        '辰': '戌', '戌': '辰',
        '巳': '亥', '亥': '巳'
    }
    opponent = clash_map.get(target_zhi)
    return opponent in all_zhis

def get_all_earth_statuses(pillars, scores):
    """
    Calculate Warehouse/Tomb status for ALL 4 Earth branches (Chen, Xu, Chou, Wei).
    Logic (Phase 1: Priority Filtering Identity):
    - Priority 1: Roots -> Warehouse.
    - Priority 2: Stems -> Warehouse.
    - Priority 3: Residual Score > 12 -> Warehouse.
    """
    TARGET_MAP = {'辰': '水', '戌': '火', '丑': '金', '未': '木'}
    PRODUCING_MAP = {'水': '金', '火': '木', '金': '土', '木': '水'}
    
    stems = [p.get('gan') for p in pillars if p and p.get('gan')]
    branches = [p.get('zhi') for p in pillars if p and p.get('zhi')]
    stems_wx = [GAN_WX.get(s) for s in stems]

    results = {}
    
    for zhi in ['辰', '戌', '丑', '未']:
        target_wx = TARGET_MAP.get(zhi)
        producing_wx = PRODUCING_MAP.get(target_wx)
        status_type = 'Tomb' # Default
        desc = '墓'
        
        # P1: Root
        has_root = False
        for b_zhi in branches:
            if ZHI_WX.get(b_zhi) == target_wx:
                has_root = True
                break
        if has_root:
            results[zhi] = {'type': 'Warehouse', 'desc': '库'}
            continue

        # P2: Stem
        is_revealed = False
        for wx in stems_wx:
            if wx == target_wx or wx == producing_wx:
                is_revealed = True
                break
        if is_revealed:
            results[zhi] = {'type': 'Warehouse', 'desc': '库'}
            continue

        # P3: Residual
        residual = 0
        for b_zhi in branches:
            for h in HIDDEN_STEMS_MAP.get(b_zhi, []):
                if GAN_WX.get(h) == target_wx:
                    residual += 8
                    break
        if residual > 12:
            results[zhi] = {'type': 'Warehouse', 'desc': '库'}
        else:
            results[zhi] = {'type': 'Tomb', 'desc': '墓'}
            
    return results

def calculate_body_strength(pillars):
    """
    Calculates Strength. Supports 4 (Yuan Ju) or 6 (Dynamic) pillars.
    Updated for Advanced Logic: Dynamic Thresholds, Sui Yun Bing Lin, Zhan Ke.
    + Phase 2 Dynamic Correction for Tomb/Warehouse.
    """
    # Pillar Structure: [{'gan':.., 'zhi':..}, ...]
    dm = pillars[2]['gan']
    dm_wx = GAN_WX.get(dm)

    # Weights
    weights = {
        'stem': 7,
        'monthZhi': 45,
        'dayZhi': 20,
        'otherZhi': 10,
        'dyZhi': 20,
        'lnZhi': 30
    }

    # Helpers
    def get_rel(w):
        return WX_RELATION.get(dm_wx, {}).get(w)

    def is_same_party(w):
        return get_rel(w) in ['同', '生']

    total_score = 0
    max_possible_score = 0
    logs = []

    # --- 0. Pre-check Day Master Transformation ---
    stem_mods = get_stem_interactions_map(pillars)
    dm_mod = stem_mods.get(2)
    if dm_mod and dm_mod['status'] == 'he_hua':
        target_wx = dm_mod['target_wx']
        if target_wx:
            dm_wx = target_wx
            logs.append(f"日主{dm}化为{dm_wx}，按新五行判定身强身弱")
    elif dm_mod and dm_mod['status'] == 'he_ban':
        logs.append(f"日主{dm}被合绊，自身能量受限")
        
    # --- Prepare Phase 2 Data for Earth Branches ---
    # 1. Get Identity Map
    # We pass empty scores dict as P1 Logic doesn't use passed scores anymore.
    earth_statuses = get_all_earth_statuses(pillars, {}) 
    
    # 2. Get Collision/Void Info
    all_zhis = [p['zhi'] for p in pillars if p]
    day_gan = pillars[2]['gan']
    day_zhi = pillars[2]['zhi']
    void_branches = get_void_branches(day_gan, day_zhi)

    # --- 1. Calculate Scores ---

    # Stems (Year 0, Month 1, Hour 3 + DY 4, LN 5 if exist)
    stem_indices = [0, 1, 3]
    if len(pillars) > 4:
        stem_indices.append(4) # DY
        stem_indices.append(5) # LN

    for idx in stem_indices:
        if idx >= len(pillars): continue
        max_possible_score += weights['stem']
        gan = pillars[idx]['gan']
        orig_wx = GAN_WX.get(gan)
        
        mod = stem_mods.get(idx)
        effective_wx = orig_wx
        multiplier = 1.0
        is_locked = False
        
        if mod:
            if mod['status'] == 'he_hua':
                effective_wx = mod['target_wx']
                logs.append(f"{gan}合化成功，按{effective_wx}计分")
            else:
                multiplier = 0.6
                is_locked = True
                logs.append(f"{gan}合绊：能量x0.6且锁定生克职能")

        if is_same_party(effective_wx):
            rel = get_rel(effective_wx)
            score = weights['stem'] * multiplier
            
            if is_locked and rel == '生':
                score = 0
                logs.append(f"{gan}由于合绊，停止生助日主")
            
            if score > 0:
                # Gai Tou Check
                zhi = pillars[idx]['zhi']
                zhi_wx = ZHI_WX.get(zhi)
                rel_g_z = WX_RELATION.get(effective_wx, {}).get(zhi_wx)
                rel_z_g = WX_RELATION.get(zhi_wx, {}).get(effective_wx)

                if rel_g_z == '克' or rel_z_g == '克':
                    score *= 0.4
                    logs.append(f"{gan}({effective_wx}){zhi} 盖头/截脚，计分折损")
                
                total_score += score

    # Branches
    
    # Branches
    is_guan_yin = False
    
    def apply_branch_score(idx, base_weight, is_month=False):
        nonlocal is_guan_yin
        if idx >= len(pillars): return 0
        p = pillars[idx]
        if not p: return 0
        zhi = p['zhi']
        zhi_wx = ZHI_WX.get(zhi)
        
        score = base_weight
        
        # Phase 2 Dynamic Correction (Earth Branches)
        if zhi in ['辰', '戌', '丑', '未']:
            identity_info = earth_statuses.get(zhi, {'type': 'Tomb'})
            identity = identity_info['type']
            
            # 1. State: Clash vs Closed
            is_clashed = check_is_clashed(zhi, all_zhis)
            # User: "Clashed... 1.5 if Warehouse else 0.2"
            #       "Else (Closed)... 0.5"
            state_mult = 0.5 # Default Closed
            if is_clashed:
                if identity == 'Warehouse':
                    state_mult = 1.5
                    logs.append(f"{zhi}({identity})被冲开(Open): 能量释放 x1.5")
                else:
                    state_mult = 0.2
                    logs.append(f"{zhi}({identity})被冲破(Broken): 能量损毁 x0.2")
            else:
                logs.append(f"{zhi}({identity})处于闭合(Closed)状态: 能量潜伏 x0.5")
            
            score *= state_mult
            
            # 2. Void Modifier
            if zhi in void_branches:
                score *= 0.3
                logs.append(f"{zhi}逢空亡: 能量 x0.3")

        # Guan Yin Check (Month Only)
        # Note: If Earth Month is modified by Phase 2, we still check Guan Yin?
        # Yes, but on the *modified* score? Or logic check.
        # Check Guan Yin logic... it converts Clashing Month to Producing.
        # If Earth Month is same party, we just add score.
        # If not same party, we check Guan Yin.
        
        # Apply Party Check
        if is_same_party(zhi_wx):
            return score
        else:
            if is_month:
                # Guan Yin Check
                if get_rel(zhi_wx) == '克':
                    mg = pillars[1]['gan']
                    dz = pillars[2]['zhi']
                    mg_is_yin = (get_rel(GAN_WX.get(mg)) == '生')
                    dz_is_yin = (get_rel(ZHI_WX.get(dz)) == '生')
                    
                    if mg_is_yin or dz_is_yin:
                        converted = score * 0.8
                        logs.append(f"触发[官印相生]：月令{zhi}({zhi_wx})由克转生")
                        return converted
        return 0

    # Month (1)
    max_possible_score += weights['monthZhi']
    total_score += apply_branch_score(1, weights['monthZhi'], is_month=True)

    # Day Zhi (2)
    max_possible_score += weights['dayZhi']
    total_score += apply_branch_score(2, weights['dayZhi'])

    # Other Zhi (Year 0, Hour 3)
    for idx in [0, 3]:
        max_possible_score += weights['otherZhi']
        total_score += apply_branch_score(idx, weights['otherZhi'])

    # Dynamic Zhi
    if len(pillars) > 4:
        # DY (4)
        max_possible_score += weights['dyZhi']
        total_score += apply_branch_score(4, weights['dyZhi'])
        
        # LN (5)
        if len(pillars) > 5 and pillars[5]: 
            max_possible_score += weights['lnZhi']
            total_score += apply_branch_score(5, weights['lnZhi'])

    # --- 2. Determine Status ---
    neutral_min = max_possible_score * 0.48
    neutral_max = max_possible_score * 0.52

    level = ''
    if total_score > neutral_max: level = '身强'
    elif total_score < neutral_min: level = '身弱'
    else: level = '中和'

    # Override Logic
    if level == '中和' and is_guan_yin:
        level = '身强'
        logs.append('官印相生助旺')

    # --- 3. Alerts ---
    alerts = []
    if len(pillars) > 5:
        dy = pillars[4]
        ln = pillars[5]
        month = pillars[1]
        
        # Sui Yun Bing Lin
        if dy['gan'] == ln['gan'] and dy['zhi'] == ln['zhi']:
            alerts.append("【警告】岁运并临：能量极端叠加，运势波动剧烈。")
            
        # Zhan Ke (Tian Ke Di Chong)
        # Helper check control
        def check_gan_ke(g1, g2):
            w1 = GAN_WX.get(g1)
            w2 = GAN_WX.get(g2)
            return WX_RELATION.get(w1, {}).get(w2) == '克'

        is_tian_ke = check_gan_ke(ln['gan'], month['gan']) or check_gan_ke(month['gan'], ln['gan'])
        
        chong_pairs = [{'子', '午'}, {'丑', '未'}, {'寅', '申'}, {'卯', '酉'}, {'辰', '戌'}, {'巳', '亥'}]
        pair_set = {ln['zhi'], month['zhi']}
        is_di_chong = pair_set in chong_pairs
        
        if is_tian_ke and is_di_chong:
            alerts.append("【预警】流年与月令战克：环境震荡，根基不稳。")

    return {
        'total_score': total_score,
        'max_possible_score': max_possible_score,
        'level': level,
        'logs': logs,
        'alerts': alerts,
        'is_guan_yin': is_guan_yin
    }

def calculate_global_scores(pillars):
    weights = {'stem': 7, 'zhi': [10, 45, 20, 10, 20, 30]} # Year, Month, Day, Hour, DY, LN
    scores = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
    
    # Get modifications from He Hua / He Ban
    stem_mods = get_stem_interactions_map(pillars)
    
    for idx, p in enumerate(pillars):
        if not p: continue
        
        # Stem Logic
        gan = p['gan']
        orig_wx = GAN_WX.get(gan)
        
        mod = stem_mods.get(idx)
        if mod:
            if mod['status'] == 'he_hua':
                # Use transformed element
                target_wx = mod['target_wx']
                if target_wx: scores[target_wx] += weights['stem']
            else:
                # He Ban: Reduced score (x0.6)
                if orig_wx: scores[orig_wx] += weights['stem'] * 0.6
        else:
            if orig_wx: scores[orig_wx] += weights['stem']
        
        # Zhi Logic
        zhi_wx = ZHI_WX.get(p['zhi'])
        zhi_weight = weights['zhi'][idx] if idx < len(weights['zhi']) else 10
        if zhi_wx: scores[zhi_wx] += zhi_weight
        
    return scores

def get_five_element_profile(pillars):
    scores = calculate_global_scores(pillars)
    total = sum(scores.values())
    dm = pillars[2]['gan']
    dm_wx = GAN_WX.get(dm)
    
    # Debug info
    # print(f"DEBUG PROFILE: DM={dm}, WX={dm_wx}, Scores={scores}")

    RELATION_MAP = {
        '同': '比劫',
        '生': '食伤', 
        '克': '财',
        '被克': '官杀',
        '被生': '印'
    }

    # WX Relationships relative to DM (Explicit Definition)
    WX_RELATION_LOCAL = {
        '木': { '木': '同', '火': '生', '土': '克', '金': '被克', '水': '被生' },
        '火': { '木': '被生', '火': '同', '土': '生', '金': '克', '水': '被克' },
        '土': { '木': '被克', '火': '被生', '土': '同', '金': '生', '水': '克' },
        '金': { '木': '克', '火': '被克', '土': '被生', '金': '同', '水': '生' },
        '水': { '木': '生', '火': '克', '土': '被克', '金': '被生', '水': '同' }
    }
    
    result = []
    threshold = total * 0.20
    
    for el in ['木', '火', '土', '金', '水']:
        rel_type = WX_RELATION_LOCAL.get(dm_wx, {}).get(el)
        ten_god = RELATION_MAP.get(rel_type, '?')
        score = scores[el]
        is_strong = score >= threshold
        
        result.append({
            'element': el,
            'tenGod': ten_god,
            'score': score,
            'isStrong': is_strong,
            'desc': f"{el}({ten_god}){'强' if is_strong else '弱'}"
        })
        
    return result


def get_tomb_warehouse_status(pillars, scores):
    """
    Determine specific 'Tomb'(墓) vs 'Warehouse'(库) status for Earth branches.
    Returns a dict mapping index -> status ('Warehouse' or 'Tomb' or None).
    """
    # 1. Config
    # Chen->Water, Xu->Fire, Chou->Metal, Wei->Wood
    TARGET_MAP = {'辰': '水', '戌': '火', '丑': '金', '未': '木'}
    # Producing: Water<-Metal, Fire<-Wood, Metal<-Earth, Wood<-Water
    PRODUCING_MAP = {'水': '金', '火': '木', '金': '土', '木': '水'}
    GAN_WX_MAP = GAN_WX # Reuse global
    
    stems = [p['gan'] for p in pillars if p]
    stems_wx = [GAN_WX_MAP.get(s) for s in stems]
    
    # Calculate Total Score for Percentage
    total_score = sum(scores.values())
    if total_score == 0: total_score = 1
    
    results = {}
    
    for idx, p in enumerate(pillars):
        if not p: continue
        zhi = p['zhi']
        
        target_wx = TARGET_MAP.get(zhi)
        if not target_wx:
            continue # Not an Earth Tomb/Warehouse branch
            
        # Condition A: Score > 20%
        target_score = scores.get(target_wx, 0)
        ratio = target_score / total_score
        cond_a = ratio > 0.20
        
        # Condition B: Stem Revealed (Target OR Producing)
        # Check if ANY stem corresponds to Target or Producing Element
        producing_wx = PRODUCING_MAP.get(target_wx)
        cond_b = False
        
        if producing_wx:
            # Check stems
            # Logic: Check raw stems. Even if bound, counts.
            for wx in stems_wx:
                if wx == target_wx or wx == producing_wx:
                    cond_b = True
                    break
        
        if cond_a and cond_b:
            results[idx] = {'type': 'Warehouse', 'desc': '库'}
        else:
            results[idx] = {'type': 'Tomb', 'desc': '墓'}
            
    return results

def get_all_earth_statuses(pillars, scores):
    """
    Calculate Warehouse/Tomb status for ALL 4 Earth branches (Chen, Xu, Chou, Wei).
    Logic (User Refined - Priority Filtering):
    - Priority 1 (Identity Anchor): If Branch has Main Qi Root (e.g. Zi/Hai for Water), Locked as Warehouse.
    - Priority 2 (Image Anchor): If Stem Revealed (Target/Producing), Locked as Warehouse.
    - Priority 3 (Score threshold): Only if neither above, check Residual/Hidden accumulation > 12.
    """
    TARGET_MAP = {'辰': '水', '戌': '火', '丑': '金', '未': '木'}
    PRODUCING_MAP = {'水': '金', '火': '木', '金': '土', '木': '水'}
    
    # 1. Prepare Data
    stems = [p.get('gan') for p in pillars if p and p.get('gan')]
    branches = [p.get('zhi') for p in pillars if p and p.get('zhi')]
    stems_wx = [GAN_WX.get(s) for s in stems]

    results = {}
    
    for zhi in ['辰', '戌', '丑', '未']:
        target_wx = TARGET_MAP.get(zhi)
        producing_wx = PRODUCING_MAP.get(target_wx)
        
        status_type = 'Tomb' # Default
        desc = '墓'
        
        # Priority 1: Identity Anchor (Main Qi Root)
        # Check if any branch's Main Qi matches Target
        has_root = False
        for b_zhi in branches:
            if ZHI_WX.get(b_zhi) == target_wx:
                has_root = True
                break
        
        if has_root:
            results[zhi] = {'type': 'Warehouse', 'desc': '库'}
            continue # Locked
            
        # Priority 2: Image Anchor (Stem Revealed)
        is_revealed = False
        for wx in stems_wx:
            if wx == target_wx or wx == producing_wx:
                is_revealed = True
                break
        
        if is_revealed:
            results[zhi] = {'type': 'Warehouse', 'desc': '库'}
            continue # Locked
            
        # Priority 3: Residual Score Threshold
        # Only reached if No Root and No Stem.
        # Check accumulation of Hidden Stems.
        residual_score = 0
        for b_zhi in branches:
            hidden_stems = HIDDEN_STEMS_MAP.get(b_zhi, [])
            for h_stem in hidden_stems:
                if GAN_WX.get(h_stem) == target_wx:
                    residual_score += 8 # Hidden Qi weight
                    break
        
        # Threshold > 12 (e.g. 2 Tombs = 16 > 12)
        if residual_score > 12:
            results[zhi] = {'type': 'Warehouse', 'desc': '库'}
        else:
            results[zhi] = {'type': 'Tomb', 'desc': '墓'}

    return results

def calculate_yong_xi_ji(pillars, bs_result):
    scores = calculate_global_scores(pillars)
    sorted_details = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top1 = sorted_details[0]
    top2 = sorted_details[1]
    total_score = sum(scores.values())
    
    # Helpers
    idx_map = {'木': 0, '火': 1, '土': 2, '金': 3, '水': 4}
    rev_idx_map = {0: '木', 1: '火', 2: '土', 3: '金', 4: '水'}
    
    def get_bridge(w1, w2):
        id1, id2 = idx_map[w1], idx_map[w2]
        if (id1 + 2) % 5 == id2: return rev_idx_map[(id1 + 1) % 5]
        if (id2 + 2) % 5 == id1: return rev_idx_map[(id2 + 1) % 5]
        return ''
        
    result = {'mode': '', 'yong': '', 'xi': '', 'ji': '', 'reason': ''}
    
    # 1. Mediation
    bridge = get_bridge(top1[0], top2[0])
    diff = abs(top1[1] - top2[1])
    
    if bridge and diff < 15:
        bridge_score = scores[bridge]
        combined = top1[1] + top2[1]
        if bridge_score < 25 or bridge_score < combined * 0.3:
            result['mode'] = '通关'
            result['yong'] = bridge
            result['xi'] = rev_idx_map[(idx_map[bridge] - 1 + 5) % 5]
            result['ji'] = rev_idx_map[(idx_map[bridge] - 2 + 5) % 5]
            result['reason'] = f"两强对峙，取通关用神"
            return result
            
    # 2. Climate
    mz = pillars[1]['zhi']
    is_winter = mz in ['亥', '子', '丑']
    is_summer = mz in ['巳', '午', '未']
    threshold = total_score * 0.25
    
    if is_winter:
        if scores['火'] < threshold:
            needed = True
            # Simple check, skip complex logic for now
            if needed:
                result['mode'] = '调候'
                result['yong'] = '火'
                result['xi'] = '木'
                result['ji'] = '水, 金'
                result['reason'] = "冬生严寒，取火调候"
                return result
                
    elif is_summer:
        if scores['水'] < threshold:
            result['mode'] = '调候'
            result['yong'] = '水'
            result['xi'] = '金'
            result['ji'] = '火, 土'
            result['reason'] = "夏生酷热，取水调候"
            return result
            
    # 3. Balancing
    level = bs_result['level']
    result['mode'] = '扶抑'
    dm = pillars[2]['gan']
    dm_wx = GAN_WX.get(dm)
    dm_idx = idx_map[dm_wx]
    
    def get_el(offset): return rev_idx_map[(dm_idx + offset) % 5]
    
    id_map = {'木': 0, '火': 1, '土': 2, '金': 3, '水': 4}
    
    seal = get_el(4) # -1
    official = get_el(3) # -2
    wealth = get_el(2) # +2
    output = get_el(1) # +1
    same = dm_wx
    
    if level in ['弱', '极弱']:
        # Weak -> Use Seal or Same
        guan = scores[official]
        cai = scores[wealth]
        shi = scores[output]
        
        # Priority: If Guan is heavy -> Seal
        if guan > (cai + shi) * 0.8:
            result['yong'] = seal
            result['xi'] = same
            result['ji'] = f"{wealth}, {output}"
            result['reason'] = "身弱官杀旺，首取印星化杀"
        elif cai > (guan + shi) * 0.8:
            result['yong'] = same
            result['xi'] = seal
            result['ji'] = f"{output}, {wealth}" # Cai breaks Seal
            result['reason'] = "身弱财旺，首取比劫帮身"
        elif shi > (guan + cai) * 0.8:
            result['yong'] = seal
            result['xi'] = same
            result['ji'] = f"{output}, {wealth}"
            result['reason'] = "身弱食伤泄气，取印制食生身"
        else:
             # Default Weak
             result['yong'] = seal
             result['xi'] = same
             result['ji'] = f"{wealth}, {output}, {official}"
             
    else:
        # Strong -> Use Output, Wealth, Official
        # Priority: Depends on what is available. 
        # Simplified logic:
        # If Seal is heavy -> Wealth breaks Seal
        # If Same is heavy -> Official controls Same
        
        seal_score = scores[seal]
        same_score = scores[same]
        
        if seal_score > same_score:
            result['yong'] = wealth
            result['xi'] = output
            result['ji'] = f"{seal}, {same}"
            result['reason'] = "身旺印旺，喜财坏印"
        else:
            result['yong'] = official
            result['xi'] = wealth
            result['ji'] = f"{same}, {seal}"
            result['reason'] = "身旺比劫旺，喜官杀制身"
            
    # --- Override Logic (User Patch) ---
    total_energy = sum(scores.values())
    fire_ratio = scores.get('火', 0) / total_energy if total_energy > 0 else 0
    
    # 1. Fire Scorched Earth (火多土焦)
    if dm_wx == '土' and fire_ratio > 0.40:
        result['yong'] = wealth # Water
        result['xi'] = output # Metal
        result['ji'] = f"{seal}, {official}" # Fire, Wood
        result['reason'] = "检测到【火多土焦】：印星过旺导致土质干裂，强制取水润局，金为助水之臣。"
    
    # 2. Guan Yin Refinement (官印局细分)
    # Note: bs passed in might be dict or object, check usage
    if bs_result.get('isGuanYin'):
        fire_score = scores.get('火', 0)
        # Assuming Guan Yin context implies Wood -> Fire -> Earth usually? 
        # But here we just follow the rule:
        if fire_score < 40:
             # Standard Guan Yin
             result['yong'] = official # Wood
             result['xi'] = wealth # Water (as per user snippet, implies favoring "Water" to support Wood?) 
             # Wait, user snippet says: return {"yong_shen": "木", "xi_shen": "水", "ji_shen": "火/土"}
             result['ji'] = f"{seal}, {same}"
        else:
             # Fire too strong
             result['yong'] = wealth # Water
             result['xi'] = official # Wood
             result['ji'] = seal # Fire
             # Keeping reason or appending? The user snippet returns distinct object.
             # We should probably update reason too if it wasn't set by step 1
             if dm_wx == '土' and fire_ratio > 0.40:
                 pass # Already handled above with specific reason
             else:
                 result['reason'] = "官印局但火气偏旺，取财(水)损印，喜官(木)生水"

    # 3. Universal Heavy Seal, Light Body (印重身轻 - 虚强实弱 - 通用版)
    # Logic: Body Strength Score > 52 AND Seal Ratio > 0.7
    group_a_score = scores.get(seal, 0) + scores.get(same, 0)
    
    # 52 is roughly 43%-45% of 120, or maybe the user implies a percentage scaled to 100?
    # Assuming user's 52 refers to my generic score scale where passing 40-50 is "passing".
    # My neutral min/max is usually calculated, but let's stick to the user's explicit > 52 if using raw scores.
    # Or better, check if 'level' is Strong (which implies > 52ish usually)
    
    # Let's use the explicit logic provided:
    # "if total_score > 52" -> referring to Strength Score (Seal + Same).
    
    seal_score = scores.get(seal, 0)
    # Lowered threshold from 52 to 40 to catch charts like 1996-3-22 (Group A ~44)
    # "Heavy Seal" allows for "False Strong", so absolute strength doesn't need to be > 52.
    if group_a_score > 40: 
        seal_ratio = seal_score / group_a_score if group_a_score > 0 else 0
        
        # Check Season Support (Month Zhi)
        mz = pillars[1]['zhi']
        mz_wx = ZHI_WX.get(mz)
        # Relation: Subject=Seal, Object=Month. If Seal is 'Sheng' (Born/Generated) by Month -> True
        # WX_RELATION[Seal][Month] == '生' (Seal is generated by Month)
        # OR Month IS Seal (Same element support)
        season_supports_seal = (mz_wx == seal) or (WX_RELATION.get(seal, {}).get(mz_wx) == '生')
        
        # New Trigger: > 70% OR (> 60% AND Season Supports)
        if seal_ratio > 0.7 or (seal_ratio > 0.6 and season_supports_seal):
            # Mapping
            # Wood DM (Seal=Water) -> Water heavy Wood floats -> Wealth(Earth) stops Water. Xi=Fire. Ji=Metal.
            # Fire DM (Seal=Wood) -> Wood heavy Fire smothered -> Wealth(Metal) chops Wood. Xi=Earth. Ji=Water.
            # Earth DM (Seal=Fire) -> Fire heavy Earth scorched -> Wealth(Water) cools. Xi=Metal. Ji=Wood.
            # Metal DM (Seal=Earth) -> Earth heavy Metal buried -> Wealth(Wood) loosens Earth. Xi=Water. Ji=Fire.
            # Water DM (Seal=Metal) -> Metal heavy Water cold -> Wealth(Fire) warms/controls. Xi=Wood. Ji=Earth.
            
            mapping = {
                '木': {'desc': '水多木漂', 'reason': '水多木漂，取土(财)止水，喜火(食伤)暖局', 'yong': wealth},
                '火': {'desc': '木多火塞', 'reason': '木多火塞，取金(财)劈木，喜土(食伤)泄秀', 'yong': wealth},
                '土': {'desc': '火多土焦', 'reason': '火多土焦，取水(财)润局，喜金(食伤)助水', 'yong': wealth},
                '金': {'desc': '土多金埋', 'reason': '土多金埋，取木(财)疏土，喜水(食伤)洗金', 'yong': wealth},
                '水': {'desc': '金多水浊', 'reason': '金多水浊，取火(财)炼金，喜木(食伤)泄秀', 'yong': wealth}
            }
            
            # Additional robustness for Water case (User said "金多水寒" in snippet, traditionally "金多水浊" or "寒")
            # User snippet: 'Water': {'yong': 'Fire', 'result': '金多水寒，取火暖局'}
            
            info = mapping.get(dm_wx)
            if info:
                # Update Mode for Tiao Hou cases (Fire Scorched Earth / Metal Cold Water)
                if dm_wx in ['土', '水']:
                    result['mode'] = '调候'
                else:
                    result['mode'] = '扶抑' # Or 病药, but sticking to standard classification
                    
                result['yong'] = info['yong']
                result['xi'] = output
                result['ji'] = official
                result['type_desc'] = info['desc'] # New field for UI display
                
                extra_msg = ""
                if seal_ratio <= 0.7:
                     extra_msg = " (得月令之助)"
                
                result['reason'] = f"检测到【印重身轻】：{info['reason']}。(印星占比: {int(seal_ratio*100)}%{extra_msg})"

    return result
