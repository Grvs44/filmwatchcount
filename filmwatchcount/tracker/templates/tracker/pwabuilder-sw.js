importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');
const noCachePages = ['create','delete','deleted','duplicate','update','pwadate'];
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});
workbox.routing.registerRoute(
  new RegExp("/admin*"),
  new workbox.strategies.NetworkOnly()
);
workbox.routing.registerRoute(
  ({url}) => CheckIfNoCachePage(url),
  new workbox.strategies.NetworkOnly()
);
workbox.routing.registerRoute(
  ({event}) => (event.request.destination === 'document'),
  new workbox.strategies.NetworkFirst({
    cacheName: "html",
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 100,
      }),
    ],
  })
);
workbox.routing.setCatchHandler(async (options) => {
  const cache = await self.caches.open('offline');
  if(options.request.destination === 'document') return (await cache.match('{% url "tracker:offline" %}')) || Response.error();
  return Response.error();
});
workbox.routing.registerRoute(
  ({event}) => (event.request.destination === 'script' || event.request.destination === 'javascript'),
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: "javascript",
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
    cacheName: "stylesheets",
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
    cacheName: "images",
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
    cacheName: "fonts",
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
    cacheName: "json",
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
    cacheName: "text",
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 100,
      }),
    ],
  })
);
self.addEventListener('activate', event => {
  console.log("activate");
  event.waitUntil((async () => {
    const names = await caches.keys();
    const usedCacheNames = ['html','javascript','stylesheets','images','fonts','json','text','offline']
    await Promise.all(names.map(name => {
      if (!usedCacheNames.includes(name)) {
        return caches.delete(name);
      }
    }));
    let cacheAdd = [["javascript","{% url 'tracker:sw' %}"],["offline","{% url 'tracker:offline' %}"],["html","{% url 'tracker:home' %}"],["json","{% url 'tracker:manifest' %}"]]
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