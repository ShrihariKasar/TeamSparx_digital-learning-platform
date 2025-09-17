// PWA service worker 
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/static/js/sw.js')
    .then(() => console.log('SW registered'))
    .catch(err => console.log('SW reg failed', err));
}