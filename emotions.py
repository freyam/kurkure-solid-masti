from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import softmax


def getEmotion(message):
    def preprocess(text):
        new_text = []
        for t in text.split(" "):
            t = "@user" if t.startswith("<@!") else t
            t = "http" if t.startswith("http") else t
            new_text.append(t)
        processed_text = " ".join(new_text)
        return processed_text

    MODEL = "cardiffnlp/twitter-roberta-base-emotion"

    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    tokenizer = AutoTokenizer.from_pretrained(MODEL)

    # model.save_pretrained(MODEL)
    # tokenizer.save_pretrained(MODEL)

    text = preprocess(message)
    encoded_input = tokenizer(text, return_tensors="pt")
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    labels = ["anger", "joy", "optimism", "sadness"]

    results = {}
    for i in range(len(labels)):
        results[labels[i]] = scores[i]

    emotion = max(results, key=results.get)
    score = round(float(results[emotion]), 4)

    print("-----------")
    print(f"{text}\n{emotion}:{score}")

    return score, emotion
