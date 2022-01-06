class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.greeting = "Salam"
        self.count_requests = 0
        self.count_exceptions = 0

    def __call__(self, request, *args, **kwargs):
        self.count_requests += 1
        print("number of requests: ", self.count_requests)
        print(request.headers["X-MYHEADER"])
        # logger.info(f"Handled {self.count_requests} requests so far")
        if "Gr" in request.headers["X-MYHEADER"]:
            print("hallo")
            request.GET["name"] = "traum"
    elif "En" in request.headers["X-MYHEADER"]:
        print("Hi")
        request.data["name"] = "dream"
    else:
        print(self.greeting)
        request.data["name"] = "roya"
    return self.get_response(request)

    def process_exception(self, request, exception):
        self.count_exceptions += 1
        # logger.error(f"Encountered {self.count_exceptions} exceptions so far")
