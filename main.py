#Importing the series module
import series, json

if __name__ == "__main__":
    currentInventory = series.generateInventory('/../../../video/Series', 'inventories/inventory.json')

    with open('../inventories/inventory.json', 'r') as content_file:
        previousInventory = json.load(content_file, encoding="UTF-8")
    series.generateDeltaInventory('inventories/deltaInventory.json', previousInventory, currentInventory)