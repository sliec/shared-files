---
name: stale-detector
description: "Scan a Yuque knowledge base for stale or outdated documents and recommend updates or archiving. Use when the user is cleaning up, maintaining, or periodically reviewing a knowledge base; trigger phrases include 鈥滃府鎴戞鏌ュ摢浜涙枃妗ｈ繃鏈熶簡鈥? 鈥滅煡璇嗗簱浣撴鈥? and 鈥渇ind stale docs鈥?"
license: MIT
compatibility: Requires the yuque-mcp MCP server connected with a personal Yuque token
metadata:
  author: yuque
  version: "1.0"
---

# Stale Detector 鈥?Knowledge Base Freshness Audit

Scan a Yuque knowledge base to discover documents that haven't been updated in a long time, analyze whether their content may be outdated, and generate a maintenance report with actionable recommendations.

## When to Use

- User wants to clean up or maintain their knowledge base
- User says "甯垜妫€鏌ュ摢浜涙枃妗ｈ繃鏈熶簡", "find stale docs", "鐭ヨ瘑搴撲綋妫€"
- User wants to identify documents that need updating or archiving
- User is doing a periodic knowledge base review

## Required MCP Tools

All tools are from the `yuque-mcp` server:

- `yuque_list_books` 鈥?List user's knowledge bases
- `yuque_list_docs` 鈥?List all documents in a knowledge base with metadata
- `yuque_get_doc` 鈥?Read document content for staleness analysis
- `yuque_get_toc` 鈥?Get knowledge base structure

## Workflow

### Step 1: Identify the Target Knowledge Base

**Case A 鈥?User specifies a knowledge base:**
Extract `repo_id` (namespace) from the provided link or name.

**Case B 鈥?User wants to scan all knowledge bases:**
List all repos first:

```
Tool: yuque_list_books
Parameters:
  user_id: "<user_id>"
```

Present the list and let the user choose, or scan them one by one if the user confirms.

**Case C 鈥?User is vague:**
Ask: "浣犳兂妫€鏌ュ摢涓煡璇嗗簱锛熸垜鍙互鍏堝垪鍑轰綘鐨勬墍鏈夌煡璇嗗簱銆?

### Step 2: Fetch Document List

Get all documents in the target knowledge base:

```
Tool: yuque_list_docs
Parameters:
  repo_id: "<namespace>"
```

Extract key metadata for each document:
- `title` 鈥?Document title
- `slug` 鈥?Document identifier
- `updated_at` 鈥?Last update timestamp
- `created_at` 鈥?Creation timestamp
- `word_count` 鈥?Document length
- `status` 鈥?Publication status

If the knowledge base is empty (no documents), inform the user: "杩欎釜鐭ヨ瘑搴撶洰鍓嶆病鏈夋枃妗ｃ€?

### Step 3: Classify Documents by Freshness

Calculate the age of each document (days since last update) and classify:

| Category | Criteria | Label |
|----------|----------|-------|
| 馃煝 **Fresh** | Updated within 90 days | 娲昏穬 |
| 馃煛 **Aging** | Updated 90-180 days ago | 鑰佸寲涓?|
| 馃煚 **Stale** | Updated 180-365 days ago | 闄堟棫 |
| 馃敶 **Dormant** | Not updated for 365+ days | 浼戠湢 |

### Step 4: Deep Analysis of Stale Documents

For documents classified as 馃煚 Stale or 馃敶 Dormant, read the content of up to 10 documents (prioritize the oldest and most important-looking ones by title):

```
Tool: yuque_get_doc
Parameters:
  repo_id: "<namespace>"
  doc_id: "<slug>"
```

For each document, analyze:

1. **Time-sensitive content** 鈥?Does it reference specific dates, versions, or events that may have passed?
   - Software version numbers (e.g., "React 16", "Node 12")
   - Date references (e.g., "2023骞磋鍒?, "Q3 鐩爣")
   - Links that may be broken
   - Policies or processes that may have changed

2. **Evergreen content** 鈥?Is the content timeless?
   - Conceptual explanations, principles, personal reflections
   - These may be old but still valid

3. **Recommendation:**
   - **Update** 鈥?Content is valuable but contains outdated information
   - **Archive** 鈥?Content is no longer relevant, move to archive
   - **Keep** 鈥?Content is evergreen, no action needed despite age
   - **Review** 鈥?Uncertain, needs human judgment

If `yuque_get_doc` fails (404/403), note the document as inaccessible and skip.

### Step 5: Generate Maintenance Report

```markdown
## 馃攳 鐭ヨ瘑搴撳仴搴锋姤鍛?
**鐭ヨ瘑搴?*锛歔鐭ヨ瘑搴撳悕绉癩(鐭ヨ瘑搴撻摼鎺?
**鎵弿鏃堕棿**锛歒YYY-MM-DD HH:MM
**鏂囨。鎬绘暟**锛歑 绡?
### 馃搳 鏁翠綋鍋ュ悍搴?
| 鐘舵€?| 鏁伴噺 | 鍗犳瘮 |
|------|------|------|
| 馃煝 娲昏穬锛?0 澶╁唴鏇存柊锛?| X | XX% |
| 馃煛 鑰佸寲涓紙90-180 澶╋級 | X | XX% |
| 馃煚 闄堟棫锛?80-365 澶╋級 | X | XX% |
| 馃敶 浼戠湢锛?65 澶╀互涓婏級 | X | XX% |

**鍋ュ悍璇勫垎**锛歑/100
锛堣绠楁柟寮忥細馃煝脳100 + 馃煛脳70 + 馃煚脳30 + 馃敶脳0锛屽姞鏉冨钩鍧囷級

### 馃敶 闇€瑕佸叧娉ㄧ殑鏂囨。

#### 寤鸿鏇存柊

| 鏂囨。 | 涓婃鏇存柊 | 鍘熷洜 |
|------|----------|------|
| [鏂囨。鏍囬](閾炬帴) | YYYY-MM-DD | [e.g., 寮曠敤浜?Node 12锛屽綋鍓嶅凡鏄?Node 22] |
| [鏂囨。鏍囬](閾炬帴) | YYYY-MM-DD | [e.g., 鍖呭惈 2023 骞寸殑璁″垝锛岄渶瑕佹洿鏂癩 |

#### 寤鸿褰掓。

| 鏂囨。 | 涓婃鏇存柊 | 鍘熷洜 |
|------|----------|------|
| [鏂囨。鏍囬](閾炬帴) | YYYY-MM-DD | [e.g., 宸插畬鎴愮殑椤圭洰璁板綍锛屽彲褰掓。] |

#### 寤鸿淇濈暀锛堣櫧鏃т絾鏈夋晥锛?
| 鏂囨。 | 涓婃鏇存柊 | 鍘熷洜 |
|------|----------|------|
| [鏂囨。鏍囬](閾炬帴) | YYYY-MM-DD | [e.g., 閫氱敤鏂规硶璁猴紝鍐呭涓嶈繃鏃禲 |

#### 闇€瑕佷汉宸ュ垽鏂?
| 鏂囨。 | 涓婃鏇存柊 | 鍘熷洜 |
|------|----------|------|
| [鏂囨。鏍囬](閾炬帴) | YYYY-MM-DD | [e.g., 鏃犳硶纭畾鍐呭鏄惁浠嶇劧鏈夋晥] |

### 馃挕 缁存姢寤鸿

1. [鍏蜂綋寤鸿 1锛歟.g., 寤鸿姣忓搴﹀鏌ヤ竴娆°€屾妧鏈枃妗ｃ€嶅垎绫讳笅鐨勬枃妗
2. [鍏蜂綋寤鸿 2锛歟.g., 鑰冭檻鍒涘缓涓€涓€屽綊妗ｃ€嶇煡璇嗗簱锛屽皢涓嶅啀缁存姢鐨勬枃妗ｈ縼绉昏繃鍘籡
3. [鍏蜂綋寤鸿 3锛歟.g., 鏈?X 绡囨枃妗ｈ秴杩?2 骞存湭鏇存柊锛屽缓璁泦涓鐞哴
```

### Step 6: Offer Follow-up Actions

After presenting the report, offer:

- "闇€瑕佹垜甯綘鎶婂缓璁綊妗ｇ殑鏂囨。绉诲埌褰掓。鐭ヨ瘑搴撳悧锛?
- "闇€瑕佹垜甯綘閫愮瘒鏌ョ湅闇€瑕佹洿鏂扮殑鏂囨。锛岀粰鍑哄叿浣撶殑鏇存柊寤鸿鍚楋紵"
- "闇€瑕佹垜瀹氭湡锛堟瘮濡傛瘡鏈堬級甯綘鍋氫竴娆＄煡璇嗗簱浣撴鍚楋紵"

These are suggestions only 鈥?do not take action without user confirmation.

## Guidelines

- Always answer in the same language the user used (Chinese or English)
- Be conservative with "archive" recommendations 鈥?when in doubt, suggest "review" instead
- Don't read every document in a large knowledge base 鈥?sample strategically
- The health score is a rough indicator, not a precise metric 鈥?present it as such
- Evergreen content (personal reflections, principles, methodologies) should not be flagged as stale just because of age
- Focus on actionable recommendations, not just listing old documents
- If the knowledge base has fewer than 5 documents, simplify the report format

## Error Handling

| Situation | Action |
|-----------|--------|
| Knowledge base not found | Inform user and suggest listing their repos with `yuque_list_books` |
| Knowledge base is empty | Inform user: "杩欎釜鐭ヨ瘑搴撶洰鍓嶆病鏈夋枃妗ｏ紝鏃犻渶浣撴" |
| `yuque_list_docs` returns error | Inform user of the issue, suggest checking the knowledge base link |
| Too many documents (100+) | Analyze metadata for all, but only deep-read the top 10 stalest documents |
| All documents are fresh | Congratulate the user: "鐭ヨ瘑搴撶姸鎬佸緢鍋ュ悍锛佹墍鏈夋枃妗ｉ兘鍦ㄦ椿璺冪淮鎶や腑 馃帀" |
| API rate limiting | Slow down requests, inform user if the scan takes longer than expected |
