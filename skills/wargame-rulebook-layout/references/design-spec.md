# GBII Ds 版排版规格（精确值）

> 基准成品：`GBII_Reprint_Rules_zh-CN_Ds版.pdf`，49 页，Letter 竖版。
> 基准脚本：`assets/build_rulebook_pdf.py`（2026-10-21 验证：与基准 PDF 逐页文本一致）。

## 1. 页面

```css
@page { size: 215.9mm 279.4mm; margin: 19mm 18mm 20mm 18mm; }
```

- 开本：Letter 竖版 215.9 × 279.4 mm
- 版心：左右 18 mm，上 19 mm，下 20 mm
- 正文可用宽度：约 179.9 mm；双栏时每栏约 85.7 mm

## 2. 字体

| 用途 | 字体 | 字号 / 行高 |
|:--|:--|:--|
| 正文 | `C:/Windows/Fonts/NotoSerifSC-VF.ttf` | 9.7 pt / 1.72 |
| 标题 | `NotoSansSC-VF.ttf` | h3 11.2 pt；h2 14.5 pt |
| 部分横幅 h1 | `NotoSerifSC-VF.ttf` | 25 pt / 1.15，900 |
| 封面大标题 | `NotoSerifSC-VF.ttf` | 45 pt / 1.12，900 |
| 封面副标题 | `NotoSansSC-VF.ttf` | 15 pt，500 |
| 表格 | `NotoSansSC-VF.ttf` | 7.7 pt / 1.4 |
| 注框 | `NotoSerifSC-VF.ttf` | 8.8 pt / 1.68 |
| 图注 | `NotoSansSC-VF.ttf` | 7.4 pt |
| 页眉 | `NotoSerifSC-VF.ttf` | 6.8 pt |
| 页脚 | `NotoSerifSC-VF.ttf` | 6.6 pt |
| 页码 | `NotoSansSC-VF.ttf` | 8.2 pt |

## 3. 色板

| 变量 | 色值 | 用途 |
|:--|:--|:--|
| ink | `#1b1b1b` | 正文 |
| black | `#111` | 标题、部分横幅底、封面黑条 |
| red | `#9e1b1b` | 强调色、封面第二行、章节左线、页码、注框左线 |
| note-bg | `#f5f2ec` | 注框底 |
| table-head | `#222` | 表头底 |
| zebra | `#f4f4f4` | 表格偶数行 |
| rule | `#d8d8d8` | 表格横线 |
| grey | `#666` | 图注、次要信息 |
| header-grey | `#6b6b6b` | 页眉/页脚 |

## 4. 封面

从上到下：

1. 顶部黑条：高 13 mm，白字 7.5 pt，字距 1.6 pt，左内边距 8 mm
2. 暗红横带：高 2.2 mm，紧接黑条
3. 系列小字：距顶 26 mm，8 pt，字距 2 pt，灰色
4. 大标题：距顶 36 mm，左右 8 mm，45 pt，行高 1.12；第二行 `.red`
5. 副标题：距顶 84 mm，15 pt，字距 3 pt
6. 英文标题：距顶 98 mm，9 pt，字距 1.2 pt，灰色
7. 红星：距顶 124 mm，18 × 18 mm，`clip-path` 十角星
8. 细线：距顶 158 mm，0.5 pt `#bbb`
9. 翻译信息：距顶 165 mm，8.4 pt，行高 2.1
10. 底部黑条：高 16 mm，白字 7.2 pt

标签（机翻版/Ds版）出现在副标题、封面 meta、页眉、页脚、PDF 标题/主题。

## 5. 部分横幅

```css
.part { break-before:page; background:#111; color:#fff; padding:9mm 8mm 8mm; margin:0 0 6mm; position:relative; }
.part:after { content:''; position:absolute; left:0; bottom:0; width:100%; height:2mm; background:#9e1b1b; }
.part-kicker { font-family:'NotoSansSC'; font-size:7pt; letter-spacing:2pt; color:#bbb; margin-bottom:2mm; }
.part h1 { color:#fff; font-family:'NotoSerifSC'; font-size:25pt; font-weight:900; line-height:1.15; }
.part-inline { break-before:auto; margin-top:7mm; }
```

- `# 主规则`：整页横幅
- 含“可选规则”的 `#`：紧凑横幅，不另起页
- 多部合订本可加 `.part.accent`（暗红底），但 GBII 样板不用

## 6. 章节

```css
.section h2 { font-size:14.5pt; font-weight:800; color:#111; border-left:3.2mm solid #9e1b1b; padding-left:3.2mm; line-height:1.3; }
.section-break { break-before:page; }
```

- `## 1.0`、`## 2.0`… 自动另起页
- `## 《蓝色方案》规则变更`、`## 插图核验清单` 另起页
- `### 1.1` 等不另起页，随双栏流动

## 7. 双栏

```css
.cols { column-count:2; column-gap:8.5mm; column-fill:balance; }
```

- 每个通栏块（表/图/注/横幅）前后的内容各起一个 `.cols` 容器
- 不依赖 `column-span`（Edge 兼容性差）
- 通栏块按文档顺序插入，双栏流在其前后自动续接

## 8. 表格

```css
table { width:100%; border-collapse:collapse; font-family:'NotoSansSC'; font-size:7.7pt; line-height:1.4; }
thead { display:table-header-group; }
thead th { background:#222; color:#fff; font-weight:700; padding:1.2mm 1.5mm; text-align:left; white-space:nowrap; }
tbody td { padding:1.0mm 1.5mm; border-bottom:0.4pt solid #d8d8d8; vertical-align:top; }
tbody tr:nth-child(even) td { background:#f4f4f4; }
tbody tr { break-inside:avoid; }
```

- 所有表格通栏
- 长表前 `break-before:page`（config `table_break_headers`）
- 表头尽量不超过 4 列；宽表拆成两张或缩短列名

## 9. 注框

```css
blockquote { margin:3.2mm 0 4mm; padding:3mm 4mm 2.6mm; background:#f5f2ec; border-left:3mm solid #9e1b1b;
  font-size:8.8pt; line-height:1.68; color:#333; }
blockquote strong { color:#8f1d1d; }
```

- `>` 引用全部按注框处理
- 注框通栏，会打断双栏；这是设计的一部分

## 10. 图

```css
figure { margin:3mm 0 4mm; text-align:center; break-inside:avoid; }
figure img { display:block; margin:0 auto; }
figcaption { font-family:'NotoSansSC'; font-size:7.4pt; color:#666; margin-top:1.2mm; }

.fig-counter { float:right; width:27mm; margin:0.5mm 0 2mm 3.5mm; text-align:center; }
.fig-counter img { width:100%; }
.fig-counter figcaption { font-size:6.8pt; line-height:1.3; }

.fig-symbols img { width:78mm; }
.fig-photos img { width:158mm; }
```

| 类 | 宽度 | 排法 |
|:--|:--|:--|
| `fig-counter` | 27 mm | 右浮动，正文绕排；图注 6.8 pt |
| `fig-symbols` | 78 mm | 居中通栏；图下附中文誊录表 |
| `fig-photos` | 158 mm | 居中通栏 |
| 默认 `fig` | 自适应 | 通栏居中 |

## 11. 页眉/页脚

- 页眉：距顶 11.5 mm；左书名 6.8 pt，右系列名 6.8 pt；下方 y=13.2 mm 画 0.45 pt 暗红线
- 页脚：y=270 mm；左 `书名 中文翻译 vX.Y 标签` 6.6 pt；中页码 8.2 pt 暗红；右版权 6.4 pt
- 封面/前置页不盖章；正文第一页起盖章
- 盖章字体必须含 © 与 ·：`NotoSansSC-VF.ttf` / `NotoSerifSC-VF.ttf`

## 12. 目录

- 两栏，`column-count:2`，栏间距 10 mm
- 行：标题 + 点线 + 页码
- 只收 h1/h2；h1 作为红色组标题，h2 作为条目
- 两遍编译：第一遍无页码 → 扫描标题页 → 第二遍回填
- 目录标题本身不排（`## 目录` 被 builder 跳过）

## 13. 分页规则（builder 默认）

| 触发 | 行为 |
|:--|:--|
| `#` 一级标题 | 部分横幅；默认另起页；含“可选规则”则紧凑 |
| `## N.0` | 另起页 |
| `## 《蓝色方案》…` | 另起页 |
| `## 插图核验清单` | 另起页 |
| 表头 `缩略语` | 表格另起页 |
| 图片/表/注框 | 通栏块，`break-inside:avoid` |

这些规则都可在 `rulebook_config.py` 增删。

## 14. 基准数据

- 页数：49（前置 4 + 正文 45）
- 正文标题映射：25/25
- 插图：12 幅（清单 12/12）
- 目录条目：h1 3 个、h2 22 个
- PDF 元数据：标题/作者/主题/关键词/creator/producer
- 书签：h1 一级、h2 二级
