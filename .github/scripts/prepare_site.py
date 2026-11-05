
import re
import sys
from pathlib import Path

html_file = Path(sys.argv[1])
html = html_file.read_text(encoding="utf-8")

# Sender's original integration script
sender_script = r"""
<script>
(function (s, e, n, d, er) {
  s['Sender'] = er;
  s[er] = s[er] || function () {
    (s[er].q = s[er].q || []).push(arguments)
  }, s[er].l = 1 * new Date();
  s[er].on = function(event, callback) {
    s[er].listeners = s[er].listeners || {};
    (s[er].listeners[event] = s[er].listeners[event] || []).push(callback);
  };
  var a = e.createElement(n),
      m = e.getElementsByTagName(n)[0];
  a.async = 1;
  a.src = d;
  m.parentNode.insertBefore(a, m)
})(window, document, 'script',
   'https://cdn.sender.net/accounts_resources/universal.js',
   'sender');
sender('5c60693bf40566');
</script>
"""

# Add Sender's script if Mobirise has removed it
if "5c60693bf40566" not in html:
    if not re.search(r"</head\s*>", html, re.I):
        raise SystemExit("ERROR: Cannot find closing head tag.")

    html = re.sub(
        r"</head\s*>",
        sender_script + "\n</head>",
        html,
        count=1,
        flags=re.I
    )

# Preserve the existing appearance of the Sender form
sender_style = """
<style id="sender-form-styles">
.sender-form-field {
    display: flex;
    justify-content: center;
    text-align: center;
}
.sender-form-field > * {
    margin-left: auto;
    margin-right: auto;
}
</style>
"""

if 'id="sender-form-styles"' not in html:
    html = re.sub(
        r"</head\s*>",
        sender_style + "\n</head>",
        html,
        count=1,
        flags=re.I
    )

# Recreate the existing Mobirise subscription section
sender_section = """
<section data-bs-version="5.1"
         class="form5 cid-tIskrx6sZd"
         id="form02-4">
    <div class="container-fluid">
        <div class="mbr-section-head mb-5">
            <h4 class="mbr-section-title mbr-fonts-style
                       align-center mb-0 display-7">
                <strong>Subscribe to receive the latest
                Out, Amongst The Stars Movie News</strong>
            </h4>
        </div>
        <div class="row justify-content-center mt-4">
            <div class="col-lg-8 mx-auto">
                <div style="text-align: left"
                     class="sender-form-field"
                     data-sender-form-id="bqxyJk"></div>
            </div>
        </div>
    </div>
</section>
"""

# Find the original subscription section
pattern = re.compile(
    r'<section\b(?=[^>]*\bid=["\']form02-4["\'])[^>]*>.*?</section>',
    re.I | re.S
)

if not pattern.search(html):
    raise SystemExit(
        "ERROR: Mobirise subscription section form02-4 was not found. "
        "Website was not published. Check the Mobirise section ID."
    )

# Replace it with the Sender version
html = pattern.sub(sender_section, html, count=1)

html_file.write_text(html, encoding="utf-8")

print("SUCCESS: Sender integration restored.")
