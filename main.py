import os
from playwright.sync_api import sync_playwright
import subprocess
import time
import html
import json
import socket

five_years_ago=time.time()-(5*365*24*60*60)
#using old.reddit.com as it is less strict in blocking requests compared to new reddit
web=[]
#reddit can only provide a maximum of 100 posts per request, if we want more posts make multiple requests using the 'after' paramater at the end of the url (apply pagination)
url= "https://old.reddit.com/r/developersindia/search.json?q=resume+OR+graduate&restrict_sr=on&limit=100&t=all"
alt_url="https://old.reddit.com/r/btechtards/search.json?q=resume+OR+graduate&restrict_sr=on&limit=100&t=all"
web.append(url)
web.append(alt_url)
def wait_for_port(port,timeout=30):
    print(f"Waiting for port {port} to be open")
    start_time=time.time()
    while time.time()-start_time<timeout:
        try:
            with socket.create_connection(("localhost",port),timeout=1):
                print(f"Port {port} is open")
                return True
        except (ConnectionRefusedError,TimeoutError,OSError):
            time.sleep(1)
    print("Timed out waiting for the port to be open")
    return False
def launch_chrome():
    print("Commander Cody, the time has come. Execute Order 66")
    #subprocess.run(["taskkill","/F","/IM","chrome.exe","/T"],capture_output=True) don't need to close chrome instances anymore
    time.sleep(2)
    print("Launching chrome with remote debugging enabled...")
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Update this path according to your Chrome installation
    profile_path=os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
    try:
        subprocess.Popen([
            chrome_path,
            "--remote-debugging-port=9225",
            "--remote-allow-origins=*",
            r"--user-data-dir=C:\ChromeDebug",
            "--new-window"
        ])
        if not wait_for_port(9225):
            print("Chrome failed to open debugging port")
            exit(1)
        print("Chrome launched successfully")
    except FileNotFoundError:
        print("Error:Could not find Chrome executable in the given path. Please check chrome is installed and update the chrome_path variable with the correct path to your Chrome installation.")
        exit()     
def main():
    print("Reddit Resume Scraper by SonicX1829")
    launch_chrome()
    #list for storing scraped data
    scraped_data=[]
    global_post_count=0
    with sync_playwright() as p:
        try:
            browser=p.chromium.connect_over_cdp("http://localhost:9225")
            default_context=browser.contexts[0]
            page=default_context.pages[0]
            for url in web:
                subreddit_name=url.split("r/")[1].split("/")[0]
                response=page.goto(url)
                print(f"Browser navigated to r/{subreddit_name}.")
                time.sleep(3)
                raw_text=page.locator("body").inner_text()
                if "You've been blocked by network security" in raw_text:
                    print("Error 403: we doomed")
                elif "Too Many Requests" in raw_text:
                    print("Error: 429: getting rate limited. Please try again later")
                else:
                    try:
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
                                global_post_count+=1
                                scraped_data.append({
                                    "id": global_post_count,
                                    "subreddit": subreddit_name,
                                    "title": title,
                                    "link": permalink,
                                    "images": image_urls
                                })
                        print(f"Found {valid_post_count} valid image posts within the last 5 years")
                    except json.JSONDecodeError:
                        print("Failed to parse JSON response")
                        page.screenshot(path="/debug/reddit_block_screenshot.png")
                        print("Saved a screenshot of Reddit for debugging help")
            if scraped_data:
                with open("data.json","w",encoding="utf-8") as json_file:
                    json.dump(scraped_data,json_file,indent=4,ensure_ascii=False)
                    print("Data successfully saved to data.json")
            else:
                print("No valid posts found")
        except Exception as e:
            print(f"Failed to connect to Chrome: {e}")
if __name__ == "__main__":
    main()