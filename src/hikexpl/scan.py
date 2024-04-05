from shodan import Shodan
def scan(token, dork, pages):
    api = Shodan(token)
    print(api.info())
    urls = []
    for i in range(1, pages):
        results = api.search(dork, page=i)
        for result in results['matches']:
            ip = result['ip_str']
            port = result['port']
            if port == 443:
                url = "https://" + str(ip)
            else:
                url = "http://" + str(ip) + ":" + str(port)

            urls.append(url)

    return urls



