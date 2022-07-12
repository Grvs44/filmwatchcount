{% load static %}
importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');
const noCachePages = ['/create','/delete','/deleted','/duplicate','/update'];
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
  ({event}) => event.request.destination === 'document',
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
  if(options.request.destination === 'document') return (await cache.match('/offline.html')) || Response.error();
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
  new workbox.strategies.StaleWhileRevalidate({
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
  new workbox.strategies.StaleWhileRevalidate({
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
    (await caches.open("offline")).add("/offline.html");
    (await caches.open("html")).add("/");
    (await caches.open("json")).add("/manifest.json");
    (await caches.open("stylesheets")).add("{% static '/css/list.css' %}");
  })());
});
function CheckIfNoCachePage(url){
  for(var page of noCachePages)
    if(url.pathname.endsWith(page)) return true;
  return false;
}