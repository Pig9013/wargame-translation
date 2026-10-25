# -*- coding: utf-8 -*-
"""
Copy this file next to build_rulebook_pdf.py as `rulebook_config.py` and edit.
All paths may be absolute, or relative to `base`.
"""

CONFIG = {
    # ---------- 项目路径 ----------
    "base": r"D:/兵棋/OCS大全",
    "work": "_layout_work",                  # 中间文件目录（相对 base）
    "md": "GBII_Reprint_Rules_zh-CN_Ds版.md",
    "out": "GBII_Reprint_Rules_zh-CN_Ds版_排版测试.pdf",
    "html": "_layout_work/rulebook.html",
    "raw": "_layout_work/rulebook_raw.pdf",

    # ---------- 封面 / 版本 ----------
    "label": "Ds版",                         # 可留空
    "version": "v1.1",
    "date": "2026-10-21",
    "topbar": "OPERATIONAL COMBAT SERIES · MULTI-MAN PUBLISHING",
    "series_cn": "作战对抗系列 · OCS",
    "title_cn_1": "古德里安",
    "title_cn_2": "闪电战",                   # 封面第二行，自动用强调红
    "title_cn_suffix": "II",
    "title_en": "GUDERIAN'S BLITZKRIEG II",
    "title_en_suffix": "REPRINT RULES",
    "subtitle": "重印版规则",
    "meta_line": "中文翻译 · 中英术语对照",
    "meta_refs": "依据 OCS 4.3 / 2.0i / 朝鲜战争 / 第三个冬天 系列译名",
    "translator": "Pig9013 Deepseek大模型",
    "bottom": "© 2011 MULTI-MAN PUBLISHING, LLC · 中文译本仅供推演查阅",

    # ---------- 页眉 / 页脚 ----------
    "header_left": "古德里安闪电战II · 重印版规则",
    "header_right": "OCS 系列规则",
    "footer_left": "GBII 中文翻译",
    "footer_right": "© 2011 Multi-Man Publishing",

    # ---------- 正文结构 ----------
    # 正文第一页的判定文本（必须出现在 md 正文第一页）
    "body_start_marker": "1.1 地形与地图说明",
    # 一级部分横幅的小字
    "part_kicker": "OCS · GUDERIAN'S BLITZKRIEG II",
    # 含此关键词的一级标题用“紧凑横幅”（不另起一页）
    "part_inline_keyword": "可选规则",
    # 这些二级标题另起一页（正则 / 前缀 / 精确匹配）
    "page_break_h2_regex": r"^(1|2|3|4)\.0\s",
    "page_break_h2_prefixes": ["《蓝色方案》"],
    "page_break_h2_exact": ["插图核验清单"],
    # 这些表头让表格另起一页（如缩略语长表）
    "table_break_headers": ["缩略语"],

    # ---------- 贴图 ----------
    # 文件名关键词 -> CSS 类；未命中用 default
    "figure_class_map": {
        "special_symbols": "fig-symbols",
        "moscow_photos": "fig-photos",
    },
    "default_figure_class": "fig-counter",

    # ---------- PDF 元数据 ----------
    "metadata": {
        "author": "Pig9013 Deepseek大模型",
        "subject": "Guderian's Blitzkrieg II Reprint Rules 中译",
        "keywords": "OCS, GBII, 古德里安闪电战, 兵棋, 规则中译",
        "creator": "Pig9013 / Deepseek",
        "producer": "Edge + PyMuPDF",
    },
}
