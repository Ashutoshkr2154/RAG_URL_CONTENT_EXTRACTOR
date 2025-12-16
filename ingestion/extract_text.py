import time 
from bs4 import BeautifulSoup
from typing import List 

from fetch_main_url import fetch_main_url_html , URLFetchError
from extract_urls import extract_child_urls

class TextExtractionError(Exception):
    """Custom exception for text exception failures.
    """

def clean_text(text : str) -> str : 
    """Clean extra spaces and newlines"""
    return " ".join(text.split())

def extract_page_text(html:str) -> str: 
    """
    Extract visible text from HTML.
    """
    soup = BeautifulSoup(html ,"html.parser")
    return clean_text(soup.get_text(separator=" "))

def fetch_child_text(url:str , retries:int= 3) -> str: 
    """Fetch child URL text with retry logic """

    for attempt in range(retries):
        try : 
            html = fetch_main_url_html(url)
            return extract_page_text(html)
        
        except URLFetchError: 
            time.sleep(2)
    
    return ["CONTENT NOT AVAILABLE DUE TO TIMEOUT"]

def build_final_text(main_url :str , output_file:str = "data.txt") -> None : 
    """
    Build final merged text : 
    main text + inline child URL replacement 
    """

    try : 
        ## step 1 : fetch main URL HTML . 
        main_html = fetch_main_url_html(main_url)

        ## Step 2 : extract child urls 
        child_urls = extract_child_urls(main_html , main_url)

        ## Step 3 : extract main URL Text 
        main_text = extract_page_text(main_html)

        final_text = main_text 

        ## Step 4 : inline replace child URLs with their content. 

        for child_url in child_urls: 
            child_text = fetch_child_text(child_url)
            child_text = child_text[:1500] 

            replacement  = f"({child_text})"
            final_text = final_text.replace(child_url , replacement)
        
        # step 5 : save to data.txt 
        with open(output_file , "w" , encoding="utf-8") as f : 
            f.write(final_text)
        
        print(f"Final merged content saved to {output_file}")

    except Exception as e : 
        raise TextExtractionError(f"Text extraction failed:{e}")
"""
if __name__ == "__main__":
    MAIN_URL = "https://www.rnc-pro.com/rnc-pro/pfm/100/192_0100.HTM"
    build_final_text(MAIN_URL)
"""