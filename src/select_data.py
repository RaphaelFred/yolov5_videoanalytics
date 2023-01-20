import os
import sys
import json
import random
import shutil


def select_data(label, num_images, source, destination):
    """Copies images of a specific label type in a specific folder

    @param str label: Label name to be filtered for
    @param int num_images: Sample size of label type
    @param str source: Copy job source path. Provide upper folder (with images and labels as subfolders)
    @param str destination: Copy job destination path. Provide upper folder (with images and labels as subfolders)

    """
    # Image and json path
    images = os.listdir(source + "/images")
    jsons = os.listdir(source + "/labels")

    # Empty lkist for jsons of interest
    labelset = []
    # Loop over jsons
    for json_file in jsons:
        # Opening JSON file
        f = open(source + "/labels/" + json_file)
        # returns JSON object as a dictionary
        data = json.load(f)
        # Iterating through the json list
        for i in data:
            # Save entries that match the label of interest
            if i['ObjectClassName'] == label:
                labelset.append(json_file)
        # Closing file
        f.close()

    # Pick random sample of labelset
    choice = random.sample(labelset, int(num_images))

    # Iterate of sample and copy jsons and images to destination folder
    for jpgfile in choice:
        shutil.copy(source + "/labels/" + jpgfile, destination + "/labels/" + jpgfile)
        shutil.copy(source + "/images/" + jpgfile[:-5] + ".jpg", destination + "/images/" + jpgfile[:-5] + ".jpg")

if __name__ == "__main__":
    select_data(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])