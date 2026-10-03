# Generates the static content pages of cryptorobot.software and its sitemap.
# Run from anywhere: python3 _build/build_pages.py (writes <slug>/index.html
# next to this folder). GitHub Pages skips folders starting with "_".
import os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://cryptorobot.software"
GA_ID = "G-0GTB2G1NR9"
UPDATED = "3 October 2026"

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://cryptorobot.software/{slug}/">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://cryptorobot.software/{slug}/">
<meta property="og:type" content="{ogtype}">
{robots}<meta name="theme-color" content="#0d1612">
<link rel="preload" href="/assets/fonts/Archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/consent.js" data-ga="{ga}"></script>
{jsonld}</head>
<body>
<div class="wrap top">
  <a class="mark" href="/"><i aria-hidden="true"></i>Crypto Robot</a>
  <nav aria-label="Main"><a href="/#rules">The rules</a><a class="hide-sm" href="/how-to-build-a-crypto-trading-bot/"{cur_review}>Build a bot</a><a href="/contact/"{cur_contact}>Contact</a></nav>
</div>

<main class="page">
  <div class="wrap">
    <p class="kicker">{kicker}</p>
    <h1>{h1}</h1>
{updated}    <div class="prose">
{body}
    </div>
  </div>
</main>

<footer>
  <div class="wrap">
    {footer_nav}
    <span>&copy; 2026 Crypto Robot</span>
    <small>Educational simulator. All balances are virtual and no real money is traded. Nothing on this site is financial advice. Crypto-assets are high risk and results on virtual money do not predict real results. Sign-up is handled by our partner AFFCOIN, and we may receive a commission when you open an account.</small>
  </div>
</footer>
{scripts}</body>
</html>
"""

CTA = """      <div class="page-cta">
        <p>{text}</p>
        <a class="btn" href="/#start">Build my first bot <span aria-hidden="true">&rarr;</span></a>
      </div>"""

PAGES = []

# ---------------------------------------------------------------- contact
PAGES.append(dict(
  slug="contact", kicker="Contact", h1="Talk to the Crypto Robot team",
  title="Contact | Crypto Robot",
  desc="Questions about the crypto bot challenges, your virtual balance or the rules? Send the Crypto Robot team a message and we will reply by email.",
  body="""      <p>Questions about a challenge, the rules or how your bot is evaluated? Send us a message and we will reply by email, usually within two working days.</p>
      <form class="cform" id="cform" novalidate>
        <div class="row">
          <label>Name<input name="name" type="text" autocomplete="name" maxlength="100" required></label>
          <label>Email<input name="email" type="email" autocomplete="email" maxlength="200" required></label>
        </div>
        <label>Message<textarea name="message" maxlength="5000" required></textarea></label>
        <div class="hp" aria-hidden="true"><label>Website<input name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
        <button class="btn" type="submit">Send message <span aria-hidden="true">&rarr;</span></button>
        <p class="cform-status" role="status" aria-live="polite"></p>
      </form>
      <h2>Login, password or verification code</h2>
      <p>Accounts are handled by our partner AFFCOIN. For a lost password, a verification code that never arrived or a request about your account data, you can also write to <a href="mailto:support@affcoin.com">support@affcoin.com</a>.</p>
      <div class="callout"><p><strong>We will never ask you for money, a card number or a crypto wallet.</strong> Every balance on Crypto Robot is virtual. If someone contacts you on our behalf and asks for a payment, it is not us.</p></div>""",
  scripts="""<script>
(function(){
  var f=document.getElementById("cform");if(!f)return;
  var st=f.querySelector(".cform-status"),btn=f.querySelector("button");
  function show(msg,cls){st.textContent=msg;st.className="cform-status "+(cls||"")}
  f.addEventListener("submit",function(e){
    e.preventDefault();
    var d={name:f.name.value.trim(),email:f.email.value.trim(),message:f.message.value.trim(),website:f.website.value};
    if(!d.name||!d.message||!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(d.email)){show("Please fill in your name, a valid email and a message.","err");return}
    btn.disabled=true;show("Sending...");
    fetch("https://bitcoinera-contact.martinratinaud.workers.dev",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)})
      .then(function(r){return r.json().then(function(j){return{ok:r.ok&&j.ok,j:j}})})
      .then(function(res){if(res.ok){f.reset();show("Thanks, your message has been sent. We will reply by email.","ok")}else{show(res.j.error||"Message could not be sent. Please try again later.","err")}})
      .catch(function(){show("Message could not be sent. Please try again later.","err")})
      .then(function(){btn.disabled=false});
  });
})();
</script>
"""))

# ---------------------------------------------------------------- legal notice
# TODO before going live: replace the publisher block with the legal entity
# (company name, registration number, address, director of publication).
PAGES.append(dict(
  slug="legal-notice", kicker="Legal", h1="Legal notice", title="Legal notice | Crypto Robot",
  desc="Who publishes cryptorobot.software, who hosts it, who runs the trading accounts and how to reach us.",
  body="""      <h2>Publisher</h2>
      <dl class="facts">
        <dt>Site</dt><dd>cryptorobot.software</dd>
        <!-- TODO: legal entity, registration number and registered address of the publisher -->
        <dt>Publisher</dt><dd>Crypto Robot, independent publisher and owner of the cryptorobot.software domain name</dd>
        <dt>Contact</dt><dd><a href="/contact/">Contact form</a></dd>
      </dl>
      <h2>Hosting</h2>
      <dl class="facts">
        <dt>Host</dt><dd>GitHub, Inc. (GitHub Pages)</dd>
        <dt>Address</dt><dd>88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, United States</dd>
        <dt>Contact form relay</dt><dd>Cloudflare, Inc., 101 Townsend Street, San Francisco, CA 94107, United States</dd>
      </dl>
      <h2>Accounts and affiliate disclosure</h2>
      <p>Account creation and login are handled by our partner AFFCOIN, an affiliate network. We may receive a commission when you open an account through this site. This never costs you anything, since the challenge is free. AFFCOIN can be reached at <a href="https://affcoin.com/" rel="nofollow noopener" target="_blank">affcoin.com</a> and <a href="mailto:contact@affcoin.com">contact@affcoin.com</a>. The data you enter in the sign-up form is sent directly to AFFCOIN and handled under <a href="https://affcoin.com/privacy" rel="nofollow noopener" target="_blank">its privacy policy</a>.</p>
      <h2>No connection with other &ldquo;crypto robot&rdquo; products</h2>
      <p>Crypto Robot is the name of this independent, free simulator. It has no connection with the automated trading products sold online under similar names that ask you to deposit money. We never ask for a deposit.</p>
      <h2>Not financial advice</h2>
      <p>Crypto Robot is an educational simulator. Every balance is virtual, no real money is traded and nothing on this site is investment, financial or tax advice, or an invitation to buy crypto-assets. Results achieved with virtual money do not predict results with real money. Crypto-assets are high risk: you could lose all the money you invest, and you are unlikely to be protected if something goes wrong.</p>
      <h2>Intellectual property</h2>
      <p>The texts, design and code of this site belong to the publisher unless stated otherwise. Brand names quoted on this site belong to their owners and are used for identification only.</p>
      <h2>Related pages</h2>
      <ul><li><a href="/terms/">Terms of use</a></li><li><a href="/privacy-policy/">Privacy policy</a></li></ul>"""))

# ---------------------------------------------------------------- privacy
PAGES.append(dict(
  slug="privacy-policy", kicker="Legal", h1="Privacy policy", title="Privacy policy | Crypto Robot",
  desc="What personal data cryptorobot.software collects, why, who receives it, how long it is kept and how to exercise your rights.",
  body="""      <p>This policy explains what happens to your personal data when you visit cryptorobot.software, write to us or open an account. We collect as little as we can.</p>
      <h2>1. Who is responsible</h2>
      <p>The publisher of cryptorobot.software (see the <a href="/legal-notice/">legal notice</a>) is responsible for the data collected through this site&rsquo;s contact form. Data entered in the sign-up form is collected on this page and sent directly to our partner AFFCOIN. For that collection and transfer we act together with AFFCOIN; AFFCOIN then handles your account and is responsible for it under <a href="https://affcoin.com/privacy" rel="nofollow noopener" target="_blank">its own privacy policy</a>. You can exercise your rights with either of us.</p>
      <h2>2. What we collect and why</h2>
      <table>
        <thead><tr><th>When</th><th>Data</th><th>Purpose</th><th>Legal basis</th></tr></thead>
        <tbody>
          <tr><td>You use the contact form</td><td>Name, email, message</td><td>Answer your message</td><td>Legitimate interest, or steps before a contract</td></tr>
          <tr><td>You open an account</td><td>First and last name, email, password, phone number, newsletter choice</td><td>Create and run your challenge account, verify it, and send you news if you opted in (handled by AFFCOIN)</td><td>Contract; consent for the newsletter</td></tr>
          <tr><td>You visit any page</td><td>IP address, browser, pages requested (technical logs)</td><td>Deliver the site and keep it secure</td><td>Legitimate interest</td></tr>
        </tbody>
      </table>
      <p>We do not sell your data and we do not run advertising trackers on this site. Analytics only uses cookies if you accept them (see section 5).</p>
      <h2>3. Who receives it</h2>
      <ul>
        <li><strong>AFFCOIN</strong> and the providers it works with, for everything you type in the sign-up form, sent directly from your browser to its servers.</li>
        <li><strong>Cloudflare</strong>, which relays contact-form messages to our mailbox.</li>
        <li><strong>GitHub</strong>, which hosts the site and keeps technical access logs.</li>
        <li><strong>Google</strong> (Google Analytics), only if you accept analytics cookies: pages viewed, approximate location, device and browser, used to count visits. IP addresses are not stored by Google Analytics 4. Data may be processed in the United States under the EU-US Data Privacy Framework.</li>
      </ul>
      <p>Some of these providers are based in the United States. Transfers rely on the safeguards they offer, such as the EU-US Data Privacy Framework or standard contractual clauses.</p>
      <h2>4. How long we keep it</h2>
      <p>Contact messages are kept for up to 3 years after our last exchange, then deleted. Account data is kept by AFFCOIN for as long as your account is open and then according to its policy.</p>
      <h2 id="cookies">5. Cookies</h2>
      <p>We use Google Analytics cookies (<code>_ga</code>, <code>_ga_*</code>, kept up to 13 months) to count visits and see which pages are useful. They are set only after you click &ldquo;Accept&rdquo; in the cookie banner. If you decline, Google Analytics runs without cookies and receives no identifier for you. We do not use advertising cookies. Your choice is stored in your browser and you can change it at any time with the <a href="/privacy-policy/#cookies" data-cookie-settings>cookie settings</a> link at the bottom of every page.</p>
      <p>Our fonts are served from our own host. The sign-up widget, loaded from affcoin.com, may store what it needs to run the form and your session. Those cookies are covered by AFFCOIN&rsquo;s policy.</p>
      <h2>6. Your rights</h2>
      <p>You can ask to access, correct or delete your data, object to its use, restrict it, or receive a copy. Withdraw your newsletter consent at any time with the unsubscribe link in each email. To exercise a right, use our <a href="/contact/">contact form</a>, or write to <a href="mailto:support@affcoin.com">support@affcoin.com</a> for account data. You can also complain to your data protection authority.</p>
      <h2>7. Changes</h2>
      <p>We will update this page when our practices change. The date at the top shows the latest version.</p>"""))

# ---------------------------------------------------------------- terms
PAGES.append(dict(
  slug="terms", kicker="Legal", h1="Terms of use", title="Terms of use | Crypto Robot",
  desc="The rules for using cryptorobot.software and taking part in the virtual crypto bot trading challenges.",
  body="""      <p>By using cryptorobot.software or opening an account through it, you accept these terms. If you do not agree with them, please do not use the site.</p>
      <h2>1. What Crypto Robot is</h2>
      <p>Crypto Robot is an educational simulator. You build a crypto trading bot, run it on live market prices with a <strong>virtual balance of $10,000</strong>, and try to clear three levels. No real money is deposited, traded or won, and the virtual balance has no cash value.</p>
      <h2>2. Who can join</h2>
      <p>You must be at least 18 years old and allowed to use this kind of service where you live. One person, one account. The information you give when signing up must be accurate.</p>
      <h2>3. Your account</h2>
      <p>Accounts are created and run by our partner AFFCOIN, whose own terms also apply. We may receive a commission when you open an account. Keep your password private. You are responsible for what happens under your account.</p>
      <h2>4. Challenge rules</h2>
      <table>
        <thead><tr><th>Level</th><th>Target</th><th>Min. days</th><th>Max. days</th><th>Max. drawdown</th><th>Daily drawdown</th></tr></thead>
        <tbody>
          <tr><td>Level 1</td><td>+10%</td><td>5</td><td>10</td><td>-10%</td><td>-5%</td></tr>
          <tr><td>Level 2</td><td>+5%</td><td>5</td><td>No limit</td><td>-10%</td><td>-5%</td></tr>
          <tr><td>Level 3</td><td>+5%</td><td>None</td><td>No limit</td><td>-10%</td><td>-5%</td></tr>
        </tbody>
      </table>
      <p>Breaching the daily or the maximum drawdown ends the challenge immediately. We may adjust the rules for future challenges; a challenge already running keeps the rules it started with.</p>
      <h2>5. Fair use</h2>
      <p>Do not exploit bugs, price-feed errors or latency, share accounts, use several accounts to game the levels, or attack the platform. We may suspend an account that breaks these rules.</p>
      <h2>6. No financial advice, no guarantee</h2>
      <p>Nothing on Crypto Robot is investment, financial or tax advice, or an invitation to buy crypto-assets. Performance on virtual money does not predict results on real money, and crypto-assets are high risk. The service is provided as is, and may be interrupted for maintenance.</p>
      <h2>7. Liability</h2>
      <p>Since no real money is at stake, we are not liable for any trading decision you take outside Crypto Robot, or for any loss arising from it. Nothing in these terms limits liability that cannot legally be limited.</p>
      <h2>8. Personal data</h2>
      <p>See our <a href="/privacy-policy/">privacy policy</a>.</p>
      <h2>9. Changes and contact</h2>
      <p>We may update these terms; the date at the top shows the current version. Questions: <a href="/contact/">contact us</a>.</p>"""))

# ---------------------------------------------------------------- SEO guides
# One dict per guide; guide() adds the FAQ block, the CTA, the related-guides
# list and the Article + FAQPage JSON-LD. Angles differ from bitcoinera.com on
# purpose: sister sites must not publish the same text.
LEVELS_TABLE = """      <table>
        <thead><tr><th>Level</th><th>Target</th><th>Min. days</th><th>Max. days</th><th>Max. drawdown</th><th>Daily drawdown</th></tr></thead>
        <tbody>
          <tr><td>Level 1</td><td>+10%</td><td>5</td><td>10</td><td>-10%</td><td>-5%</td></tr>
          <tr><td>Level 2</td><td>+5%</td><td>5</td><td>No limit</td><td>-10%</td><td>-5%</td></tr>
          <tr><td>Level 3</td><td>+5%</td><td>None</td><td>No limit</td><td>-10%</td><td>-5%</td></tr>
        </tbody>
      </table>"""

def guide(slug, h1, title, desc, body, faq, cta, short):
    PAGES.append(dict(
      slug=slug, kicker="Guide", ogtype="article", h1=h1, title=title, desc=desc, short=short,
      body=body + "\n      <h2>Frequently asked questions</h2>\n"
        + "\n".join(f"      <h3>{q}</h3>\n      <p>{a}</p>" for q, a in faq)
        + "\n" + CTA.format(text=cta) + "\n{related}",
      jsonld=[
        {"@context":"https://schema.org","@type":"Article","headline":h1,"datePublished":"2026-10-03","dateModified":"2026-10-03","author":{"@type":"Organization","name":"Crypto Robot"},"publisher":{"@type":"Organization","name":"Crypto Robot"},"mainEntityOfPage":f"{SITE}/{slug}/"},
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in faq]},
      ]))

# ---- how to build a crypto trading bot (US 30 + github 40 + strategy 40; SERP = tutorials, open)
guide("how-to-build-a-crypto-trading-bot",
  "How to build a crypto trading bot: a step-by-step guide for beginners",
  "How to Build a Crypto Trading Bot (Step by Step, No Real Money)",
  "Build your first crypto trading bot in six steps: pick a market, write the rules, set the risk limits, code or configure it, backtest it, then run it on live prices with virtual money.",
  """      <p>A crypto trading bot is a program that buys and sells for you according to rules you set. It does not get tired, scared or greedy, and it does exactly what you told it to, including your mistakes. Building one is less about code than about writing rules precise enough for a machine to follow. This guide walks through the whole process, from the first idea to a bot running on live prices with virtual money.</p>
      <h2>What a trading bot is made of</h2>
      <p>Every bot, from a weekend script to a hedge-fund system, has the same four parts:</p>
      <ul>
        <li><strong>Data.</strong> The prices the bot watches: candles of 1 minute, 1 hour or 1 day.</li>
        <li><strong>Signal.</strong> The condition that triggers a trade, for example &ldquo;the 20-hour average crosses above the 50-hour average&rdquo;.</li>
        <li><strong>Risk rules.</strong> How much to put on each trade, where to cut a loss, and when to stop trading for the day.</li>
        <li><strong>Execution.</strong> The part that actually places orders on an exchange or a simulator.</li>
      </ul>
      <p>Beginners spend most of their time on the signal. The risk rules decide whether the bot survives.</p>
      <h2>Step 1: pick one market and one timeframe</h2>
      <p>Start with a single pair, such as BTC/USD or ETH/USD, and a single candle size. Bitcoin on 1-hour candles is a reasonable first choice: liquid, closely watched and not as noisy as 1-minute data. Adding coins and timeframes later is easy. Debugging five at once is not.</p>
      <h2>Step 2: write the rules in plain sentences</h2>
      <p>Before any code, write the strategy as if you were explaining it to a friend. Every rule must be testable with a yes or no.</p>
      <ul>
        <li><strong>Entry:</strong> buy when the RSI(14) closes below 30 and the price is above the 200-hour average.</li>
        <li><strong>Exit:</strong> sell when the RSI closes above 55, or after 48 hours, whichever comes first.</li>
        <li><strong>Stop:</strong> sell if the trade is down 3%.</li>
      </ul>
      <p>If a sentence contains &ldquo;usually&rdquo;, &ldquo;roughly&rdquo; or &ldquo;when it looks strong&rdquo;, it is not a rule yet.</p>
      <h2>Step 3: set the risk limits before anything else</h2>
      <p>Decide the size of each trade from the loss you accept, not from the gain you hope for. A common starting point is to risk 1% of the balance per trade. With a 3% stop, that means a position of about a third of the balance. Add two account-level brakes: a daily loss limit that stops the bot for the day, and a maximum drawdown that switches it off until you review it.</p>
      <h2>Step 4: code it or configure it</h2>
      <p>You have three routes:</p>
      <table>
        <thead><tr><th>Route</th><th>Skills needed</th><th>Good for</th></tr></thead>
        <tbody>
          <tr><td>Python with an exchange library</td><td>Basic programming</td><td>Full control, any strategy</td></tr>
          <tr><td>Open-source bot framework</td><td>Some programming, setup on a server</td><td>Ready-made backtesting and order handling</td></tr>
          <tr><td>No-code bot builder</td><td>None</td><td>Testing simple rule sets quickly</td></tr>
        </tbody>
      </table>
      <p>AI assistants can turn your plain-English rules into code. Read what they write, line by line: they make confident mistakes, and the bot will repeat them every time. Our guide to the <a href="/chatgpt-trading-bot/">ChatGPT trading bot</a> covers this in detail.</p>
      <h2>Step 5: backtest to throw out bad ideas</h2>
      <p>A backtest runs the rules over past prices. It is fast and it kills weak ideas early. It also flatters: tweak the parameters enough and any strategy looks great on the past. Keep the parameters round and few, test on a period you did not use to design the rules, and include trading fees.</p>
      <h2>Step 6: run it forward on live prices, with virtual money</h2>
      <p>The real test is the future. Run the bot on live prices with a virtual balance and hard limits for a few weeks. That is what Crypto Robot is built for: your bot starts with a virtual $10,000 on live crypto prices and has to clear three levels.</p>
""" + LEVELS_TABLE + """
      <p>Breaking the -5% daily drawdown or the -10% maximum drawdown ends the run, and you see exactly which day and which trades did it.</p>
      <h2>A checklist before you trust a bot</h2>
      <ol>
        <li>Every rule is written down and testable.</li>
        <li>Position size comes from the stop, not from a hunch.</li>
        <li>A daily loss limit stops the bot automatically.</li>
        <li>The backtest includes fees and a period not used for design.</li>
        <li>The bot has survived several weeks forward on live prices without breaking a limit.</li>
      </ol>""",
  [
    ("Can I build a crypto trading bot without coding?", "Yes. No-code bot builders let you set entry, exit and risk rules from menus. AI assistants can also turn plain-English rules into code, which you should still read and test."),
    ("What programming language is best for a trading bot?", "Python is the most common choice: it has libraries for exchange connections, indicators and backtesting, and plenty of examples."),
    ("How much money do I need to start a trading bot?", "None to start. Build and test it on live prices with virtual money first. Only consider real money once the bot has survived several weeks under hard loss limits."),
    ("Is a crypto trading bot profitable?", "Some are, many are not. Profit depends on the strategy, the costs and the risk rules, which is why forward testing on virtual money matters before anything else."),
  ],
  "Built a bot? Put it on live prices with virtual money.",
  "How to build a crypto trading bot")

# ---- ai crypto trading bot (US 880, KD 32; SERP mixed, ndlabs DA 23 in top 6)
guide("ai-crypto-trading-bot",
  "AI crypto trading bots: what they really do, and how to test one",
  "AI Crypto Trading Bot: What It Really Does and How to Test One",
  "What an AI crypto trading bot actually is, the three kinds sold today, the claims to distrust, and how to test any AI bot on live prices with a virtual $10,000.",
  """      <p>&ldquo;AI&rdquo; has become the default label for crypto trading bots. Some use machine learning, many use classic rules with an AI badge, and a few are simply scams with a new word on the box. Knowing which is which saves money. This guide explains what AI can add to a trading bot, what it cannot, and how to test one before trusting it.</p>
      <h2>Three kinds of &ldquo;AI&rdquo; trading bots</h2>
      <h3>1. Rule-based bots with an AI label</h3>
      <p>Grid, DCA and indicator bots follow fixed rules. They can be useful, but there is no learning inside. The &ldquo;AI&rdquo; is marketing.</p>
      <h3>2. Machine-learning bots</h3>
      <p>These train a model on past data, for example to estimate whether the next hour is more likely up or down. They can find patterns humans miss, and they can just as easily learn noise. Markets change, so a model trained on last year may not fit this one.</p>
      <h3>3. Language-model bots</h3>
      <p>The newest kind sends news, charts or numbers to a large language model and asks it what to do. The answers are fluent, vary from one call to the next and cost money per request. A confident answer is not a correct one.</p>
      <h2>What AI can genuinely help with</h2>
      <ul>
        <li><strong>Writing and checking code</strong> for a strategy you designed.</li>
        <li><strong>Reading lots of data quickly</strong>, such as order books or news headlines, to filter trades.</li>
        <li><strong>Adapting parameters</strong> within limits you set, for example widening a stop when volatility rises.</li>
        <li><strong>Listing scenarios</strong> where your strategy could fail.</li>
      </ul>
      <h2>What no AI can do</h2>
      <ul>
        <li><strong>Know tomorrow&rsquo;s price.</strong> Markets react to news nobody has seen yet.</li>
        <li><strong>Guarantee returns.</strong> Any product promising a fixed daily profit is a red flag on its own.</li>
        <li><strong>Remove risk.</strong> A model can lose faster than a human, because it never hesitates.</li>
      </ul>
      <h2>Red flags in AI bot offers</h2>
      <table>
        <thead><tr><th>Claim</th><th>Why to distrust it</th></tr></thead>
        <tbody>
          <tr><td>&ldquo;90% win rate&rdquo;</td><td>A high win rate says nothing about the size of the losses.</td></tr>
          <tr><td>&ldquo;Guaranteed daily profit&rdquo;</td><td>No trading strategy can guarantee it.</td></tr>
          <tr><td>Deposit with a broker they choose</td><td>The classic pattern of auto-trading scams.</td></tr>
          <tr><td>Celebrity endorsement in an ad</td><td>Usually fake. Check the person&rsquo;s official channels.</td></tr>
          <tr><td>No public track record or rules</td><td>Nothing to verify means nothing to trust.</td></tr>
        </tbody>
      </table>
      <h2>How to test an AI bot properly</h2>
      <ol>
        <li><strong>Ask what it does in one sentence.</strong> If nobody can say when it buys and when it sells, you cannot judge it.</li>
        <li><strong>Run it forward, not backward.</strong> Backtests of AI models are especially easy to overfit.</li>
        <li><strong>Put hard limits around it.</strong> Whatever the model decides, a daily loss limit should stop it.</li>
        <li><strong>Use virtual money first.</strong> Weeks on live prices with a virtual balance cost nothing and teach a lot.</li>
      </ol>
      <h2>Test your AI bot on Crypto Robot</h2>
      <p>Crypto Robot gives every bot a virtual $10,000 on live crypto prices and the same rules for all: three levels, a -10% maximum drawdown and a -5% daily drawdown. AI-built or hand-written, the market judges the strategy the same way.</p>
""" + LEVELS_TABLE,
  [
    ("Do AI crypto trading bots work?", "Some can help, especially to write code or filter trades, but none can predict prices. Their results depend on the strategy and the risk rules around them, which is why they need testing on live prices first."),
    ("Is Crypto Robot an AI trading bot?", "No. Crypto Robot is a free simulator. You bring the bot, AI-built or not, and it trades live prices with a virtual $10,000 under fixed drawdown rules."),
    ("How can I tell if an AI trading bot is a scam?", "Be wary of guaranteed profits, deposits with a broker the bot chooses, celebrity endorsements and the absence of public rules or a track record."),
    ("Can I test an AI trading bot without risking money?", "Yes. Run it on live prices with a virtual balance. On Crypto Robot sign-up asks for no card and no deposit."),
  ],
  "Test any AI bot on live prices, with virtual money.",
  "AI crypto trading bots explained")

# ---- chatgpt trading bot (US 170, KD 2)
guide("chatgpt-trading-bot",
  "ChatGPT trading bot: how to build one with AI and test it",
  "ChatGPT Trading Bot: Build One With AI, Then Test It Safely",
  "How to use ChatGPT to write a crypto trading bot: the prompts that work, the mistakes it makes, and how to test the bot on live prices with virtual money before trusting it.",
  """      <p>ChatGPT cannot trade for you, and OpenAI does not sell a trading bot. What it can do is write the code for a strategy you describe, explain indicators, and point out weak spots in your rules. Used that way, it turns a trading idea into a working bot in an afternoon. Used as a fortune teller, it loses money with great confidence.</p>
      <div class="callout"><p><strong>Independent guide.</strong> Crypto Robot is not affiliated with OpenAI. ChatGPT is a trademark of OpenAI.</p></div>
      <h2>What ChatGPT is good at</h2>
      <ul>
        <li><strong>Translating rules into code.</strong> Python, Pine Script or the language of your bot framework.</li>
        <li><strong>Explaining indicators.</strong> RSI, MACD, Bollinger Bands, ATR, in plain words.</li>
        <li><strong>Finding gaps.</strong> Ask what your rules do in a crash, a squeeze or a quiet week.</li>
        <li><strong>Reading errors.</strong> Paste a stack trace and it usually finds the bug.</li>
      </ul>
      <h2>Where it goes wrong</h2>
      <ul>
        <li><strong>It invents functions.</strong> Library calls that do not exist, or parameters in the wrong order.</li>
        <li><strong>It looks into the future.</strong> A classic backtest bug: using the close of a candle to decide a trade at its open.</li>
        <li><strong>It forgets costs.</strong> Fees and slippage are often left out unless you ask.</li>
        <li><strong>It sounds sure.</strong> A fluent answer is not a tested one.</li>
      </ul>
      <h2>A workflow that works</h2>
      <ol>
        <li><strong>Write the strategy yourself</strong>, in plain sentences: market, timeframe, entry, exit, stop, size, daily loss limit.</li>
        <li><strong>Ask for code in small pieces.</strong> First the data loading, then the signal, then the risk rules. Check each piece.</li>
        <li><strong>Ask it to explain its own code</strong>, line by line, and compare with what you asked for.</li>
        <li><strong>Ask for the failure cases.</strong> &ldquo;List ten situations where this strategy loses money.&rdquo;</li>
        <li><strong>Backtest with fees</strong>, on a period you did not use to design the rules.</li>
        <li><strong>Run it forward on live prices with virtual money</strong> for several weeks.</li>
      </ol>
      <h2>Prompts to copy</h2>
      <ul>
        <li>&ldquo;Write a Python function that returns a buy signal when the RSI(14) on 1-hour BTC candles closes below 30 and the close is above the 200-period moving average. Use only the closed candle.&rdquo;</li>
        <li>&ldquo;Add a rule that stops all trading for the day once the account is down 5% from the start of the day.&rdquo;</li>
        <li>&ldquo;Check this code for look-ahead bias and tell me every line where future data could leak in.&rdquo;</li>
        <li>&ldquo;Include a 0.1% fee on every trade and show me how the result changes.&rdquo;</li>
      </ul>
      <h2>Asking ChatGPT to trade live: why to avoid it</h2>
      <p>Some bots send market data to the model before each trade and follow its answer. Two identical questions can get two different answers, every call costs money and adds delay, and nothing guarantees the model sees the same thing twice. If you try it anyway, keep the model as a filter inside strict rules, never as the only decision maker.</p>
      <h2>Test the bot on Crypto Robot</h2>
      <p>Step 6 is where Crypto Robot comes in. Your bot gets a virtual $10,000 on live crypto prices and three levels to clear, with a -10% maximum drawdown and a -5% daily drawdown. It costs nothing and asks for no card.</p>
""" + LEVELS_TABLE,
  [
    ("Can ChatGPT trade crypto for me?", "No. ChatGPT can write and explain code, but it does not connect to exchanges by itself and cannot predict prices. You build the bot; it helps you write it."),
    ("Is there an official ChatGPT trading bot?", "No. OpenAI does not sell a trading bot. Products using the name are built by third parties."),
    ("Is code written by ChatGPT safe to run with real money?", "Not until you have read it, backtested it with fees and run it forward on live prices with virtual money. It regularly makes mistakes that look correct."),
    ("Where can I test a ChatGPT-built bot for free?", "On Crypto Robot: live crypto prices, a virtual $10,000, three levels with drawdown limits, no card or deposit."),
  ],
  "Wrote your bot with ChatGPT? Test it before you trust it.",
  "ChatGPT trading bot guide")

# ---- crypto trading bot strategies (strategy 40/mo; supports the head term "crypto trading bot")
guide("crypto-trading-bot-strategies",
  "Crypto trading bot strategies: grid, DCA, trend and mean reversion explained",
  "Crypto Trading Bot Strategies: Grid, DCA, Trend, Mean Reversion",
  "The five strategies most crypto trading bots use, when each one works, when it fails, and the risk rules that keep a bot alive in every market.",
  """      <p>Most crypto trading bots run one of a handful of strategies. Each one makes money in a certain kind of market and loses in another. Picking a strategy is less about finding the best one than about knowing when yours breaks, and putting a limit in place before it does.</p>
      <h2>The five common strategies at a glance</h2>
      <table>
        <thead><tr><th>Strategy</th><th>Works when</th><th>Fails when</th></tr></thead>
        <tbody>
          <tr><td>Grid</td><td>Price moves sideways in a range</td><td>Price breaks out of the range</td></tr>
          <tr><td>DCA</td><td>Price recovers after a fall</td><td>Price keeps falling</td></tr>
          <tr><td>Trend following</td><td>Long, clear moves up or down</td><td>Choppy, directionless markets</td></tr>
          <tr><td>Mean reversion</td><td>Price snaps back after extremes</td><td>A strong trend starts</td></tr>
          <tr><td>Breakout</td><td>Volatility expands after a quiet period</td><td>False breakouts that reverse</td></tr>
        </tbody>
      </table>
      <h2>Grid bots</h2>
      <p>A grid bot places buy orders below the price and sell orders above it, at regular steps. Every bounce inside the range earns a small profit. The danger is a breakout: if the price falls through the bottom of the grid, the bot ends up holding coins bought on the way down. Set a lower bound below which the bot stops buying.</p>
      <h2>DCA bots</h2>
      <p>Dollar-cost averaging buys a fixed amount at set intervals or after each drop, lowering the average entry price. It suits long-term accumulation. As a trading strategy, it can turn a small loss into a large one if the market keeps falling. Cap the number of extra buys and the total exposure.</p>
      <h2>Trend-following bots</h2>
      <p>These buy strength and sell weakness, often with moving-average crosses or breakouts of recent highs. They lose small amounts often and win big occasionally. They need patience and a stop on every trade, because the losing streaks in a sideways market can be long.</p>
      <h2>Mean-reversion bots</h2>
      <p>These bet that extremes do not last: buy when the RSI is very low, sell when it is very high. They win often, in small amounts. The risk is the trend that does not revert, which is why a hard stop matters more here than anywhere else.</p>
      <h2>Breakout bots</h2>
      <p>A breakout bot waits for a quiet range, then trades the move when price leaves it. It catches the start of big moves and suffers from false starts. Filters such as volume or a close outside the range reduce, but never remove, the false signals.</p>
      <h2>The rules every strategy needs</h2>
      <ul>
        <li><strong>A stop on every trade</strong>, or a maximum holding time.</li>
        <li><strong>A position size</strong> derived from that stop, typically 0.5% to 2% of the balance at risk.</li>
        <li><strong>A daily loss limit</strong> that switches the bot off for the day.</li>
        <li><strong>A maximum drawdown</strong> that switches it off until you review it.</li>
      </ul>
      <h2>How to choose and test a strategy</h2>
      <ol>
        <li>Look at the market you want to trade. Ranging or trending over the last months?</li>
        <li>Pick the strategy that fits, and write its rules down.</li>
        <li>Backtest it with fees, then run it forward on live prices with virtual money.</li>
        <li>Note the worst day. If it is close to your limit, cut the position size.</li>
      </ol>
      <p>Crypto Robot runs that last step for you. Your bot gets a virtual $10,000 on live prices and three levels to clear:</p>
""" + LEVELS_TABLE + """
      <p>Since the -5% daily and -10% maximum drawdown never change, a strategy that only works in one kind of market shows its weakness quickly.</p>""",
  [
    ("What is the best crypto trading bot strategy?", "There is no single best one. Grid bots suit ranges, trend bots suit long moves, mean reversion suits markets that snap back. The best choice fits the current market and comes with strict loss limits."),
    ("Are grid bots profitable?", "In sideways markets they often earn small, steady gains. When price breaks out of the range they can lose much more, so a lower bound and a stop are essential."),
    ("What risk per trade should a bot use?", "Many traders risk between 0.5% and 2% of the balance per trade, so a losing streak does not break the daily or the maximum loss limit."),
    ("How do I test a strategy without risking money?", "Backtest it on past data, then run it forward on live prices with a virtual balance. Crypto Robot gives every bot a virtual $10,000 for free."),
  ],
  "Pick a strategy and see how it holds up on live prices.",
  "Crypto trading bot strategies")

GUIDES = [p for p in PAGES if p["kicker"] in ("Review", "Guide")]
FOOTER_NAV = ('<nav aria-label="Footer">' + "".join(f'<a href="/{g["slug"]}/">{g["short"]}</a>' for g in GUIDES)
  + '<a href="/contact/">Contact</a><a href="/terms/">Terms</a><a href="/privacy-policy/">Privacy</a><a href="/legal-notice/">Legal notice</a>'
  + '<a href="/privacy-policy/#cookies" data-cookie-settings>Cookie settings</a></nav>')

def related(slug):
    items = "".join(f'<li><a href="/{g["slug"]}/">{g["short"]}</a></li>' for g in GUIDES if g["slug"] != slug)
    return f"      <h2>Related guides</h2>\n      <ul>{items}</ul>"

for p in PAGES:
    jsonld = "".join('<script type="application/ld+json">\n' + json.dumps(j, ensure_ascii=False) + "\n</script>\n" for j in p.get("jsonld", []))
    html = HEAD.format(
        title=p["title"], desc=p["desc"], slug=p["slug"], ogtype=p.get("ogtype", "website"),
        robots="", jsonld=jsonld, kicker=p["kicker"], h1=p["h1"], updated="" if p["slug"]=="contact" else f'    <p class="updated">Last updated: {UPDATED}</p>\n', body=p["body"].replace("{related}", related(p["slug"])), ga=GA_ID, footer_nav=FOOTER_NAV,
        cur_review=' aria-current="page"' if p["slug"] == "how-to-build-a-crypto-trading-bot" else "",
        cur_contact=' aria-current="page"' if p["slug"] == "contact" else "",
        scripts=p.get("scripts", ""))
    os.makedirs(os.path.join(ROOT, p["slug"]), exist_ok=True)
    open(os.path.join(ROOT, p["slug"], "index.html"), "w").write(html)

urls = [("", "1.0")] + [(p["slug"] + "/", "0.8" if p in GUIDES else "0.3") for p in PAGES]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>2026-10-03</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls)
sm += "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /app/\n\nSitemap: {SITE}/sitemap.xml\n")
print("built", [p["slug"] for p in PAGES])
