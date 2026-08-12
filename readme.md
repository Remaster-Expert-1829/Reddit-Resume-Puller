# Reddit Resume Puller

A modern, premium web application that pulls and displays developer resumes from various subreddits for review and feedback. Built with a sleek glassmorphism UI, this tool makes it easy to browse, sort, and analyze resumes with high-quality image zooming and panning features.

## Features

- **Dynamic Resume Grid**: Beautiful glassmorphism cards displaying the resume title, subreddit origin, upvotes, and comments.
- **Advanced Sorting**: Filter resumes by:
  - Random (Fresh mix)
  - Most/Least Upvotes
  - Most/Least Comments
- **Interactive Image Viewer**: Click on any resume to open a fullscreen lightbox modal. Supports:
  - Mouse wheel zoom in/out
  - Click and drag to pan around high-resolution resumes
  - Left/Right click zooming
- **One-Click Data Refresh**: Instantly trigger the Python scraper script directly from the website to pull the latest resumes, with seamless UI auto-reloading.
- **Direct Reddit Integration**: Click on any resume title to instantly navigate to the original Reddit thread to read comments and roasts.

## Tech Stack

- **Frontend**: Vanilla HTML5, CSS3 (Custom Grid, CSS Variables, Animations), and JavaScript (ES6+).
- **Backend Options**: Includes both **Node.js (Express)** and **Python** backend implementations to handle data refreshing and static file serving.
- **Data Source**: A local `data.json` file populated by the background Python script (`main.py`).

## Installation & Setup

### Prerequisites
- [Python 3.x](https://www.python.org/downloads/) (for the data pulling script)
- [Node.js](https://nodejs.org/) (optional, if you prefer the Node backend)
- **Google Chrome** installed on your system.
### Configuration
Before running the application, ensure the Python script can find your Google Chrome installation:
1. Open `main.py` in your code editor.
2. Locate the `chrome_path` variable (around line 34).
3. If your Chrome is installed in a different directory than the default (`C:\Program Files\Google\Chrome\Application\chrome.exe`), you **must** update this path manually for the scraper to work.

### Installing Dependencies
Before running anything, you need to install the required Python packages (such as Playwright). You can automatically install everything by running the included setup script in your terminal:
```bash
python requirements.py
```

### Running the Application

You have a few flexible ways to run this application. Because the "Refresh Data" button needs to execute a local Python script, you must run one of the included backends.

#### Option 1: The Node.js Backend (Recommended)
This method uses Express to serve the website and handle the refresh API.
1. Open your terminal in the project directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the server:
   ```bash
   node server.js
   ```
4. Visit `http://localhost:8000` in your browser.

#### Option 2: The Python Backend
If you prefer an all-Python environment, a custom server script is provided.
1. Open your terminal in the project directory.
2. Start the server:
   ```bash
   python server.py
   ```
3. Visit `http://localhost:8000` in your browser.

#### Option 3: VS Code Live Server + Backend API
If you are developing and want to use the **VS Code Live Server** extension for frontend auto-reloading:
1. Start your VS Code Live Server (typically opens on `http://localhost:5500`).
2. Open a separate terminal and start either backend (Node or Python) on port 8000:
   ```bash
   node server.js
   # OR
   python server.py
   ```
3. The frontend is specifically configured with CORS to talk to port `8000`, so the "Refresh Data" button will still work perfectly even while using Live Server!

## Project Structure

- `index.html`: The main dashboard structure.
- `style.css`: All styling, animations, and glassmorphism effects.
- `script.js`: Frontend logic (DOM manipulation, sorting, fetching data, modal zooming/panning).
- `server.js`: Node.js Express backend.
- `server.py`: Python custom HTTP backend.
- `main.py`: The core script that pulls resume data from Reddit.
- `data.json`: The database file where pulled resumes are stored.

## Customizing the Reddit Queries

The core logic of which resumes are pulled lives at the very top of `main.py`. You can change these URLs to pull different posts, target different subreddits, or change the search terms.

### Understanding the URL Structure
Currently, the script uses URLs like this:
`https://old.reddit.com/r/developersindia/search.json?q=resume+OR+graduate&restrict_sr=on&limit=100&t=all`

Here is how you can modify the parameters to get different results:

- **Change the Subreddit**: Replace `r/developersindia` with any other subreddit (e.g., `r/cscareerquestions`, `r/resumes`).
- **Change Search Keywords**: Modify the `q=` parameter. For example, `q=software+engineer+resume` or `q=frontend+portfolio`. (Use `+` for spaces and `OR` for multiple optional terms).
- **Time Filters**: Modify the `t=` parameter to search within a specific timeframe. 
  - `t=all` (All time - default)
  - `t=year` (Past year)
  - `t=month` (Past month)
  - `t=week` (Past week)
  - `t=day` (Past 24 hours)
- **Number of Posts**: The `limit=100` parameter tells Reddit how many posts to return. **Note:** Reddit enforces a strict maximum of 100 posts per single request. Will update the project to be able to pull more than 100 posts later though.

### Troubleshooting: Blocked by Reddit (429/Forbidden Errors)
Reddit has strict rate limits and occasionally blocks automated requests. If the script fails to pull data and you suspect you are being blocked:
1. **Generate Cookies**: The script launches a debug instance of Chrome. When it opens, manually navigate to `reddit.com` and just scroll around for a few seconds. This allows the browser to naturally acquire some fresh session cookies, which usually bypasses the block.
2. **Login Method**: If scrolling anonymously doesn't work, manually log into your Reddit account on the debug browser, scroll around for a few seconds, and then let the script run. You can safely log out afterwards.

#### How to manually launch the debug browser
If you need to open the isolated debug browser on your own (to pre-load cookies or log in before running the script), you can launch it manually by opening your terminal or command prompt and running:
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9225 --remote-allow-origins=* --user-data-dir=C:\ChromeDebug --new-window
```
*(Note: If your Chrome is installed in a different directory, adjust the path accordingly).*

---

## Developer Notes & Roadmap (WIP)

code is working great now, we can fetch resumes successfully;

**Worthy additions:**
1. modify url to go through a large number of posts preferably over 500 posts (requires pagination) + add more keywords for searching posts
2. people can adjust number of posts, add/remove subreddits, adjust filters, etc on the webpage itself
3. host the webpage publicly where the python script would be running and refreshing periodically and people can adjust number of posts, add/remove subreddits, adjust filters, etc

**Project documentation goals:**
wish to have complete installation, how to use, modify url to have different results, modify the code to user's specific use case sections in future once project is okayishingly complete

**Failure story:**
document the entire try attempts, what worked and what didn't, explain everything thoroughly including reddit's new policies to block everyone trying to scrape their data