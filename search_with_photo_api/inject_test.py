from elasticsearch import Elasticsearch
from tqdm import tqdm
from datetime import datetime
import urllib.request
from sentence_transformers import SentenceTransformer
from PIL import Image
import os
import sys
import glob
import time
import json
import pandas as pd
import cv2
from transformers import AutoImageProcessor, TFViTModel




image_processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
model = TFViTModel.from_pretrained("google/vit-base-patch16-224-in21k")


config ={
  "mappings": {
    "properties": {
          "url": {"type": "text","index": True},
      "embeddings": {
                    "type": "dense_vector",
                    "dims":768,
                    "index": True
                },
      "status" : {
        "type" : "keyword"
      }
    }
  },
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 1
    }
}


es = Elasticsearch("http://localhost:9200")
"""es.indices.create(
    index="photoembs",
    settings=config["settings"],
    mappings=config["mappings"],
)"""

save_folder = "photos"

image_processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
model = TFViTModel.from_pretrained("google/vit-base-patch16-224-in21k")
#file_name = os.path.join(save_folder,"caat2.jpg")


save_folder = "photos"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)
f = open("emmbeddings11.txt", "r")
df=f.readlines()
ID=2865
for image_url in df[119:]:
    file_name = os.path.join(save_folder,"image.jpg")
    try:
        urllib.request.urlretrieve(image_url, file_name)

        image = cv2.imread(file_name )
        image= cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 





        print(image.shape)

        if image is not None:
            
            # Display the image (optional)

            # Display the image (optional)
            #embedding=image_embedding(image,img_model)
            #print(embedding.tolist())
            inputs = image_processor(image, return_tensors="np")
            outputs = model(**inputs)
            embedding=outputs.pooler_output.numpy().flatten().tolist()
            doc = {
                
        
                "url":image_url,
            
                "embeddings": embedding,
                "status" : "published" 
            }
            res = es.index(index="photoembs", id=ID, body=doc)
            ID+=1
         


    except Exception as e:
        print(f"Error image deprecated: {str(e)}")

print(es.count(index='photoembs'))
            


