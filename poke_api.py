import requests

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Test out the get_pokemon_info() function
    # Use breakpoints to view returned dictionary
    poke_info = get_pokemon_info("Rockruff")
    if poke_info:
        print(poke_info)
    
    # Test out the get_all_pokemon_names() function
    all_pokemon_names = get_all_pokemon_names()
    if all_pokemon_names:
        print("Total Pokémon names:", len(all_pokemon_names))
    
    # Test out the download_pokemon_artwork() function
    download_pokemon_artwork("pikachu", "pikachu.png")
    return

def get_pokemon_info(pokemon):
    """Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    pokemon = str(pokemon).strip().lower()

    if not pokemon:
        print('Error: No Pokemon name specified.')
        return

    url = POKE_API_URL + pokemon
    resp_msg = requests.get(url)

    if resp_msg.status_code == requests.codes.ok:
        return resp_msg.json()
    else:
        print(f'Failed to retrieve Pokemon data. Response code: {resp_msg.status_code} ({resp_msg.reason})')

def get_all_pokemon_names():
    """Gets a list of all Pokemon names from the PokeAPI.

    Returns:
        list: List of all Pokemon names, if successful. Otherwise None.
    """
    url = POKE_API_URL + "?limit=10000"
    resp_msg = requests.get(url)

    if resp_msg.status_code == requests.codes.ok:
        pokemon_data = resp_msg.json()
        pokemon_names = [entry["name"] for entry in pokemon_data["results"]]
        return pokemon_names
    else:
        print(f'Failed to retrieve Pokemon names. Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return None

def download_pokemon_artwork(pokemon, filename):
    """Downloads and saves Pokemon artwork from the PokeAPI.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)
        filename (str): Name of the file to save the artwork as

    Returns:
        None
    """
    url = POKE_API_URL + f"{pokemon}/"
    resp_msg = requests.get(url)

    if resp_msg.status_code == requests.codes.ok:
        pokemon_data = resp_msg.json()
        artwork_url = pokemon_data["sprites"]["front_default"]
        artwork_resp = requests.get(artwork_url)

        if artwork_resp.status_code == requests.codes.ok:
            with open(filename, 'wb') as f:
                f.write(artwork_resp.content)
            print(f'Artwork for {pokemon} downloaded and saved as {filename}')
        else:
            print(f'Failed to download artwork for {pokemon}. Response code: {artwork_resp.status_code} ({artwork_resp.reason})')
    else:
        print(f'Failed to retrieve Pokemon data. Response code: {resp_msg.status_code} ({resp_msg.reason})')

if __name__ == '__main__':
    main()
