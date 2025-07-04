import json
import csv
from typing import Dict, List
from datetime import datetime

def export_results(results: Dict, format: str = "json") -> str:
    """Export scan results in specified format"""
    if format == "json":
        return json.dumps(results, indent=2)
    elif format == "csv":
        output = []
        flat_results = flatten_dict(results)
        fieldnames = sorted(set().union(*[d.keys() for d in flat_results]))
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat_results)
        
        return "\n".join(output)
    else:
        return str(results)

def flatten_dict(data: Dict, parent_key: str = '', sep: str = '.') -> List[Dict]:
    """Flatten nested dictionary structure"""
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep))
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f"{new_key}[{i}]", sep=sep))
                else:
                    items.append({new_key: item})
        else:
            items.append({new_key: v})
    return items
