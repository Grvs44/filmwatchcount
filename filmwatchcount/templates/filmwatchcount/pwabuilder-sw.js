importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');
const noCachePages = ['create','delete','deleted','duplicate','update','pwadate','settings'];
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});
workbox.routing.registerRoute(
  ({url}) => CheckIfNoCachePage(url),
  new workbox.strategies.NetworkOnly()
);
workbox.routing.registerRoute(
  ({event}) => (event.request.destination === 'document'),
  new workbox.strategies.NetworkFirst({
    cacheName: "fw-html",
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 100,
      }),
    ],
  })
);
workbox.routing.setCatchHandler(async (options) => {
  const cache = await self.caches.open('fw-offline');
  if(options.request.destination === 'document') return (await cache.match('{% url "filmwatchcount:offline" %}')) || Response.error();
  return Response.error();
});
workbox.routing.registerRoute(
  ({event}) => (event.request.destination === 'script' || event.request.destination === 'javascript'),
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: "fw-javascript",
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 15,
      }),
    ],
  })
);
workbox.routing.registerRoute(
  ({event}) => event.request.destination === 'style',
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: "fw-stylesheets",
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 15,
      }),
    ],
  })
);
workbox.routing.registerRoute(
  ({event}) => event.request.destination === 'image',
  new workbox.strategies.CacheFirst({
    cacheName: "fw-images",
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 15,
      }),
    ],
  })
);
workbox.routing.registerRoute(
  ({event}) => event.request.destination === 'font',
  new workbox.strategies.CacheFirst({
    cacheName: "fw-fonts",
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 15,
      }),
    ],
  })
);
workbox.routing.registerRoute(
  ({event}) => (event.request.destination === 'json' || event.request.destination === 'manifest'),
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: "fw-json",
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 4,
      }),
    ],
  })
);
workbox.routing.registerRoute(
  ({url}) => (url.pathname.endsWith('/count') || url.pathname.endsWith('.txt')),
  new workbox.strategies.NetworkFirst({
    cacheName: "fw-text",
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 100,
      }),
    ],
  })
);
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    const usedCacheNames = ['fw-html','fw-javascript','fw-stylesheets','fw-images','fw-fonts','fw-json','fw-text','fw-offline']
    await Promise.all(names.map(name => {
      if (!usedCacheNames.includes(name)) {
        return caches.delete(name);
      }
    }));
    let cacheAdd = [["fw-javascript","{% url 'filmwatchcount:sw' %}"],["fw-offline","{% url 'filmwatchcount:offline' %}"],["fw-html","{% url 'filmwatchcount:home' %}"],["fw-json","{% url 'filmwatchcount:manifest' %}"]]
    for(let item of cacheAdd){
      let cache = await caches.open(item[0])
      if((await cache.match(item[1])) === undefined) await cache.add(item[1])
    }
  })());
});
function CheckIfNoCachePage(url){
  for(var page of noCachePages)
    if(url.pathname.endsWith(page)) return true;
  return false;
}