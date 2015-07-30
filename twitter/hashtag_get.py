from bs4 import BeautifulSoup
import mechanize
import cookielib

url = 'https://twitter.com/search?f=realtime&q=%23ep2014%20since%3A2014-01-31%20until%3A2014-07-01&src=typd'

br = mechanize.Browser()

# set cookies
cookies = cookielib.LWPCookieJar()
br.set_cookiejar(cookies)

# browser settings (used to emulate a browser)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_debug_http(False)
br.set_debug_responses(False)
br.set_debug_redirects(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br.open(url)
print br.response().read()