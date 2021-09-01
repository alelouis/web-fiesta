export const environment = {
  production: true,
  backend: window.location.origin + '/api',
  websocket: window.location.origin + '/',
  image: 'to_be_replaced' // sed -i '' 's/to_be_replaced/{{tag used in CI}}/g' environment.prod.ts
};
