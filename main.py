#could have used the reddit api only if it was not locked behind a form
#import requests                            reddit keeps on detecting and blocking the user agent
#from curl_cffi import requests             also doesn't work wow
#from playwright.sync_api import sync_playwright     I am gonna cry broooo
#from playwright_stealth import Stealth              even big dawg not working :crying emoji:
#from seleniumbase import SB                         I am crying ngl
from playwright.sync_api import sync_playwright
import time
import html
import json
#import random                              didnt work

five_years_ago=time.time()-(5*365*24*60*60)
#using old.reddit.com as it is less strict in blocking requests compared to new reddit
url= "https://old.reddit.com/r/developersindia/search.json?q=resume+OR+graduate&restrict_sr=on&limit=20&t=all"
#random_version=random.randint(10000000,99999999)
#random version used to avoid crashing as Reddit might block requests from same agent
'''headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0"
}''' #No more needed as curl_cffi handles it itself
#print("Fetching data from Reddit... might take some time\n")
#response=requests.get(url,impersonate="chrome116")                      well tried but rip
def main():
    print("Launching browser instance to fetch data...")
    #with Stealth().use_sync(sync_playwright()) as p:
    #with SB(uc=True,headless=False) as sb:
    with sync_playwright() as p:
        try:
            browser=p.chromium.connect_over_cdp("http://localhost:9222")
            #browser=p.chromium.launch(headless=False)
            #telling playwright to use a normal chrome user agent to avoid it explicitly announcing itself as a bot
            '''context=browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )'''
            default_context=browser.contexts[0]
            page=default_context.pages[0]
            #page=browser.new_page()
            #page=context.new_page()
            #stealth_sync(page)
            response=page.goto(url)
            #sb.driver.get(url)
            
            print(f"Browser navigated to the page.")
            #delay incase Cloudflare has an invisible challenge to process, thus giving it some time to complete before trying to access the content
            time.sleep(3)
            raw_text=page.locator("body").inner_text()
            #raw_text=sb.get_text("body")
            if "You've been blocked by network security" in raw_text:
                print("Error 403: we doomed")
            elif "Too Many Requests" in raw_text:
                print("Error: 429: getting rate limited. Please try again later")
            else:
                try:
                    #data=response.json()
                    data=json.loads(raw_text)

                    valid_post_count=0

                    for post in data['data']['children']:
                        post_data=post['data']
                        #skipping posts that are older than 5 years
                        if post_data['created_utc'] < five_years_ago:
                            continue
                        title=post_data['title']
                        permalink=f"https://www.reddit.com{post_data['permalink']}"
                        #for storing all image urls from a post
                        image_urls = []
                        #getting image urls from a gallery post
                        if post_data.get('is_gallery'):
                            media_dict=post_data.get('media_metadata',{})
                            
                            for media_id,media_info in media_dict.items():
                                if media_info['e']=='Image':
                                    raw_url=media_info['s'].get('u', '')
                                    clean_url=html.unescape(raw_url)
                                    image_urls.append(clean_url)
                        else:
                            post_url=post_data.get('url', '')
                            if post_url.endswith(('.jpg',',jpeg','.png')) or 'i.redd.it' in post_url:
                                image_urls.append(post_url)
                        if image_urls:
                            valid_post_count+=1
                            print(f"[{valid_post_count}] Title: {title}")
                            print(f"Post link: {permalink}")
                            for count,img in enumerate(image_urls,1):
                                print(f" -> Image {count}: {img}")
                            print("-"*60)
                    print(f"\nFound {valid_post_count} valid image posts within the last 5 years")
                #except requests.exceptions.JSONDecodeError:         sorri
                except json.JSONDecodeError:
                    print("Failed to parse JSON response")
                    page.screenshot(path="/debug/reddit_block_screenshot.png")
                    #sb.save_screenshot("/debug/reddit_block_screenshot.png")
                    print("Saved a screenshot of Reddit for debugging help")
                    #print("Raw Response content snippet:")
                    #print(response.text[:500])
            '''if response.status !=200:
                print(f"Error fetching data: Reddit returned status code {response.status}")
                if response.status == 429:
                    print("Getting rate limited. Please try again later")
                elif response.status == 403:
                    print("Access forbidden. Reddit is blocking this User-agent")''' #this no more for old guys as selenium kinda like a human so it is
                    #hard to read HTTP status codes as it opens the website and doesn't return any response object like requests does, so we have to check
                    #the page content for any error messages instead
        except Exception as e:
            print(f"Failed to connect to Chrome: {e}")
            print("Make sure you ran the 'chrome.exe --remote-debugging-port=9222 --user-data-dir='C:\\ChromeDebug'' command first!")
if __name__ == "__main__":
    main()