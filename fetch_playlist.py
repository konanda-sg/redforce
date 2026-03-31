import re
import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# --- Channel Data provided by the user ---
CHANNELS = [
    { "id": "1", "name": "T SPORTS", "group": "Sports" },
    { "id": "88", "name": "A SPORTS HD", "group": "Sports" },
    { "id": "85", "name": "ALJAZEETA HD", "group": "English" },
    { "id": "35", "name": "AND FLIX HD", "group": "English" },
    { "id": "5", "name": "AND PICTURS HD", "group": "Hindi" },
    { "id": "41", "name": "AND PRIVE HD", "group": "English" },
    { "id": "61", "name": "AND XPLORE", "group": "English" },
    { "id": "26", "name": "ANIMAL PLANET HD", "group": "English" },
    { "id": "80", "name": "ATN BANGLA", "group": "Bangla" },
    { "id": "95", "name": "ATN NEWS", "group": "Bangla" },
    { "id": "97", "name": "AXN HD", "group": "English" },
    { "id": "50", "name": "BAL BHARAT", "group": "Kids" },
    { "id": "102", "name": "BBC EARTH HD", "group": "English" },
    { "id": "55", "name": "BBC NEWS", "group": "English" },
    { "id": "8", "name": "CARTOON NETWORK", "group": "Kids" },
    { "id": "82", "name": "CHANNEL 24", "group": "Bangla" },
    { "id": "81", "name": "CHANNEL I", "group": "Bangla" },
    { "id": "47", "name": "COLORS BANGLA CINEMA", "group": "Bangla" },
    { "id": "12", "name": "COLORS BANGLA HD", "group": "Bangla" },
    { "id": "10", "name": "COLORS CINEPLEX HD", "group": "Hindi" },
    { "id": "4", "name": "COLORS HD", "group": "Hindi" },
    { "id": "22", "name": "DISCOVERY HD", "group": "English" },
    { "id": "68", "name": "DURANTA TV", "group": "Kids" },
    { "id": "84", "name": "ENTERR 10", "group": "Bangla" },
    { "id": "40", "name": "EUROSPORTS HD", "group": "Sports" },
    { "id": "87", "name": "FAST SPORTS HD", "group": "Sports" },
    { "id": "90", "name": "GEO NEWS HD", "group": "Hindi" },
    { "id": "66", "name": "GOLF SPORTS", "group": "Sports" },
    { "id": "56", "name": "GTV", "group": "Bangla" },
    { "id": "98", "name": "HBO HD", "group": "English" },
    { "id": "15", "name": "HISTORY TV HD", "group": "English" },
    { "id": "70", "name": "HITZ MUSIC", "group": "English" },
    { "id": "89", "name": "HUM TV", "group": "Hindi" },
    { "id": "49", "name": "HUNGAMA", "group": "Kids" },
    { "id": "77", "name": "INDEPENDENT TV", "group": "Bangla" },
    { "id": "19", "name": "JALSHA MOVIES HD", "group": "Bangla" },
    { "id": "76", "name": "JAMUNA TV", "group": "Bangla" },
    { "id": "91", "name": "LOTUS TV", "group": "English" },
    { "id": "67", "name": "LOVE NATURE", "group": "English" },
    { "id": "78", "name": "MAASRANGA HD", "group": "Bangla" },
    { "id": "83", "name": "MADANI TV HD", "group": "Islamic" },
    { "id": "36", "name": "MN PLUS", "group": "English" },
    { "id": "33", "name": "MNX HD", "group": "English" },
    { "id": "39", "name": "MOVIES NOW HD", "group": "English" },
    { "id": "54", "name": "NAGORIK", "group": "Bangla" },
    { "id": "25", "name": "NATGEO HD", "group": "English" },
    { "id": "23", "name": "NATGEO WILD HD", "group": "English" },
    { "id": "46", "name": "NICK", "group": "Kids" },
    { "id": "51", "name": "NICK JR", "group": "Kids" },
    { "id": "86", "name": "PEACE TV BANGLA", "group": "Islamic" },
    { "id": "48", "name": "POGO", "group": "Kids" },
    { "id": "92", "name": "PTV SPORTS HD", "group": "Sports" },
    { "id": "34", "name": "ROMEDY NOW", "group": "English" },
    { "id": "79", "name": "SOMOY TV", "group": "Bangla" },
    { "id": "45", "name": "SONIC", "group": "Kids" },
    { "id": "44", "name": "SONY AAT", "group": "Bangla" },
    { "id": "6", "name": "SONY BBC EARTH HD", "group": "English" },
    { "id": "11", "name": "SONY ENT HD", "group": "Hindi" },
    { "id": "21", "name": "SONY MAX HD", "group": "Hindi" },
    { "id": "32", "name": "SONY PIX HD", "group": "English" },
    { "id": "74", "name": "SONY SPORTS 1 HD", "group": "Sports" },
    { "id": "29", "name": "SONY SPORTS 2 HD", "group": "Sports" },
    { "id": "30", "name": "SONY SPORTS 3", "group": "Sports" },
    { "id": "72", "name": "SONY SPORTS 4", "group": "Sports" },
    { "id": "101", "name": "SONY SPORTS 5 HD", "group": "Sports" },
    { "id": "93", "name": "SONY YAY", "group": "Kids" },
    { "id": "96", "name": "SSC SPORTS", "group": "Sports" },
    { "id": "103", "name": "SSC SPORTS 5 HD", "group": "Sports" },
    { "id": "100", "name": "STAR BHARAT HD", "group": "Hindi" },
    { "id": "69", "name": "STAR GOLD 2 HD", "group": "Hindi" },
    { "id": "20", "name": "STAR GOLD HD", "group": "Hindi" },
    { "id": "71", "name": "STAR GOLD SELECT HD", "group": "Hindi" },
    { "id": "18", "name": "STAR JALSHA HD", "group": "Bangla" },
    { "id": "38", "name": "STAR MOVIES HD", "group": "English" },
    { "id": "27", "name": "STAR MOVIES SELECT HD", "group": "English" },
    { "id": "24", "name": "STAR PLUS HD", "group": "Hindi" },
    { "id": "28", "name": "STAR SELECT 1 HD", "group": "Sports" },
    { "id": "2", "name": "STAR SPORTS 1 HD", "group": "Sports" },
    { "id": "3", "name": "STAR SPORTS 2 HD", "group": "Sports" },
    { "id": "31", "name": "STAR SPORTS 3", "group": "Sports" },
    { "id": "16", "name": "STAR SPORTS SELECT 2 HD", "group": "Sports" },
    { "id": "17", "name": "SUN BANGLA HD", "group": "Bangla" },
    { "id": "75", "name": "SUPER HUNGAMA", "group": "Kids" },
    { "id": "9", "name": "TLC HD", "group": "English" },
    { "id": "62", "name": "TRAVEL XP", "group": "English" },
    { "id": "43", "name": "ZEE BANGLA CINEMA", "group": "Bangla" },
    { "id": "14", "name": "ZEE BANGLA HD", "group": "Bangla" },
    { "id": "37", "name": "ZEE CAFE HD", "group": "English" },
    { "id": "13", "name": "ZEE CINEMA HD", "group": "Hindi" },
    { "id": "7", "name": "ZEE TV HD", "group": "Hindi" },
    { "id": "53", "name": "ZING", "group": "Hindi" },
    { "id": "42", "name": "ZOOM", "group": "Hindi" }
]

BASE_URL = 'http://103.144.89.251/'
PLAYLIST_FILENAME = "playlist.m3u"
MAX_WORKERS = 20
PAGE_LOAD_TIMEOUT = 4

def get_channel_stream(channel_info):
    player_url, channel_name, group = channel_info
    print(f"-> Processing: {channel_name}")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(player_url)
        time.sleep(PAGE_LOAD_TIMEOUT)

        player_html = driver.page_source
        if "error code: 1003" in player_html:
            print(f"SKIPPED (Blocked): {channel_name}")
            return None

        match = re.search(r"var primarySource = '(.*?)';", player_html)
        if match and match.group(1):
            m3u8_url = match.group(1)
            print(f"SUCCESS: {channel_name}")
            return f'#EXTINF:-1 tvg-name="{channel_name}" group-title="{group}",{channel_name}\n{m3u8_url}'
        else:
            print(f"SKIPPED (No URL): {channel_name}")
            return None
    except Exception as e:
        print(f"ERROR on {channel_name}: {e}")
        return None
    finally:
        if driver:
            driver.quit()

def create_playlist_from_list():
    start_time = time.time()

    channels_to_process = []
    for channel in CHANNELS:
        player_url = f"{BASE_URL}player.php?stream={channel['id']}"
        channels_to_process.append((player_url, channel['name'], channel['group']))

    print(f"Using provided list of {len(channels_to_process)} channels. Starting parallel fetch with {MAX_WORKERS} workers...")

    playlist_entries = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = executor.map(get_channel_stream, channels_to_process)
        playlist_entries = [res for res in results if res is not None]

    if playlist_entries:
        print(f"\nWriting {len(playlist_entries)} channels to {PLAYLIST_FILENAME}...")
        playlist_entries.sort()
        final_content = ["#EXTM3U"] + playlist_entries
        with open(PLAYLIST_FILENAME, "w") as f:
            f.write("\n".join(final_content))
        print("Playlist creation complete!")
    else:
        print("\nNo stream URLs were extracted. Playlist file was not created.")

    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    create_playlist_from_list()
