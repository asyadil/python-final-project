import climage
import requests
import urllib.parse
import time
from tabulate import tabulate
from io import BytesIO

def data_fetching(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("Fetching data...")
            time.sleep(1)
            print("Completed!")
            return response.json()
        elif response.status_code == 404:
            print("Pokemon not found!")
            return None
        else:
            print(f"Request failed.\nStatus code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def pokemon_searching():
    keyword = input("Enter pokemon name: ").strip()
    if not keyword:
        print("Invalid, try again")
        return None
    
    keyword = urllib.parse.quote(keyword.lower())
    url = f"https://pokeapi.co/api/v2/pokemon/{keyword}"
    return data_fetching(url)

def get_details(searching_results):
    name = searching_results['name'].capitalize()
    
    stats = searching_results['stats']
    data_statistics = []
    for i in stats:
        stat_name = i['stat']['name'].replace('-', ' ').title()
        stat_value = i['base_stat']
        data_statistics.append([stat_name, stat_value])
    
    types = searching_results['types']
    type_names = [type_info['type']['name'].capitalize() for type_info in types]
    
    image = searching_results['sprites']['other']['official-artwork']['front_default']
    
    moves = searching_results['moves']
    move_names = [move_info['move']['name'].replace('-', ' ').title() 
    for move_info in moves[:10]]
    
    return name, data_statistics, type_names, move_names, image

def display_image(image):
    try:
        response = requests.get(image, timeout=10)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            
            output = climage.convert(image_data, width=50)
            print(output)
        else:
            print("Failed to load image")
    except Exception as e:
        print(f"Error displaying image: {e}")

def stats_display(name, data_statistics, types, moves, image):
    print(f"\n{'='*50}")
    print(f"Statistics for {name}")
    print(f"{'='*50}\n")
    display_image(image)

    print(tabulate(data_statistics, headers=['Stat', 'Value'], tablefmt='grid'))
    
    print(f"\nType: {', '.join(types)}")
    
    print(f"\nFirst 10 Moves:")
    for idx, move in enumerate(moves, 1):
        print(f"   {idx}. {move}")
    
    print(f"\n{'='*50}")
    input("\nPress Enter to search another pokemon...")
    print()

def main():
    searching_results = pokemon_searching()

    if searching_results is None:
        print("\nCannot display stats. Try again.\n")
        time.sleep(1)
        return

    name, data_statistics, types, moves, image = get_details(searching_results)

    stats_display(name, data_statistics, types, moves, image)

if __name__ == "__main__":
    print("=== Pokemon Stats Viewer ===\n")
    while True:
        main()









