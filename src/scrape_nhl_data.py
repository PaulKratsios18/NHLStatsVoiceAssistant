from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import glob

# Configuration for each data category
CATEGORIES = {
    'skaters_alltime_regular': {
        'url': 'https://www.nhl.com/stats/skaters?reportType=allTime&seasonFrom=19171918&seasonTo=20242025&gameType=2&sort=points,goals,assists&page=0&pageSize=100',
        'pages': 78,
        'file_prefix': 'skaters_alltime_regular',
        'export_button_selector': '#allTime-tabpanel > h4 > a',
        'next_button_selector': '#allTime-tabpanel > span > nav > button.sc-dFlEjz.sc-evkevg.dOqwlm.buIKAH.sc-knozUR.fFqRwM'
    },
    'skaters_alltime_playoffs': {
        'url': 'https://www.nhl.com/stats/skaters?reportType=allTime&seasonFrom=19171918&seasonTo=20242025&gameType=3&sort=points,goals,assists&page=0&pageSize=100',
        'pages': 44,
        'file_prefix': 'skaters_alltime_playoffs',
        'export_button_selector': '#allTime-tabpanel > h4 > a',
        'next_button_selector': '#allTime-tabpanel > span > nav > button.sc-dFlEjz.sc-evkevg.dOqwlm.buIKAH.sc-knozUR.fFqRwM'
    },
    'skaters_current': {
        'url': 'https://www.nhl.com/stats/skaters?reportType=season&seasonFrom=20242025&seasonTo=20242025&gameType=2&sort=points,goals,assists&page=0&pageSize=100',
        'pages': 8,
        'file_prefix': 'skaters_current',
        'export_button_selector': '#season-tabpanel > h4 > a',
        'next_button_selector': '#season-tabpanel > span > nav > button.sc-dFlEjz.sc-evkevg.dOqwlm.buIKAH.sc-knozUR.fFqRwM'
    },
    'teams_alltime_regular': {
        'url': 'https://www.nhl.com/stats/teams?reportType=allTime&seasonFrom=19171918&seasonTo=20242025&gameType=2&sort=points,wins&page=0&pageSize=50',
        'pages': 1,
        'file_prefix': 'teams_alltime_regular',
        'export_button_selector': '#allTime-tabpanel > h4 > a',
        'next_button_selector': '#allTime-tabpanel > span > nav > button.sc-dFlEjz.sc-evkevg.dOqwlm.buIKAH.sc-knozUR.fFqRwM'
    },
    'teams_alltime_playoffs': {
        'url': 'https://www.nhl.com/stats/teams?reportType=allTime&seasonFrom=19171918&seasonTo=20242025&gameType=3&sort=points,wins&page=0&pageSize=50',
        'pages': 1,
        'file_prefix': 'teams_alltime_playoffs',
        'export_button_selector': '#allTime-tabpanel > h4 > a',
        'next_button_selector': '#allTime-tabpanel > span > nav > button.sc-dFlEjz.sc-evkevg.dOqwlm.buIKAH.sc-knozUR.fFqRwM'
    },
    'teams_current': {
        'url': 'https://www.nhl.com/stats/teams?reportType=season&seasonFrom=20242025&seasonTo=20242025&gameType=2&sort=points,wins&page=0&pageSize=50',
        'pages': 1,
        'file_prefix': 'teams_current',
        'export_button_selector': '#season-tabpanel > h4 > a',
        'next_button_selector': '#season-tabpanel > span > nav > button.sc-dFlEjz.sc-evkevg.dOqwlm.buIKAH.sc-knozUR.fFqRwM'
    },
    'goalies_alltime_regular': {
        'url': 'https://www.nhl.com/stats/goalies?reportType=allTime&seasonFrom=19171918&seasonTo=20242025&gameType=2&sort=wins,savePct&page=0&pageSize=100',
        'pages': 9,
        'file_prefix': 'goalies_alltime_regular',
        'export_button_selector': '#allTime-tabpanel > h4 > a',
        'next_button_selector': '#allTime-tabpanel > span > nav > button.sc-dFlEjz.sc-evkevg.dOqwlm.buIKAH.sc-knozUR.fFqRwM'
    },
    'goalies_alltime_playoffs': {
        'url': 'https://www.nhl.com/stats/goalies?reportType=allTime&seasonFrom=19171918&seasonTo=20242025&gameType=3&sort=wins,savePct&page=0&pageSize=100',
        'pages': 4,
        'file_prefix': 'goalies_alltime_playoffs',
        'export_button_selector': '#allTime-tabpanel > h4 > a',
        'next_button_selector': '#allTime-tabpanel > span > nav > button.sc-dFlEjz.sc-evkevg.dOqwlm.buIKAH.sc-knozUR.fFqRwM'
    },
    'goalies_current': {
        'url': 'https://www.nhl.com/stats/goalies?reportType=season&seasonFrom=20242025&seasonTo=20242025&gameType=2&sort=wins,savePct&page=0&pageSize=100',
        'pages': 1,
        'file_prefix': 'goalies_current',
        'export_button_selector': '#season-tabpanel > h4 > a',
        'next_button_selector': '#season-tabpanel > span > nav > button.sc-dFlEjz.sc-evkevg.dOqwlm.buIKAH.sc-knozUR.fFqRwM'
    }
}

# Directory to save downloaded files
download_dir = "/Users/paulkratsios/Library/Mobile Documents/com~apple~CloudDocs/Documents/Code Projects/NHLstatsVoiceAssistant/data"
downloads_folder = "/Users/paulkratsios/Downloads"

# Ensure the download directory exists
os.makedirs(download_dir, exist_ok=True)

def scrape_category(driver, category_config):
    driver.get(category_config['url'])
    time.sleep(0.1)
    
    # Accept cookies if present
    try:
        accept_cookies = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        accept_cookies.click()
    except:
        print("No cookie banner found or already accepted")

    # Loop through pages
    for page in range(category_config['pages']):
        print(f"Processing {category_config['file_prefix']} - page {page}")
        
        try:
            # Wait for table to be visible
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
            )
            
            # Get initial list of xlsx files in Downloads
            before_download = set(glob.glob(os.path.join(downloads_folder, "*.xlsx")))
            
            # Click export button using the correct selector
            js_click_script = f"""
            const exportButton = document.querySelector('{category_config['export_button_selector']}');
            if (exportButton) {{
                exportButton.click();
                return true;
            }}
            return false;
            """
            time.sleep(0.1)
            success = driver.execute_script(js_click_script)
            
            if not success:
                raise Exception("Could not find export button")
                
            # Wait for new file to appear
            max_attempts = 10
            attempts = 0
            new_file = None
            
            while attempts < max_attempts:
                current_files = set(glob.glob(os.path.join(downloads_folder, "*.xlsx")))
                new_files = current_files - before_download
                
                if new_files:
                    new_file = new_files.pop()
                    break
                    
                attempts += 1
                time.sleep(0.1)
            
            if new_file:
                # Move file to destination with category prefix
                destination = os.path.join(download_dir, f"{category_config['file_prefix']}_{page}.xlsx")
                os.rename(new_file, destination)
                print(f"Successfully moved file to {destination}")
            else:
                print("Download failed")
                break

            # Scroll and click next page
            js_scroll_script = "window.scrollTo(0, document.body.scrollHeight);"
            driver.execute_script(js_scroll_script)
            time.sleep(0.1)
            
            if page < category_config['pages'] - 1:  # Don't click next on last page
                js_next_script = f"""
                const nextButton = document.querySelector('{category_config['next_button_selector']}');
                if (nextButton) {{
                    nextButton.click();
                    return true;
                }}
                return false;
                """
                success = driver.execute_script(js_next_script)
                if success:
                    print(f"Successfully navigated to page {page + 1}")
                    time.sleep(0.1)
                else:
                    print("Could not find next button")
                    break
                    
        except Exception as e:
            print(f"Error processing page {page}: {str(e)}")
            break

def main():
    driver = webdriver.Safari()
    
    for category_name, config in CATEGORIES.items():
        print(f"\nStarting category: {category_name}")
        scrape_category(driver, config)
    
    driver.quit()

if __name__ == "__main__":
    main()