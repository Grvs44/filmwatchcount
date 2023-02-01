export const apiRootPath = (window.location.port === '3000')? 'http://localhost:8000/filmwatchcount/api/' : window.location.pathname + 'api/'
console.log('apiRootPath = ', apiRootPath)
