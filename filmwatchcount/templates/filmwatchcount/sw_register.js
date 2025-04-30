if('serviceWorker' in navigator) navigator.serviceWorker.register('{% url "filmwatchcount:sw" %}',{updateViaCache:'all'})
  