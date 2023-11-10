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


class find:
    image_processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
    model = TFViTModel.from_pretrained("google/vit-base-patch16-224-in21k")
    es = Elasticsearch("http://localhost:9200")
    save_folder = "photos"
    def __init__(self, image_name):
        self.image_name=image_name
    

    def preprocess_img(self):
        file_name = os.path.join(self.save_folder,self.image_name)
        image = cv2.imread(file_name)
        image= cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image
    
    def embed(self):
        image=self.preprocess_img()
        inputs = self.image_processor(image, return_tensors="np")
        outputs = self.model(**inputs)
        return outputs.pooler_output.numpy().flatten().tolist()
    



    def search(self):
        embedding =self.embed()
        s_body= {
             "query": {
            "script_score": {
            "query" : {
                "bool" : {
                "filter" : {
                    "term" : {
                    "status" : "published" 
                    }
                }
                }
            },
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'embeddings') + 1.0", 
                "params": {
                "query_vector":embedding
                }
            }
            }
        },
                
        "fields": ["url"],
        "_source": False
        }

        result = self.es.search(index="testphoto", body=s_body)
        return result['hits']['hits']



if __name__ == "__main__":
    finder =find("image.jpg")
    print(finder.search())