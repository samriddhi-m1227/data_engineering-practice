from pathlib import Path
import csv
import json
from typing import Any, Dict, List


def main():
    #first query the dir (includes sub-dir) to find all json files:
    #using pathlib:
    for json_path in Path("data").rglob("*.json"): #gives me a list of filenames
        with json_path.open('r', encoding='utf-8') as f:
            obj=json.load(f) #reads contents and stores it
        
        flat_obj=flatten(obj) #after json contents are flattend

        #convert to csv: Use csv.DictWriter since keys turn into columns and values turn into row vals 
        out_path=json_path.with_suffix(".csv") # writed back everyhting to same filepath just a csv instead
        with out_path.open('w', newline="", encoding="utf-8") as out:
            writer=csv.DictWriter(out, fieldnames=flat_obj.keys()) #keys are colnames
            writer.writeheader() #writes the first row (header/colnames)
            writer.writerow(flat_obj) #writes one data row to csv (because these are single record json files



def flatten(obj: Any, parent_key: str = "", sep: str = "_") -> Dict[str, Any]:
    """
    Flatten nested dict/list JSON into a single dict.

    - Dicts become joined keys: parent_child_grandchild
    - GeoJSON Point objects become: <base>_type, <base>_lon, <base>_lat
    - Primitive lists become pipe-joined strings
    - List of dicts becomes indexed keys
    """
    flat: Dict[str, Any] = {}

    # Special case: GeoJSON Point
    if isinstance(obj, dict) and obj.get("type") == "Point" and isinstance(obj.get("coordinates"), list):
        coords: List[Any] = obj.get("coordinates", [])
        lon = coords[0] if len(coords) > 0 else None
        lat = coords[1] if len(coords) > 1 else None

        base = parent_key if parent_key else "geolocation"
        flat[f"{base}{sep}type"] = "Point"
        flat[f"{base}{sep}lon"] = lon
        flat[f"{base}{sep}lat"] = lat
        return flat

    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
            flat.update(flatten(v, new_key, sep=sep))
        return flat

    if isinstance(obj, list):
        # list of dicts -> index them
        if all(isinstance(x, dict) for x in obj):
            for i, v in enumerate(obj):
                idx_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
                flat.update(flatten(v, idx_key, sep=sep))
            return flat

        # primitive list -> join
        flat[parent_key or "value"] = "|".join("" if x is None else str(x) for x in obj)
        return flat

    # primitive
    flat[parent_key or "value"] = obj
    return flat

if __name__ == "__main__":
    main()
