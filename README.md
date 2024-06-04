# Twitter Alerts (Scraper and Repost)

## Overview

This project aims to automate the process of scraping tweets containing a specific keyword, downloading associated media, and reposting the most liked tweets. The script performs these actions every 20 minutes, ensuring that you stay updated with the latest and most popular tweets. 

## Process of Script

1. **Scrape Tweets**: Fetch tweets containing the exact phrase specified by the given keyword every 20 minutes.
2. **Download Media**: Download all media from the fetched tweets and save them into the `media` folder.
3. **Repost Popular Tweets**: Identify the top 2 tweets with the most likes and repost them.
4. **Log Scraped Tweets**: Save the scraped tweets into `twitter_alert.txt`.
5. **Repeat**: Wait for 20 minutes and repeat the process.

## Technologies Used
- Python
- JSON


## Libraries Used

- `beautifulsoup4`: A library for parsing HTML and XML documents, used for web scraping purposes.
- `lxml`: A library for processing XML and HTML in Python, often used in conjunction with BeautifulSoup for parsing.
- `requests`: A simple HTTP library for making requests to web services and APIs.
- `requests-oauthlib`: An OAuth library for requests, used for handling OAuth authentication.
- `python-dotenv`: A library for reading key-value pairs from a `.env` file and setting them as environment variables.


## Installation

#### 1. Install Python

- Ensure you have [Python](https://www.python.org/downloads/) installed.
- During installation, check the `Add to PATH` checkbox.

#### 2. Install Required Packages
Open your command prompt (cmd) and run the following commands to install the necessary packages:

     ```
     pip install requests
     pip install requests-oauthlib
     pip install python-dotenv

     ```


#### 3. Download the Repository
   - Download this repository's code from [GitHub](https://github.com/arnaldo31/twitter-alerts/archive/refs/heads/main.zip).

#### 4. Unzip the File
   - Unzip the downloaded file. If you do not have an unzip application, you can download one [here](https://www.7-zip.org/a/7z2406-x64.exe).

## How to Use

1. Open the folder where this project is saved on your local machine.
2. Open `.env` file as text file and edit the filters.

    - keyword=`TARGET KEYWORD`
    - bearer_token=`BEARER TOKEN`
    - consumer_key =`CONSUMER KEY`
    - consumer_secret =`CONSUMER SECRET`
    - access_token=`ACCESS TOKEN`
    - access_token_secret=`ACCESS TOKEN SECRET`

   Make sure to replace the placeholder text with your actual credentials obtained from your Twitter Developer account. These credentials are necessary for authenticating your application and accessing Twitter's API.

3. To get API KEYS, visit Twitter Developer. [TwitterDev](https://developer.twitter.com/).
4. Go to Permissions and change OAuth 1.0a Authentication to "Read and write".
   ![alt text](https://github.com/arnaldo31/twitter-alerts/blob/main/permit.png?raw=true)

5. Run the `main.py` script to start the scraping.
6. Scrape results will be saved as `twitter_alerts.txt` located inside the save folder.

## Files and Directory Structure

 - `main.py` - The main script to start the scraping.
 - `save/` - Folder where scraped tweets are saved.
 - `media/` - Folder where downloaded media files are saved.
 - `.env` - Environment file containing your Twitter API credentials and keyword.
