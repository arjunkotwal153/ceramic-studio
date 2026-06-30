import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

debug_script = '''
<script>
window.onerror = function(msg, url, lineNo, columnNo, error) {
    var errDiv = document.createElement('div');
    errDiv.style.position = 'fixed';
    errDiv.style.top = '0';
    errDiv.style.left = '0';
    errDiv.style.background = 'red';
    errDiv.style.color = 'white';
    errDiv.style.zIndex = '9999';
    errDiv.style.padding = '10px';
    errDiv.style.fontFamily = 'monospace';
    errDiv.innerHTML = "Error: " + msg + "<br>Line: " + lineNo + "<br>URL: " + url;
    document.body.appendChild(errDiv);
    return false;
};
window.addEventListener('unhandledrejection', function(event) {
    var errDiv = document.createElement('div');
    errDiv.style.position = 'fixed';
    errDiv.style.top = '50px';
    errDiv.style.left = '0';
    errDiv.style.background = 'orange';
    errDiv.style.color = 'white';
    errDiv.style.zIndex = '9999';
    errDiv.style.padding = '10px';
    errDiv.style.fontFamily = 'monospace';
    errDiv.innerHTML = "Promise Rejection: " + event.reason;
    document.body.appendChild(errDiv);
});
</script>
'''

if 'window.onerror' not in html:
    html = html.replace('<body>', '<body>\n' + debug_script)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
