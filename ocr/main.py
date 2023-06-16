import os
import sys
os.environ['USE_TORCH'] = '1'
import matplotlib.pyplot as plt
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
# Read the file

images = os.listdir("images")
images = list(map(lambda x: x.replace(x, "images/" + x), images))
print(images)
doc = DocumentFile.from_images(images)
# Instantiate a pretrained model
predictor = ocr_predictor(pretrained=True)
result = predictor(doc)

# JSON export
json_export = result.export()
#Processing
text = []
for page_index, page in enumerate(json_export["pages"]):
    pagelines = []
    
    # Add image path to the page
    image_path = images[page_index]
    d_image = {"imagePath": image_path}
    pagelines.append(d_image)
    
    for block in page["blocks"]:
        for line in block["lines"]:
            sentence = ""
            for word in line["words"]:
                sentence += word["value"] + " "
            d_label = {"labelText": sentence}
            pagelines.append(d_label)
    
    
    d_page = {"labels": pagelines}
    text.append(d_page)

d3 = {"pages": text}

#Writing to json
import json
with open("docgen/src/labels.json", "w") as f:
    json.dump(d3, f)