from datasets import load_dataset
import argparse
import json
import datasets
from random import sample
import numpy as np
import random
import gzip

def dicts_to_jsonl(data_list: list, filename: str, compress: bool = False) -> None:
    """
    Method saves list of dicts into jsonl file.
    :param data: (list) list of dicts to be stored,
    :param filename: (str) path to the output file. If suffix .jsonl is not given then methods appends
        .jsonl suffix into the file.
    :param compress: (bool) should file be compressed into a gzip archive?
    """
    sjsonl = '.jsonl'
    sgz = '.gz'
    # Check filename
    if not filename.endswith(sjsonl):
        filename = filename + sjsonl
    # Save data
    
    if compress:
        filename = filename + sgz
        with gzip.open(filename, 'w') as compressed:
            for ddict in data_list:
                jout = json.dumps(ddict) + '\n'
                jout = jout.encode('utf-8')
                compressed.write(jout)
    else:
        with open(filename, 'w') as out:
            for ddict in data_list:
                jout = json.dumps(ddict) + '\n'
                out.write(jout)
def main():
    labels = {"world": 0, "sports": 1, "business": 2, "scitech": 3}
    index_to_label = {0: "world", 1: "sports", 2: "business", 3: "scitech"}
    parser = argparse.ArgumentParser()

    # Required parameters
    parser.add_argument("--input_file", type=str, required=True,
                        help="The JSONL file that contains the DINO-generated dataset to train on.")
    real_dataset = load_dataset("ag_news")
   # print('****************', real_dataset.data['train']['text' == "Robinhos Mom Comes Home Safe The kidnapped mother of Santos starlet Robinho has been returned to her family in good health, allowing the teenage forward to breath a huge sigh of relief."])
   # print('****************', real_dataset['train'][298])
    args = parser.parse_args()

    percent_of_original = 0.2

    filename = args.input_file
    headlines = []
    for headline in open(filename, 'r'):
        headlines.append(json.loads(headline))
    indices_Dino = [i for i in range(len(headlines))]
    #indices_real = [i for i in range(len(headlines))]
    num_of_examples = int(percent_of_original*len(headlines))
    subset = sample(indices_Dino, num_of_examples)
   # subset_new = sample(indices, num_of_examples)
   # print(subset)
   # print(len(subset))
   # print('dataset: ', headlines['text_a' == 'Scientists discover new life-sustaining gas'])

   # remaining_headlines = [headline for headline in headlines]
    subset.sort()
   # print('subset: ', subset)

    real_label_list = real_dataset['train']['label']
    '''
    real_headlines = {}
    for i, label in enumerate(real_headlines['label']):
        #print(label)
        real_headlines['text_a'] = real_dataset['train'][i]['text']
        real_headlines['text_b'] = "null"
        real_headlines['label'] = index_to_label[label] 
        print('checking: ', real_headlines[i]['label'])
    '''
    for i, example_index in enumerate(subset):
      #  print('**: ', example_index)

        label = headlines[example_index - i]['label']
        original_subset = [k for k in real_label_list if k == labels[label]]
        rand_idx = random.randrange(len(original_subset))

        real_headline = {}
        real_headline['text_a'] = real_dataset['train'][rand_idx]['text']
        real_headline['text_b'] = "null"
        label = real_dataset['train'][rand_idx]['label']
        real_headline['label'] = index_to_label[label] 
        headlines.pop(example_index - i)
        headlines.append(real_headline)
        real_label_list.pop(rand_idx)
        
       # original_subset = real_dataset['train']['label' == ]
       # headlines.append()
   # print(headlines)
    dicts_to_jsonl(headlines, 'newfile.jsonl')
   # out_file = open("newFile.json", "w")
  #  json.dump(headlines, out_file)
  #  out_file.close()

if __name__ == "__main__":
    main()
