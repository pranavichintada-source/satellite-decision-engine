from skyfield.api import load

def load_satellites():
    # Download TLE data from CelesTrak
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
    
    satellites = load.tle_file(url)
    
    print(f"Loaded {len(satellites)} satellites")
    
    return satellites[:5]  # keep only 5 for demo