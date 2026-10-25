---
name: wargame-rulebook-layout
description: 兵棋规则书中译的“GBII Ds版”排版方案——黑/暗红编辑风格、Letter 竖版双栏、部分横幅、算子图右浮动、符号图框/照片通栏、深色表头与米色注框、Edge 无头 + PyMuPDF 盖章与书签。Use when the user asks to 排版/制作 PDF for a translated wargame rulebook, mentions “GBII Ds版”“排版版”“配色方案”“贴图/嵌图”“规则书 PDF”“排版 skill”, or wants any new rulebook to follow the GBII Ds layout. This skill governs layout only; content translation follows `wargame-translation`. 2026-10-21 起为兵棋规则书默认排版方案；18xx 作品用 `18xx-translation` 的原版式流程。
version: 1.1.2
---

# 兵棋规则书「GBII Ds版」排版

## 0. 定位

这是 **GBII Ds 版**（《古德里安闪电战II》重印版规则中译，2026-10-21，49 页）定稿的排版方案。用户明确表示喜欢其**配色、版式和贴图实现**，今后规则书 PDF 默认采用本方案。

- **内容源唯一**：`.md` 是唯一内容源；排版阶段**不改正文一字**。
- **两步交付**：先完成 `wargame-translation` 的逐句翻译与术语库，再用本 skill 生成排版版 PDF。
- **样板成品**：
  - `D:\兵棋\OCS大全\GBII_Reprint_Rules_zh-CN_Ds版.md`
  - `D:\兵棋\OCS大全\GBII_Reprint_Rules_zh-CN_Ds版.pdf`
  - 样例图：`assets/sample-cover.png`、`sample-symbols.png`、`sample-counters.png`、`sample-columns.png`

### 0.1 适用边界（2026-10-21）

| 场景 | 用什么 |
|:--|:--|
| 兵棋规则书中译（SCS / TCS / GTS / OCS / VUCA / 独立作品） | **本 skill（GBII Ds 版）** |
| 18xx 作品（Railways、1880 China 等） | `18xx-translation` + 它的 `references/中译排版PDF.md`（横版/原版式） |
| 用户明确要求“复刻原书版式”（三栏、横版、原书纸色） | 旧批次模板（SCS/TCS/GTS `_tools`），不套 Ds 版 |
| 只改内容、不改版式 | 先改 md，再按本 skill 重排；排版阶段不改正文 |

> 本 skill 的“默认”不等于“唯一”。Ds 版是 Letter 竖版双栏的编辑风方案；若原书是横版/三栏且用户要求版式一致，改用旧模板并在交付说明里写明理由。

---

## 1. 视觉 DNA（先记这几条）

| 元素 | 规格 |
|:--|:--|
| 开本 | Letter 竖版 **215.9 × 279.4 mm**；页边距 上19 / 左右18 / 下20 mm |
| 正文字体 | `NotoSerifSC-VF.ttf`，**9.7 pt / 1.72**，两端对齐 |
| 标题/表格字体 | `NotoSansSC-VF.ttf` |
| 墨色 | 正文 `#1b1b1b`；标题/表头 `#111` / `#222` |
| 强调色 | 暗红 **`#9e1b1b`**（封面、部分横幅底线、章节左线、页码、注框左线） |
| 注框 | 米色 `#f5f2ec` 底 + 3 mm 暗红左线，8.8 pt |
| 表格 | 7.7 pt 无衬线；深色表头反白；偶数行 `#f4f4f4`；跨页重复 `thead` |
| 正文分栏 | 双栏，栏间距 **8.5 mm**，`column-fill:balance` |
| 页眉 | 6.8 pt 灰色，左侧书名、右侧系列名，下方 0.45 pt 暗红细线 |
| 页脚 | 左：`书名 中文翻译 vX.Y 标签`；中：暗红页码；右：版权 |
| 封面 | 顶部黑条 + 暗红横带；45 pt 衬线大标题，第二行暗红；红星；底部黑条 |

> 完整 CSS token、字号、间距、封面坐标见 `references/design-spec.md`。不要凭感觉改色号或字号。

---

## 2. 标准 md 结构（builder 依赖）

builder 按固定钩子解析，**新书沿用同一骨架**：

```markdown
# 《作品名》规则中文翻译

## 中文翻译（Ds版）

---

## 翻译说明
- **翻译人：** Pig9013 Deepseek大模型
- **版本：** Ds版 v1.0
……

---

## 出版信息
……

---

## 引言
……

## 目录
- **主规则**
  - 1.0 ……
- **可选规则**
  - ……
- **附录**
  - ……

---

# 主规则
## 1.0 ……
### 1.1 ……
**1.1a ……** 正文……
……

# 可选规则
## ……
### a) ……
……

---

## 专业名词对照库
……

## 原书勘误注记
……

## 版本沿革
……

## 插图核验清单
……
```

硬钩子：

| md 构造 | 用途 |
|:--|:--|
| `## 翻译说明` / `## 出版信息` / `## 引言` | 前置页，自动加红色分隔线 |
| `## 目录` | 该标题本身不排；正文 `#`/`##` 自动生成带页码的两栏目录 |
| `# 主规则` / `# 可选规则…` | 一级部分横幅；含“可选规则”的横幅自动改为紧凑型（不另起页） |
| `## 1.0`、`## 2.0`… | 自动另起一页 |
| `## 《蓝色方案》规则变更` / `## 插图核验清单` | 自动另起一页（可在 config 增删） |
| `> **注：**` / `> **设计说明：**` | 通栏米色注框 |
| `| … |` 表格 | 通栏；表头 `缩略语` 自动另起一页 |
| `![图：…](相对路径)` | 图 + 自动图注；按文件名决定浮动/通栏 |

完整骨架见 `assets/template.md`。

---

## 3. 使用方式

### 3.1 复制资产

把以下文件复制到项目 `_tools/`（或任意工作目录）：

- `assets/build_rulebook_pdf.py`
- `assets/rulebook_config.example.py` → 改名为 `rulebook_config.py`
- `assets/template.md`（可选，作为 md 骨架）

### 3.2 改 `rulebook_config.py`

只改配置，不改 builder：

```python
CONFIG = {
    "base": r"D:/兵棋/OCS大全",
    "md": "GBII_Reprint_Rules_zh-CN_Ds版.md",
    "out": "GBII_Reprint_Rules_zh-CN_Ds版.pdf",
    "label": "Ds版",
    "version": "v1.1",
    "date": "2026-10-21",
    "title_cn_1": "古德里安",
    "title_cn_2": "闪电战",
    "title_cn_suffix": "II",
    "title_en": "GUDERIAN'S BLITZKRIEG II",
    "title_en_suffix": "REPRINT RULES",
    "header_left": "古德里安闪电战II · 重印版规则",
    "header_right": "OCS 系列规则",
    "footer_left": "GBII 中文翻译",
    "footer_right": "© 2011 Multi-Man Publishing",
    "body_start_marker": "1.1 地形与地图说明",
    "part_kicker": "OCS · GUDERIAN'S BLITZKRIEG II",
    "page_break_h2_regex": r"^(1|2|3|4)\.0\s",
    "page_break_h2_exact": ["插图核验清单"],
    "figure_class_map": {
        "special_symbols": "fig-symbols",
        "moscow_photos": "fig-photos",
    },
    "default_figure_class": "fig-counter",
}
```

### 3.3 运行

```bash
cd <项目>/_tools
python -I build_rulebook_pdf.py
```

也可用环境变量覆盖配置：

```bash
RULEBOOK_CONFIG="D:/.../rulebook_config.py" python -I build_rulebook_pdf.py
```

产物：

- `out` 指定的成品 PDF
- `_layout_work/rulebook.html`（中间 HTML）
- `_layout_work/rulebook_raw.pdf`（Edge 原始 PDF）

### 3.4 新书配置清单（只改这些，不改 builder）

| 配置键 | 新书要改成什么 |
|:--|:--|
| `base` / `md` / `out` | 新项目目录、内容源文件名、成品名 |
| `label` / `version` / `date` | 如 `Ds版`、`v1.0`、交付日期 |
| `topbar` / `series_cn` | 出版社系列条、中文系列名 |
| `title_cn_1` / `title_cn_2` / `title_cn_suffix` | 封面中文标题（第二行自动暗红） |
| `title_en` / `title_en_suffix` / `subtitle` | 封面英文标题与副标题 |
| `meta_line` / `meta_refs` / `translator` / `bottom` | 封面 meta、译名依据、译者、版权条 |
| `header_left` / `header_right` / `footer_left` / `footer_right` | 页眉页脚 |
| `body_start_marker` | 正文第一页的判定文本（必须出现在 md 正文第一页） |
| `part_kicker` | 部分横幅上的系列小字 |
| `page_break_h2_regex` / `_prefixes` / `_exact` | 哪些二级标题另起页 |
| `table_break_headers` | 哪些表头强制分页（如“缩略语”） |
| `figure_class_map` / `default_figure_class` | 图片文件名关键词 → 图类 |
| `metadata` | PDF 元数据（作者/主题/关键词/creator/producer） |

**不要**为了新书去改 builder 里的 CSS 常量；确需通用性改进时，改完把新 builder 回写本 skill 的 `assets/`，并升 skill 版本。

---

## 4. 版式规则

### 4.1 封面

- 顶部黑条：`OPERATIONAL COMBAT SERIES · MULTI-MAN PUBLISHING`（可按书改）
- 暗红横带 2.2 mm
- 系列小字、45 pt 大标题（第二行暗红）、15 pt 副标题、英文标题
- 红星（CSS clip-path）、细线、翻译信息、底部黑条
- 标签与版本同时出现在：封面副标题、封面 meta、页眉、页脚、PDF 元数据

### 4.2 前置页与目录

- `翻译说明` 与 `出版信息` 同页；`引言` 另起页；`目录` 另起页
- 目录**两栏**，点线引导，页码由第二次编译回填
- 目录只收 `#`/`##`，不收 `###`
- 目录下可加一条 `> 注：……` 说明另册/未译内容

### 4.3 部分横幅

- `# 主规则`：整幅黑底白字，底部 2 mm 暗红条，**另起一页**
- `# …可选规则`：紧凑横幅，不另起页（config `part_inline_keyword`）
- 多部分合订本可给第二部换暗红底（改 CSS `.part.accent`），但 GBII 样板是黑底

### 4.4 正文

- 双栏，`h3`（1.1/1.2…）随栏流动，`break-after:avoid`
- `h2`（1.0/2.0…）通栏，左侧 3.2 mm 暗红竖线
- 段落 2.6 mm 下距；列表 4.5 mm 左缩进
- 规则编号用 `**1.1a 标题。**` 开头，编号与原文完全一致

### 4.5 表格

- 表格一律通栏，避免在双栏里挤压
- 表头深色反白；跨页自动重复表头
- 长表（缩略语）前强制分页
- 复杂表格逐格誊录，不用截图代替

### 4.6 注框

- `>` 引用 → 米色底 + 暗红左线
- `**注：**`、`**设计说明：**`、`**历史注：**`、`**推演注：**` 均适用
- 注框通栏；会打断双栏流，这是预期行为

---

## 5. 贴图实现（用户最喜欢的部分）

### 5.1 三类图

| 类 | 触发 | CSS | 用法 |
|:--|:--|:--|:--|
| `fig-counter` | 默认（文件名未命中映射） | `float:right; width:27mm` | 算子图、标记图，挂在规则标题下，正文绕排 |
| `fig-symbols` | 文件名含 `special_symbols` | `width:78mm; 居中` | Unit Symbol Key 等图框；图下必须附中文誊录表 |
| `fig-photos` | 文件名含 `moscow_photos` | `width:158mm; 居中` | 海报、照片、地图插图等通栏大图 |

映射在 `rulebook_config.py` 的 `figure_class_map` 中增删。

### 5.2 md 写法

算子图（浮动，放在规则标题后、正文前）：

```markdown
**2.5c 德军警戒单位。**

![图：警戒营算子](art/alert.png)

在苏军发动大规模攻势后……
```

符号图框（通栏 + 中文表）：

```markdown
![图：特殊单位符号](art/special_symbols.png)

| 符号 | 含义 | 符号 | 含义 |
|:---|:---|:---|:---|
| Alert | 警戒（临时）单位 | UR | 筑垒地域（UR）单位 |
……
```

照片/海报（通栏）：

```markdown
![图：1941年莫斯科保卫战海报与苏军坦克](art/moscow_photos.png)
```

### 5.3 贴图纪律

1. 图内英文标签属于原图，**保留不动**；图框文字另在 md 誊录为中文表。
2. 图注由 `alt` 自动生成，格式统一为 `图：……`。
3. 每张图必须进「插图核验清单」：原书页 → 元素名 → md 锚点 → 排版版页 → 正文页。
4. 交付前逐张核验：PDF 该页确有图、图注正确、位置对应、无邻栏文字/页码混入。
5. 裁图按 `wargame-translation` 第六步执行：整页高分渲染 + 坐标裁剪，不用 `extract_image` 抠碎片。

---

## 6. 管线

```
md
 ── 行级解析 ──▶ HTML + CSS（本 skill 的版式）
 ── Edge 无头 --print-to-pdf ──▶ 原始 PDF（第一次，无页码）
 ── 扫描标题所在页 ──▶ 回填目录页码 ──▶ 第二次打印
 ── PyMuPDF 后处理 ──▶ 页眉/页脚/页码/书签/元数据/字体子集 ──▶ 成品
```

关键点：

- Edge 路径：`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
- 参数：`--headless=new --disable-gpu --no-first-run --no-pdf-header-footer --print-to-pdf=...`
- 必须用 Python `subprocess` 调用，避免 git-bash 中文路径编码问题
- 页码/页脚只能后处理盖章；`--print-to-pdf` 没有页眉页脚模板
- 盖章字体用 `NotoSansSC-VF.ttf` / `NotoSerifSC-VF.ttf`（simhei 缺 © 字形）
- 书签：`d.set_toc()`，h1 一级、h2 二级
- 元数据：`d.set_metadata()`，标题带标签与版本
- 保存：`garbage=4, deflate=True, deflate_images=True, deflate_fonts=True, clean=True`

### 6.1 与旧管线的关系

本 skill 的 builder 是从 GBII Ds 版成品反推、验证过的配置驱动版本（`assets/build_rulebook_pdf.py`）。2026-10-03 的 SCS/TCS/GTS 三栏或原版式模板仍在各项目 `_tools/` 下：

- `D:\兵棋\SCS大全\_tools\_legacy\build_scs_pdf.py`（SCS 全系列 + TMEE）
- `D:\兵棋\TCS\_tools\_legacy\build_gd42_pdf.py`（TCS）
- `D:\兵棋\GTS大全\_tools\_legacy\build_gts_series_pdf.py`、`build_scs_pdf.py`（GTS）

这些是**历史批次模板**，只在“复刻原书版式”或旧稿重排时使用；新兵棋书默认用本 skill。旧手册 `18xx-analysis/references/中译排版PDF.md` 同理，仅作对照。

---

## 7. 交付前 QA（缺一不可）

- [ ] 页数、开本、页边距正确
- [ ] 封面标题/副标题/标签/版本/日期正确
- [ ] 目录两栏、页码与实际正文一致（h1/h2 全部映射）
- [ ] 所有规则编号与原文一致，无跳号/漏号（原书自身编号跳跃另列勘误）
- [ ] 双栏无内容被截断；通栏表/注框/图前后无孤行
- [ ] 所有表格跨页重复表头；长表未挤爆页面
- [ ] 插图清单 N/N：每张图在对应页、图注正确、中文誊录表存在
- [ ] 页眉/页脚/页码/标签在每一页正确；无 □/乱码
- [ ] PDF 书签、元数据正确
- [ ] 版本沿革已写；每次改动升版本
- [ ] md 与 PDF 内容一致（排版不改正文）

---

## 8. 版本与快照

- **内容版**（中译 vX.Y）与**排版版**（vX.Y）分别记录；每次改 md 或 CSS 都要升版本并写沿革。
- 快照目录：`<项目>/_layout_work/_snapshot/YYYYMMDD/`，放：
  - `build_rulebook_pdf.py`
  - `rulebook_config.py`
  - 成品 PDF
- 样板基准：GBII Ds 版 **v1.1 / 49 页 / 12 幅图 / 25 个目录标题全部映射**。

---

## 9. 已踩坑（不要重犯）

| 坑 | 现象 | 对策 |
|:--|:--|:--|
| 目录页码不更新 | 第一次打印后直接交付 | 必须两次编译：先扫描标题页，再回填目录重打 |
| 表格尾部单独一页且无表头 | `thead` 在 Edge 分页时未重复 | 长表前强制分页；`thead{display:table-header-group}` |
| 注框打断双栏 | 注框出现在段落中间 | 这是通栏设计的预期；注框放在段落后，不要塞进段落中 |
| 图片压住正文 | 浮动图太宽/太高 | 算子图统一 27 mm；符号图 78 mm；照片 158 mm；图后留 4 mm |
| 图中混入邻栏文字/页码 | 裁剪框过大 | 裁图前量邻栏边界与原书页码位置，边界内收 4–8 pt |
| 页脚 © 变 □ | 用了 simhei | 盖章一律用 NotoSansSC/NotoSerifSC |
| PDF 标题是 `xxx.html` | Edge 默认元数据 | 后处理 `set_metadata()` |
| 标签只写在文件名 | 打开 PDF 看不出机翻/Ds | 封面、页眉、页脚、元数据四处都写 |
| 机翻版被覆盖 | 用户原文件丢失 | 先复制原文件再改；交付时保留原版/新版两份并标注 |

---

## 10. 参考

- 完整设计规格：`references/design-spec.md`
- md 骨架与钩子：`references/md-structure.md`
- builder：`assets/build_rulebook_pdf.py`
- 配置样例：`assets/rulebook_config.example.py`
- 视觉样例：`assets/sample-cover.png`、`sample-symbols.png`、`sample-counters.png`、`sample-columns.png`
- 翻译与插图普查：skill `wargame-translation`（第六步）
- 18xx 排版手册：skill `18xx-translation` 的 `references/中译排版PDF.md`（**本 skill 以 GBII Ds 版为准**，两者互不替代）
- 发布纪律：skill `wargame-translation` 第八步（仓库结构、版本四处一致、版权边界、静态自检）

---

## 11. 更新记录（本 skill）

- **v1.0.0**（2026-10-21）：从 GBII Ds 版成品固化——视觉 DNA、md 硬钩子、builder、配置样例、QA、踩坑。
- **v1.1.0**（2026-10-21）：清理与完善——新增适用边界（兵棋默认 / 18xx 例外 / 复刻原书例外）、新书配置清单、旧管线关系说明；builder 移除无用变量；补更新记录。
- **v1.1.1**（2026-10-21）：旧排版模板路径统一改到各项目 `_tools\_legacy\`。
- **v1.1.2**（2026-10-25）：18xx 排版路由改到新拆出的 `18xx-translation`；补发布纪律指针（与 `wargame-translation` 第八步同一口径）。
