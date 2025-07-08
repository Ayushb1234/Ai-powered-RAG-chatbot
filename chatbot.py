from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM
import torch

model_cache = {}

def generate_response(prompt, selected_model="gpt2"):
    if selected_model not in model_cache:
        try:
            tokenizer = AutoTokenizer.from_pretrained(selected_model)
            device = 0 if torch.cuda.is_available() else -1

            if "t5" in selected_model.lower():
                model = AutoModelForSeq2SeqLM.from_pretrained(selected_model)
                pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=device)
            else:
                model = AutoModelForCausalLM.from_pretrained(selected_model)
                pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)

            model_cache[selected_model] = pipe

        except Exception as e:
            return f"❌ Failed to load model '{selected_model}': {str(e)}"

    pipe = model_cache[selected_model]

    try:
        if "t5" in selected_model.lower():
            result = pipe(prompt, max_new_tokens=150)[0]['generated_text']
        else:
            result = pipe(prompt, max_new_tokens=150, do_sample=True, temperature=0.7)[0]['generated_text']
        return result.strip()
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"
