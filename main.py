from os import path
import requests
import random
import argparse

def fetch_wallpapers(keywords):
    """
    Fetch wallpaper links from Wallhaven API based on keywords
    """
    base_url = "https://wallhaven.cc/api/v1/search"
    
    query = '+'.join(keywords)
    
    params = {
        'q': query,
        'page': '1',
        'sorting': 'random',
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        wallpapers = data.get('data', [])
        if len(wallpapers) >1:
            wallpaper = random.choice(wallpapers)["path"]
        else:
            print(wallpapers)
            exit()
        
        return str(wallpaper) 
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching wallpapers: {e}")
        return "" 
    except ValueError:
        print("Error parsing API response")
        return "" 

def main():
    parser = argparse.ArgumentParser(description="Fetch wallpapers from Wallhaven based on keywords")
    parser.add_argument("--keywords", nargs='+', required=True, help="Keywords for search")
    args = parser.parse_args()
    
    wallpaper_links = fetch_wallpapers(args.keywords)
    
    if wallpaper_links:
        from os import system
        import os 
        from urllib.parse import urlparse 
        link =  os.path.basename(urlparse(wallpaper_links).path)
        r = requests.get(wallpaper_links,stream=True)
        cache_dir = os.path.expanduser("~/.cache/wallpapers/")
        link = os.path.basename(urlparse(wallpaper_links).path)
        cache = os.path.join(cache_dir, link)

        with open(cache,"wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        if path.exists("~/.cache/wallpapers/"):
            system("mkdir ~/.cache/wallpapers")
        system(f"walrs -i ~/.cache/wallpapers/{link}")

    else:
        print("No wallpapers found matching your criteria.")

if __name__ == "__main__":
    main()
