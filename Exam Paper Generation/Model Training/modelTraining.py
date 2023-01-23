import pandas as pd
from datasets import Dataset, load_dataset, load_from_disk, load_metric
from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding, TrainingArguments,Trainer
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import numpy as np

# Reading the csv file
X = pd.read_csv('table_to_train_the_model.csv')

# Converting pandas dataframe into a dataset
dataset = Dataset.from_pandas(X, preserve_index=False)
# Splitting the data into train and test
dataset = dataset.train_test_split(test_size=0.3)
raw_train_ds = dataset["train"]  # Training dataset
remaining_data = dataset["test"]

# Get the validation dataset testing dataset
dataset_2 = remaining_data.train_test_split(test_size=0.5)
raw_test_ds = dataset_2["train"]  # Testing dataset
raw_val_ds = dataset_2["test"]  # Validation dataset

print(len(raw_train_ds))
print(len(raw_test_ds))
print(len(raw_val_ds))
print(dataset['train']['RelatedLesson'][:5])

# analysing the class (no_of_occurrence) distribution in each dataset.
fig, axs = plt.subplots(1, 3, tight_layout=True)
distributions = []

axs[0].set_title("Train")
axs[1].set_title("Validation")
axs[2].set_title("Test")

train_distributions = axs[0].hist(raw_train_ds["no_of_occurance"], bins=5)
val_distributions = axs[1].hist(raw_val_ds["no_of_occurance"], bins=5)
test_distributions = axs[2].hist(raw_test_ds["no_of_occurance"], bins=5)

for distributions, ax in zip([train_distributions, val_distributions, test_distributions], axs):
    for j in range(5):
        # Display the counts on each column of the histograms
        ax.text(distributions[1][j], distributions[0][j], str(int(distributions[0][j])), weight="bold")

# Load the model and the tokenizer
BASE_MODEL = "camembert-base"
LEARNING_RATE = 2e-5
MAX_LENGTH = 256
BATCH_SIZE = 16
EPOCHS = 20

# Let's name the classes 1, 2, 3, 4, 5 like their indices
id2label = {k: k for k in range(0, 6)}
label2id = {k: k for k in range(0, 6)}

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
model = AutoModelForSequenceClassification.from_pretrained(BASE_MODEL, id2label=id2label, label2id=label2id)

# Tokenize the dataset and associate the label attribute to each dataset item
ds = {"train": raw_train_ds, "validation": raw_val_ds, "test": raw_test_ds}


def preprocess_function(examples):
    label = examples["no_of_occurance"]
    examples = tokenizer(examples["RelatedLesson"], truncation=True, padding="max_length", max_length=256)
    examples["label"] = label
    return examples


for split in ds:
    ds[split] = ds[split].map(preprocess_function, remove_columns=["RelatedLesson", "no_of_occurance"])

# Creating a function to calculate the global accuracy score
metric = load_metric("accuracy")


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


# Training the model

training_args = TrainingArguments(
    output_dir="../Model Training/camembert-fine-tuned-regression",
    learning_rate=LEARNING_RATE,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=EPOCHS,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    metric_for_best_model="accuracy",
    load_best_model_at_end=True,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=ds["train"],
    eval_dataset=ds["validation"],
    compute_metrics=compute_metrics
)

trainer.train()
