# -*- coding: utf-8 -*-
"""
知学 TV —— 从幼儿园到高中的大屏学习应用原型
================================================
面向泉州台商投资区在读学生的本地化大屏学习应用原型，
桌面亦可运行演示。操作方式（模拟遥控器）：方向键移动焦点，回车确认，ESC 返回。

知识体系：幼儿园 / 小学 / 初中 / 高中 全学段 + 全学科，贴合福建省教学大纲与教材版本
本地化特色：
  · 泉州台商投资区本地升学政策与学区信息（首页本地服务入口）
  · 中考政策专区：对标泉州中考 800 分制、6月21-23日省级统考日程
  · 本地学情数据：全区 7.5 万在校生、11 所中学、42 所小学
  · 12 大 AI 辅导场景（错题精讲、随时答疑、学习规划、口语陪练、
    作文批改、编程辅导、古诗文赏析、口算闯关、科学实验、听力训练、历史故事、心理陪伴）
"""

import os
import sys
import json
import random

# ---------- Kivy 环境设置（必须在导入 kivy 模块前）----------
os.environ.setdefault("KIVY_NO_ARGS", "1")
os.environ.setdefault("KIVY_NO_CONSOLELOG", "1")

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.behaviors import FocusBehavior
from kivy.graphics import (
    Color, RoundedRectangle, Rectangle, Ellipse, Line,
)
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import (
    StringProperty, ListProperty, BooleanProperty, NumericProperty, ObjectProperty,
)
from kivy.metrics import dp, sp
from kivy.core.text import LabelBase

# TV 标准分辨率
TV_W, TV_H = 1280, 720
Window.size = (TV_W, TV_H)

# ---------- 全局配色 ----------
C = {
    "bg":         (0.07, 0.09, 0.14, 1),
    "bg2":        (0.10, 0.13, 0.20, 1),
    "panel":      (0.13, 0.17, 0.26, 1),
    "panel_hi":   (0.18, 0.23, 0.34, 1),
    "white":      (1, 1, 1, 1),
    "gray":       (0.72, 0.76, 0.84, 1),
    "gray2":      (0.50, 0.55, 0.66, 1),
    "accent":     (0.98, 0.62, 0.24, 1),   # 橙
    "accent2":    (0.26, 0.72, 0.96, 1),   # 蓝
    "green":      (0.28, 0.82, 0.55, 1),
    "red":        (0.96, 0.40, 0.46, 1),
    "yellow":     (1.00, 0.84, 0.32, 1),
    "purple":     (0.66, 0.48, 0.96, 1),
    "pink":       (0.96, 0.48, 0.78, 1),
}

STAGE_COLOR = {
    "幼儿园": (1.00, 0.76, 0.30, 1),
    "小学":   (0.30, 0.80, 0.55, 1),
    "初中":   (0.32, 0.66, 0.96, 1),
    "高中":   (0.84, 0.46, 0.94, 1),
}

# ---------- 台商投资区本地服务数据 ----------
LOCAL_SERVICES = [
    {
        "id": "policy", "title": "本地升学政策", "icon": "📋", "color": (0.30, 0.72, 0.96, 1),
        "desc": "2026 台商区义务教育招生、中考中招政策解读",
        "lines": [
            "【招生】公办小学 42 所，2025 秋季一年级招生 3725 人",
            "【学位】湖东学园（师院附小台商区分校+泉州五中台商区分校）实行落户截止 3月1日、产权超 50%、六年一学位",
            "【中考】总分 800 分，省级统考 6月21-23日；2025 台商区一级达标校入围线 698.9 分",
            "【咨询】台商区招考办 27395510；泉州五中台商区分校 2025 录取线 718.4 分",
            "【学位】2025 全区 15 所新改扩建校开工，新增公办学位 5940 个",
        ],
    },
    {
        "id": "schools", "title": "身边好学校", "icon": "🏫", "color": (0.98, 0.62, 0.24, 1),
        "desc": "台商区优质校与教育共同体，找准学习榜样",
        "lines": [
            "泉州师院附属小学台商区分校：2025 招生 868 人，全区规模最大的小学",
            "泉州五中台商区分校：2025 首届高一录取线 718.4 分，对标泉州五中本部",
            "泉州惠南中学：省一级达标高中，2025 录取线 678.7 分",
            "泉州台商区实验高级中学：民办高中，2025 计划 576.6 分",
            "泉州第十七中学：省二级达标高中，2025 录取线 576.6 分",
            "名优校+教育共同体、5G+专递课堂，城乡共享优质资源",
        ],
    },
    {
        "id": "gaokao", "title": "中考政策专区", "icon": "🎯", "color": (0.96, 0.40, 0.46, 1),
        "desc": "福建新中考 800 分制全解析，提前规划备考节奏",
        "lines": [
            "【总分】语文150+数学150+英语150+物理90+化学60+道法50+历史50+地理30+生物30+体育40=800 分",
            "【统考】6月21日 语文/数学；6月22日 物理/化学/英语；6月23日 历史/道法/地理/生物",
            "【体育】满分 40 分，安排在 4-5 月测试，往届生须重考",
            "【等级】10 门等级性考试 + 9 门等级底线要求，理化生实验操作 5 月考查",
            "【录取】全市普通高中最低控制线 425 分；中外课程实验班 629 分",
            "【提醒】2026 中考已进入倒计时，合理分配 800 分的每一分",
        ],
    },
    {
        "id": "minnan", "title": "闽南文化课堂", "icon": "🌊", "color": (0.40, 0.86, 0.70, 1),
        "desc": "海丝起点、闽南风韵，让学习扎根家乡",
        "lines": [
            "【海丝起点】泉州是联合国认定的海上丝绸之路起点，台商区洛阳桥列入世界遗产",
            "【洛阳桥】宋代四大名桥之首，蔡襄主持修建，走在桥上就是一堂活历史课",
            "【南音】世界级非物质文化遗产，古汉语活化石，唱腔保留唐宋遗韵",
            "【闽南语】厝（家）、呷饭（吃饭）、日头（太阳），方言里的古汉语密码",
            "【侨乡】台商区是著名侨乡，下南洋的故事是近代史最生动的注脚",
        ],
    },
]

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "progress.json")


# ============================================================
# 知识体系：幼儿园 -> 高中，全学段全学科
# ============================================================
def build_courses():
    """构建 K12 全学段课程数据"""
    data = {}

    # ---------------- 幼儿园 ----------------
    data["幼儿园"] = {
        "语言启蒙": [
            "认识拼音 a o e", "声母 b p m f", "简单儿歌朗诵",
            "看图说话入门", "绘本阅读《猜猜我有多爱你》", "认识常见汉字 20 个",
        ],
        "趣味数学": [
            "认识数字 1~10", "数数与配对", "比多少", "认识形状", "简单分类", "5 以内加法",
        ],
        "快乐英语": [
            "ABC 字母歌", "颜色与动物单词", "日常问候 Hi/Hello", "数字 one~ten", "水果单词",
        ],
        "艺术创想": [
            "涂色与线条", "折纸小手工", "简笔画入门", "认识三原色", "撕贴画",
        ],
        "健康安全": [
            "洗手七步法", "交通安全儿歌", "保护牙齿", "不乱吃东西", "我的身体",
        ],
        "社会常识": [
            "家庭与成员", "认识职业", "垃圾分类", "礼貌用语", "分享与合作",
        ],
    }

    # ---------------- 小学 ----------------
    data["小学"] = {
        "语文": [
            "拼音与声调", "汉字结构与笔顺", "查字典方法", "古诗《静夜思》赏析",
            "写人作文：我的妈妈", "阅读理解：归纳中心思想", "修辞手法：比喻与拟人",
            "口语交际：看图说话", "成语故事与运用", "记叙文写作",
        ],
        "数学": [
            "100 以内加减法", "乘法口诀表", "认识钟表与人民币", "长方形与正方形周长",
            "分数初步认识", "小数加减法", "几何图形面积", "鸡兔同笼问题", "行程问题",
            "统计图与可能性",
        ],
        "英语": [
            "26 个字母与发音", "日常问候与自我介绍", "颜色/动物/食物词汇",
            "There be 句型", "一般现在时", "现在进行时", "阅读短文理解", "英语小故事",
        ],
        "科学": [
            "植物的生长", "动物分类与特征", "水的三态变化", "磁铁与磁力",
            "天气与季节", "太阳系认识", "简单电路", "声音的产生",
        ],
        "道德与法治": [
            "我是小学生", "我爱我的家", "我们的班级", "规则与秩序", "爱护环境",
        ],
    }

    # ---------------- 初中 ----------------
    data["初中"] = {
        "语文": [
            "文言文《论语》十二章", "古诗词鉴赏：意象与情感", "记叙文阅读与写作",
            "说明文结构与说明方法", "议论文三要素", "名著《朝花夕拾》导读",
            "修辞手法综合运用", "作文：审题与立意", "口语交际与综合性学习",
        ],
        "数学": [
            "有理数与绝对值", "一元一次方程", "二元一次方程组", "一元一次不等式",
            "一次函数与图像", "全等三角形", "相似三角形", "勾股定理", "二次函数",
            "圆的性质与计算", "统计与概率",
        ],
        "英语": [
            "时态综合：现在完成时", "被动语态", "宾语从句与定语从句",
            "情态动词用法", "阅读长难句技巧", "写作：书信与应用文", "听力专项训练",
            "词汇拓展与构词法",
        ],
        "物理": [
            "声音的产生与传播", "光的反射与折射", "凸透镜成像规律", "力的三要素",
            "牛顿第一定律", "压强与浮力", "简单机械与功", "欧姆定律", "电功率",
        ],
        "化学": [
            "物质的变化与性质", "元素与化学式", "化学方程式配平", "质量守恒定律",
            "酸碱盐的性质", "常见气体的制取", "金属与金属材料", "溶液与溶解度",
        ],
        "生物": [
            "细胞的结构与功能", "光合作用与呼吸作用", "人体的消化系统",
            "血液循环与心脏", "遗传与变异", "生态系统与食物链",
        ],
        "历史": [
            "秦朝统一与中央集权", "丝绸之路", "唐宋经济繁荣", "明清君主专制",
            "鸦片战争与近代史开端", "抗日战争", "新中国的成立", "世界古代文明",
        ],
        "地理": [
            "地球与地图", "天气与气候类型", "世界海陆分布", "中国地形与气候",
            "人口与聚落", "区域发展差异",
        ],
        "道德与法治": [
            "青春期心理与健康", "法律基础与未成年人保护", "宪法与公民权利",
            "责任与担当", "民族团结与国家统一",
        ],
    }

    # ---------------- 高中 ----------------
    data["高中"] = {
        "语文": [
            "文言文实词与虚词", "文言文特殊句式", "诗歌鉴赏：意境与手法",
            "论述类文本阅读", "文学类文本阅读", "作文：思辨性写作", "整本书阅读《红楼梦》",
            "古代文化常识",
        ],
        "数学": [
            "集合与常用逻辑用语", "函数与导数", "三角函数与解三角形",
            "数列与数学归纳法", "立体几何", "解析几何：圆锥曲线", "概率与统计",
            "复数与向量", "不等式选讲",
        ],
        "英语": [
            "非谓语动词", "定语从句与状语从句", "名词性从句", "虚拟语气",
            "完形填空技巧", "阅读理解：推理判断", "七选五解题策略", "读后续写",
            "应用文写作", "高考高频词汇",
        ],
        "物理": [
            "匀变速直线运动", "牛顿运动定律", "曲线运动与万有引力", "机械能守恒",
            "动量守恒", "电场与磁场", "电磁感应", "交流电与电磁波", "近代物理基础",
        ],
        "化学": [
            "原子结构与元素周期律", "化学键与分子结构", "化学反应速率与平衡",
            "电化学：原电池与电解池", "有机化学基础", "同分异构体",
            "化学实验方案设计", "工业流程题突破",
        ],
        "生物": [
            "细胞代谢与酶", "DNA 结构与复制", "基因的表达与调控", "基因突变与进化",
            "内环境稳态", "生态系统与能量流动", "基因工程与生物技术",
        ],
        "历史": [
            "中国古代政治制度演变", "中国经济结构变动", "思想解放潮流",
            "世界市场的形成", "两次世界大战", "冷战与多极化趋势", "改革开放与现代化",
        ],
        "地理": [
            "大气环流与气候", "洋流与水循环", "地质作用与地貌", "人口迁移与城市化",
            "农业与工业区位", "区域可持续发展", "旅游地理与环境保护",
        ],
        "思想政治": [
            "中国特色社会主义", "经济生活：市场与宏观调控", "政治生活：政府与公民",
            "文化生活：中华文化", "生活与哲学：唯物辩证法", "法治与国家治理",
        ],
    }
    # 追加泉州台商区本地特色内容
    data["_local"] = {
        "海丝文化": [
            "泉州：海上丝绸之路起点", "洛阳桥：宋代四大名桥之首", "九日山祈风石刻与海丝贸易",
            "开元寺与东西塔：多元宗教共存", "蟳埔女与蚵壳厝：海洋民居智慧",
        ],
        "闽南非遗": [
            "南音：中国音乐活化石", "提线木偶戏的操纵技艺", "惠安女服饰与文化符号",
            "泉州刻纸与花灯制作", "闽南语中的古汉语遗存",
        ],
        "家乡地理": [
            "洛阳江与泉州湾的水系", "台商区的海岸线与滩涂", "泉州湾湿地与候鸟迁徙",
            "福建地形：八山一水一分田", "台风与福建的气候特点",
        ],
        "泉州历史": [
            "古代海上贸易与市舶司", "郑和下西洋与泉州港", "明清海禁与迁界",
            "闽南华侨下南洋史", "改革开放后的泉州模式",
        ],
    }
    return data


# ============================================================
# AI 辅导：12 大场景定义
# ============================================================
AI_SCENES = [
    {
        "id": "wrong", "title": "错题精讲", "icon": "📝", "color": C["red"],
        "desc": "拍照或录入错题，AI 定位错因，举一反三",
        "hints": ["把这道错题讲一遍", "我总在同一个地方错", "帮我出几道同类题"],
    },
    {
        "id": "qa", "title": "随时答疑", "icon": "💡", "color": C["accent"],
        "desc": "任何学科难题，多轮启发式讲解",
        "hints": ["这道题怎么想", "为什么这样做", "还有别的方法吗"],
    },
    {
        "id": "plan", "title": "学习规划", "icon": "🎯", "color": C["green"],
        "desc": "对标泉州 800 分制与本区高中，生成专属提分计划",
        "hints": ["帮我规划期末复习", "数学太弱怎么补", "想考泉州五中台商区分校"],
        "tool": True,   # 工具型场景：进入专属规划工作台
    },
    {
        "id": "oral", "title": "口语陪练", "icon": "🗣️", "color": C["accent2"],
        "desc": "AI 外教情景对话，练发音与表达",
        "hints": ["模拟餐厅点餐", "聊聊我的周末", "纠正我的发音"],
    },
    {
        "id": "essay", "title": "作文批改", "icon": "✍️", "color": C["purple"],
        "desc": "智能点评结构、立意、文采",
        "hints": ["帮我改这篇作文", "立意怎么提升", "结尾怎么升华"],
    },
    {
        "id": "code", "title": "编程辅导", "icon": "💻", "color": C["pink"],
        "desc": "Python / Scratch 一对一教学",
        "hints": ["教我做贪吃蛇", "Scratch 怎么做动画", "这段代码为什么报错"],
    },
    {
        "id": "poem", "title": "古诗文赏析", "icon": "📜", "color": (0.90, 0.70, 0.30, 1),
        "desc": "名家名篇精讲，背景、意象、鉴赏",
        "hints": ["赏析《水调歌头》", "这首诗的意象", "作者写时的心境"],
    },
    {
        "id": "calc", "title": "口算闯关", "icon": "🔢", "color": (0.40, 0.86, 0.70, 1),
        "desc": "分学段心算训练，即时判对错",
        "hints": ["出 10 道口算题", "两位数乘一位数", "计时挑战"],
    },
    {
        "id": "sci", "title": "科学实验", "icon": "🔬", "color": (0.50, 0.74, 1.00, 1),
        "desc": "在家能做的趣味实验，原理+步骤",
        "hints": ["在家做的化学实验", "彩虹牛奶怎么做", "火山喷发小实验"],
    },
    {
        "id": "listen", "title": "听力训练", "icon": "🎧", "color": (0.74, 0.62, 1.00, 1),
        "desc": "分级英语听力，听后答题反馈",
        "hints": ["初中听力专项", "VOA 慢速练习", "听后给我出几道题"],
    },
    {
        "id": "history", "title": "历史故事", "icon": "🏛️", "color": (0.86, 0.62, 0.46, 1),
        "desc": "把朝代与事件讲成故事",
        "hints": ["讲讲赤壁之战", "丝绸之路的故事", "秦始皇统一六国"],
    },
    {
        "id": "mind", "title": "心理陪伴", "icon": "🤗", "color": (1.00, 0.66, 0.78, 1),
        "desc": "考前焦虑、同伴压力，随时倾诉",
        "hints": ["考试前很紧张", "和同学闹别扭了", "学不进去怎么办"],
    },
]


def ai_reply(scene_id, user_text):
    """模拟 AI 回复（启发式教学，不给直答案）"""
    t = user_text.strip()
    base = {
        "wrong": "我们先一起读一遍这道题，看看它到底在问什么。你觉得关键条件藏在哪一句里？",
        "qa": "好问题！我们不直接给答案，先一起想想：已知条件里哪些能用？",
        "plan": "我先帮你做一次小诊断。你最近哪一类题错得最多？说出来我们一起定计划。",
        "oral": "Great! Let's talk. Imagine we're at a cafe — what would you like to order?",
        "essay": "我读了你的作文。先说说亮点：开头很抓人。再想想——如果把中间这段换个角度，会不会更有力？",
        "code": "我们来拆解一下。程序要做成什么效果？先写出步骤，再一行行转成代码，好不好？",
        "poem": "这首词写于中秋之夜。词人望着月亮，心里想的却是'人长久'。你觉得这个意象妙在哪里？",
        "calc": "第 1 题：12 × 4 = ?  先在心里算，说出答案，我来判对错！",
        "sci": "这个实验超好玩！先猜猜会怎样——把洗洁精滴入牛奶，会发生什么？原理和'表面张力'有关哦。",
        "listen": "现在开始播放一段小对话，仔细听，听完后我会问你一个问题。准备好了吗？",
        "history": "那是一个风起云涌的夜晚。赤壁江面上火光冲天——你想先听周瑜，还是诸葛亮？",
        "mind": "我在听呢。慢慢说，不着急。是最近发生了什么事，让你有这种感觉吗？",
    }
    return base.get(scene_id, "我们一起想办法，你先说说自己的想法？")


# ============================================================
# 通用绘图工具
# ============================================================
def rounded_rect(canvas, pos, size, radius=12, color=(1, 1, 1, 1), width=None, outline=None):
    with canvas:
        Color(*color)
        if width and outline:
            RoundedRectangle(pos=pos, size=size, radius=[radius], width=0)
            Color(*outline)
            RoundedRectangle(pos=pos, size=size, radius=[radius], width=width)
        else:
            RoundedRectangle(pos=pos, size=size, radius=[radius])


# ============================================================
# 焦点卡片（TV 核心：可获焦 + 高亮）
# ============================================================
class FocusCard(FocusBehavior, Widget):
    """可获焦卡片：获得焦点时显示高亮框并轻微放大"""
    title = StringProperty("")
    sub = StringProperty("")
    bg_color = ListProperty([0.13, 0.17, 0.26, 1])
    accent_color = ListProperty([0.98, 0.62, 0.24, 1])
    scale = NumericProperty(1.0)
    radius = NumericProperty(18)
    show_focus = BooleanProperty(True)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.size_hint = (None, None)
        self.bind(pos=self._redraw, size=self._redraw, scale=self._redraw)
        self._bg = None
        self._focus_box = None
        self._title_lbl = None
        self._sub_lbl = None
        Clock.schedule_once(lambda dt: self._build_content(), 0)

    def _build_content(self):
        from kivy.uix.label import Label
        self._title_lbl = Label(
            text=self.title, font_size=sp(26), color=C["white"],
            bold=True, halign="left", valign="top",
            text_size=(self.width - dp(36), None),
            size_hint=(None, None),
            pos=(self.x + dp(18), self.y + self.height - dp(56)),
        )
        self._title_lbl.size = (self.width - dp(36), dp(40))
        self._sub_lbl = Label(
            text=self.sub, font_size=sp(16), color=C["gray"],
            halign="left", valign="top",
            text_size=(self.width - dp(36), None),
            size_hint=(None, None),
            pos=(self.x + dp(18), self.y + dp(16)),
        )
        self._sub_lbl.size = (self.width - dp(36), dp(60))
        self.add_widget(self._title_lbl)
        self.add_widget(self._sub_lbl)
        self._redraw()

    def _redraw(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(
                pos=(self.x + dp(2), self.y + dp(2)),
                size=(self.width - dp(4), self.height - dp(4)),
                radius=[self.radius],
            )
            if self.show_focus and self.focus:
                Color(*self.accent_color)
                RoundedRectangle(
                    pos=(self.x, self.y), size=(self.width, self.height),
                    radius=[self.radius], width=dp(4),
                )
        if self._title_lbl:
            self._title_lbl.text = self.title
            self._title_lbl.pos = (self.x + dp(18), self.y + self.height - dp(56))
            self._title_lbl.text_size = (self.width - dp(36), None)
        if self._sub_lbl:
            self._sub_lbl.text = self.sub
            self._sub_lbl.pos = (self.x + dp(18), self.y + dp(16))
            self._sub_lbl.text_size = (self.width - dp(36), None)

    def on_focus(self, *a):
        target = 1.06 if self.focus else 1.0
        anim = Animation(scale=target, d=0.12, t="out_quad")
        cx, cy = self.center
        def _anchor(a_self, p):
            self.center = cx, cy
        anim.bind(on_progress=_anchor)
        anim.start(self)
        self._redraw()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.focus = True
            self.dispatch("on_activate")
            return True
        return super().on_touch_down(touch)

    def on_activate(self):
        pass


# ============================================================
# 各类型卡片
# ============================================================
class StageCard(FocusCard):
    def __init__(self, stage, **kw):
        self.stage = stage
        color = STAGE_COLOR.get(stage, C["accent"])
        kw.setdefault("size", (dp(260), dp(150)))
        kw.setdefault("bg_color", C["panel"])
        kw.setdefault("accent_color", color)
        kw.setdefault("title", stage)
        kw.setdefault("sub", {"幼儿园": "启蒙·趣味", "小学": "习惯·基础",
                              "初中": "思维·进阶", "高中": "冲刺·拔高"}[stage])
        super().__init__(**kw)
        Clock.schedule_once(lambda dt: self._add_badge(color), 0)

    def _add_badge(self, color):
        with self.canvas:
            Color(*color)
            Ellipse(pos=(self.x + dp(16), self.y + self.height - dp(52)),
                    size=(dp(26), dp(26)))


class SubjectCard(FocusCard):
    def __init__(self, subject, lessons, **kw):
        self.subject = subject
        self.lessons = lessons
        kw.setdefault("size", (dp(300), dp(120)))
        kw.setdefault("bg_color", C["panel"])
        kw.setdefault("title", subject)
        kw.setdefault("sub", f"{len(lessons)} 节课 · 点击进入")
        super().__init__(**kw)


class LessonItem(FocusCard):
    show_focus = BooleanProperty(True)
    def __init__(self, title, idx, duration, **kw):
        self.idx = idx
        self.duration = duration
        kw.setdefault("size", (dp(720), dp(70)))
        kw.setdefault("radius", 12)
        kw.setdefault("title", f"{idx:02d}  {title}")
        m, s = divmod(duration, 60)
        kw.setdefault("sub", f"{m}:{s:02d}  ·  未学习")
        super().__init__(**kw)
        Clock.schedule_once(lambda dt: self._add_play(), 0)

    def _add_play(self):
        from kivy.uix.label import Label
        if not self._sub_lbl:
            return
        self._play = Label(
            text="▶", font_size=sp(20), color=C["accent"],
            size_hint=(None, None), size=(dp(30), dp(30)),
            pos=(self.x + self.width - dp(44), self.y + dp(22)),
        )
        self.add_widget(self._play)


class SceneCard(FocusCard):
    def __init__(self, scene, **kw):
        self.scene = scene
        kw.setdefault("size", (dp(300), dp(120)))
        kw.setdefault("bg_color", C["panel"])
        kw.setdefault("accent_color", scene["color"])
        kw.setdefault("title", f"{scene['icon']}  {scene['title']}")
        kw.setdefault("sub", scene["desc"])
        super().__init__(**kw)


# ============================================================
# 聊天气泡
# ============================================================
class ChatBubble(BoxLayout):
    def __init__(self, text, mine=False, **kw):
        kw.setdefault("size_hint", (1, None))
        kw.setdefault("orientation", "vertical")
        kw.setdefault("padding", (dp(8), dp(4)))
        super().__init__(**kw)
        inner = FloatLayout(size_hint=(None, None))
        lbl = Label(
            text=text, font_size=sp(20),
            color=C["white"] if mine else C["bg"],
            halign="left", valign="top",
            text_size=(dp(560), None),
            size_hint=(None, None),
        )
        lbl.bind(texture_size=lbl.setter("size"))
        w = min(dp(600), lbl.texture_size[0] + dp(32))
        h = max(dp(46), lbl.texture_size[1] + dp(24))
        inner.size = (w, h)
        bgc = C["accent"] if mine else (0.92, 0.94, 0.98, 1)
        with inner.canvas.before:
            Color(*bgc)
            RoundedRectangle(
                pos=(dp(620) - w if mine else dp(20), dp(4)),
                size=(w, h), radius=[14],
            )
        lbl.pos = (dp(632) - w if mine else dp(32), h - lbl.texture_size[1] - dp(10))
        inner.add_widget(lbl)
        self.add_widget(inner)
        self.height = h + dp(12)


# ============================================================
# 圆形头像
# ============================================================
class AvatarChip(Widget):
    def __init__(self, text="知", color=None, **kw):
        kw.setdefault("size_hint", (None, None))
        kw.setdefault("size", (dp(40), dp(40)))
        super().__init__(**kw)
        self.text = text
        self.color = color or C["accent"]
        Clock.schedule_once(lambda dt: self._draw(), 0)

    def _draw(self):
        from kivy.uix.label import Label
        with self.canvas:
            Color(*self.color)
            Ellipse(pos=self.pos, size=self.size)
        self.clear_widgets()
        lb = Label(
            text=self.text, font_size=sp(20), color=C["white"], bold=True,
            size=self.size, pos=self.pos,
            halign="center", valign="center",
        )
        self.add_widget(lb)


# ============================================================
# 页面：学段选择
# ============================================================
class StageScreen(Screen):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.name = "stage"
        root = FloatLayout()
        # 背景
        with root.canvas.before:
            Color(*C["bg"])
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        # 标题
        self.title_lbl = Label(
            text="知学 TV · 泉州台商区", font_size=sp(52), color=C["white"], bold=True,
            size_hint=(None, None), size=(dp(500), dp(70)),
            pos=(dp(60), TV_H - dp(150)),
        )
        root.add_widget(self.title_lbl)
        root.add_widget(Label(
            text="从幼儿园到高中 · 泉州台商投资区在读学生专属 · 方向键选择，回车进入",
            font_size=sp(22), color=C["gray"],
            size_hint=(None, None), size=(dp(700), dp(40)),
            pos=(dp(62), TV_H - dp(205)),
        ))
        # 卡片网格
        grid = GridLayout(
            cols=4, spacing=dp(28), size_hint=(None, None),
            size=(dp(260*4+28*3), dp(150*2+28)),
            pos=(dp(60), TV_H - dp(430)),
        )
        stages = ["幼儿园", "小学", "初中", "高中"]
        for s in stages:
            card = StageCard(stage=s)
            card.bind(on_activate=lambda c: self.app.open_subjects(c.stage))
            grid.add_widget(card)
        root.add_widget(grid)
        # AI 辅导入口
        ai = FocusCard(
            title="🤖  AI 智能辅导", sub="12 大辅导场景 · 随时答疑",
            size=(dp(405), dp(110)), bg_color=C["panel_hi"],
            accent_color=C["accent2"], pos=(dp(60), dp(146)),
        )
        ai.bind(on_activate=lambda c: self.app.open_ai_hall())
        root.add_widget(ai)
        # 本地服务 3 张卡片
        srv = [
            ("📋  本地升学政策", "招生 · 中考 · 学区"),
            ("🏫  身边好学校",   "台商区优质校盘点"),
            ("🎯  中考政策专区", "800 分制全解析"),
        ]
        for i, (t, sub) in enumerate(srv):
            c = FocusCard(
                title=t, sub=sub, size=(dp(405), dp(110)),
                bg_color=C["panel_hi"], accent_color=LOCAL_SERVICES[i]["color"],
                pos=(dp(60 + 465 * (i + 1)), dp(146)),
            )
            c.bind(on_activate=lambda c, i=i: self.app.open_local(LOCAL_SERVICES[i]["id"]))
            root.add_widget(c)
        root.add_widget(ai)
        # 底部提示
        root.add_widget(Label(
            text="← → ↑ ↓  移动选择       ⏎  确认       ESC  返回       🌊 泉州台商区在读学生专属",
            font_size=sp(18), color=C["gray2"],
            size_hint=(None, None), size=(dp(600), dp(30)),
            pos=(dp(60), dp(40)),
        ))
        self.add_widget(root)


# ============================================================
# 页面：学科选择
# ============================================================
class SubjectScreen(Screen):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.name = "subject"
        self.root = FloatLayout()
        with self.root.canvas.before:
            Color(*C["bg"])
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        self.add_widget(self.root)

    def load(self, stage):
        self.root.clear_widgets()
        self.stage = stage
        with self.root.canvas.before:
            Color(*C["bg"])
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        color = STAGE_COLOR.get(stage, C["accent"])
        self.root.add_widget(Label(
            text=f"{stage}  ·  选择学科", font_size=sp(44), color=C["white"], bold=True,
            size_hint=(None, None), size=(dp(600), dp(60)),
            pos=(dp(60), TV_H - dp(130)),
        ))
        self.root.add_widget(Label(
            text="← 返回学段选择", font_size=sp(18), color=C["gray2"],
            size_hint=(None, None), size=(dp(300), dp(30)),
            pos=(dp(60), TV_H - dp(180)),
        ))
        subjects = self.app.courses.get(stage, {})
        cols = 3
        card_w, card_h = dp(300), dp(120)
        gap = dp(24)
        n = len(subjects)
        rows = (n + cols - 1) // cols
        grid_h = rows * card_h + (rows - 1) * gap
        grid = GridLayout(
            cols=cols, spacing=gap, size_hint=(None, None),
            size=(cols * card_w + (cols - 1) * gap, grid_h),
            pos=(dp(60), TV_H - dp(220) - grid_h),
        )
        for sub, lessons in subjects.items():
            card = SubjectCard(subject=sub, lessons=lessons)
            card.accent_color = color
            card.bind(on_activate=lambda c: self.app.open_lessons(stage, c.subject))
            grid.add_widget(card)
        self.root.add_widget(grid)


# ============================================================
# 页面：课时列表
# ============================================================
class LessonScreen(Screen):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.name = "lesson"
        self.root = FloatLayout()
        with self.root.canvas.before:
            Color(*C["bg"])
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        self.add_widget(self.root)

    def load(self, stage, subject):
        self.root.clear_widgets()
        self.stage, self.subject = stage, subject
        with self.root.canvas.before:
            Color(*C["bg"])
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        color = STAGE_COLOR.get(stage, C["accent"])
        self.root.add_widget(Label(
            text=f"{stage}  ›  {subject}", font_size=sp(40), color=C["white"], bold=True,
            size_hint=(None, None), size=(dp(800), dp(56)),
            pos=(dp(60), TV_H - dp(130)),
        ))
        lessons = self.app.courses.get(stage, {}).get(subject, [])
        self.root.add_widget(Label(
            text=f"共 {len(lessons)} 节课", font_size=sp(18), color=C["gray"],
            size_hint=(None, None), size=(dp(300), dp(30)),
            pos=(dp(60), TV_H - dp(176)),
        ))
        # 滚动列表
        sv = ScrollView(
            size_hint=(None, None), size=(dp(760), dp(420)),
            pos=(dp(60), dp(90)),
            bar_width=dp(6), bar_color=color,
        )
        box = BoxLayout(orientation="vertical", size_hint=(None, None),
                        spacing=dp(12), width=dp(720))
        box.bind(minimum_height=box.setter("height"))
        for i, title in enumerate(lessons):
            item = LessonItem(title=title, idx=i + 1, duration=random.randint(180, 900))
            item.accent_color = color
            item.bind(on_activate=lambda c: self.app.open_player(
                stage, subject, c.idx - 1, c.title.split("  ", 1)[-1]))
            box.add_widget(item)
        sv.add_widget(box)
        self.root.add_widget(sv)
        self.root.add_widget(Label(
            text="↑↓ 滚动列表   ⏎ 播放   ESC 返回", font_size=sp(18), color=C["gray2"],
            size_hint=(None, None), size=(dp(500), dp(30)), pos=(dp(60), dp(40)),
        ))


# ============================================================
# 页面：学习播放页
# ============================================================
class PlayerScreen(Screen):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.name = "player"
        self.root = FloatLayout()
        with self.root.canvas.before:
            Color(0.04, 0.05, 0.09, 1)
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        self.add_widget(self.root)
        self.playing = True
        self.progress = 0.0
        self.quiz_shown = False

    def load(self, stage, subject, idx, title):
        self.root.clear_widgets()
        self.stage, self.subject, self.idx, self.title = stage, subject, idx, title
        self.playing = True
        self.progress = 0.0
        self.quiz_shown = False
        with self.root.canvas.before:
            Color(0.04, 0.05, 0.09, 1)
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        color = STAGE_COLOR.get(stage, C["accent"])
        # 模拟视频区
        vid = FocusCard(
            title="", sub="", size=(dp(840), dp(380)), bg_color=(0.06, 0.08, 0.13, 1),
            accent_color=color, show_focus=False,
            pos=(dp(60), dp(200)),
        )
        with vid.canvas:
            Color(0.06, 0.08, 0.13, 1)
            RoundedRectangle(pos=(vid.x, vid.y), size=vid.size, radius=[16])
            Color(*color)
            Ellipse(pos=(vid.center_x - dp(45), vid.center_y - dp(45)), size=(dp(90), dp(90)))
            Color(1, 1, 1, 0.95)
            Rectangle(pos=(vid.center_x - dp(16), vid.center_y - dp(22)), size=(dp(16), dp(44)))
            Rectangle(pos=(vid.center_x + dp(6), vid.center_y - dp(22)), size=(dp(16), dp(44)))
        self.root.add_widget(vid)
        self.root.add_widget(Label(
            text=f"正在学习 · {self.title}", font_size=sp(30), color=C["white"], bold=True,
            size_hint=(None, None), size=(dp(840), dp(44)), pos=(dp(60), TV_H - dp(140)),
        ))
        self.root.add_widget(Label(
            text=f"{stage}  ›  {subject}", font_size=sp(20), color=C["gray"],
            size_hint=(None, None), size=(dp(840), dp(30)), pos=(dp(60), TV_H - dp(185)),
        ))
        # 进度条
        self.bar = ProgressBar(
            max=1.0, value=0.0, size_hint=(None, None),
            size=(dp(840), dp(10)), pos=(dp(60), dp(140)),
        )
        self.root.add_widget(self.bar)
        self.time_lbl = Label(
            text="00:00 / 10:00", font_size=sp(18), color=C["gray"],
            size_hint=(None, None), size=(dp(200), dp(28)), pos=(dp(60), dp(110)),
        )
        self.root.add_widget(self.time_lbl)
        # 操作按钮
        self.btn_pause = FocusCard(
            title="⏸  暂停", sub="", size=(dp(160), dp(60)),
            bg_color=C["panel_hi"], accent_color=color, show_focus=True, pos=(dp(760), dp(60)),
        )
        self.btn_pause.bind(on_activate=lambda c: self.toggle())
        self.root.add_widget(self.btn_pause)
        btn_quiz = FocusCard(
            title="📝  随堂测验", sub="", size=(dp(200), dp(60)),
            bg_color=C["panel_hi"], accent_color=C["yellow"], show_focus=True,
            pos=(dp(560), dp(60)),
        )
        btn_quiz.bind(on_activate=lambda c: self.show_quiz())
        self.root.add_widget(btn_quiz)
        self.root.add_widget(Label(
            text="ESC 返回课程列表", font_size=sp(18), color=C["gray2"],
            size_hint=(None, None), size=(dp(300), dp(28)), pos=(dp(60), dp(60)),
        ))
        Clock.schedule_interval(self._tick, 0.2)

    def _tick(self, dt):
        if not self.playing:
            return
        self.progress += 0.004
        if self.progress >= 1.0:
            self.progress = 1.0
        self.bar.value = self.progress
        total = 600
        cur = int(self.progress * total)
        m, s = divmod(cur, 60)
        tm, ts = divmod(total, 60)
        self.time_lbl.text = f"{m:02d}:{s:02d} / {tm:02d}:{ts:02d}"
        if self.progress >= 0.5 and not self.quiz_shown:
            self.quiz_shown = True
            self.show_quiz()

    def toggle(self):
        self.playing = not self.playing
        self.btn_pause.title = "⏸  暂停" if self.playing else "▶  播放"
        self.btn_pause._redraw()

    def show_quiz(self):
        self.playing = False
        content = BoxLayout(orientation="vertical", spacing=dp(16), padding=dp(24))
        content.add_widget(Label(
            text="随堂测验", font_size=sp(28), color=C["white"], bold=True,
            size_hint=(1, None), height=dp(40),
        ))
        q = "下面哪个数是质数？"
        content.add_widget(Label(
            text=q, font_size=sp(22), color=C["white"], halign="left",
            text_size=(dp(520), None), size_hint=(1, None), height=dp(40),
        ))
        for opt in ["A. 12", "B. 17", "C. 21", "D. 24"]:
            content.add_widget(Button(
                text=opt, font_size=sp(20), color=C["white"],
                background_color=(0.18, 0.23, 0.34, 1),
                size_hint=(1, None), height=dp(48),
            ))
        content.add_widget(Label(
            text="答案 B. 17 —— 只能被 1 和自身整除的数叫质数。",
            font_size=sp(18), color=C["green"],
            size_hint=(1, None), height=dp(40), halign="left",
        ))
        popup = Popup(
            title="", content=content, size_hint=(None, None),
            size=(dp(600), dp(360)), background_color=(0.10, 0.13, 0.20, 0.97),
            separator_height=0,
        )
        btn = Button(
            text="继续学习", font_size=sp(20), color=C["white"],
            background_color=(0.98, 0.62, 0.24, 1),
            size_hint=(None, None), size=(dp(200), dp(44)),
            pos_hint={"center_x": 0.5},
        )
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        popup.open()
        popup.bind(on_dismiss=lambda p: setattr(self, "playing", True))

    def on_leave(self, *a):
        Clock.unschedule(self._tick)


# ============================================================
# 页面：AI 辅导场景大厅
# ============================================================
# ============================================================
# 数据：泉州中考 800 分制学科权重
# ============================================================
# 原始分 / 折算分：语数英各150(原始)，物理90、化学60、历史道法各50、
# 地理生物各30、体育40，合计800分
EXAM_WEIGHTS = [
    {"name": "语文", "score": 150, "mode": "原始", "tag": "语数英合计450分，最大变量"},
    {"name": "数学", "score": 150, "mode": "原始", "tag": "拉分主战场，错题闭环最关键"},
    {"name": "英语", "score": 150, "mode": "原始", "tag": "含听力30分，可提前抢分"},
    {"name": "物理", "score": 90,  "mode": "折算90%", "tag": "100分卷按90%计入"},
    {"name": "化学", "score": 60,  "mode": "折算60%", "tag": "100分卷按60%计入"},
    {"name": "道德与法治", "score": 50, "mode": "折算50%", "tag": "开卷记忆，性价比高"},
    {"name": "历史", "score": 50,  "mode": "折算50%", "tag": "时间线梳理即可拿分"},
    {"name": "地理", "score": 30,  "mode": "折算30%", "tag": "八年级末已考完"},
    {"name": "生物", "score": 30,  "mode": "折算30%", "tag": "八年级末已考完"},
    {"name": "体育与健康", "score": 40, "mode": "原始", "tag": "最易白拿的40分"},
]

# 台商区高中目标（2025 统招录取线，供目标倒推）
TARGET_SCHOOLS = [
    {"name": "泉州五中台商区分校", "line": 720, "color": (0.96, 0.40, 0.46, 1),
     "note": "全区顶尖，对标泉州五中本部"},
    {"name": "泉州惠南中学", "line": 683.6, "color": (0.98, 0.62, 0.24, 1),
     "note": "省一级达标高中，稳扎稳打可冲"},
    {"name": "台商区实验高级中学", "line": 576.6, "color": (0.32, 0.66, 0.96, 1),
     "note": "民办高中，保底选择"},
    {"name": "泉州第十七中学", "line": 425, "color": (0.66, 0.48, 0.96, 1),
     "note": "全市普高最低控制线附近"},
]

# 每周可用学习时长档位（单位：小时）
WEEK_HOURS = {"1小时": 7, "1.5小时": 10.5, "2小时": 14, "3小时+": 21}

# 800 分制下各科"性价比系数"（按单点投入可贡献到总分的权重，越高越该先补）
def _priority(sub):
    base = sub["score"]
    if sub["mode"] == "原始":
        base *= 1.0
    elif sub["mode"] == "折算90%":
        base *= 0.9
    elif sub["mode"] == "折算60%":
        base *= 0.6
    elif sub["mode"] in ("折算50%",):
        base *= 0.5
    else:
        base *= 0.3
    return round(base)


# ============================================================
# 页面：学习规划工作台（台商区专属）
# ============================================================
class PlanScreen(Screen):
    """
    学习规划工作台：三步走
      ① 目标选择 —— 选定目标高中（自动算出 800 分制差距）
      ② 学科权重 —— 按 800 分制展示各科分值与性价比排序
      ③ 周计划表 —— 按可用时长生成 7 天提分安排
    所有数据来自台商区真实分数线与泉州 800 分制。
    """
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.name = "plan"
        self.step = 0
        self.target = None
        self.weak = []
        self.hours = None
        self.root = FloatLayout()
        with self.root.canvas.before:
            Color(*C["bg"])
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        self.add_widget(self.root)

    # ---------- 生命周期 ----------
    def load(self):
        self.root.clear_widgets()
        self.step = 0
        self.target = None
        self.weak = []
        self.hours = None
        with self.root.canvas.before:
            Color(*C["bg"])
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        self._draw_header()
        self._draw_step1()
        self._draw_footer()

    # ---------- 绘制：顶部标题 ----------
    def _draw_header(self):
        self.root.add_widget(Label(
            text="🎯  学习规划 · 台商区专属",
            font_size=sp(38), color=C["white"], bold=True,
            size_hint=(None, None), size=(dp(800), dp(54)),
            pos=(dp(60), TV_H - dp(125)),
        ))
        self.root.add_widget(Label(
            text="对标泉州中考 800 分制与本区高中录取线，倒推你的提分路线",
            font_size=sp(18), color=C["gray"],
            size_hint=(None, None), size=(dp(800), dp(28)),
            pos=(dp(62), TV_H - dp(168)),
        ))
        # 步骤进度条
        steps = ["① 选目标高中", "② 诊断薄弱学科", "③ 生成周计划"]
        bx = dp(60)
        for i, s in enumerate(steps):
            done = i < self.step
            cur = i == self.step
            clr = C["green"] if done else (C["accent"] if cur else C["panel_hi"])
            w = dp(380)
            with self.root.canvas:
                Color(*clr)
                RoundedRectangle(pos=(bx, TV_H - dp(200)), size=(w, dp(8)),
                                 radius=[dp(4)])
            self.root.add_widget(Label(
                text=s, font_size=sp(16),
                color=C["white"] if (done or cur) else C["gray2"],
                size_hint=(None, None), size=(w, dp(26)),
                pos=(bx, TV_H - dp(228)),
            ))
            bx += w + dp(20)

    def _draw_footer(self):
        txt = {
            0: "← → 选择目标高中 · 回车确认",
            1: "← → 切换学科 · 回车标记为薄弱 · 完成键下一步",
            2: "← → 选择每日时长 · 回车生成计划表",
        }.get(self.step, "")
        self.root.add_widget(Label(
            text=txt, font_size=sp(18), color=C["accent2"],
            size_hint=(None, None), size=(dp(800), dp(30)),
            pos=(dp(60), dp(30)),
        ))
        self.root.add_widget(Label(
            text="ESC 返回场景大厅", font_size=sp(16), color=C["gray2"],
            size_hint=(None, None), size=(dp(260), dp(24)),
            pos=(dp(1000), dp(34)),
        ))

    # ---------- 步骤一：选目标高中 ----------
    def _draw_step1(self):
        self.root.add_widget(Label(
            text="第一步：你想冲刺哪所高中？录取线越高，规划越精确。",
            font_size=sp(20), color=C["yellow"],
            size_hint=(None, None), size=(dp(900), dp(32)),
            pos=(dp(60), TV_H - dp(270)),
        ))
        self._cards = []
        y = TV_H - dp(330)
        for i, sc in enumerate(TARGET_SCHOOLS):
            gap = sc["line"] - 800  # 占位，第二步会重算
            card = FocusCard(
                title=f"{sc['name']}  ·  录取线 {sc['line']} 分",
                sub=sc["note"],
                size=(dp(1140), dp(72)), bg_color=C["panel"],
                accent_color=sc["color"], show_focus=True,
            )
            card.school = sc
            card.bind(on_activate=lambda c: self._pick_target(c.school))
            card.pos = (dp(60), y)
            self.root.add_widget(card)
            self._cards.append(card)
            y -= dp(86)
        Clock.schedule_once(lambda dt: self._cards[0].focus_set(), 0.1)

    def _pick_target(self, school):
        self.target = school
        self.step = 1
        self._redraw()

    # ---------- 步骤二：诊断薄弱学科 ----------
    def _draw_step2(self):
        gap = self.target["line"]
        self.root.add_widget(Label(
            text=f"目标：{self.target['name']}（{self.target['line']} 分）",
            font_size=sp(20), color=self.target["color"], bold=True,
            size_hint=(None, None), size=(dp(600), dp(32)),
            pos=(dp(60), TV_H - dp(270)),
        ))
        self.root.add_widget(Label(
            text=f"要在 800 分里拿到 {self.target['line']} 分，语数英三科合计需稳定在约 {int(self.target['line']*0.56)} 分以上",
            font_size=sp(17), color=C["gray"],
            size_hint=(None, None), size=(dp(900), dp(28)),
            pos=(dp(62), TV_H - dp(306)),
        ))
        self.root.add_widget(Label(
            text="回车标记你的薄弱学科（标红的即为重点提分项）：",
            font_size=sp(20), color=C["yellow"],
            size_hint=(None, None), size=(dp(900), dp(32)),
            pos=(dp(60), TV_H - dp(348)),
        ))
        # 按性价比排序
        ranked = sorted(EXAM_WEIGHTS, key=_priority, reverse=True)
        self._cards = []
        cols = 2
        cw, ch = dp(560), dp(92)
        x0, y0 = dp(60), TV_H - dp(410)
        for i, sub in enumerate(ranked):
            col, row = i % cols, i // cols
            x = x0 + col * (cw + dp(20))
            y = y0 - row * (ch + dp(14))
            is_weak = sub["name"] in self.weak
            card = FocusCard(
                title=f"{sub['name']}  {sub['score']} 分（{sub['mode']}）",
                sub=("★ 薄弱项 · " if is_weak else "") + sub["tag"],
                size=(cw, ch),
                bg_color=C["red"] if is_weak else C["panel"],
                accent_color=C["red"] if is_weak else C["accent2"],
                show_focus=True,
            )
            card.subject = sub
            card.bind(on_activate=lambda c: self._toggle_weak(c.subject))
            card.pos = (x, y)
            self.root.add_widget(card)
            self._cards.append(card)
        # 完成按钮
        done = FocusCard(
            title=f"下一步：生成计划 →  已选 {len(self.weak)} 个薄弱项",
            sub="", size=(dp(1140), dp(56)),
            bg_color=C["green"], accent_color=C["green"], show_focus=True,
        )
        done.bind(on_activate=lambda c: self._to_plan())
        done.pos = (dp(60), y0 - 5 * (ch + dp(14)))
        self.root.add_widget(done)
        self._done_card = done

    def _toggle_weak(self, sub):
        if sub["name"] in self.weak:
            self.weak.remove(sub["name"])
        else:
            self.weak.append(sub["name"])
        self._redraw()

    def _to_plan(self):
        if not self.weak:
            self.weak = [EXAM_WEIGHTS[1]["name"], EXAM_WEIGHTS[3]["name"]]  # 默认数学、物理
        self.step = 2
        self._redraw()

    # ---------- 步骤三：生成周计划 ----------
    def _draw_step3(self):
        self.root.add_widget(Label(
            text="第三步：每天能投入多少学习时间？我会按比例分配。",
            font_size=sp(20), color=C["yellow"],
            size_hint=(None, None), size=(dp(900), dp(32)),
            pos=(dp(60), TV_H - dp(270)),
        ))
        self._cards = []
        hours_list = list(WEEK_HOURS.keys())
        cw = dp(270)
        x0 = dp(60)
        for i, h in enumerate(hours_list):
            card = FocusCard(
                title=f"每天 {h}",
                sub=f"每周约 {WEEK_HOURS[h]} 小时",
                size=(cw, dp(80)), bg_color=C["panel"],
                accent_color=C["accent2"], show_focus=True,
            )
            card.hkey = h
            card.bind(on_activate=lambda c: self._pick_hours(c.hkey))
            card.pos = (x0 + i * (cw + dp(16)), TV_H - dp(380))
            self.root.add_widget(card)
            self._cards.append(card)

    def _pick_hours(self, hkey):
        self.hours = hkey
        self._build_plan()

    def _build_plan(self):
        """按 800 分制权重 × 薄弱项 × 可用时长，生成 7 天计划"""
        total = WEEK_HOURS[self.hours]
        # 薄弱项占 60%，其余学科按权重分剩余 40%
        weak_total = total * 0.6
        weak_hours = {}
        if self.weak:
            per = weak_total / len(self.weak)
            for w in self.weak:
                weak_hours[w] = round(per * 2) / 2  # 0.5 精度
        other_total = total - sum(weak_hours.values())
        others = [s["name"] for s in EXAM_WEIGHTS if s["name"] not in self.weak]
        other_hours = {}
        if others:
            # 按权重分配
            weights = {s["name"]: _priority(s) for s in EXAM_WEIGHTS if s["name"] in others}
            tot_w = sum(weights.values()) or 1
            for name, w in weights.items():
                other_hours[name] = round(other_total * w / tot_w * 2) / 2
        plan_hours = {**weak_hours, **other_hours}
        # 生成 7 天：周末加重难点
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        day_plan = {d: [] for d in days}
        # 薄弱项每日必修
        for d in days:
            for sub, hrs in weak_hours.items():
                if hrs <= 0:
                    continue
                day_plan[d].append((sub, hrs / 7))
        # 其他学科分散
        for sub, hrs in other_hours.items():
            if hrs <= 0:
                continue
            # 分给工作日
            per = hrs / 5
            for d in days[:5]:
                day_plan[d].append((sub, per))
        # 周末专项：薄弱项做综合
        for d in days[5:]:
            for sub, hrs in weak_hours.items():
                day_plan[d].append((sub, hrs / 7 * 0.5))

        # 绘制计划表
        self.root.clear_widgets()
        self._draw_header()
        self.root.add_widget(Label(
            text=f"📋  7 天提分计划表  目标 {self.target['name']}（{self.target['line']}分） · 每天 {self.hours} · 每周 {total} 小时",
            font_size=sp(20), color=C["green"], bold=True,
            size_hint=(None, None), size=(dp(1100), dp(32)),
            pos=(dp(60), TV_H - dp(270)),
        ))
        # 表头
        col_w = dp(150)
        x0 = dp(60)
        y0 = TV_H - dp(320)
        with self.root.canvas:
            Color(*C["panel_hi"])
            RoundedRectangle(pos=(x0, y0), size=(dp(1140), dp(40)), radius=[dp(8)])
        self.root.add_widget(Label(text="学科", font_size=sp(16), color=C["white"],
            size_hint=(None, None), size=(col_w, dp(30)), pos=(x0 + dp(10), y0 + dp(6))))
        for i, d in enumerate(days):
            self.root.add_widget(Label(
                text=d, font_size=sp(15), color=C["accent2"],
                size_hint=(None, None), size=(col_w, dp(30)),
                pos=(x0 + dp(150) + i * col_w, y0 + dp(6))))
        # 行
        ranked = sorted(EXAM_WEIGHTS, key=_priority, reverse=True)
        ry = y0 - dp(48)
        for sub in ranked:
            h = plan_hours.get(sub["name"], 0)
            if h <= 0:
                continue
            is_weak = sub["name"] in self.weak
            with self.root.canvas:
                Color(*(C["red"] if is_weak else C["panel"]))
                RoundedRectangle(pos=(x0, ry - dp(6)), size=(dp(1140), dp(40)),
                                 radius=[dp(6)])
            self.root.add_widget(Label(
                text=f"{'★' if is_weak else ' '}{sub['name']} {sub['score']}分",
                font_size=sp(15), color=C["white"],
                size_hint=(None, None), size=(col_w, dp(30)),
                pos=(x0 + dp(10), ry + dp(4))))
            for i, d in enumerate(days):
                cell = day_plan[d]
                spent = sum(hh for nm, hh in cell if nm == sub["name"])
                txt = f"{spent:.1f}h" if spent > 0 else "—"
                self.root.add_widget(Label(
                    text=txt, font_size=sp(15),
                    color=C["yellow"] if is_weak and spent > 0 else C["gray"],
                    size_hint=(None, None), size=(col_w, dp(30)),
                    pos=(x0 + dp(150) + i * col_w, ry + dp(4))))
            ry -= dp(46)
        # 底部建议
        tips = self._gen_tips()
        self.root.add_widget(Label(
            text="💡 提分建议：" + "  |  ".join(tips),
            font_size=sp(16), color=C["accent"],
            size_hint=(None, None), size=(dp(1140), dp(28)),
            pos=(dp(62), dp(78)),
        ))
        self.root.add_widget(Label(
            text="ESC 返回场景大厅 · 完成！你可以截图保存这份计划",
            font_size=sp(18), color=C["accent2"],
            size_hint=(None, None), size=(dp(700), dp(30)),
            pos=(dp(60), dp(30)),
        ))

    def _gen_tips(self):
        tips = []
        if "数学" in self.weak:
            tips.append("数学用错题精讲建闭环，同错因题连做 3 道")
        if "语文" in self.weak or "英语" in self.weak:
            tips.append("语英每天朗读 15 分钟，古诗文赏析+听力训练交替")
        if "物理" in self.weak:
            tips.append("物理先抓实验题，科学实验场景看原理再刷题")
        if "道德与法治" in self.weak or "历史" in self.weak:
            tips.append("政史开卷记忆性价比高，睡前 10 分钟过时间线")
        if not tips:
            tips.append("薄弱项每日必修，周末做综合卷检验")
        tips.append("体育 40 分最容易白拿，别在考场丢分")
        return tips

    # ---------- 重绘 ----------
    def _redraw(self):
        self.root.clear_widgets()
        with self.root.canvas.before:
            Color(*C["bg"])
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        self._draw_header()
        if self.step == 0:
            self._draw_step1()
        elif self.step == 1:
            self._draw_step2()
        elif self.step == 2:
            self._draw_step3()
        self._draw_footer()

    # ---------- 焦点导航（步骤二/三用方向键）----------
    def on_enter(self):
        if self._cards:
            Clock.schedule_once(lambda dt: self._cards[0].focus_set(), 0.1)


class AIHallScreen(Screen):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.name = "ai_hall"
        self.root = FloatLayout()
        with self.root.canvas.before:
            Color(*C["bg"])
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        self.add_widget(self.root)

    def load(self):
        self.root.clear_widgets()
        with self.root.canvas.before:
            Color(*C["bg"])
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        self.root.add_widget(Label(
            text="🤖  AI 智能辅导", font_size=sp(44), color=C["white"], bold=True,
            size_hint=(None, None), size=(dp(600), dp(60)), pos=(dp(60), TV_H - dp(130)),
        ))
        self.root.add_widget(Label(
            text="12 大辅导场景 · 启发式教学，带你一起思考",
            font_size=sp(20), color=C["gray"],
            size_hint=(None, None), size=(dp(700), dp(30)), pos=(dp(62), TV_H - dp(180)),
        ))
        cols = 4
        card_w, card_h = dp(270), dp(120)
        gap = dp(20)
        n = len(AI_SCENES)
        rows = (n + cols - 1) // cols
        grid_h = rows * card_h + (rows - 1) * gap
        grid = GridLayout(
            cols=cols, spacing=gap, size_hint=(None, None),
            size=(cols * card_w + (cols - 1) * gap, grid_h),
            pos=(dp(60), TV_H - dp(220) - grid_h),
        )
        for sc in AI_SCENES:
            card = SceneCard(scene=sc)
            card.bind(on_activate=lambda c: self.app.open_ai_tutor(c.scene))
            grid.add_widget(card)
        self.root.add_widget(grid)
        self.root.add_widget(Label(
            text="ESC 返回首页", font_size=sp(18), color=C["gray2"],
            size_hint=(None, None), size=(dp(300), dp(30)), pos=(dp(60), dp(40)),
        ))


# ============================================================
# 页面：AI 辅导对话
# ============================================================
class AITutorScreen(Screen):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.name = "ai_tutor"
        self.scene = None
        self.root = FloatLayout()
        with self.root.canvas.before:
            Color(*C["bg"])
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        self.add_widget(self.root)

    def load(self, scene):
        self.root.clear_widgets()
        self.scene = scene
        self.history = []
        with self.root.canvas.before:
            Color(*C["bg"])
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        color = scene["color"]
        self.root.add_widget(Label(
            text=f"{scene['icon']}  {scene['title']}",
            font_size=sp(38), color=C["white"], bold=True,
            size_hint=(None, None), size=(dp(700), dp(54)), pos=(dp(60), TV_H - dp(125)),
        ))
        self.root.add_widget(Label(
            text=scene["desc"], font_size=sp(18), color=C["gray"],
            size_hint=(None, None), size=(dp(700), dp(28)), pos=(dp(62), TV_H - dp(168)),
        ))
        # 对话区
        self.chat_box = BoxLayout(orientation="vertical", size_hint=(None, None),
                                  spacing=dp(10), padding=(dp(20), dp(10)),
                                  width=dp(1100))
        self.chat_box.bind(minimum_height=self.chat_box.setter("height"))
        self.sv = ScrollView(
            size_hint=(None, None), size=(dp(1140), dp(330)),
            pos=(dp(60), dp(180)), bar_width=dp(6), bar_color=color,
        )
        self.sv.add_widget(self.chat_box)
        self.root.add_widget(self.sv)
        # 推荐问句
        self.root.add_widget(Label(
            text="试试这样问：", font_size=sp(16), color=C["gray2"],
            size_hint=(None, None), size=(dp(200), dp(26)), pos=(dp(62), dp(150)),
        ))
        hint_box = BoxLayout(
            orientation="horizontal", spacing=dp(12), size_hint=(None, None),
            size=(dp(1100), dp(48)), pos=(dp(60), dp(98)),
        )
        self.hint_cards = []
        for h in scene["hints"]:
            card = FocusCard(
                title=h, sub="", size=(dp(352), dp(44)),
                bg_color=C["panel_hi"], accent_color=color, show_focus=True,
            )
            card.bind(on_activate=lambda c: self._send(c.title, from_hint=True))
            hint_box.add_widget(card)
            self.hint_cards.append(card)
        self.root.add_widget(hint_box)
        # 输入框
        self.input = TextInput(
            hint_text="输入你的问题，按回车发送……",
            font_size=sp(20), foreground_color=C["white"],
            background_color=(0.13, 0.17, 0.26, 1),
            cursor_color=C["accent"], size_hint=(None, None),
            size=(dp(920), dp(52)), pos=(dp(60), dp(30)),
            multiline=False,
        )
        self.input.bind(on_text_validate=self._on_enter)
        self.root.add_widget(self.input)
        btn_send = FocusCard(
            title="发送", sub="", size=(dp(150), dp(52)),
            bg_color=C["accent"], accent_color=color, show_focus=True,
            pos=(dp(1000), dp(30)),
        )
        btn_send.bind(on_activate=lambda c: self._send(self.input.text))
        self.root.add_widget(btn_send)
        self.root.add_widget(Label(
            text="ESC 返回场景大厅", font_size=sp(16), color=C["gray2"],
            size_hint=(None, None), size=(dp(260), dp(24)), pos=(dp(1160), dp(40)),
        ))
        # 开场白
        self._add_bot("你好，我是你的 AI 辅导老师。你可以问我任何学习问题，我会用启发的方式带你一起想，而不是直接给答案。你想聊点什么？")
        Clock.schedule_once(lambda dt: self.input.focus_set(), 0.1)

    def _add_bot(self, text):
        self.history.append(("bot", text))
        row = BoxLayout(orientation="horizontal", size_hint=(1, None),
                        spacing=dp(10), padding=(dp(8), dp(4)))
        row.add_widget(AvatarChip(text="AI", color=self.scene["color"]))
        row.add_widget(ChatBubble(text, mine=False))
        self.chat_box.add_widget(row)
        self._scroll_bottom()

    def _add_mine(self, text):
        self.history.append(("me", text))
        row = BoxLayout(orientation="horizontal", size_hint=(1, None),
                        spacing=dp(10), padding=(dp(8), dp(4)))
        row.add_widget(Widget(size_hint=(1, None), height=dp(1)))
        row.add_widget(ChatBubble(text, mine=True))
        row.add_widget(AvatarChip(text="我", color=C["accent2"]))
        self.chat_box.add_widget(row)
        self._scroll_bottom()

    def _scroll_bottom(self):
        Clock.schedule_once(lambda dt: setattr(self.sv, "scroll_y", 0), 0.05)

    def _on_enter(self, w):
        self._send(w.text)

    def _send(self, text, from_hint=False):
        text = text.strip()
        if not text:
            return
        self._add_mine(text)
        self.input.text = ""
        # 模拟 AI 思考延迟
        def _reply(dt):
            self._add_bot(ai_reply(self.scene["id"], text))
        Clock.schedule_once(_reply, 0.5)


# ============================================================
# 页面：本地服务
# ============================================================
class LocalServiceScreen(Screen):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.name = "local"
        self.root = FloatLayout()
        with self.root.canvas.before:
            Color(*C["bg"])
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        self.add_widget(self.root)

    def load(self, service_id):
        self.root.clear_widgets()
        self.service = next(s for s in LOCAL_SERVICES if s["id"] == service_id)
        with self.root.canvas.before:
            Color(*C["bg"])
            Rectangle(pos=(0, 0), size=(TV_W, TV_H))
        color = self.service["color"]
        self.root.add_widget(Label(
            text=f"{self.service['icon']}  {self.service['title']}",
            font_size=sp(40), color=C["white"], bold=True,
            size_hint=(None, None), size=(dp(900), dp(56)), pos=(dp(60), TV_H - dp(130)),
        ))
        self.root.add_widget(Label(
            text=self.service["desc"], font_size=sp(18), color=C["gray"],
            size_hint=(None, None), size=(dp(900), dp(28)), pos=(dp(62), TV_H - dp(172)),
        ))
        # 条目列表
        sv = ScrollView(size_hint=(None, None), size=(dp(1140), dp(440)),
                        pos=(dp(60), dp(80)), bar_width=dp(6), bar_color=color)
        box = BoxLayout(orientation="vertical", size_hint=(None, None),
                        spacing=dp(10), width=dp(1100), padding=(dp(8), dp(4)))
        box.bind(minimum_height=box.setter("height"))
        for i, line in enumerate(self.service["lines"]):
            item = FocusCard(
                title=f"{(i + 1):02d}  {line[:40]}",
                sub=line[40:] if len(line) > 40 else "",
                size=(dp(1060), dp(74)), radius=12,
                bg_color=C["panel"], accent_color=color,
            )
            box.add_widget(item)
        sv.add_widget(box)
        self.root.add_widget(sv)
        self.root.add_widget(Label(
            text="↑↓ 浏览条目   ESC 返回首页", font_size=sp(18), color=C["gray2"],
            size_hint=(None, None), size=(dp(500), dp(30)), pos=(dp(60), dp(40)),
        ))


# ============================================================
# 主应用
# ============================================================
class ZhiXueTVApp(App):
    def build(self):
        self.courses = build_courses()
        self.sm = ScreenManager()
        self.stage_screen = StageScreen(self)
        self.subject_screen = SubjectScreen(self)
        self.lesson_screen = LessonScreen(self)
        self.player_screen = PlayerScreen(self)
        self.ai_hall = AIHallScreen(self)
        self.ai_tutor = AITutorScreen(self)
        self.plan_screen = PlanScreen(self)
        self.local_screen = LocalServiceScreen(self)
        for s in [self.stage_screen, self.subject_screen, self.lesson_screen,
                  self.player_screen, self.ai_hall, self.ai_tutor,
                  self.plan_screen, self.local_screen]:
            self.sm.add_widget(s)
        self.sm.current = "stage"
        # 键盘映射
        Window.bind(on_key_down=self._on_key)
        # 进度
        self.progress = self._load_progress()
        return self.sm

    # ---------- 导航 ----------
    def open_subjects(self, stage):
        self.subject_screen.load(stage)
        self.sm.current = "subject"

    def open_lessons(self, stage, subject):
        self.lesson_screen.load(stage, subject)
        self.sm.current = "lesson"

    def open_player(self, stage, subject, idx, title):
        self.player_screen.load(stage, subject, idx, title)
        self.sm.current = "player"

    def open_ai_hall(self):
        self.ai_hall.load()
        self.sm.current = "ai_hall"

    def open_ai_tutor(self, scene):
        # 工具型场景（学习规划）进入专属工作台
        if scene.get("tool"):
            self.plan_screen.load()
            self.sm.current = "plan"
            return
        self.ai_tutor.load(scene)
        self.sm.current = "ai_tutor"

    def open_local(self, service_id):
        self.local_screen.load(service_id)
        self.sm.current = "local"

    # ---------- 按键 ----------
    def _on_key(self, w, key, scancode, codepoint, modifier):
        s = self.sm.current
        # ESC 返回
        if key == 27:  # ESC
            if s == "plan":
                self.sm.current = "ai_hall"
            elif s == "ai_tutor":
                self.sm.current = "ai_hall"
            elif s == "ai_hall":
                self.sm.current = "stage"
            elif s == "player":
                self.sm.current = "lesson"
            elif s == "lesson":
                self.sm.current = "subject"
            elif s == "subject":
                self.sm.current = "stage"
            return True
        # 回车：激活当前焦点
        if key in (13, 271):
            w2 = self._current_focus()
            if w2 and hasattr(w2, "dispatch"):
                w2.dispatch("on_activate")
            return True
        # 规划工作台：方向键切换选项
        if s == "plan" and self.sm.current_screen:
            plan = self.sm.current_screen
            if hasattr(plan, "_cards") and plan._cards:
                cur = None
                for c in plan._cards:
                    if getattr(c, "focus", False):
                        cur = c
                        break
                idx = plan._cards.index(cur) if cur else -1
                if key in (275, 276):  # → ←
                    nxt = (idx + (1 if key == 275 else -1)) % len(plan._cards)
                    plan._cards[nxt].focus_set()
                    return True
                if key == 273 and idx > 0:  # ↑
                    plan._cards[idx - 1].focus_set()
                    return True
                if key == 274 and idx < len(plan._cards) - 1:  # ↓
                    plan._cards[idx + 1].focus_set()
                    return True
        return False

    def _current_focus(self):
        for w in Window.children:
            f = self._walk_focus(w)
            if f:
                return f
        return None

    def _walk_focus(self, w):
        if getattr(w, "focus", False) and isinstance(w, FocusCard):
            return w
        for c in getattr(w, "children", []):
            r = self._walk_focus(c)
            if r:
                return r
        return None

    # ---------- 进度持久化 ----------
    def _load_progress(self):
        try:
            if os.path.exists(DATA_FILE):
                return json.load(open(DATA_FILE))
        except Exception:
            pass
        return {}

    def save_progress(self):
        try:
            json.dump(self.progress, open(DATA_FILE, "w"), ensure_ascii=False)
        except Exception:
            pass

    def on_stop(self):
        self.save_progress()


if __name__ == "__main__":
    ZhiXueTVApp().run()
