function handler(event) {
  var request = event.request;
  var uri = request.uri;

  if (uri.endsWith("/")) {
    uri = uri.slice(0, -1);
  }

  var routes = [
    "/mortgage-calculator",
    "/market-data",
    "/tech"
  ];

  if (routes.indexOf(uri) !== -1) {
    request.uri = "/index.html";
  }

  return request;
}
