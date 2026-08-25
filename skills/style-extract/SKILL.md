---
name: style-extract
description: "Analyze Yuque documents to extract vocabulary, sentence, and tone patterns into a reusable writing-style profile. Use when the user wants to understand or reproduce their voice or keep documents consistent; trigger phrases include 鈥滃垎鏋愪竴涓嬫垜鐨勫啓浣滈鏍尖€? 鈥滅敤鎴戠殑椋庢牸鍐欎竴绡?..鈥? 鈥滃府鎴戠敓鎴愪竴涓鏍肩敾鍍忊€? 鈥渆xtract my writing style鈥? and 鈥渨rite like me鈥?"
license: MIT
compatibility: Requires the yuque-mcp MCP server connected with a personal Yuque token
metadata:
  author: yuque
  version: "1.0"
---

# Style Extract 鈥?Your Writing Style Profile

Analyze your existing Yuque documents to extract your unique writing style 鈥?vocabulary habits, sentence structures, tone characteristics. Generate a reusable style profile that helps you (or AI) maintain a consistent voice when writing new content.

## When to Use

- User wants to understand their own writing style
- User says "鍒嗘瀽涓€涓嬫垜鐨勫啓浣滈鏍?, "鎴戠殑鏂囬鏄粈涔堟牱鐨?, "extract my writing style"
- User wants AI to write in their voice: "鐢ㄦ垜鐨勯鏍煎啓涓€绡?..", "write like me"
- User wants to ensure consistency across documents
- User says "甯垜鐢熸垚涓€涓鏍肩敾鍍?, "create my style profile"

## Required MCP Tools

All tools are from the `yuque-mcp` server:

- `yuque_list_books` 鈥?List user's knowledge bases
- `yuque_list_docs` 鈥?List documents in a knowledge base
- `yuque_get_doc` 鈥?Read document content for style analysis
- `yuque_search` 鈥?Find specific types of documents for analysis
- `yuque_create_doc` 鈥?Save the style profile as a document

## Workflow

### Step 1: Gather Writing Samples

Ask the user for source material:

**Case A 鈥?Specific documents:**
User provides links to documents they consider representative of their style.

**Case B 鈥?Entire knowledge base:**
User specifies a knowledge base. Sample documents from it.

**Case C 鈥?Auto-detect best samples:**
If the user isn't sure, search for their most substantial documents:

```
Tool: yuque_list_books
```

```
Tool: yuque_list_docs
Parameters:
  repo_id: "<namespace>"
```

Select 5-10 documents that are:
- Written by the user (not copied/quoted content)
- Substantial in length (> 500 characters)
- Diverse in topic (to capture general style, not topic-specific patterns)

For each selected document:

```
Tool: yuque_get_doc
Parameters:
  repo_id: "<namespace>"
  doc_id: "<slug>"
```

### Step 2: Analyze Writing Dimensions

Analyze the collected writing samples across these dimensions:

#### Vocabulary (鐢ㄨ瘝涔犳儻)
- **Formality level** 鈥?Casual, semi-formal, or formal?
- **Jargon density** 鈥?Heavy use of domain terms or plain language?
- **Favorite words** 鈥?Recurring words or phrases the user gravitates toward
- **Filler patterns** 鈥?Common transitions, connectors, hedging words
- **Language mixing** 鈥?Do they mix Chinese/English? In what pattern?

#### Sentence Structure (鍙ュ紡缁撴瀯)
- **Average sentence length** 鈥?Short and punchy or long and flowing?
- **Complexity** 鈥?Simple sentences or nested clauses?
- **Paragraph length** 鈥?Brief paragraphs or dense blocks?
- **List usage** 鈥?Frequent bullet points or prose-heavy?
- **Question usage** 鈥?Do they use rhetorical questions?

#### Tone & Voice (璇皵鐗圭偣)
- **Perspective** 鈥?First person, second person, or impersonal?
- **Confidence level** 鈥?Assertive ("X is Y") or hedged ("X might be Y")?
- **Humor** 鈥?Dry wit, playful, or strictly serious?
- **Engagement style** 鈥?Conversational or lecture-like?
- **Emotional range** 鈥?Neutral/analytical or expressive/passionate?

#### Structural Habits (缁撴瀯涔犳儻)
- **Opening style** 鈥?How do they start articles? (Question, statement, story, context)
- **Closing style** 鈥?How do they end? (Summary, call-to-action, open question)
- **Heading style** 鈥?Descriptive, concise, or creative headings?
- **Use of examples** 鈥?Frequent concrete examples or abstract reasoning?
- **Formatting preferences** 鈥?Heavy use of bold, quotes, code blocks, tables?

### Step 3: Generate Style Profile

Create a structured style profile:

```markdown
# 鉁嶏笍 鍐欎綔椋庢牸鐢诲儚

> 鍩轰簬 [N] 绡囨枃妗ｅ垎鏋愮敓鎴?> 鍒嗘瀽鏃ユ湡锛歒YYY-MM-DD

## 涓€鍙ヨ瘽椋庢牸姒傛嫭

[鐢ㄤ竴鍙ヨ瘽鎻忚堪鐢ㄦ埛鐨勬暣浣撳啓浣滈鏍硷紝濡?"绠€娲佺洿鎺ョ殑鎶€鏈啓浣滆€咃紝鍋忓ソ鐭彞鍜屽ぇ閲忎唬鐮佺ず渚嬶紝璇皵鑷俊浣嗕笉鍌叉參"]

## 鐢ㄨ瘝涔犳儻

- **姝ｅ紡绋嬪害**锛歔鎻忚堪 + 绀轰緥]
- **鏈瀵嗗害**锛歔鎻忚堪 + 绀轰緥]
- **楂橀璇嶆眹**锛歔鍒楀嚭 5-10 涓爣蹇楁€х敤璇峕
- **杩囨浮璇嶅亸濂?*锛歔甯哥敤鐨勮繛鎺ヨ瘝鍜岃繃娓¤〃杈綸
- **涓嫳娣风敤**锛歔妯″紡鎻忚堪锛屽 "鎶€鏈悕璇嶇敤鑻辨枃锛岃В閲婄敤涓枃"]

## 鍙ュ紡鐗瑰緛

- **鍙ュ瓙闀垮害**锛歔骞冲潎瀛楁暟/鍙ワ紝涓庡弬鑰冨€煎姣擼
- **娈佃惤闀垮害**锛歔骞冲潎鍙ユ暟/娈礭
- **澶嶆潅搴?*锛歔绠€鍗曞彞涓轰富 / 澶嶅悎鍙ヤ负涓籡
- **鏍囧織鎬у彞寮?*锛歔鐢ㄦ埛甯哥敤鐨勫彞寮忔ā寮忥紝闄勫師鏂囩ず渚媇

## 璇皵鐢诲儚

- **瑙嗚**锛歔绗竴浜虹О / 绗簩浜虹О / 鏃犱汉绉癩
- **鑷俊搴?*锛歔鏂█鍨?/ 鎺㈣鍨?/ 璋﹂€婂瀷]
- **骞介粯鎰?*锛歔鎻忚堪]
- **浜掑姩鎬?*锛歔瀵硅瘽寮?/ 鐙櫧寮?/ 鏁欏寮廬

## 缁撴瀯鍋忓ソ

- **寮€澶存柟寮?*锛歔鎻忚堪 + 绀轰緥]
- **缁撳熬鏂瑰紡**锛歔鎻忚堪 + 绀轰緥]
- **鏍囬椋庢牸**锛歔鎻忚堪]
- **涓句緥棰戠巼**锛歔楂?/ 涓?/ 浣嶿
- **鏍煎紡鍋忓ソ**锛歔甯哥敤鐨?Markdown 鍏冪礌]

## 椋庢牸鎸囩汗锛堜緵 AI 鍙傝€冿級

褰撻渶瑕佹ā浠挎椋庢牸鍐欎綔鏃讹紝閬靛惊浠ヤ笅瑙勫垯锛?
1. [鍏蜂綋瑙勫垯 1锛屽 "姣忔涓嶈秴杩?4 鍙ヨ瘽"]
2. [鍏蜂綋瑙勫垯 2锛屽 "鎶€鏈蹇甸娆″嚭鐜版椂鐢ㄤ腑鏂囪В閲?+ 鑻辨枃鍘熻瘝"]
3. [鍏蜂綋瑙勫垯 3锛屽 "澶氱敤鍙嶉棶鍙ュ紩瀵兼€濊€?]
4. [鍏蜂綋瑙勫垯 4锛屽 "閬垮厤浣跨敤'浼楁墍鍛ㄧ煡'绛夊璇?]
5. [鍏蜂綋瑙勫垯 5锛屽 "缁撳熬鍊惧悜浜庢彁鍑哄紑鏀炬€ч棶棰樿€岄潪鎬荤粨"]

## 绀轰緥瀵规瘮

### 鍘熸枃鐗囨
> [浠庣敤鎴锋枃妗ｄ腑鎽樺彇鐨勫吀鍨嬫钀絔

### 椋庢牸瑕佺礌鏍囨敞
[鏍囨敞璇ユ钀戒腑浣撶幇鐨勯鏍肩壒寰乚
```

### Step 4: Present and Refine

Show the style profile to the user and ask:

"杩欎釜椋庢牸鐢诲儚鍑嗙‘鍚楋紵鏈夋病鏈夊摢浜涘湴鏂归渶瑕佽皟鏁达紵"

Iterate based on user feedback. They might say:
- "鎴戣寰楁垜娌￠偅涔堟寮? 鈫?Adjust formality assessment
- "杩欎釜楂橀璇嶄笉鏄垜鐨勯鏍硷紝鏄偅绡囨枃绔犵壒鏈夌殑" 鈫?Remove outliers
- "鎴戝笇鏈涙柊鍐呭姣旀垜鐜板湪鐨勯鏍兼洿绠€娲? 鈫?Note as a style aspiration

### Step 5: Save Style Profile (Optional)

Ask the user: "瑕佹妸椋庢牸鐢诲儚淇濆瓨鍒拌闆€鍚楋紵浠ュ悗鍐欎綔鏃跺彲浠ュ弬鑰冦€?

If confirmed:

```
Tool: yuque_create_doc
Parameters:
  repo_id: "<target namespace>"
  title: "鉁嶏笍 鎴戠殑鍐欎綔椋庢牸鐢诲儚"
  body: "<style profile in markdown>"
```

Confirm: "椋庢牸鐢诲儚宸蹭繚瀛樺埌銆孾鐭ヨ瘑搴撳悕绉癩銆嶏細[鏂囨。閾炬帴]"

### Using the Style Profile

When the user later asks to write content in their style:

1. Retrieve the saved style profile
2. Apply the "椋庢牸鎸囩汗" rules when generating content
3. After drafting, self-check against the profile dimensions
4. Present the draft with notes on which style elements were applied

## Guidelines

- Always answer in the same language the user used (Chinese or English)
- Analyze at least 5 documents for a reliable profile 鈥?fewer may produce skewed results
- Distinguish between the user's natural style and topic-specific writing (a tech doc vs. a personal reflection will differ)
- High-frequency words should be genuinely characteristic, not just common words everyone uses
- The style profile should be descriptive, not prescriptive 鈥?describe what the user does, don't judge it
- When the user asks to "write like me", use the profile as a guide but don't produce robotic imitations
- Update the profile periodically 鈥?writing style evolves over time

## Error Handling

| Situation | Action |
|-----------|--------|
| Document not found (404) | Skip and note it; continue with other documents |
| Permission denied (403) | Tell user they may lack permission to access this document |
| Too few documents (< 3) | Inform user: "鏂囨。鏁伴噺杈冨皯锛岄鏍煎垎鏋愬彲鑳戒笉澶熷噯纭€傚缓璁彁渚涜嚦灏?5 绡囨枃妗? |
| Documents are mostly copied/quoted content | Inform user: "杩欎簺鏂囨。澶ч儴鍒嗘槸寮曠敤鍐呭锛岄渶瑕佷綘鍘熷垱鐨勬枃妗ｆ潵鍒嗘瀽椋庢牸" |
| `yuque_create_doc` fails | Present the style profile in chat for manual saving |
| Mixed authorship | Ask user to confirm which documents are their own writing |
