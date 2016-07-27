import json
import os

#Custom function to get only a certain level of directory
def walkLevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def createInventory(inputDir, outputDir):
    inventory = []

    for dirpath, seriesDirNames, fileNames in walkLevel(inputDir, 0) :
        for seriesDirName in seriesDirNames:
            serie = {"name" : seriesDirName, "seasons" : []}
            for seriesPath, seasonsDirNames, seriesFileNames in walkLevel(inputDir + "/"+seriesDirName, 0):
                for seasonDirName in seasonsDirNames :
                    season = {"seasonName" : seasonDirName, "episodes" : []}
                    for seasonPath, episodeDirNames, episodeFileNames in walkLevel(inputDir+ "/"+seriesDirName+ "/"+seasonDirName, 0):
                        for episodeFileName in episodeFileNames:
                            episode = {"episodeName" : episodeFileName}
                            #We can also add some other information, to do later
                            season["episodes"].append(episode)

                    serie["seasons"].append(season)
            inventory.append(serie)

    #print data
    with open(outputDir, 'w') as outfile:
        json.dump(inventory, outfile)

    return inventory

def createDeltaInventory(inputDir, outputDir, prevInventory, currInventory):
    deltaInventory = []


    #The goal of this part is to find the series that has been added and to remove them for the currentInventory
    if len(prevInventory) != len(currInventory):
        #Here, we're  in the case where some complete serie has been added
        #We must first add completely those series to the delta before going further in the inventory

        #Here we define the number of series to add to the delta inventory
        nbOfSeriesToAdd = len(currInventory)-len(prevInventory)

        #We keep track of the shifted index for the prevIndex
        shiftedI = 0
        removeSeriesIndexes =[]
        for i in range (0, len(currInventory)):
            #We check if the name of the series is the same, or if we arrived at the end of the prevInventory
            if (shiftedI == len(prevInventory))or (currInventory[i]["name"] !=  prevInventory[shiftedI]["name"]) :
                #We add the serie that differed
                deltaInventory.append(currInventory[i])
                #We register the indexes of the series that has already been treated, in order to remove them later
                removeSeriesIndexes.append(i)
                #We take into account that one series was found
                nbOfSeriesToAdd-=1
            else :
                #If the name was the same, we also iterate through the prevInventory
                shiftedI+=1

            #If we found all the series to add, we can stop the iteration
            if nbOfSeriesToAdd ==0:
                break;

    for r in range(0,len(removeSeriesIndexes)):
        del currInventory[removeSeriesIndexes[r]]

    #We now do the exact same loop but through all of the seasons of the series
    #First we iterate through all the series
    for i in range(0, len(currInventory)):
        #First we create the serie object (containing the seasons only) for both the previous and the current one
        prevSerie = prevInventory[i]["seasons"]
        currSerie = currInventory[i]["seasons"]



        #Now, we check that the number of seasons is the same. If not, we'll do as above
        if len(prevSerie) != len(currSerie):
            #Here we're in the case where some complete season has been added
            #We must first completely add those seasons to the delta inventory before going further

            #We initiate the object that we'll add to the delta inventory
            deltaSerie = {"name" : currInventory[i]["name"], "seasons" : []}
            #Here we define the number of seasons to add to the delta
            nbOfSeasonsToAdd = len(currSerie) - len(prevSerie)

            # We keep track of the shifted index for the prevIndex
            shiftedJ = 0
            removeSeasonsIndexes = []
            #We iterate now through the seasons
            for j in range(0, len(currSerie)):
                # We check if the name of the season is the same, or if we arrived at the end of the prevSerie
                if (shiftedJ == len(prevSerie)) or (currSerie[j]["seasonName"] != prevSerie[shiftedJ]["seasonName"]):
                    # We add the season that differed
                    deltaSerie["seasons"].append(currSerie[j])
                    # We register the indexes of the season that has already been treated, in order to remove it later
                    removeSeasonsIndexes.append(j)
                    # We take into account that one series was found
                    nbOfSeasonsToAdd -= 1
                else:
                    # If the name was the same, we also iterate through the prevInventory
                    shiftedJ += 1

                # If we found all the seasons to add, we can stop the iteration
                if nbOfSeasonsToAdd == 0:
                    break;

            for r in range(0, len(removeSeasonsIndexes)):
                del currSerie[removeSeasonsIndexes[r]]

            #We add the deltaSerie to the deltaInventory
            deltaInventory.append(deltaSerie)



        # First we initiate a potential deltaSerie that can be added to the deltaInventory if not empty
        deltaSerie = {"name": currInventory[i]["name"], "seasons": []}

        #Now that we checked if any seasons were added, we can iterate through the seasons and check the episodes
        for j in range(0, len(currSerie)):
            currSeason = currSerie[j]["episodes"]
            prevSeason = prevSerie[j]["episodes"]

            #Now we check if the length of the season is the same, if not, we'll do as above
            if len(currSeason) != len(prevSeason):
                #We're now in the case where an episode had been added
                #We initiate a season object that we'll add to the delta inventory if necessary
                deltaSeason = {"seasonName" : currSerie[j]["seasonName"], "episodes" : []}

                #Here we define the number of episodes that need to be added to the delta
                nbOfEpisodesToAdd = len(currSeason) - len(prevSeason)

                # We keep track of the shifted index for the prevIndex
                shiftedK = 0

                #Now we iterate through the episodes
                for k in range(0, len(currSeason)):
                    # We check if the name of the episode is the same, or if we arrived at the end of the prevSeason
                    if (shiftedK == len(prevSeason)) or (currSeason[k]["episodeName"]
                                                      != prevSeason[shiftedK]["episodeName"]):
                        # We add the episode that differed
                        deltaSeason["episodes"].append(currSeason[k])
                        # We take into account that one episode was found
                        nbOfEpisodesToAdd -= 1
                    else:
                        shiftedK += 1

                    # If we found all the episodes to add, we can stop the iteration
                    if nbOfEpisodesToAdd == 0:
                        break;

                # We add the deltaSeason to the deltaSerie
                deltaSerie["seasons"].append(deltaSeason)

        #Before adding the serie to the deltaInventory, we must check if the deltaSerie is not empty
        if (deltaSerie["seasons"] != []):
            deltaInventory.append(deltaSerie)

    print deltaInventory


    return deltaInventory

if __name__ == "__main__":
    createInventory()