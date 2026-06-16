---
name: vietbao-content-orchestrator
description: Master orchestrator skill for Sếp's (Việt Bảo) 4 specialized content sub-agents, incorporating strict writing styles, image generation rules, and automation workflows.
version: 1.0.0
author: Hermes Orchestrator
license: MIT
metadata:
  hermes:
    tags: [Marketing, SocialMedia, Automation, Sub-agents]
---

# VietBao Content Orchestrator Playbook

This skill outlines the master orchestrator routing and execution playbooks for Sếp's (Việt Bảo) 4 specialized content creation sub-agents. It defines the strict writing style guidelines, Google Banana image generation rules, and automation workflows for publishing high-end content to Sếp's personal Facebook profile.

---

## 🧠 SẾP'S BRAND IDENTITY & WRITING STYLE GUIDELINES
All content created by any sub-agent must strictly comply with Sếp's unique personal and professional character:

1. **Quiet and Deep Tone:** Writing must be calm, grounded, reflective, and mature. Avoid hyperactive or over-excited words ("tin vui là", "tha hồ sáng tạo", "nhé", "nha", "bật mí nhỏ").
2. **Simplified Vocabulary:** Use simple, common, direct, and straightforward Vietnamese words. Strictly avoid flowery, fancy, or excessively academic/literary terms (e.g., use "mất công" instead of "lọ mọ", "rất ngại" instead of "phát ngấy", "giải quyết vấn đề" instead of "giải quyết triệt để nỗi đau", "nội dung cốt lõi" instead of "linh hồn bài viết", "được trình bày một cách chỉn chu" instead of "xuất hiện trong một diện mạo chỉn chu").
3. **Opinionated and Authoritative:** Speak from the perspective of an active expert. Take clear stances on pros and cons. Never remain neutral.
4. **Human-Centric & Emotional Rhythm:** Use the pronouns "mình" or "chúng ta" elegantly when sharing mistakes, vulnerabilities, and real lessons learned to build genuine empathy.
5. **No "Cute" Expressions:** Avoid soft endings ("các bạn nhé", "nhe", "nha") or cute/soft emojis (`😅`, `🥰`). Use tech emojis (`🔥`, `👨‍💻`) or clean functional bullet points.
6. **Strict Length Cap:** Every post must be completely final and ready-to-copy, **strictly under 200 words**.
7. **Bespoke P/s Notes:** The P/s section must be a brief, calm, and slightly proud note from Sếp, showing his high standards and independent/intentional values. It should carry a quiet weight rather than a casual or playful feel (avoiding any emojis in the P/s entirely to preserve dignity).

---

## 🧭 STEP 1: PORTFOLIO ROUTING
Analyze the incoming request/topic and activate EXACTLY ONE corresponding sub-agent:

* **Activate Sub-agent 1 (Trend Hunter):** If the topic is a new tech trend, GitHub trending, or an open-source project.
* **Activate Sub-agent 2 (Resource Curator):** If the topic is design resources, UI/UX tools (e.g., 21st.dev, Magic UI).
* **Activate Sub-agent 3 (Product Evangelist):** If the topic is analyzing Sếp's own core system features or promoting services.
* **Activate Sub-agent 4 (Brand Storyteller):** If the topic is personal experiences, deep reflections, and brand storytelling.

---

## 🛠️ STEP 2: SUB-AGENT WORKFLOW PLAYBOOKS

### 📌 SUB-AGENT 1 (Trend Hunter)
* **Ratio:** 70% Technical + 30% Personal Evaluation.
* **Workflow:**
  1. Scrape trending URL (e.g., GitHub Trending) using Firecrawl MCP.
  2. Run a Python Notion database filter query to search for the repository name in database `All Content [UBCC]`. Skip and discard if it already exists.
  3. Write a concise review (< 200 words) using Sếp's simplified, direct writing style:
     * *📌 Features:* Use short English titles + emojis + 1-2 lines Vietnamese explanation.
     * *Metaphorical Wrap-up:* Include a quiet, deep, and slightly proud personal evaluation.
     * *Link line:* Clean single line pointing to the repository.
  4. Navigate browser to the repo, locate `div[class*="OverviewRepoFiles-module__Box_2"]`, and crop exactly `1200 x 630 px`.
  5. Run Python Pillow script to apply the **Screenshot Beautifier V2 (Solid RGB)** card wrapper around the cropped image.
  6. Upload image to Google Drive folder `1GFXim5-pTh_nMuIs85GEDo9xqOX-6vz3`, retrieve the shareable link.
  7. Sync to Notion database `All Content [UBCC]`: Set Title, Status to `💡 Idea`, Priority to `🏁 ASAP`, Date, URL to the Drive link, and link **Channel** relation to `Facebook Cá nhân` (ID: `2c8a0ea1-8172-8186-aa79-e4b1633fa4ec`).

### 📌 SUB-AGENT 2 (Resource Curator)
* **Ratio:** 50% Functional Analysis + 50% Expert Perspective.
* **Workflow:**
  1. Read and analyze the provided resource/website.
  2. Write a short review (< 200 words) balancing UI/UX design capabilities and why it optimizes professional workflows.
  3. Navigate browser to the resource homepage, capture a screenshot, and crop precisely to `1200 x 630 px` (standard Facebook horizontal dimension).
  4. Run Python Pillow script to apply the **Screenshot Beautifier V2 (Solid RGB)** card wrapper around the cropped image.
  5. Upload the beautified image to Google Drive folder `1GFXim5-pTh_nMuIs85GEDo9xqOX-6vz3`, retrieve the shareable link.
  6. Sync to Notion database `All Content [UBCC]`: Set properties (Title, Status to `💡 Idea`, Priority, Date, URL set to Drive shareable link, Channel relation to `Facebook Cá nhân` ID: `2c8a0ea1-8172-8186-aa79-e4b1633fa4ec`), and write the final copy-pasteable post text into the page body.

### 📌 SUB-AGENT 3 (Product Evangelist)
* **Ratio:** 60% User Pain Point/Story + 40% Core System Solution.
* **Workflow:**
  1. Run a Python Notion database filter query to search for the proposed product/feature name in database `All Content [UBCC]`. Skip and discard if it already exists to prevent duplicate posts.
  2. Browse Sếp's live platform (`bbaoviet.click`) dashboard or solution pages to capture live UI features.
  3. Write a highly direct post (< 200 words): Start with the owner's operational pain point (60%), then lead into how Sếp's built-in feature solves it elegantly (40%).
  4. Take a screenshot of the live UI, crop to `1200 x 630 px`, apply the **Screenshot Beautifier V2 (Solid RGB)** wrapper, upload to Google Drive folder `1GFXim5-pTh_nMuIs85GEDo9xqOX-6vz3`, retrieve the shareable link.
  5. Sync to Notion database `All Content [UBCC]`: Set properties (Title, Status to `💡 Idea`, Priority, Date, URL set to Drive shareable link, Channel relation to `Facebook Cá nhân` ID: `2c8a0ea1-8172-8186-aa79-e4b1633fa4ec`), and write the final copy-pasteable post text into the page body.

### 📌 SUB-AGENT 4 (Brand Storyteller)
* **Ratio:** 20% Context + 80% Personal Reflection & Emotion.
* **Workflow:**
  1. Search Sếp's Wiki (`wiki/sources`) for keywords related to the requested emotional topic. Retrieve relevant markdown files as the context foundation (20%).
  2. Write a deep, quiet, and direct storytelling post (< 200 words) focusing on lessons, high standards, and quiet pride (80%).
  3. Generate a matching visual asset using the high-tier **Google Banana Pro** model (`gemini-3-pro-image`) on Vertex AI.
  4. Upload image to Drive, link URL in Notion, and sync to DB.

---

## 🎨 GOOGLE BANANA IMAGE GENERATION TEMPLATE (gemini-3-pro-image)
All AI generated visuals must follow this exact prompt structure to ensure compliance with Sếp's premium dark aesthetics:

```text
[Aspect Ratio, e.g. "A highly realistic 16:9 macro photography shot of..."] [Tangible Physical Object, e.g., a vintage clockwork mechanism or dark stained wooden block tower]. The physical surface of the object has the words '[Vietnamese Text, e.g., "Tư duy hệ thống"]' beautifully engraved in clean, minimalist off-white geometric typography. The background is a minimalist modern dark office with a soft desk lamp casting a warm diffused golden glow, creating deep realistic shadows and diffused ambient occlusion on the surface of the object. The color palette is strictly deep grey #1E1D1B, matte charcoal, and subtle muted gold #B89A5A accents on the edges. No shiny surfaces, no plastics, no glowing elements, no levitations. The brand watermark '#VietBao' is naturally engraved onto the bottom corner of the wooden block. Cinematic look, shot on 85mm lens, shallow depth of field.
```

### Strict Visual Guidelines:
*   **Dimensions:** Square `1200x1200px` (1:1) | Horizontal `1200x630px`/`1200x800px` (16:9) | Vertical `960x1200px` (4:5).
*   **Materials:** Matte charcoal paper, dark stained wood, dark matte leather, soft graphite. No plastics, chrome, or glass.
*   **Output Format:** Convert the final image to solid RGB mode (Flatten layers) before saving to eliminate any transparency.
