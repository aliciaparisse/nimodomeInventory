import sys,json
sys.path.insert(0, '..')

import series

if __name__ == "__main__":
    currentInventory = series.generateInventory('testUpdatedHierarchy/series', 'testUpdatedInventory.json')

    with open('../inventories/inventory.json', 'r') as content_file:
        previousInventory = json.load(content_file,encoding="UTF-8")
    series.generateDeltaInventory('testUpdatedInventory.json', previousInventory, currentInventory)
