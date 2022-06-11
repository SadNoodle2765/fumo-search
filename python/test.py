from fake_useragent import UserAgent
ua = UserAgent(use_cache_server=False)

print(ua.random)