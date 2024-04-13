from transformers import AutoModelForCausalLM, AutoTokenizer
device = "cuda" # the device to load the model onto

# model_path = "/home/qilixin/code/AI_project/ancient/llm-model/baichuan-inc/Baichuan2-7B-Chat"
model_path = "/home/qilixin/code/AI_project/ancient/llm-model/qwen/Qwen1___5-7B-Chat"

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_path)

prompt = "为什么fastapi可以支持高并发？"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(device)

generated_ids = model.generate(
    model_inputs.input_ids,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(response)
