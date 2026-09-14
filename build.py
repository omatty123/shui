#!/usr/bin/env python3
"""Build index.html for 水 · Water in Chinese Philosophy.

    python3 build.py

Organized by one question, not by school: in early China, taming a flood was the
first proof of the right to rule, so writing about water is writing about how to
govern people. Block it, or guide it?

Every passage is quoted from the Chinese text linked beside it (checked against
Chinese Wikisource, September 14, 2026). English renderings are close
translations made for this page. Edit QUESTIONS, then rebuild.
"""
import html, math, urllib.parse
from pathlib import Path

BASE = "https://omatty123.github.io/shui/"
WS = "https://zh.wikisource.org/wiki/"
SEP = "https://plato.stanford.edu/entries/"

WHO = {
  "mengzi": dict(name="Mengzi", zh="孟子", school="Ru", dates="fourth century BCE", href=SEP+"mencius/"),
  "kongzi": dict(name="Kongzi", zh="孔子", school="Ru", dates="551–479 BCE", href=SEP+"confucius/"),
  "xunzi":  dict(name="Xunzi",  zh="荀子", school="Ru", dates="third century BCE", href=SEP+"xunzi/"),
  "laozi":  dict(name="Laozi",  zh="老子", school="Dao", dates="traditionally sixth century BCE", href=SEP+"laozi/"),
  "zhuangzi": dict(name="Zhuangzi", zh="莊子", school="Dao", dates="fourth century BCE", href=SEP+"zhuangzi/"),
  "shu":    dict(name="Book of Documents", zh="尚書", school="", dates="", href=""),
}

FRAME_H = "Gun and Yu"
FRAME = ("Here’s the oldest water story in China. A great flood covers the land, and the emperor’s ministers agree that no one is better suited to fight it than Gun. "
         "Gun works at it for nine years, building walls against the water, and still the flood keeps coming. He is punished for failing, and his son Yu is given the job of carrying on his father’s work. "
         "Yu never forgets that failure. He spends years away from home, digging channels, building embankments, and learning how the water wants to move, until he finally leads it out to the sea. "
         "Legend says he went on to found China’s first dynasty.")
FRAME_2 = ("So the lesson is not “walls bad, channels good.” Yu used both. The lesson is in how he worked: with the water, and not only against it. "
           "Keep that in mind as you read. Every passage on this page is asking some version of that question, about water, and about people and power.")
FRAME_SRC = ("Shiji 2: Gun and Yu", WS+"史記/卷002")

FLOODS_H = "Four floods from our course"
FLOODS = [
  ("Gilgamesh, Tablet XI", "https://www.livius.org/articles/misc/great-flood/flood3_t-gilgamesh/",
   "The great gods", "Utnapishtim, warned by the god Ea, tears down his house and builds a boat."),
  ("Genesis 6–9", "https://www.biblegateway.com/passage/?search=Genesis+6-9&version=NRSVUE",
   "God", "Noah builds the ark as God instructs."),
  ("Quran, Sura 11 (Hud)", "https://quran.com/11",
   "God, against those who would not believe", "Nuh builds the ship. His own son refuses to board, and drowns."),
  ("Yu the Great", WS+"孟子/滕文公上",
   "No one", "Yu carries on his father’s work: years of channels and embankments, until the water reaches the sea."),
]
FLOODS_NOTE = ("Notice the difference? In Gilgamesh, Genesis and the Quran, the flood is decided in heaven, and the hero’s job is to hear the warning, "
               "do what he is told, and survive. In Yu’s story, nobody sends the flood. Floods are simply what rivers do. The hero’s job is to study the land, "
               "organize years of hard work, and get the water right for everyone. And his reward is more than survival: Heaven hands him the Great Plan, "
               "the pattern for ruling well. That is a whole different idea of power. You earn it by managing the water, and, as Xunzi will warn us, "
               "you can lose it the same way.")
HOW_H = "Before you start"
HOW = [
  "You’ll meet two traditions on this page, and we start with the older one. Dao 道 (dào, say “dow,” to rhyme with “how”) means “the Way.” Its founding teacher is Laozi, “the Old Master,” who in the traditional story was older than Kongzi. The Daoists ask us to follow the natural way of things instead of forcing them, which is exactly what water does. You’ll also meet Zhuangzi, a later Daoist famous for his stories.",
  "Ru 儒 (rú, say “roo”) is the tradition of Kongzi, the teacher English speakers call Confucius. It cares about learning, ritual, and growing into a good person who helps build a well-run society. In a famous story from the Shiji, the Records of the Historian, Kongzi travels to ask Laozi about ritual and comes away telling his students, “Today I met Laozi. He is like a dragon!”",
  "On each card, the Chinese reads from top to bottom, starting at the right, and the English translation sits right beside it.",
]

QUESTIONS = [
  dict(id="block-or-guide", zh="疏", py="shū", gloss="to clear a channel", title="Gun and Yu: fighting the water, or working with it?",
       lede="First the story itself. Then watch Mengzi turn Yu’s way of working into advice about clever people, and about human nature.",
       passages=[
    {"id": "yu-gun", "who": "shu", "zh": "我聞在昔，鯀陻洪水，汩陳其五行……鯀則殛死，禹乃嗣興。天乃錫禹洪范九疇，彝倫攸敘。", "en": "I have heard that long ago Gun dammed the flood waters and threw the Five Phases into disorder… Gun was punished and died, and Yu rose to take his place. Heaven then gave Yu the Great Plan in its nine divisions, and the lasting order of things was set right.", "cite": "Book of Documents, “Great Plan”", "work": "尚書 · 洪範", "href": "https://zh.wikisource.org/wiki/尚書/洪範"},
    {"id": "yu-flood", "who": "mengzi", "zh": "當堯之時，天下猶未平，洪水橫流，氾濫於天下……禹疏九河，瀹濟、漯而注諸海；決汝、漢，排淮、泗，而注之江，然後中國可得而食也。當是時也，禹八年於外，三過其門而不入。", "en": "In the time of Yao, the world was not yet in order. Flood waters ran crosswise, overflowing everywhere under heaven… Yu dredged the Nine Rivers, cleared the Ji and the Ta and sent them into the sea; he opened the Ru and the Han, drained the Huai and the Si, and sent them into the Yangzi. Only then could the central states grow food. In those years Yu was away eight years. Three times he passed his own gate and did not go in.", "cite": "Mengzi 3A4", "work": "孟子 · 滕文公上", "href": "https://zh.wikisource.org/wiki/孟子/滕文公上"},
    {"id": "yu-moves-water", "who": "mengzi", "zh": "所惡於智者，為其鑿也。如智者若禹之行水也，則無惡於智矣。禹之行水也，行其所無事也。", "en": "What people dislike about the clever is that they chisel their way through. If the clever moved the way Yu moved water, no one would dislike cleverness. When Yu moved water, he moved it along the course that needed no forcing.", "cite": "Mengzi 4B26", "work": "孟子 · 離婁下", "href": "https://zh.wikisource.org/wiki/孟子/離婁下"},
    {"id": "mengzi-nature", "who": "mengzi", "zh": "告子曰：「性，猶湍水也。決諸東方則東流，決諸西方則西流。人性之無分於善不善也，猶水之無分於東西也。」孟子曰：「水信無分於東西，無分於上下乎？人性之善也，猶水之就下也。人無有不善，水無有不下。今夫水：搏而躍之，可使過顙；激而行之，可使在山。是豈水之性哉？其勢則然也。人之可使為不善，其性亦猶是也。」", "en": "Gaozi said: “Human nature is like swirling water. Open a channel to the east and it flows east; open one to the west and it flows west. Human nature does not lean toward good or not-good, just as water does not lean toward east or west.” Mengzi said: “Water truly does not lean east or west. But does it not lean up or down? The goodness of human nature is like water’s going downward. There is no person who is not good, and no water that does not flow down. Now, strike water and make it leap, and you can send it over your head; dam it and drive it, and you can keep it on a mountain. But is that the nature of water? Force makes it so. People can be made to do what is not good, and their nature is being treated just like that.”", "cite": "Mengzi 6A2", "work": "孟子 · 告子上", "href": "https://zh.wikisource.org/wiki/孟子/告子上"}
       ]),
  dict(id="soft", zh="柔", py="róu", gloss="soft", title="Why does the soft win?",
       lede="Water is about the softest thing there is, and yet it wears away stone. It always sinks to the lowest place, and that is exactly why every river ends up in the sea. In the Zhuangzi, the River God, swollen with autumn floods, thinks he is the greatest water in the world, until he reaches the sea. What could a ruler, or any of us, learn from that?",
       passages=[
    {"id": "laozi-highest-good", "who": "laozi", "zh": "上善若水。水善利萬物而不爭，處眾人之所惡，故幾於道。居善地，心善淵，與善仁，言善信，正善治，事善能，動善時。夫唯不爭，故無尤。", "en": "The highest good is like water. Water is good at benefiting the ten thousand things and does not compete. It settles in the places everyone scorns, and so it comes close to the Way. It dwells in good ground, its heart is deep, it gives with kindness, speaks with trust, governs with order, works with skill, moves in time. Because it does not compete, it is never blamed.", "cite": "Daodejing 8", "work": "道德經 · 八章", "href": "https://zh.wikisource.org/wiki/道德經_(王弼本)"},
    {"id": "laozi-softest", "who": "laozi", "zh": "天下莫柔弱於水，而攻堅強者，莫之能勝，其無以易之。弱之勝強，柔之勝剛，天下莫不知，莫能行。", "en": "Nothing in the world is softer or weaker than water, yet nothing can beat it at wearing down the hard and strong, because nothing can change it. The weak overcomes the strong; the soft overcomes the hard. Everyone in the world knows this. No one can live by it.", "cite": "Daodejing 78", "work": "道德經 · 七十八章", "href": "https://zh.wikisource.org/wiki/道德經_(王弼本)"},
    {"id": "laozi-lowest", "who": "laozi", "zh": "江海所以能為百谷王者，以其善下之，故能為百谷王。是以欲上民，必以言下之。欲先民，必以身後之。是以聖人處上而民不重，處前而民不害。是以天下樂推而不厭，以其不爭，故天下莫能與之爭。", "en": "Rivers and seas can be kings of the hundred valleys because they are good at staying below them. That is how they become kings of the hundred valleys. So whoever wants to be above the people must speak as if below them, and whoever wants to lead the people must put himself behind them. That is why the sage can stand above the people without being a weight on them, and stand in front of them without doing them harm. The whole world is glad to push him forward and never grows tired of him. Because he does not compete, no one in the world can compete with him.", "cite": "Daodejing 66", "work": "道德經 · 六十六章", "href": "https://zh.wikisource.org/wiki/道德經_(王弼本)"},
    {"id": "zhuangzi-sea", "who": "zhuangzi", "zh": "北海若曰：「天下之水，莫大於海，萬川歸之，不知何時止而不盈；尾閭泄之，不知何時已而不虛；春秋不變，水旱不知……而吾未嘗以此自多者，自以比形於天地，而受氣於陰陽。」", "en": "Ruo of the North Sea said: “Of all the waters under heaven, none is greater than the sea. Ten thousand rivers flow into it, and no one knows when they will stop, yet it never fills. It drains away at Weilü, and no one knows when that will end, yet it never runs dry. Spring or autumn, it never changes; it knows nothing of floods or droughts… And yet I have never thought much of myself for this, since I take my shape from heaven and earth and my breath from yin and yang.”", "cite": "Zhuangzi 17, “Autumn Floods”", "work": "莊子 · 秋水", "href": "https://zh.wikisource.org/wiki/莊子/秋水"}
       ]),
  dict(id="river", zh="川", py="chuān", gloss="river", title="The river that never stops",
       lede="Kongzi stood by a river and said just one sentence. Generations later, Mengzi explained what he thought Kongzi saw in it.",
       passages=[
    {"id": "kongzi-river", "who": "kongzi", "zh": "子在川上曰：「逝者如斯夫！不舍晝夜。」", "en": "Standing by a river, the Master said: “Look how it all flows past, day and night, never stopping!”", "cite": "Analects 9.17", "work": "論語 · 子罕", "href": "https://zh.wikisource.org/wiki/論語/子罕第九"},
    {"id": "mengzi-source", "who": "mengzi", "zh": "徐子曰：「仲尼亟稱於水曰：『水哉！水哉！』何取於水也？」孟子曰：「源泉混混，不舍晝夜，盈科而後進，放乎四海；有本者如是，是之取爾。茍為無本，七、八月之間雨集，溝澮皆盈；其涸也，可立而待也。故聲聞過情，君子恥之。」", "en": "Xuzi said: “Zhongni kept praising water: ‘Water! Oh, water!’ What did he see in water?” Mengzi said: “A spring with a source gushes on, never stopping day or night. It fills each hollow, then moves on, out to the four seas. Whatever has a source is like this. That is what he saw in it. Without a source, the summer rains gather in the seventh and eighth months and every ditch fills, but you can stand there and watch them dry. So a noble person is ashamed when reputation runs beyond the facts.”", "cite": "Mengzi 4B18", "work": "孟子 · 離婁下", "href": "https://zh.wikisource.org/wiki/孟子/離婁下"}
       ]),
  dict(id="boat", zh="舟", py="zhōu", gloss="boat", title="Who carries whom?",
       lede="Picture the ruler sitting in a boat. Now picture the people as the water underneath. So who is really holding up whom?",
       passages=[
    {"id": "xunzi-boat", "who": "xunzi", "zh": "庶人安政，然後君子安位。傳曰：「君者，舟也；庶人者，水也。水則載舟，水則覆舟。」此之謂也。", "en": "Only when the common people are at peace with their government is the noble person secure in his place. As the saying goes: “The ruler is the boat; the common people are the water. Water carries the boat, and water overturns the boat.” That is what this means.", "cite": "Xunzi 9, “Regulations of a King”", "work": "荀子 · 王制", "href": "https://zh.wikisource.org/wiki/荀子/王制篇"}
       ])
]

BUILT = dict(id="built", zh="渠", py="qú", gloss="a canal",
  title="The world Yu built",
  lede=("This is not just an old story. People built by it for more than two thousand years. Before the modern age, nobody on earth built anything "
        "bigger than China’s waterworks, and today China is building the biggest ones again."),
  facts=[
    ("Dujiangyan, about 256 BCE",
     "Engineers in Sichuan divided the Min River using the shape of the land itself, without the use of dams. It still waters the Chengdu plain today: 668,700 hectares of farmland.",
     [("UNESCO", "https://whc.unesco.org/en/list/1001/")],
     ("img/dujiangyan.webp", "The Min River at Dujiangyan seen from a hillside, split in two around a long wooded island.",
      "星星", "https://commons.wikimedia.org/wiki/File:Dujiang_Weir.jpg", "CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/")),
    ("The Grand Canal, from the 5th century BCE",
     "Built in sections and joined into one system in the 7th century CE, it was the largest civil engineering project in the world before the Industrial Revolution. Boats still use it.",
     [("UNESCO", "https://whc.unesco.org/en/list/1443/")],
     ("img/grand-canal.webp", "A long cargo barge moving along the Grand Canal past apartment blocks.",
      "IcaN", "https://commons.wikimedia.org/wiki/File:A_boat_on_Grand_Canal_of_China.JPG", "public domain", "")),
    ("Today",
     "Like Yu, China uses both today, walls and channels. The Three Gorges Dam on the Yangtze is the largest hydroelectric plant on earth, and the South–North Water Diversion has already carried more than 90 billion cubic meters of water to China’s dry north.",
     [("USGS", "https://www.usgs.gov/water-science-school/science/three-gorges-dam-worlds-largest-hydroelectric-plant"),
      ("Xinhua", "https://english.news.cn/20260811/9dad0d0e1f974c6b8dfd712c770a2e21/c.html")],
     ("img/three-gorges.webp", "The Three Gorges Dam, a long concrete wall with red cranes on top, holding back the Yangtze.",
      "Le Grand Portage", "https://commons.wikimedia.org/wiki/File:ThreeGorgesDam-China2009.jpg", "CC BY 2.0", "https://creativecommons.org/licenses/by/2.0/")),
  ],
  close=("So here is a question to carry through the rest of our course. When you look at the Great Lakes, at New Orleans in Blood Dazzler, "
         "at the rising coasts in Rush: who is working with the water, and who is only fighting it?"))

YT = "https://www.youtube.com/watch?v="
# Short CGTN videos, each linked where it helps. "China in the Classics" clips are staged dramatizations.
WATCH = {
  "how": [("Stone Carving of Confucius Meeting Laozi", YT+"VjPuepc1qiw", "museum short from CGTN’s Every Treasure Tells a Story", "5 min")],
  "soft": [("Laozi finally understands the Way", YT+"ror4fpbWkhI", "dramatization from China in the Classics", "19 min")],
}
# A still from the video, shown as a clickable poster above its link.
POSTER = {
  "soft": ("img/laozi-video.webp", "A still from the video: an old teacher, a child and a younger man walk toward the camera in front of a waterfall. Subtitle: “Supreme good is like water.”"),
}
play_svg = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M10 8.5v7l6-3.5z"/></svg>'

def watch_html(key):
    items = WATCH.get(key, [])
    if not items:
        return ""
    lis = "".join(
        f'<li><a href="{e(href)}" target="_blank" rel="noopener">{play_svg}<span class="w-title">{e(title)}</span></a>'
        f'<span class="w-meta">{e(kind)} · {e(length)}</span></li>'
        for title, href, kind, length in items)
    poster = ""
    if key in POSTER:
        src, alt = POSTER[key]
        poster = (f'<a class="w-poster" href="{e(items[0][1])}" target="_blank" rel="noopener">'
                  f'<img src="{src}" alt="{e(alt)}" width="800" height="450" loading="lazy" decoding="async">{play_svg}</a>')
    return f'<div class="watch"><p class="watch-h">Watch</p>{poster}<ul>{lis}</ul></div>'

TITLE = "Water in Chinese Philosophy"
DESC = "Block it, or guide it? Water and ruling in Yu the Great, Kongzi, Mengzi, Laozi and Xunzi, with the Chinese beside close English translations."

e = lambda s: html.escape(s, quote=True)
han = sorted({c for q in QUESTIONS for p in q["passages"] for c in p["zh"] + p["work"]}
             | set("水儒道" + "".join(q["zh"] for q in QUESTIONS) + "".join(w["zh"] for w in WHO.values())))
latin = "https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap"
cjk = "https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500&display=swap&text=" + urllib.parse.quote("".join(han))
share_svg = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12M7 8l5-5 5 5M5 13v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/></svg>'

def who_line(key):
    w = WHO[key]
    bits = [f'<span lang="zh-Hant">{w["zh"]}</span> {e(w["name"])}']
    if w["school"]:
        bits.append(e(w["school"]))
    if w["dates"]:
        bits.append(f'<a href="{w["href"]}">{e(w["dates"])}</a>')
    return '<p class="who">' + " · ".join(bits) + "</p>"

floods_rows = "".join(
    ('<tr class="yu">' if story == "Yu the Great" else "<tr>") + f'<th scope="row"><a href="{e(href)}">{e(story)}</a></th><td>{e(who)}</td><td>{e(what)}</td></tr>'
    for story, href, who, what in FLOODS)
nav = "".join(f'<a href="#{q["id"]}">{e(q["title"])}</a>' for q in QUESTIONS) + f'<a href="#{BUILT["id"]}">{e(BUILT["title"])}</a>'
body = []
for q in QUESTIONS:
    items = []
    for p in q["passages"]:
        rows = max(6, min(14, math.ceil(math.sqrt(len(p["zh"]) * 1.7))))
        items.append(f'''
    <article class="passage" id="{p["id"]}">
      <blockquote class="zh" lang="zh-Hant" cite="{e(p["href"])}" style="--rows:{rows}">{e(p["zh"])}</blockquote>
      <div class="en-col">
        {who_line(p["who"])}
        <blockquote class="en">{e(p["en"])}</blockquote>
        <div class="cite">
          <a href="{e(p["href"])}"><span lang="zh-Hant">{e(p["work"])}</span> {e(p["cite"])}</a>
          <button class="share" type="button" data-id="{p["id"]}" data-title="{e(p["cite"])}">{share_svg}<span>Share</span></button>
        </div>
      </div>
    </article>''')
    body.append(f'''
  <section class="q" id="{q["id"]}" aria-labelledby="{q["id"]}-h">
    <header class="q-head">
      <p class="q-mark"><span class="q-glyph" lang="zh-Hant">{q["zh"]}</span><span class="q-py">{q["py"]}</span><span class="q-gloss">{e(q["gloss"])}</span></p>
      <div><h2 id="{q["id"]}-h">{e(q["title"])}</h2><p class="lede">{e(q["lede"])}</p>{watch_html(q["id"])}</div>
    </header>{"".join(items)}
  </section>''')

def fact_photo(src, alt, who, page, lic, lic_url):
    lic_html = f'<a href="{e(lic_url)}">{e(lic)}</a>' if lic_url else e(lic)
    return (f'<figure class="fact-photo"><img src="{src}" alt="{e(alt)}" width="960" height="640" loading="lazy" decoding="async">'
            f'<figcaption>Photo: <a href="{e(page)}">{e(who)}</a>, {lic_html}</figcaption></figure>')

built_facts = "".join(
    f'<div class="fact">{fact_photo(*photo)}<h3>{e(t)}</h3><p>{e(txt)}</p><p class="fact-src">Source: '
    + " · ".join(f'<a href="{e(h)}">{e(n)}</a>' for n, h in links) + '</p></div>'
    for t, txt, links, photo in BUILT["facts"])
body.append(f'''
  <section class="q built" id="{BUILT["id"]}" aria-labelledby="{BUILT["id"]}-h">
    <header class="q-head">
      <p class="q-mark"><span class="q-glyph" lang="zh-Hant">{BUILT["zh"]}</span><span class="q-py">{BUILT["py"]}</span><span class="q-gloss">{e(BUILT["gloss"])}</span></p>
      <div><h2 id="{BUILT["id"]}-h">{e(BUILT["title"])}</h2><p class="lede">{e(BUILT["lede"])}</p></div>
    </header>
    <div class="facts">{built_facts}</div>
    <p class="built-close">{e(BUILT["close"])}</p>
  </section>''')
han = sorted(set(han) | set(BUILT["zh"]))
cjk = "https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500&display=swap&text=" + urllib.parse.quote("".join(han))

doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE}</title>
<meta name="description" content="{e(DESC)}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta property="og:title" content="水 · {TITLE}">
<meta property="og:description" content="{e(DESC)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}">
<meta property="og:image" content="{BASE}og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="水 · {TITLE}">
<meta name="twitter:description" content="{e(DESC)}">
<meta name="twitter:image" content="{BASE}og.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{latin}">
<link rel="stylesheet" href="{e(cjk)}">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="hero">
  <p class="hero-mark"><span class="hero-glyph" lang="zh-Hant">水</span><span class="hero-py">shuǐ · water</span></p>
  <div class="hero-text">
    <h1>{TITLE}</h1>
    <nav class="jump" aria-label="Questions">{nav}</nav>
    <button class="share share-page" type="button" data-id="" data-title="{TITLE}">{share_svg}<span>Share this page</span></button>
  </div>
</header>
<main>
  <section class="frame" aria-labelledby="frame-h">
    <h2 id="frame-h">{FRAME_H}</h2>
    <p class="frame-text">{e(FRAME)}</p>
    <p class="frame-text">{e(FRAME_2)}</p>
    <p class="frame-src"><a href="{e(FRAME_SRC[1])}">{e(FRAME_SRC[0])}</a></p>
    <div class="floods-wrap">
      <table class="floods">
        <caption>{e(FLOODS_H)}</caption>
        <thead><tr><th scope="col">Story</th><th scope="col">Who sends the flood</th><th scope="col">What the hero does</th></tr></thead>
        <tbody>{floods_rows}</tbody>
      </table>
    </div>
    <p class="frame-compare">{e(FLOODS_NOTE)}</p>
    <div class="frame-how"><h3>{e(HOW_H)}</h3>{"".join(f"<p>{e(x)}</p>" for x in HOW)}<p class="frame-src"><a href="{WS}史記/卷063">Shiji 63: Kongzi visits Laozi</a></p>{watch_html("how")}</div>
  </section>{"".join(body)}
</main>
<footer class="foot">
  <p>Chinese texts as given on <a href="https://zh.wikisource.org/">Chinese Wikisource</a>, linked with each passage (Daodejing: Wang Bi text). “……” marks omitted lines. English renderings are close translations made for this page. Dates: <a href="https://plato.stanford.edu/">Stanford Encyclopedia of Philosophy</a>. Photos from <a href="https://commons.wikimedia.org/">Wikimedia Commons</a>, cropped and resized, credited under each; video still from CGTN.</p>
</footer>
<div class="toast" role="status" aria-live="polite" hidden></div>
<script src="share.js"></script>
</body>
</html>
'''
Path(__file__).with_name("index.html").write_text(doc)
print(f"wrote index.html: {sum(len(q['passages']) for q in QUESTIONS)} passages, {len(han)} Chinese characters subset")
