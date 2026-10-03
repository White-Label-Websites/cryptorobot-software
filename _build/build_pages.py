# Generates the static content pages of cryptorobot.software and its sitemap.
# Run from anywhere: python3 _build/build_pages.py (writes <slug>/index.html
# next to this folder). GitHub Pages skips folders starting with "_".
# The homepage (index.html) is hand-written; keep its footer nav in sync with
# FOOTER_NAV below.
import os, json, shutil
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
{robots}<meta name="theme-color" content="#f5f2ea">
<link rel="preload" href="/assets/fonts/BricolageGrotesque-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/consent.js" data-ga="{ga}"></script>
{jsonld}</head>
<body>
<header class="bar">
  <div class="wrap">
    <a class="logo" href="/"><span class="logo-glyph" aria-hidden="true"></span>Crypto Robot</a>
    <nav aria-label="Main"><a href="/#pipeline">How it works</a><a class="hide-sm" href="/how-to-backtest-a-crypto-trading-bot/"{cur_guide}>Backtesting guide</a><a href="/contact/"{cur_contact}>Contact</a></nav>
  </div>
</header>

<main class="page">
  <div class="wrap">
    <div class="page-head">
      <p class="label">{kicker}</p>
      <h1>{h1}</h1>
{updated}    </div>
    <div class="prose">
{body}
    </div>
  </div>
</main>

<footer class="foot">
  <div class="wrap">
    {footer_nav}
    <p class="copy">&copy; 2026 Crypto Robot</p>
    <small>Educational simulator. All balances are virtual and no real money is traded. Nothing on this site is financial advice. Crypto-assets are high risk and results on virtual money do not predict real results. Sign-up is handled by our partner AFFCOIN, and we may receive a commission when you open an account.</small>
  </div>
</footer>
{scripts}</body>
</html>
"""

CTA = """      <div class="page-cta">
        <p>{text}</p>
        <a class="btn" href="/#start">Start a live test <span aria-hidden="true">&rarr;</span></a>
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
# list and the Article + FAQPage JSON-LD. cryptorobot.software owns the
# BACKTESTING cluster; bitcoinera.com owns prop firm / simulator / paper
# trading / claude bot / competition / free bot. Never publish the same text
# on both sites.
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

# ---- backtest crypto bot / backtesting trading bot (US 40 KD 0 + 40 KD 5; SERP = tool pages, open)
guide("how-to-backtest-a-crypto-trading-bot",
  "How to backtest a crypto trading bot, step by step",
  "How to Backtest a Crypto Trading Bot (Step-by-Step Guide)",
  "A practical method to backtest a crypto trading bot: get clean candle data, model fees, split in-sample and out-of-sample, read the report, then confirm the result on live prices.",
  """      <p>Backtesting means replaying a trading bot's rules over price history and recording every trade it would have taken. Done carefully, it tells you in an hour whether an idea deserves weeks of attention. Done carelessly, it produces a beautiful equity curve that collapses the first day the bot meets a real market. This guide covers the careful version.</p>
      <div class="callout"><p><strong>Where Crypto Robot fits.</strong> Crypto Robot does not run historical backtests. You backtest with the tools described below, then bring the strategy here to run on live prices with a virtual $10,000. The last section explains that handover.</p></div>
      <h2>What you need before you start</h2>
      <ul>
        <li><strong>A written rule set.</strong> Entry, exit, stop, position size. If a rule needs your judgement on the day, a backtest cannot test it.</li>
        <li><strong>Historical candles</strong> for the pair and timeframe you will trade.</li>
        <li><strong>A backtesting tool.</strong> A charting platform's strategy tester, a Python library or an open-source bot framework. Our <a href="/free-crypto-backtesting-tools/">comparison of free backtesting tools</a> helps you choose.</li>
        <li><strong>Your exchange's fee schedule</strong>, because fees decide whether many short-term strategies make or lose money.</li>
      </ul>
      <h2>Step 1: get data you can trust</h2>
      <p>Most exchanges publish historical OHLCV candles (open, high, low, close, volume) through their public API, and the open-source CCXT library fetches them from dozens of exchanges with the same code. Download more history than you think you need: at least one full bull phase, one bear phase and one long sideways stretch. Then check the file. Look for missing candles, duplicated timestamps and absurd spikes. A single bad print at a tenth of the real price can create a trade that never could have happened.</p>
      <p>Use data from the exchange you plan to trade on, or one with similar liquidity. Prices for small coins differ from one venue to the next, and a strategy tuned on one exchange's quirks may not travel.</p>
      <h2>Step 2: split the history before you look at it</h2>
      <p>Cut the data into two parts and decide the cut date before running anything. Use the first part, around 70%, to design and tune the strategy. Keep the last 30% locked away. When the strategy is finished, run it once on the locked period. That out-of-sample result is the number that matters; the in-sample result mostly measures how hard you tuned.</p>
      <p>For a stricter version, use walk-forward testing: tune on a window, test on the next slice, roll both forward, repeat, and stitch the test slices together.</p>
      <h2>Step 3: model costs honestly</h2>
      <ul>
        <li><strong>Fees.</strong> Apply the taker fee on market orders and the maker fee on limit orders, on both sides of each trade. A strategy that trades 300 times a year pays the fee 600 times.</li>
        <li><strong>Slippage.</strong> Add a small penalty to every market order. Fast moves and thin order books make it larger than you expect.</li>
        <li><strong>Funding.</strong> On perpetual futures, include funding payments for positions held across funding times.</li>
      </ul>
      <p>Run the backtest once with no costs and once with them. If the edge disappears with costs, the strategy was trading noise.</p>
      <h2>Step 4: make the simulation match reality</h2>
      <p>The commonest bug in home-made backtests is deciding with information the bot would not have had. If the signal uses a candle's close, the trade can only happen at the next candle's open. Indicators must be computed from closed candles only. If the stop and the target could both have been hit inside the same candle, assume the worse outcome. Our list of <a href="/backtesting-mistakes/">backtesting mistakes</a> covers the other traps.</p>
      <h2>Step 5: read the report beyond the total return</h2>
      <table>
        <thead><tr><th>Metric</th><th>What it tells you</th><th>Warning sign</th></tr></thead>
        <tbody>
          <tr><td>Maximum drawdown</td><td>The worst fall from a peak, in %</td><td>Deeper than you could sit through, or than a -10% limit allows</td></tr>
          <tr><td>Worst day</td><td>The largest single-day loss</td><td>Close to -5%: a live daily limit would have stopped the bot</td></tr>
          <tr><td>Profit factor</td><td>Gross profit divided by gross loss</td><td>Below about 1.2 after costs leaves little margin</td></tr>
          <tr><td>Number of trades</td><td>How much evidence you have</td><td>A few dozen trades prove very little</td></tr>
          <tr><td>Win rate with average win and loss</td><td>How the profit is made</td><td>High win rate with rare, huge losses</td></tr>
          <tr><td>Exposure</td><td>Share of time in the market</td><td>Returns that match buy-and-hold with more risk</td></tr>
        </tbody>
      </table>
      <p>Always compare with a plain benchmark, such as buying and holding the same coin over the same period. A bot that earns less than holding, with a deeper drawdown, adds complexity for nothing.</p>
      <h2>Step 6: stress the result</h2>
      <ul>
        <li>Move each parameter a little up and down. A robust strategy degrades gently; a fragile one falls off a cliff.</li>
        <li>Run the same rules on a second coin or a second timeframe.</li>
        <li>Double the fees and slippage and see what survives.</li>
      </ul>
      <h2>Step 7: hand it over to a live test</h2>
      <p>A backtest, however careful, is still a test on data you have already seen. The next step is to run the strategy forward on prices that do not exist yet. On Crypto Robot, your bot gets a virtual $10,000 on live crypto prices and three levels to clear, under fixed risk limits:</p>
""" + LEVELS_TABLE + """
      <p>A drop of 5% in one day or 10% overall ends the challenge. Compare what happens with your backtest: if the live drawdown runs far deeper than anything the backtest showed, the backtest was too optimistic. Read <a href="/forward-testing-vs-backtesting/">forward testing vs backtesting</a> for how to compare the two.</p>""",
  [
    ("Can you backtest a crypto trading bot for free?", "Yes. Free strategy testers on charting platforms and open-source Python libraries such as backtesting.py, Backtrader or vectorbt cost nothing, and historical candles can be downloaded from exchange APIs."),
    ("How much historical data do I need for a crypto backtest?", "Enough to cover different market regimes: at least one strong rise, one strong fall and one sideways period. For most strategies on hourly candles, that means several years of data."),
    ("Does a profitable backtest mean the bot will make money?", "No. A backtest only shows how the rules would have performed on past data. Overfitting, missing costs and changing markets often make live results worse, which is why a forward test on live prices comes next."),
    ("Does Crypto Robot backtest strategies?", "No. Crypto Robot is the live step: after you backtest with your own tools, your bot runs on live prices with a virtual $10,000 under fixed drawdown limits."),
  ],
  "Backtest done? Find out how the strategy behaves on live prices.",
  "How to backtest a crypto bot")

# ---- free backtesting (KD ~15) / crypto backtesting (US 40, KD 5)
guide("free-crypto-backtesting-tools",
  "Free crypto backtesting tools: what each one is good for",
  "Free Crypto Backtesting Tools Compared (No-Code and Python)",
  "The free ways to backtest a crypto strategy: browser strategy testers, Python libraries and open-source bot frameworks, with the strengths, limits and best use of each.",
  """      <p>You do not need to pay for software to backtest a crypto strategy. The free options range from a strategy tester inside a charting website to full open-source trading frameworks. They differ in how much code they ask for, how realistic the simulation is and how easily the strategy moves to live trading afterwards.</p>
      <h2>The short answer</h2>
      <table>
        <thead><tr><th>You are</th><th>Start with</th><th>Why</th></tr></thead>
        <tbody>
          <tr><td>New to code</td><td>A charting platform's strategy tester</td><td>Results on the chart in minutes, a short scripting language</td></tr>
          <tr><td>Comfortable with Python</td><td>backtesting.py or Backtrader</td><td>Full control, readable code, large communities</td></tr>
          <tr><td>Testing many parameter sets</td><td>vectorbt (open-source edition)</td><td>Vectorised, very fast on large grids</td></tr>
          <tr><td>Planning to automate the bot</td><td>Freqtrade or Jesse</td><td>The same strategy file runs in backtest and live modes</td></tr>
        </tbody>
      </table>
      <h2>Browser strategy testers</h2>
      <p>Charting platforms such as TradingView let you write a strategy in a scripting language (Pine Script on TradingView) and show the trades and a performance summary on the chart. It is the fastest way to see whether an idea has any life in it.</p>
      <ul>
        <li><strong>Good for:</strong> quick checks of indicator strategies, visual inspection of every trade.</li>
        <li><strong>Watch out for:</strong> the amount of history and some features depend on the plan; fees and slippage are off unless you set them in the strategy properties; the default fill logic may be kinder than a real order book.</li>
      </ul>
      <h2>Python libraries</h2>
      <h3>backtesting.py</h3>
      <p>A small, open-source library. You write a strategy class with an initialisation step and a per-candle step, feed it a table of candles, and get statistics plus an interactive chart. It is the friendliest Python entry point.</p>
      <h3>Backtrader</h3>
      <p>An older, event-driven framework with many built-in indicators, analysers and order types. More verbose than backtesting.py, with a large archive of examples and forum answers.</p>
      <h3>vectorbt</h3>
      <p>Computes signals for whole price series at once instead of looping candle by candle, which makes it very fast for testing thousands of parameter combinations. The open-source edition is free; a paid edition adds features. Speed has a cost: testing thousands of combinations makes overfitting easy, so keep an out-of-sample period.</p>
      <h3>Getting the data</h3>
      <p>The open-source CCXT library connects to the public APIs of many exchanges and downloads historical candles with a single function call, which you can save to a CSV file and reuse in any of the libraries above.</p>
      <h2>Open-source crypto bot frameworks</h2>
      <p><strong>Freqtrade</strong> and <strong>Jesse</strong> are Python frameworks built for crypto. The strategy you backtest is the same file the bot runs later, which removes a whole class of bugs that appear when a strategy is rewritten for live use. Both include data download and backtest reports. Freqtrade also has a hyperparameter optimiser, which is useful and dangerous in equal measure.</p>
      <ul>
        <li><strong>Good for:</strong> anyone who wants to automate the strategy afterwards.</li>
        <li><strong>Watch out for:</strong> setup takes time; you will need to be comfortable with a command line and configuration files.</li>
      </ul>
      <h2>A spreadsheet still works</h2>
      <p>For a slow strategy, such as a weekly moving-average rule, a spreadsheet with one row per candle and a few formula columns is a perfectly honest backtest. It forces you to see every trade, and that is often where the flaws show up.</p>
      <h2>Settings that matter more than the tool</h2>
      <ul>
        <li>Fees on both sides of every trade, at your exchange's actual rate.</li>
        <li>Slippage on market orders.</li>
        <li>Signals computed on closed candles only.</li>
        <li>An out-of-sample period you do not touch while tuning.</li>
      </ul>
      <p>Every tool above can produce a misleading result if these are wrong. The <a href="/backtesting-mistakes/">backtesting mistakes guide</a> goes through them one by one.</p>
      <h2>After the backtest: a free live test</h2>
      <p>Every free backtesting tool tests the past. To see the strategy on prices it has never seen, run it forward. Crypto Robot does that for free: your bot trades live crypto prices with a virtual $10,000, through three levels with a -5% daily and a -10% maximum drawdown. No card, no deposit.</p>""",
  [
    ("What is the best free crypto backtesting tool?", "It depends on your skills. A charting platform's strategy tester is quickest without code, backtesting.py is the easiest Python option, vectorbt is fastest for large parameter tests, and Freqtrade or Jesse suit you if you plan to automate the bot."),
    ("Can I backtest crypto without coding?", "Mostly. Browser strategy testers use a short scripting language that many people learn from examples, and slow strategies can be backtested in a spreadsheet."),
    ("Where can I get free historical crypto data?", "Most exchanges publish historical candles through their public APIs. The open-source CCXT library downloads them from many exchanges with the same code."),
    ("Is free backtesting software accurate?", "The calculation is usually correct. Accuracy depends on your settings: fees, slippage, closed-candle signals and an untouched out-of-sample period."),
  ],
  "Tested on the past for free? Test on live prices for free too.",
  "Free backtesting tools")

# ---- backtesting mistakes / overfitting (supports the cluster, informational)
guide("backtesting-mistakes",
  "Seven backtesting mistakes that make a losing bot look like a winner",
  "7 Backtesting Mistakes That Fake a Winning Crypto Bot",
  "Overfitting, look-ahead bias, missing fees, survivorship bias and three other backtesting mistakes that inflate crypto bot results, with a fix for each.",
  """      <p>A backtest rarely lies on purpose. It does exactly what you told it to, and small modelling errors add up to a strategy that looks far better on paper than it can ever be in a market. These seven mistakes cause most of the damage. Each one comes with the check that catches it.</p>
      <h2>1. Overfitting the parameters</h2>
      <p>Try enough combinations of moving-average lengths, RSI thresholds and stop distances, and one of them will fit the past beautifully by chance. The more knobs a strategy has and the more you turn them, the less the best result means.</p>
      <p><strong>Fix:</strong> keep few parameters and prefer round values. Tune on one period, judge on another you never touched. Check that neighbouring values give similar results; an isolated peak is luck.</p>
      <h2>2. Look-ahead bias</h2>
      <p>The bot uses information it could not have had at the time of the trade: the candle's close to enter at its open, an indicator computed on the full dataset, a daily high used before the day is over.</p>
      <p><strong>Fix:</strong> compute every signal on closed candles and fill the trade at the next candle's open. Shift your signal column by one candle and rerun. If the result collapses, the original had a leak.</p>
      <h2>3. Ignoring fees, slippage and funding</h2>
      <p>Short-term strategies live on thin margins. Leave out costs and a strategy that trades several times a day can turn from a loss into an impressive gain.</p>
      <p><strong>Fix:</strong> charge your exchange's real fee on both sides of every trade, add slippage to market orders, include funding on perpetual futures, then double all three as a stress test.</p>
      <h2>4. Survivorship bias in coin selection</h2>
      <p>Testing on today's top coins means testing on the winners. Coins that crashed or were delisted are missing from the list, so a strategy that buys dips looks safer than it was.</p>
      <p><strong>Fix:</strong> pick the coin list as it stood at the start of the test, or limit the test to large pairs that existed throughout the whole period.</p>
      <h2>5. Too few trades</h2>
      <p>Twenty trades with a 70% win rate is a coin that landed heads 14 times. The statistics in a backtest report mean little until there are enough trades for luck to average out.</p>
      <p><strong>Fix:</strong> aim for a few hundred trades across different market conditions, or accept that the result is a hint and nothing more.</p>
      <h2>6. A single market regime</h2>
      <p>A strategy tested only during a bull run learns to buy dips that always recover. Crypto spends long periods trending and long periods ranging, and most strategies only work in one of the two.</p>
      <p><strong>Fix:</strong> include at least one rise, one fall and one sideways period. Report results for each separately; a strategy that wins everywhere is rare, so know where yours loses.</p>
      <h2>7. Judging by total return alone</h2>
      <p>A 200% return with a 60% drawdown along the way is a strategy almost nobody could hold, and one that would hit any sensible loss limit long before the profit arrived.</p>
      <p><strong>Fix:</strong> read the maximum drawdown and the worst day first. Then check whether the bot would have survived your real limits. On Crypto Robot those are -10% overall and -5% in a single day.</p>
      <h2>A quick self-check</h2>
      <ol>
        <li>Signals use closed candles only, fills happen on the next candle.</li>
        <li>Fees, slippage and funding are included at realistic levels.</li>
        <li>The out-of-sample period was never used for tuning.</li>
        <li>Nearby parameter values give similar results.</li>
        <li>There are enough trades across rising, falling and flat markets.</li>
        <li>The worst day and the maximum drawdown fit inside your limits.</li>
      </ol>
      <h2>The mistake no backtest can fix</h2>
      <p>Every backtest is built by someone who already knows how the past turned out, and that knowledge leaks into the choices: which coin, which period, which indicator. The only clean test is on data that does not exist yet. That is the job of a forward test, and Crypto Robot runs one for free: live crypto prices, a virtual $10,000, three levels and drawdown limits that do not bend.</p>""",
  [
    ("What is overfitting in backtesting?", "Overfitting means tuning a strategy so closely to past data that it captures random noise. It looks excellent in the backtest and performs much worse on new data."),
    ("How do I know if my backtest has look-ahead bias?", "Shift your signals by one candle so every trade uses only closed data, and rerun the test. A sharp drop in performance points to a leak of future information."),
    ("How many trades does a backtest need?", "There is no fixed number, but a few dozen trades say little. A few hundred trades across different market conditions give a far more reliable picture."),
    ("How can I check a backtest result for free?", "Run the strategy forward on live prices with virtual money. Crypto Robot gives each bot a virtual $10,000 at no cost and with no card."),
  ],
  "The cleanest test is on prices nobody has seen yet.",
  "Backtesting mistakes")

# ---- forward testing vs backtesting (supports "backtesting trading bot"; method page)
guide("forward-testing-vs-backtesting",
  "Forward testing vs backtesting: why a trading bot needs both",
  "Forward Testing vs Backtesting: What Each Proves for a Trading Bot",
  "Backtesting replays the past; forward testing runs the strategy on live prices as they arrive. What each test proves, how long to run them and how to compare the results.",
  """      <p>Backtesting and forward testing answer two different questions about the same trading bot. A backtest asks how the rules would have performed on history. A forward test asks how they perform on prices arriving now, with no possibility of peeking at the outcome. A strategy worth trusting passes both, and the gap between the two results is itself one of the most useful numbers you can measure.</p>
      <h2>The two tests side by side</h2>
      <table>
        <thead><tr><th></th><th>Backtesting</th><th>Forward testing</th></tr></thead>
        <tbody>
          <tr><td>Data</td><td>Historical candles</td><td>Live prices as they arrive</td></tr>
          <tr><td>Speed</td><td>Years in minutes</td><td>Real time: days or weeks</td></tr>
          <tr><td>Best use</td><td>Rejecting weak ideas quickly</td><td>Confirming the survivors</td></tr>
          <tr><td>Main risk</td><td>Overfitting, look-ahead bias</td><td>Too short a sample</td></tr>
          <tr><td>Hindsight</td><td>Built in: you know what happened</td><td>Impossible: the future is unknown</td></tr>
          <tr><td>Money at stake</td><td>None</td><td>None when the balance is virtual</td></tr>
        </tbody>
      </table>
      <h2>What backtesting is good for</h2>
      <p>Speed. In an afternoon you can check an idea over several years of bull, bear and sideways markets, throw away the ninety ideas that never worked and keep the ten that might. No forward test can match that, which is why backtesting always comes first. The <a href="/how-to-backtest-a-crypto-trading-bot/">step-by-step backtesting guide</a> covers the method.</p>
      <h2>What forward testing adds</h2>
      <ul>
        <li><strong>No hindsight.</strong> You cannot tune to prices that have not happened.</li>
        <li><strong>Real behaviour of the code.</strong> Bugs that a backtest hides, such as a signal computed on an unfinished candle, show up as soon as the bot runs on a live feed.</li>
        <li><strong>Discipline.</strong> Watching a bot lose for four days in a row, under fixed limits, tells you more about whether you would keep it running than any equity curve.</li>
      </ul>
      <p>Forward testing with a virtual balance is sometimes called demo trading. The principle is the same: live market, no real money.</p>
      <h2>How long should each test run?</h2>
      <p>Backtest across several years if your timeframe allows it, covering at least one rise, one fall and one flat stretch. Forward test long enough to see a meaningful number of trades. For a bot that trades a few times a day, a week or two gives a first reading. Slower strategies need longer. On Crypto Robot, level 1 runs between 5 and 10 days, and the next levels continue the test with smaller targets.</p>
      <h2>Comparing the two results</h2>
      <p>Expect the forward test to look worse than the backtest. Some gap is normal. What matters is its size and its source.</p>
      <ul>
        <li><strong>Similar trade frequency, a slightly lower return:</strong> healthy. Costs and normal variance explain it.</li>
        <li><strong>Far more or far fewer trades than the backtest predicted:</strong> the code behaves differently on live data. Look for a bug before anything else.</li>
        <li><strong>Drawdown much deeper than the backtest's worst:</strong> the backtest was overfitted or tested on too narrow a period.</li>
        <li><strong>A single big trade carries all the profit:</strong> treat it as luck until it repeats.</li>
      </ul>
      <h2>A simple workflow</h2>
      <ol>
        <li>Backtest on 70% of the history, tune, then run once on the remaining 30%.</li>
        <li>Note the expected trade frequency, the worst day and the maximum drawdown.</li>
        <li>Forward test on live prices with a virtual balance and hard loss limits.</li>
        <li>Compare with the numbers from step 2. Investigate any large gap before changing parameters.</li>
      </ol>
      <h2>Forward testing on Crypto Robot</h2>
      <p>Crypto Robot is built for step 3. Each bot gets a virtual $10,000 on live crypto prices and must clear three levels:</p>
""" + LEVELS_TABLE + """
      <p>Falling 5% in a single day or 10% from the start ends the challenge, which is a strict, objective check against the drawdown your backtest predicted. It is free and asks for no card or deposit.</p>""",
  [
    ("What is the difference between backtesting and forward testing?", "Backtesting runs a strategy on historical data to see how it would have performed. Forward testing runs it on live prices as they arrive, so the outcome cannot be known in advance."),
    ("Is forward testing better than backtesting?", "Each does a different job. Backtesting quickly rejects weak ideas over years of data; forward testing confirms the survivors without hindsight. A robust strategy needs both."),
    ("How long should I forward test a trading bot?", "Long enough for a meaningful number of trades. For a bot trading several times a day, one to two weeks gives a first reading; slower strategies need longer."),
    ("Can I forward test without risking money?", "Yes. Run the bot on live prices with a virtual balance. Crypto Robot gives each bot a virtual $10,000 for free."),
  ],
  "Your backtest made a prediction. Check it on live prices.",
  "Forward testing vs backtesting")

# ---- trading robot / crypto trading robot / crypto robot (brand-adjacent terms)
guide("crypto-trading-robot",
  "What is a crypto trading robot, and how do you vet one?",
  "Crypto Trading Robot: How It Works and How to Vet One",
  "What a crypto trading robot is, the parts inside it, the claims that should worry you, and a five-point check, including a backtest and a live test, before you trust one.",
  """      <p>A crypto trading robot is software that places buy and sell orders on its own, following rules written in advance. &ldquo;Robot&rdquo;, &ldquo;bot&rdquo; and &ldquo;algorithm&rdquo; describe the same thing. The useful question is never whether a robot is automated; it is whether its rules hold up when tested properly. This page explains how trading robots work and how to check one.</p>
      <h2>Inside a trading robot</h2>
      <table>
        <thead><tr><th>Part</th><th>Job</th><th>Example</th></tr></thead>
        <tbody>
          <tr><td>Market data</td><td>Feeds prices to the robot</td><td>1-hour BTC/USD candles</td></tr>
          <tr><td>Strategy</td><td>Decides when to buy and sell</td><td>Buy when the 20-hour average crosses above the 100-hour average</td></tr>
          <tr><td>Risk module</td><td>Decides how much and when to stop</td><td>Risk 1% per trade, pause after a 4% losing day</td></tr>
          <tr><td>Execution</td><td>Sends the orders</td><td>Limit orders through an exchange API</td></tr>
          <tr><td>Logging</td><td>Records every decision</td><td>Trade journal with entry reason and result</td></tr>
        </tbody>
      </table>
      <p>The strategy gets the attention. The risk module decides whether the robot is still running in a month.</p>
      <h2>Common kinds of crypto robots</h2>
      <ul>
        <li><strong>Trend robots</strong> follow sustained moves and accept many small losses while waiting for a big one.</li>
        <li><strong>Range robots</strong>, such as grid bots, buy low and sell high inside a band and suffer when the price leaves it.</li>
        <li><strong>Accumulation robots</strong> buy at intervals or after drops to build a position over time.</li>
        <li><strong>Arbitrage and market-making robots</strong> exploit tiny price differences and need speed and low fees that individuals rarely have.</li>
      </ul>
      <h2>Claims that should worry you</h2>
      <ul>
        <li><strong>A fixed daily or monthly return.</strong> Markets do not pay a salary. No honest robot can promise one.</li>
        <li><strong>A deposit with a broker chosen for you.</strong> A frequent pattern in schemes that sell &ldquo;robots&rdquo; to the public.</li>
        <li><strong>Hidden rules.</strong> If nobody will say what the robot does, you cannot test it.</li>
        <li><strong>Backtest screenshots and nothing else.</strong> Past curves are easy to tune. Ask for a live record.</li>
        <li><strong>Celebrity endorsements in ads.</strong> Almost always fabricated.</li>
      </ul>
      <div class="callout"><p><strong>About the name.</strong> Crypto Robot, the site you are reading, is a free testing environment. It sells no robot, takes no deposit and has no connection with products sold online under similar names.</p></div>
      <h2>A five-point check before trusting a robot</h2>
      <ol>
        <li><strong>State the rules in two sentences.</strong> When it buys, when it sells. If you cannot, stop here.</li>
        <li><strong>Find the risk limits.</strong> Size per trade, daily loss limit, maximum drawdown. A robot without them is a bet.</li>
        <li><strong>Backtest it with costs</strong>, on a period not used to design it. The <a href="/how-to-backtest-a-crypto-trading-bot/">backtesting guide</a> explains how, and the <a href="/free-crypto-backtesting-tools/">free tools guide</a> lists what to use.</li>
        <li><strong>Look for the usual traps</strong>: overfitting, look-ahead bias, a single market regime. See <a href="/backtesting-mistakes/">seven backtesting mistakes</a>.</li>
        <li><strong>Run it live on virtual money</strong> under limits it cannot override, and compare with the backtest.</li>
      </ol>
      <h2>Run your robot live on Crypto Robot</h2>
      <p>Step 5 is free here. Your trading robot gets a virtual $10,000 on live crypto prices and climbs three levels: +10% in 5 to 10 days, then +5% twice. A 5% loss in one day or a 10% drawdown overall ends the challenge. Nothing is deposited, and nothing is paid out: the result is a record of how the robot behaves on a live market.</p>""",
  [
    ("What is a crypto trading robot?", "Software that places buy and sell orders automatically according to rules written in advance. Robot, bot and algorithm mean the same thing in this context."),
    ("Do crypto trading robots really work?", "Some strategies make money in some markets, and many lose. A robot is only as good as its rules and risk limits, which is why it should be backtested and then run live on virtual money first."),
    ("How can I tell if a trading robot is a scam?", "Be wary of guaranteed returns, deposits with a broker chosen for you, secret rules, backtest-only results and celebrity endorsements."),
    ("Is Crypto Robot a trading robot I can buy?", "No. Crypto Robot is a free testing environment. You bring the robot, and it runs on live prices with a virtual $10,000 under fixed drawdown limits."),
  ],
  "Have a trading robot? See how it behaves on a live market.",
  "Crypto trading robots")

GUIDES = [p for p in PAGES if p["kicker"] == "Guide"]
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
        robots="", jsonld=jsonld, kicker=p["kicker"], h1=p["h1"], updated="" if p["slug"]=="contact" else f'      <p class="updated">Last updated: {UPDATED}</p>\n', body=p["body"].replace("{related}", related(p["slug"])), ga=GA_ID, footer_nav=FOOTER_NAV,
        cur_guide=' aria-current="page"' if p["slug"] == "how-to-backtest-a-crypto-trading-bot" else "",
        cur_contact=' aria-current="page"' if p["slug"] == "contact" else "",
        scripts=p.get("scripts", ""))
    os.makedirs(os.path.join(ROOT, p["slug"]), exist_ok=True)
    open(os.path.join(ROOT, p["slug"], "index.html"), "w").write(html)

# Guides removed in the backtesting repositioning (2026-10-03): delete their
# folders so GitHub Pages stops serving them.
for old in ("how-to-build-a-crypto-trading-bot", "ai-crypto-trading-bot", "chatgpt-trading-bot", "crypto-trading-bot-strategies"):
    shutil.rmtree(os.path.join(ROOT, old), ignore_errors=True)

urls = [("", "1.0")] + [(p["slug"] + "/", "0.8" if p in GUIDES else "0.3") for p in PAGES]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>2026-10-03</lastmod><priority>{pr}</priority></url>\n" for u, pr in urls)
sm += "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /app/\n\nSitemap: {SITE}/sitemap.xml\n")
print("built", [p["slug"] for p in PAGES])
