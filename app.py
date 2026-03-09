from flask import Flask, render_template, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)

# Grammar correction model
model_name = "vennify/t5-base-grammar-correction"

print("Loading Model...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

print("Model Loaded")


def correct_grammar(text):

    # Better prompt for correction
    input_text = "fix grammar: " + text

    input_ids = tokenizer.encode(
        input_text,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

    outputs = model.generate(
        input_ids,
        max_length=512,
        num_beams=7,
        early_stopping=True
    )

    corrected = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Ensure first letter capital
    corrected = corrected.capitalize()

    # Ensure period
    if not corrected.endswith("."):
        corrected += "."

    return corrected


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/correct", methods=["POST"])
def correct():

    data = request.get_json()

    text = data["text"]

    corrected_text = correct_grammar(text)

    return jsonify({
        "original": text,
        "corrected": corrected_text
    })


if __name__ == "__main__":
    app.run(debug=True)