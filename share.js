// Share a passage (or the page): the native share sheet where there is one,
// otherwise copy the link. Each passage has its own #anchor link.
(function () {
  var toast = document.querySelector('.toast'), timer;
  function say(msg) {
    toast.textContent = msg; toast.hidden = false;
    clearTimeout(timer); timer = setTimeout(function () { toast.hidden = true; }, 2200);
  }
  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    var t = document.createElement('textarea'); t.value = text; t.setAttribute('readonly', '');
    t.style.position = 'fixed'; t.style.opacity = '0'; document.body.appendChild(t); t.select();
    try { document.execCommand('copy'); } finally { document.body.removeChild(t); }
    return Promise.resolve();
  }
  document.querySelectorAll('.share').forEach(function (b) {
    b.addEventListener('click', function () {
      var id = b.dataset.id;
      var url = location.origin + location.pathname + (id ? '#' + id : '');
      var title = id ? b.dataset.title + ' · Water in Chinese Philosophy' : document.title;
      var text = id ? (document.getElementById(id).querySelector('.en') || {}).textContent : '';
      if (navigator.share) {
        navigator.share({ title: title, text: text ? '“' + text.trim().slice(0, 180) + (text.length > 180 ? '…' : '') + '”' : undefined, url: url })
          .catch(function () {});
      } else {
        copy(url).then(function () { say('Link copied'); }, function () { say(url); });
      }
    });
  });
})();
