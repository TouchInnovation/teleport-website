#!/usr/bin/env python3
"""Inject an EN / 繁 / 简 language switch into the Teleport pages.

Tags each translatable element with data-i18n="key" (matched by its exact English
innerHTML), adds the switch to the nav, and appends a small i18n runtime.
Idempotent: re-running on an already-tagged file is a no-op.
"""
import json, re, sys

# key, English innerHTML (exact as in file), 繁體 (HK), 简体
T = [
 # nav / buttons
 ("nav.product", "Product", "產品", "产品"),
 ("nav.ai", "Controlled AI", "可控 AI", "可控 AI"),
 ("nav.how", "How it works", "運作方式", "运作方式"),
 ("nav.data", "Your data", "你的資料", "你的数据"),
 ("cta.intro", "Book an intro", "預約示範", "预约演示"),
 # hero
 ("hero.h1", 'The operating system for <span class="o">recruitment agencies</span>',
  '<span class="o">招聘公司</span>的<br>營運系統', '<span class="o">招聘机构</span>的<br>运营系统'),
 ("hero.p", "Companies, candidates, jobs, pipeline and placements in one record — so consultants spend the day placing people, not re-typing them.",
  "客戶公司、候選人、職位、招聘流程與成功入職，全部集中在同一份紀錄——顧問的時間用來促成配對，而不是重複輸入資料。",
  "客户公司、候选人、职位、招聘流程与成功录用，全部集中在同一条记录里——顾问把时间花在促成录用上，而不是重复录入。"),
 ("hero.cta1", "Book a 15-minute walkthrough", "預約 15 分鐘示範", "预约 15 分钟演示"),
 ("hero.cta2", "See the product", "了解產品", "了解产品"),
 # proof strip
 ("proof.live", "<b>Live</b> at a Hong Kong agency", "<b>實際運作</b>於香港招聘公司", "<b>实际运行</b>于香港招聘机构"),
 ("proof.lang", "<b>English &amp; 中文</b> search", "<b>中英文</b>搜尋", "<b>中英文</b>搜索"),
 ("proof.db", "<b>Your own</b> isolated database", "<b>獨立</b>專屬資料庫", "<b>独立</b>专属数据库"),
 ("proof.hk", "<b>Built in</b> Hong Kong", "<b>香港</b>研發", "<b>香港</b>研发"),
 # photo panel
 ("photo.tag", "Teleport HR Operating System", "Teleport 人力資源營運系統", "Teleport 人力资源运营系统"),
 ("photo.h2", "Built inside a working agency, for the desks that place people.",
  "在真實的招聘公司內打造，為每天促成入職的顧問而設。", "在真实的招聘机构中打造，为每天促成录用的顾问而设计。"),
 ("photo.p", "Teleport began as our own agency’s system. Every feature runs on live roles before we offer it to yours.",
  "Teleport 源自我們自家招聘公司的系統。每項功能都先在真實職位上運作，才會提供給你。",
  "Teleport 源自我们自家招聘机构的系统。每项功能都先在真实职位上运行，再提供给你。"),
 # product panel
 ("prod.h2", "One record, first CV to placed", "一份紀錄，由第一份履歷到成功入職", "一条记录，从第一份简历到成功录用"),
 ("prod.p", "The best of an ATS and a CRM in one place, with AI that reads CVs and searches the way consultants think.",
  "集 ATS 與 CRM 之長於一身，配合能讀懂履歷、按顧問思路搜尋的 AI。",
  "集 ATS 与 CRM 之长于一身，AI 能读懂简历，并按顾问的思路搜索。"),
 ("prod.cta", "See it on your roles", "用你的職位試試看", "用你的职位试试看"),
 ("four.source", "Source", "搜羅人才", "寻访人才"),
 ("four.source.p", "CV in, profile filled by AI", "上載履歷，AI 自動填寫檔案", "上传简历，AI 自动填写档案"),
 ("four.search", "Search", "搜尋", "搜索"),
 ("four.search.p", "By meaning, in English or 中文", "按語意搜尋，中英文皆可", "按语义搜索，中英文皆可"),
 ("four.pipe", "Pipeline", "招聘流程", "招聘流程"),
 ("four.pipe.p", "Every candidate, every stage", "每位候選人、每個階段", "每位候选人、每个阶段"),
 ("four.place", "Place", "成功入職", "成功录用"),
 ("four.place.p", "Placements and fees tracked", "追蹤入職與佣金", "跟踪录用与佣金"),
 # illustrative app record
 ("app.companies", "Companies", "公司", "公司"),
 ("app.people", "People", "人才", "人才"),
 ("app.jobs", "Jobs", "職位", "职位"),
 ("app.placements", "Placements", "入職", "录用"),
 ("app.title", "Regional Finance Manager", "區域財務經理", "区域财务经理"),
 ("app.sub", "Candidate · Hong Kong · EN / 中文", "候選人 · 香港 · 中 / 英", "候选人 · 香港 · 中 / 英"),
 ("st.sourced", "Sourced", "已搜羅", "已寻访"),
 ("st.interested", "Interested", "有興趣", "有意向"),
 ("st.short", "Shortlisted", "已入選", "已入围"),
 ("st.sent", "Sent", "已推薦", "已推荐"),
 ("st.interview", "Interview", "面試", "面试"),
 ("st.placed", "Placed", "已入職", "已录用"),
 ("kv.job", "Job", "職位", "职位"),
 ("kv.job.v", "Finance Manager, APAC", "亞太區財務經理", "亚太区财务经理"),
 ("kv.client", "Client", "客戶", "客户"),
 ("kv.client.v", "Manufacturing group", "製造業集團", "制造业集团"),
 ("kv.cv", "CV", "履歷", "简历"),
 ("kv.cv.v", "Parsed into profile · checked by consultant", "已解析至檔案 · 顧問已核對", "已解析至档案 · 顾问已核对"),
 ("kv.act", "Activity", "活動", "动态"),
 ("kv.act.v", "Call logged · interest confirmed", "已記錄通話 · 已確認意向", "已记录通话 · 已确认意向"),
 ("draft.tag", "AI draft · client write-up", "AI 草稿 · 客戶推薦信", "AI 草稿 · 客户推荐信"),
 ("draft.p", "Please find the candidate’s profile for your consideration of the Finance Manager, APAC role.",
  "現附上候選人資料，供貴公司考慮亞太區財務經理一職。", "现附上候选人资料，供贵公司考虑亚太区财务经理一职。"),
 ("draft.ul", "<li>Regional FP&amp;A across 6 markets</li><li>Qualified accountant</li><li>Manufacturing background</li>",
  "<li>橫跨 6 個市場的區域財務規劃與分析</li><li>合資格會計師</li><li>製造業背景</li>",
  "<li>覆盖 6 个市场的区域财务规划与分析</li><li>持证会计师</li><li>制造业背景</li>"),
 ("draft.approve", "Approve", "批准", "批准"),
 ("draft.edit", "Edit", "編輯", "编辑"),
 ("draft.reject", "Reject", "拒絕", "拒绝"),
 ("caption", "Illustrative record. The AI write-up panel is Controlled AI, in development with our launch agency.",
  "示意紀錄。AI 推薦信面板屬「可控 AI」功能，正與首家合作招聘公司共同開發。",
  "示意记录。AI 推荐信面板属于“可控 AI”功能，正与首家合作招聘机构共同开发。"),
 # controlled AI
 ("ai.h2", "AI drafts. <span>Your consultant decides.</span>", "AI 起草。<span>顧問決定。</span>", "AI 起草。<span>顾问决定。</span>"),
 ("ai.r1", "Nothing leaves without a yes", "未經批准，一律不發出", "未经批准，一律不发出"),
 ("ai.r1.p", "Every write-up, client CV and email stays a draft until a consultant approves it. No autonomous sending.",
  "每份推薦信、客戶版履歷和電郵，在顧問批准前都只是草稿，絕不會自動發送。",
  "每份推荐信、客户版简历和邮件，在顾问批准前都只是草稿，绝不会自动发送。"),
 ("ai.r2", "Every match explains itself", "每個配對都有理由", "每个匹配都有理由"),
 ("ai.r2.p", "When Teleport suggests a person, it says why — in words your consultant can check against the CV.",
  "Teleport 推薦人選時，會清楚寫出原因，讓顧問可以對照履歷核實。",
  "Teleport 推荐人选时会写明原因，顾问可以对照简历核实。"),
 ("ai.r3", "Numbers come from your data", "數字來自你的資料", "数字来自你的数据"),
 ("ai.r3.p", "Counts and reports are read from the database, never guessed by a chatbot.",
  "人數與報表直接讀取資料庫，絕不由聊天機械人估算。", "数量与报表直接读取数据库，绝不由聊天机器人猜测。"),
 # people band
 ("band.h2", "Recruitment is still a people business.", "招聘，始終是關於人的生意。", "招聘，始终是关于人的生意。"),
 ("band.p", "Teleport takes the re-typing, reformatting and chasing off the desk — so the hours go to the conversations that fill roles.",
  "Teleport 為顧問處理重複輸入、排版和追進度——把時間留給真正促成招聘的對話。",
  "Teleport 替顾问处理重复录入、排版和跟进——把时间留给真正促成招聘的沟通。"),
 # flow
 ("flow.h2", "One flow, the way a desk actually works.", "一條流程，貼合顧問的實際工作方式。", "一条流程，贴合顾问的实际工作方式。"),
 ("flow.p", "From a new role to a placement — every step on the same record.", "由新職位到成功入職——每一步都在同一份紀錄上。", "从新职位到成功录用——每一步都在同一条记录上。"),
 ("tr.source.p", "Bring in CVs and contacts.", "匯入履歷與聯絡人。", "导入简历与联系人。"),
 ("tr.match", "Match", "配對", "匹配"),
 ("tr.match.p", "Search your own pool by meaning.", "按語意搜尋你的人才庫。", "按语义搜索你的人才库。"),
 ("tr.short", "Shortlist", "篩選名單", "候选名单"),
 ("tr.short.p", "Title, company, salary at a glance.", "職銜、公司、薪酬一目了然。", "职位、公司、薪资一目了然。"),
 ("tr.write", "Write-up", "推薦信", "推荐信"),
 ("tr.write.p", "The pitch for this person, this role.", "為這位人選、這個職位而寫的推介。", "为这位人选、这个职位而写的推介。"),
 ("tr.cv", "Client CV", "客戶版履歷", "客户版简历"),
 ("tr.cv.p", "Your format, contact details hidden.", "你的格式，隱藏聯絡資料。", "你的格式，隐藏联系方式。"),
 ("tr.approve.p", "A consultant signs off. Always.", "必經顧問簽批。", "必须由顾问签批。"),
 ("tr.send", "Send &amp; place", "發送及入職", "发送与录用"),
 ("tr.send.p", "Feedback, interviews, placement fee.", "回饋、面試、入職佣金。", "反馈、面试、录用佣金。"),
 ("tr.live", "Live", "已上線", "已上线"),
 ("tr.building", "Building", "開發中", "开发中"),
 ("tr.placelive", "Placement live", "入職追蹤已上線", "录用跟踪已上线"),
 # live / next
 ("duo.live", "Live today", "現已上線", "现已上线"),
 ("duo.live.h2", "In production now", "正式運作中", "正式运行中"),
 ("l1", "Companies &amp; contacts", "公司與聯絡人", "公司与联系人"),
 ("l1.p", "Clients, hiring managers and the activity behind each one.", "客戶、招聘經理，以及每段往來紀錄。", "客户、招聘经理，以及每段往来记录。"),
 ("l2", "Talent pool &amp; smart search", "人才庫與智能搜尋", "人才库与智能搜索"),
 ("l2.p", "English or 中文, by meaning, title, company or skill.", "中英文皆可，按語意、職銜、公司或技能搜尋。", "中英文皆可，按语义、职位、公司或技能搜索。"),
 ("l3", "CV in, profile out", "上載履歷，自動建檔", "上传简历，自动建档"),
 ("l3.p", "AI fills the profile for the consultant to check.", "AI 填寫檔案，再由顧問核對。", "AI 填写档案，再由顾问核对。"),
 ("l4", "Jobs, pipeline &amp; shortlists", "職位、流程與篩選名單", "职位、流程与候选名单"),
 ("l4.p", "Every candidate’s stage on every role.", "每個職位上每位候選人的進度。", "每个职位上每位候选人的进度。"),
 ("l5", "Placements &amp; fees", "入職與佣金", "录用与佣金"),
 ("l5.p", "Close the loop from first call to placement fee.", "由第一通電話到入職佣金，完整跟進。", "从第一通电话到录用佣金，完整跟进。"),
 ("duo.next", "In development", "開發中", "开发中"),
 ("duo.next.h2", "Building with our launch agency", "與首家合作招聘公司共同開發", "与首家合作招聘机构共同开发"),
 ("n1", "Match reasons", "配對理由", "匹配理由"),
 ("n1.p", "Why this person fits this role, written out.", "清楚寫出這位人選為何適合這個職位。", "写明这位人选为何适合这个职位。"),
 ("n2", "Write-up drafts", "推薦信草稿", "推荐信草稿"),
 ("n2.p", "Client pitches in your desk’s own format.", "以你團隊的格式撰寫客戶推介。", "按你团队的格式撰写客户推介。"),
 ("n3", "Branded client CVs", "品牌客戶版履歷", "品牌客户版简历"),
 ("n3.p", "Your template, your logo, contacts hidden.", "你的範本、你的標誌，隱藏聯絡資料。", "你的模板、你的标志，隐藏联系方式。"),
 ("n4", "Send &amp; track", "發送及追蹤", "发送与跟踪"),
 ("n4.p", "Client emails and feedback stay on the record.", "客戶電郵與回饋都保留在紀錄上。", "客户邮件与反馈都保留在记录上。"),
 ("n5", "Your brand", "你的品牌", "你的品牌"),
 ("n5.p", "Your logo and colours, so clients see your agency.", "你的標誌與顏色，客戶看到的是你的公司。", "你的标志与配色，客户看到的是你的公司。"),
 # data
 ("data.h2", "Your candidates stay yours.", "你的候選人，始終屬於你。", "你的候选人，始终属于你。"),
 ("data.p", "Agencies told us their first fear: a platform that looks like it belongs to someone else. So we built the opposite.",
  "招聘公司告訴我們，最擔心的是平台看起來屬於別人。所以我們反其道而行。",
  "招聘机构告诉我们，最担心的是平台看起来属于别人。所以我们反其道而行。"),
 ("f1", "Your own instance", "專屬獨立系統", "专属独立系统"),
 ("f1.p", "An isolated database per agency — not a shared pool.", "每家公司一個獨立資料庫——不是共用的人才池。", "每家机构一个独立数据库——不是共享的人才池。"),
 ("f2", "No marketplace", "不設人才市場", "不设人才市场"),
 ("f2.p", "We never pool or resell candidates between clients.", "我們絕不會在客戶之間匯集或轉售候選人。", "我们绝不会在客户之间汇集或转售候选人。"),
 ("f3", "Demos on synthetic data", "示範只用模擬資料", "演示只用模拟数据"),
 ("f3.p", "Prospects see made-up Hong Kong records, never a live agency’s.", "潛在客戶只會看到虛構的香港紀錄，絕不會看到真實公司的資料。", "潜在客户只会看到虚构的香港记录，绝不会看到真实机构的数据。"),
 ("f4", "PDPO in mind", "顧及私隱條例", "兼顾隐私条例"),
 ("f4.p", "Designed with Hong Kong’s privacy ordinance in mind. Migration from your current system scoped with you.",
  "設計時已顧及香港《個人資料（私隱）條例》。由現有系統遷移的範圍，會與你一同規劃。",
  "设计时已考虑香港《个人资料（私隐）条例》。从现有系统迁移的范围，将与你共同规划。"),
 # close
 ("close.h2", "Fifteen minutes. Your workflow. No slides.", "十五分鐘。你的流程。不用簡報。", "十五分钟。你的流程。不放幻灯片。"),
 ("close.p", "We walk one role from new job to placement on a demo with Hong Kong sample data — and show what moving your database would take.",
  "我們會用香港示範資料，帶你走一遍由新職位到成功入職的完整流程——並說明搬遷你的資料庫需要甚麼。",
  "我们会用香港示例数据，带你走完从新职位到成功录用的完整流程——并说明迁移你的数据库需要什么。"),
 # footer
 ("foot", 'HR Operating System · Hong Kong · © <span id="yr">2026</span>',
  '人力資源營運系統 · 香港 · © <span id="yr">2026</span>', '人力资源运营系统 · 香港 · © <span id="yr">2026</span>'),
]

META = {
 "en": {"title": "Teleport — The operating system for recruitment agencies",
        "desc": "Teleport keeps companies, candidates, jobs, pipeline and placements in one record for Hong Kong recruitment agencies. AI drafts; your consultant decides."},
 "zh-HK": {"title": "Teleport — 專為招聘公司而設的營運系統",
           "desc": "Teleport 把客戶公司、候選人、職位、招聘流程與成功入職集中在同一份紀錄。AI 起草，顧問決定。"},
 "zh-CN": {"title": "Teleport — 专为招聘机构打造的运营系统",
           "desc": "Teleport 把客户公司、候选人、职位、招聘流程与成功录用集中在同一条记录里。AI 起草，顾问决定。"},
}

CSS = """
/* ---------- Language switch ---------- */
.lang{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:3px;gap:2px;background:#fff}
.lang button{all:unset;cursor:pointer;min-width:34px;height:32px;padding:0 10px;border-radius:999px;font-size:14px;font-weight:500;text-align:center;line-height:32px;color:var(--ink-2)}
.lang button:hover{color:var(--ink)}
.lang button[aria-pressed="true"]{background:var(--ink);color:#fff}
.lang button:focus-visible{outline:3px solid var(--orange);outline-offset:2px}
@media (max-width:520px){.nav .pill.black{display:none}}
/* CJK typography */
html:lang(zh-HK) body{font-family:"Inter","PingFang HK","Noto Sans TC","Microsoft JhengHei",system-ui,sans-serif}
html:lang(zh-CN) body{font-family:"Inter","PingFang SC","Noto Sans SC","Microsoft YaHei",system-ui,sans-serif}
html:lang(zh-HK) h1,html:lang(zh-HK) h2,html:lang(zh-HK) h3,html:lang(zh-HK) .wm~*{font-family:inherit}
html:lang(zh-CN) h1,html:lang(zh-CN) h2,html:lang(zh-CN) h3{font-family:inherit}
html:lang(zh) body{letter-spacing:.01em;line-height:1.6}
html:lang(zh) h1,html:lang(zh) h2{letter-spacing:0;line-height:1.18;font-weight:600}
html:lang(zh) .hero h1{max-width:12em}
html:lang(zh) .statement h2,html:lang(zh) .photo .copy h2{max-width:13em}
"""

SWITCH = ('<div class="lang" role="group" aria-label="Language / 語言">'
          '<button type="button" data-lang="en" lang="en" aria-pressed="true">EN</button>'
          '<button type="button" data-lang="zh-HK" lang="zh-HK" aria-pressed="false" title="繁體中文">繁</button>'
          '<button type="button" data-lang="zh-CN" lang="zh-CN" aria-pressed="false" title="简体中文">简</button>'
          '</div>')

JS_TMPL = r"""
<script>
/* i18n: EN / 繁 / 简. ?lang=zh-HK|zh-CN|en overrides; choice saved in localStorage. */
(function(){
  var DICT = __DICT__, META = __META__, LANGS = ['en','zh-HK','zh-CN'];
  var nodes = document.querySelectorAll('[data-i18n]');
  nodes.forEach(function(n){ n.__en = n.innerHTML; });
  function pick(){
    var q = new URLSearchParams(location.search).get('lang');
    if (LANGS.indexOf(q) > -1) return q;
    try { var s = localStorage.getItem('teleport-lang'); if (LANGS.indexOf(s) > -1) return s; } catch(e){}
    var b = (navigator.language || 'en').toLowerCase();
    if (b.indexOf('zh') === 0) return /cn|sg|hans/.test(b) ? 'zh-CN' : 'zh-HK';
    return 'en';
  }
  function apply(l, save){
    nodes.forEach(function(n){
      var k = n.getAttribute('data-i18n');
      n.innerHTML = (l === 'en' || !DICT[k]) ? n.__en : DICT[k][l === 'zh-HK' ? 0 : 1];
    });
    var yr = document.getElementById('yr'); if (yr) yr.textContent = new Date().getFullYear();
    document.documentElement.lang = l;
    document.title = META[l].title;
    var d = document.querySelector('meta[name="description"]'); if (d) d.setAttribute('content', META[l].desc);
    document.querySelectorAll('.lang button').forEach(function(b){ b.setAttribute('aria-pressed', String(b.dataset.lang === l)); });
    if (save) {
      try { localStorage.setItem('teleport-lang', l); } catch(e){}
      var u = new URL(location.href); if (l === 'en') u.searchParams.delete('lang'); else u.searchParams.set('lang', l);
      history.replaceState(null, '', u);
    }
  }
  document.querySelectorAll('.lang button').forEach(function(b){
    b.addEventListener('click', function(){ apply(b.dataset.lang, true); });
  });
  apply(pick(), false);
})();
</script>
"""


def tag(html, en, key):
    """Add data-i18n=key to every element whose innerHTML is exactly `en`. Skips <b> wrappers."""
    out, i, n = [], 0, 0
    needle = '>' + en + '</'
    while True:
        j = html.find(needle, i)
        if j < 0:
            break
        lt = html.rfind('<', 0, j)
        open_tag = html[lt:j]
        # skip closing tags, already-tagged elements, and the bold fragments inside the proof strip
        if open_tag.startswith('</') or 'data-i18n' in open_tag or (open_tag == '<b' and key.startswith('tr.')):
            out.append(html[i:j + 1]); i = j + 1; continue
        out.append(html[i:lt]); out.append(open_tag + f' data-i18n="{key}"' + '>'); i = j + 1; n += 1
    out.append(html[i:])
    return ''.join(out), n


def main(path):
    s = open(path, encoding='utf-8').read()
    if 'class="lang"' in s:
        print(path, 'already has a language switch'); return
    s = s.replace('</style>', CSS + '</style>', 1)
    s = s.replace('<span class="spacer"></span>', '<span class="spacer"></span>\n    ' + SWITCH, 1)
    used, missing = {}, []
    for key, en, hk, cn in T:
        s, n = tag(s, en, key)
        if n: used[key] = [hk, cn]
        else: missing.append(key)
    js = JS_TMPL.replace('__DICT__', json.dumps(used, ensure_ascii=False)).replace('__META__', json.dumps(META, ensure_ascii=False))
    s = s.replace('</body>', js + '</body>', 1)
    # the old year script would overwrite nothing harmful; keep it.
    open(path, 'w', encoding='utf-8').write(s)
    print(path, 'tagged', len(used), 'keys; not on this page:', missing)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        main(p)
