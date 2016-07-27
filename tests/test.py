import sys
sys.path.insert(0, '..')

import series

if __name__ == "__main__":
    previousInventory = series.createInventory('testHierarchy/series', '../inventories/inventory.json')
    currentInventory = series.createInventory('testUpdatedHierarchy/series', 'testUpdatedInventory.json')

    series.createDeltaInventory('testUpdatedDir/series','testUpdatedInventory.json', previousInventory, currentInventory)