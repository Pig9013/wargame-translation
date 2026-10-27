[中文](README.md) · **English** · [Français](README.fr.md) · [日本語](README.ja.md) · [Русский](README.ru.md)

# Board Wargame Rulebook Translation into Chinese · Workflow and Delivered Titles

> A **sentence-by-sentence, reverse-lookup** English-to-Chinese workflow for board wargame rulebooks, plus 13 delivered titles.
> The translation is not a "gist edition": every English sentence maps to one Chinese sentence, heading numbers match the original exactly, and terminology traces back to the clauses of the source book — the aim is that **the Chinese lets you look up the English original**.

**Repository version: v1.0.0** (2026-10-25)

**Current versions**

| Component | Version | Notes |
|:--|:--|:--|
| skill `wargame-translation` | **v1.4.0** | Translation pipeline: extraction, terminology, sentence-by-sentence, errata, credibility, illustrations, publishing |
| skill `wargame-rulebook-layout` | **v1.1.2** | Typesetting: GBII Ds edition (Letter portrait, two columns, black/dark-red editorial style) |
| Delivered titles | see table below | 12 typeset PDFs + 1 Chinese translation awaiting typesetting + 1 game manual |

---

## 1. Delivered titles

| Series | Title | Chinese content source | Typeset PDF | Pages | Size | Notes |
|:--|:--|:--|:--|--:|--:|:--|
| SCS | 《北非》North Africa | [md](<works/SCS/NorthAfrica/NorthAfrica_规则中文翻译.md>) | [PDF](<works/SCS/NorthAfrica/NorthAfrica_规则中文翻译（排版版）.pdf>) | 45 | 19.8 MB | Typeset v1.0; first batch of SCS terminology rulings |
| SCS | 《铁幕》Iron Curtain | [md](<works/SCS/IronCurtain/SCS_Iron_Curtain_铁幕_中文规则.md>) | [PDF](<works/SCS/IronCurtain/SCS_Iron_Curtain_铁幕_中文规则（排版版）.pdf>) | 55 | 23.5 MB | Typeset v1.0; arrival sequences, scenarios and charts filled in |
| SCS | 《The Mighty Endeavor》Revised Edition + Expansion (one volume) | [md](<works/SCS/TMEE/TMEE_规则中文翻译.md>) | [PDF](<works/SCS/TMEE/TMEE_规则中文翻译（排版版）.pdf>) | 88 | 18.1 MB | Template for the combined-volume banner + edge colour tabs |
| SCS | 《罗斯托夫'41》Rostov '41 | [md](<works/SCS/Rostov41/Rostov41_规则中文翻译.md>) | [PDF](<works/SCS/Rostov41/Rostov41_规则中文翻译（排版版）.pdf>) | 15 | 14.1 MB | 2026-10-03 batch |
| SCS | 《装甲战斗》Panzer Battles | [md](<works/SCS/PanzerBattles/PanzerBattles_规则中文翻译.md>) | [PDF](<works/SCS/PanzerBattles/PanzerBattles_规则中文翻译（排版版）.pdf>) | 21 | 14.6 MB | 2026-10-03 batch |
| SCS | 《非洲II》Afrika II | [md](<works/SCS/AfrikaII/AfrikaII_规则中文翻译.md>) | [PDF](<works/SCS/AfrikaII/AfrikaII_规则中文翻译（排版版）.pdf>) | 23 | 15.0 MB | A4 wide format (663×842 pt) |
| SCS | 《十字军》Crusader | [md](<works/SCS/Crusader/Crusader_规则中文翻译.md>) | [PDF](<works/SCS/Crusader/Crusader_规则中文翻译（排版版）.pdf>) | 26 | 18.4 MB | 2026-10-03 batch |
| TCS | 《大德意志'42》GD42 | [md](<works/TCS/GD42/GD42_中文翻译.md>) | [PDF](<works/TCS/GD42/GD42_中文翻译（排版版）.pdf>) | 43 | 15.9 MB | Content v1.1 |
| GTS | Series Rules v2.0C | [md](<works/GTS/SeriesRules2.0C/GTS_Series_Rules_2.0C_中译.md>) | [PDF](<works/GTS/SeriesRules2.0C/GTS_Series_Rules_2.0C_中译（排版版）.pdf>) | 47 | 20.8 MB | Four-dimension credibility 92% |
| GTS | Strike-Counter Strike Exclusive Rules | [md](<works/GTS/StrikeCounterStrike/GTS_SCS_Exclusive_Rules_中译.md>) | [PDF](<works/GTS/StrikeCounterStrike/GTS_SCS_Exclusive_Rules_中译（排版版）.pdf>) | 27 | 24.5 MB | Four-dimension credibility 90%; typeset v1.2 |
| OCS | GBII Reprint Rules (**Ds edition**) | [md](<works/OCS/GBII/GBII_Reprint_Rules_zh-CN_Ds版.md>) | [PDF](<works/OCS/GBII/GBII_Reprint_Rules_zh-CN_Ds版.pdf>) | 49 | 6.9 MB | Ds edition v1.1; 12/12 illustrations |
| VUCA | 《胜利之痕》Traces of Victory | [md](<works/VUCA/TracesOfVictory/Traces_of_Victory_胜利之痕_规则中文翻译.md>) | Awaiting typesetting | — | — | Sample with 22 source errata |
| WitE2 | 《钢铁炼狱》Official Manual | — | [PDF](<works/WITE2/SteelInferno/WITE2_SteelInferno_手册_中文版.pdf>) | 110 | 6.2 MB | Small format 343×505; v1.0 (2026-10-25) |

> "Typeset vX" is the version of the typeset edition, tracked separately from the Chinese content version; the PDF cover, footer and metadata all carry the same number.

---

## 2. Glossary

| File | Purpose |
|:--|:--|
| [兵棋术语总表.md](<glossary/兵棋术语总表.md>) | Cross-series master glossary (Chinese–English with sources) |
| [兵棋术语总表.csv](<glossary/兵棋术语总表.csv>) | Same, machine-readable |
| [术语库索引.md](<glossary/术语库索引.md>) | Glossary navigation |
| [SCS_Terminology_DB.md](<glossary/SCS_Terminology_DB.md>) | SCS series (basis: Chinese translation of the common rules → CTO → own wording) |
| [TCS_Terminology_DB.md](<glossary/TCS_Terminology_DB.md>) | TCS series |
| [GTS_Terminology_DB.md](<glossary/GTS_Terminology_DB.md>) | GTS series |
| [OCS_Terminology_DB.md](<glossary/OCS_Terminology_DB.md>) | OCS series |
| [激斗_Terminology_DB.md](<glossary/激斗_Terminology_DB.md>) | 激斗 series |
| [美工哥_Terminology_DB.md](<glossary/美工哥_Terminology_DB.md>) | GMT 美工哥 series |

**SCS terminology precedence** (user ruling, 2026-10-03): 《SCS 标准战斗系列 系列规则 中文修订版 v1》→ CTO / 觅渡Midu translation → own wording recorded in the glossary.

---

## 3. Using the two skills

### 3.1 Installation

Copy the whole `skills/wargame-translation` and `skills/wargame-rulebook-layout` directories into your agent skills directory:

| Tool | Target directory |
|:--|:--|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.agents/skills/` |
| DeepSeek Harness | `~/.dsh/skills/` |

After reloading, the skills match automatically on tasks such as "translate a wargame rulebook / typeset / GBII Ds edition".

### 3.2 Standard workflow (two-step delivery)

1. **Content source**: `wargame-translation` produces `<作品>_规则中文翻译.md` — paragraph-by-paragraph alignment, glossary, source errata, four-dimension credibility assessment, illustration list.
2. **Typeset edition**: `wargame-rulebook-layout` uses the md as the sole content source to typeset a PDF (GBII Ds edition), embedding the original illustrations at their matching positions; the typesetting stage **changes not one character of the body text**.

### 3.3 Quality gates

- Every sentence translated; no abridging/expanding/inventing; heading numbers identical to the original;
- Terminology per the series basis; errors in the source translated as they stand + errata note;
- Delivered only at four-dimension credibility ≥90%;
- Illustrations verified N/N; character fidelity ratio ≈1.0x;
- Version history bumped at every revision.

---

## 4. Versioning and releases

- Repository tag: `v1.0.0` (first release, 2026-10-25).
- The two skills version independently; a delivered title's version is written on its PDF cover/footer and at the top of its md.
- For every content or typesetting change: bump the version → edit CHANGELOG → regenerate the PDF → tag.
- Release scope: **translations, typeset files and glossaries only**; the English originals, scans, game components and VASSAL modules are not released.

---

## 5. Copyright and terms of use

- **Copyright in the original text** belongs to the respective publishers and designers (Multi-Man Publishing / The Gamers / GMT Games / Uhlan Games, etc., by title).
- **The Chinese translation, typesetting and terminology work** are the labour of **Pig9013**, shared on an "attribution—non-commercial" basis: **credit the author and the source, no commercial use**.
- This repository is for rules study and wargaming discussion only; it may not be used for any commercial release or paid distribution.
- If a rights holder considers any content inappropriate, please contact us through a GitHub Issue; it will be taken down immediately.

---

## 6. Acknowledgements

- The original publishers and designers of each title;
- 慕容笛, Chinese translator of the SCS common rules, and the CTO / 觅渡Midu translation — key references for the SCS terminology rulings;
- The wargame community's public rules discussions and errata.

---

## 7. Repository structure

`@
skills/
  wargame-translation/      SKILL.md
  wargame-rulebook-layout/  SKILL.md + assets/ + references/
works/
  SCS/  TCS/  GTS/  OCS/  VUCA/  WITE2/
glossary/                   master glossary + per-series Terminology_DB
tools/verify_repo.py        pre-release static self-check
`@

---

*Maintenance: Pig9013 | Model: Deepseek-flash | Last updated: 2026-10-25*
