import json

def groups_to_dict(groups):
    result = {}
    
    for group in groups:
        result[group.name] = {}
        
        for item in group.items:
            result[group.name][item.name] = item.score
            
    return result

def groups_to_json(groups):
    data = groups_to_dict(groups)
    return json.dumps(data, ensure_ascii=False, indent=4)