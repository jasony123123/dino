import json
import statistics
import matplotlib.pyplot as plt

files = ["naive6200.jsonl", "human6200.jsonl", "agnews6200.jsonl",
         "mixed_dataset_20%.jsonl", "mixed_dataset_50%.jsonl"]

unique = []
avg_len = []
lengths_per_file = []
stddev = []

for file in files:
    file = open(file, 'r')
    lines = file.readlines()
    file.close()

    tokens = set()
    lengths = []

    for example in lines:

        info = json.loads(example)
        headline = info["text_a"]
        headline = headline.replace(".", "")
        headline_words = headline.replace("'", "").split()

        # unique tokens
        for word in headline_words:
            tokens.add(word.lower())

        # avg length
        lengths.append(len(headline_words))

    unique.append(len(tokens))
    avg_len.append(sum(lengths)/len(lines))
    lengths_per_file.append(lengths)
    stddev.append(statistics.stdev(lengths))



print(unique)
print(avg_len)
print(stddev)

nice_labels = ["Naive", "Human", "ag_news", "Mixed (20)", "Mixed (50)"]

plt.violinplot(lengths_per_file, showmeans=True)
plt.xticks(ticks=[1,2,3,4,5], labels=nice_labels)
plt.ylabel("Headline length")
plt.show()
