"""
Reads all published restaurant .md files and outputs GeoJSON to public/data/restaurants.geojson
Run from site root: python3 scripts/build_geojson.py
"""
import os, re, json

restaurants_dir = "/sessions/bold-funny-sagan/mnt/Morristown Eats/morristown-eats-site/src/content/restaurants"
output_path = "/sessions/bold-funny-sagan/mnt/Morristown Eats/morristown-eats-site/public/data/restaurants.geojson"

def extract(content, key, default=None):
    """Extract a scalar value from YAML frontmatter."""
    m = re.search(rf'^{key}:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    return m.group(1).strip() if m else default

def extract_bool(content, key, default=False):
    m = re.search(rf'^{key}:\s*(true|false)\s*$', content, re.MULTILINE)
    if m: return m.group(1) == 'true'
    return default

def extract_array(content, key):
    """Extract inline array like: cuisine: ["pizza", "italian"]"""
    m = re.search(rf'^{key}:\s*\[(.+?)\]', content, re.MULTILINE)
    if m:
        return [x.strip().strip('"').strip("'") for x in m.group(1).split(',')]
    return []

features = []
files = sorted(os.listdir(restaurants_dir))

for fname in files:
    if not fname.endswith('.md'):
        continue
    
    fpath = os.path.join(restaurants_dir, fname)
    with open(fpath) as f:
        content = f.read()
    
    # Only published + active
    published = extract_bool(content, 'published', False)
    status = extract(content, 'status', 'active')
    if not published or status == 'closed':
        continue
    
    lat = extract(content, 'lat')
    lng = extract(content, 'lng')
    if not lat or not lng:
        continue
    
    slug = fname.replace('.md', '')
    
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(lng), float(lat)]
        },
        "properties": {
            "slug": slug,
            "name": extract(content, 'name', slug),
            "one_liner": extract(content, 'one_liner', ''),
            "price": extract(content, 'price', '$'),
            "neighborhood": extract(content, 'neighborhood', ''),
            "ownership": extract(content, 'ownership', 'independent'),
            "byob": extract_bool(content, 'byob', False),
            "cuisine": extract_array(content, 'cuisine'),
            "visit_status": extract(content, 'visit_status', 'fact-shell'),
            "address": extract(content, 'address', ''),
        }
    }
    features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open(output_path, 'w') as f:
    json.dump(geojson, f, indent=2)

print(f"Written {len(features)} restaurants to {output_path}")
