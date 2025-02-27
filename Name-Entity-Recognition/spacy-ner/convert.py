import json 
import argparse
import os
from pprint import pprint
from pydoc import describe
from turtle import color
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
from rich import print as rprint
from rich.progress import track

# print(data)
class ConvertToSpacy:

    def __init__(self):
        # super().__init__()
        self.train_data=[]
        self.db = DocBin() 
        self.nlp = spacy.load('en_core_web_sm') # load spacy model
        pass

    def merge(self,dir_path):
        for i in os.listdir(dir_path):
            rprint(f"[purple] {i}")
            with open(dir_path+"/"+i, 'r',encoding='utf-8') as f:
                data=json.load(f)
            self.train_data.append((data['annotations'][0][0],data['annotations'][0][1]))
        return 'file-merged succesfully'
    
    def Transform(self, file_path):
        for text, annot in track(self.train_data,description="Transforming files..."): # data in previous format
            doc = self.nlp.make_doc(text) # create doc object from text
            ents = []
            for start, end, label in annot["entities"]: # add character indexes
                span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span is None:
                print(annot)
                print("Skipping entity")
            else:
                ents.append(span)
        doc.ents = ents # label the text with the ents
        self.db.add(doc)

        self.db.to_disk(f"{file_path}/train.spacy") 
        return 'file-transformed and saved succesfully'

    def get_data(self):
        return self.train_data



if __name__ == '__main__':
    cs = ConvertToSpacy()
    cs.merge("/media/pranav/3CDEB4E6DEB4999A/Github/NLP/Name-Entity-Recognition/data")
    # print(cs.get_data())
    print(cs.Transform("/media/pranav/3CDEB4E6DEB4999A/Github/NLP/Name-Entity-Recognition/spacy-data"))