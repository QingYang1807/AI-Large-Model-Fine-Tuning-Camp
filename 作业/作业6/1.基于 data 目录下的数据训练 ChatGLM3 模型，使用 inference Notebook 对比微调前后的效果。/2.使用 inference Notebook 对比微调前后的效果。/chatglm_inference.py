# -*- coding: utf-8 -*-
"""chatglm_inference.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XOf8hKZVehtIPsIfnfjfRxvVlpUMyyA9

# 模型推理 - 使用 QLoRA 微调后的 ChatGLM-6B
"""

!pip install bitsandbytes

!pip install accelerate

!pip install peft

!pip list

from google.colab import drive
drive.mount('/content/drive')

cp -r /content/drive/MyDrive/AI/FineTune/homework/week6-chatglm/models/THUDM ./

# Commented out IPython magic to ensure Python compatibility.
# %mv

import torch
from transformers import AutoModel, AutoTokenizer, BitsAndBytesConfig

# 模型ID或本地路径
model_name_or_path = 'THUDM/chatglm3-6b'

_compute_dtype_map = {
    'fp32': torch.float32,
    'fp16': torch.float16,
    'bf16': torch.bfloat16
}

# QLoRA 量化配置
q_config = BitsAndBytesConfig(load_in_4bit=True,
                              bnb_4bit_quant_type='nf4',
                              bnb_4bit_use_double_quant=True,
                              bnb_4bit_compute_dtype=_compute_dtype_map['bf16'])
# 加载量化后模型
base_model = AutoModel.from_pretrained(model_name_or_path,
                                  quantization_config=q_config,
                                  device_map='auto',
                                  trust_remote_code=True)

# 将模型base_model中所有参数的requires_grad属性设置为False。在PyTorch中，requires_grad属性标识了一个张量（Tensor）是否需要计算梯度。如果requires_grad=True，PyTorch会在后向传播（backpropagation）时自动计算这个张量的梯度，这对于训练阶段是必需的。然而，在模型评估或进行推理时，我们不需要计算梯度，设置requires_grad=False可以减少计算和内存开销，因为这样PyTorch就不会在这些参数上累积梯度了。
base_model.requires_grad_(False)
# 将模型设置为评估模式。在PyTorch中，模型对象通常有两种模式：训练模式（train）和评估模式（eval）。这两种模式的区别主要在于某些层的行为差异，如Dropout层和BatchNorm层。在训练模式下，Dropout层会随机丢弃一部分神经元（以减少过拟合），BatchNorm层会根据当前批次的数据更新其统计量（均值和方差）。而在评估模式下，Dropout层会停止工作（即不丢弃任何神经元），BatchNorm层会使用在训练过程中学到的统计量。因此，调用.eval()确保模型在评估或推理时表现得和训练时不同的层能正确工作。
base_model.eval()

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)

"""## 使用微调前 ChatGLM3"""

input_text = "解释下乾卦是什么？"

response, history = base_model.chat(tokenizer, query=input_text)

print(response)



response, history = base_model.chat(tokenizer, query="地水师卦是什么？", history=history)
print(response)



"""## 微调前后效果对比

#### 加载 QLoRA Adapter(Epoch=50, Overfit, handmade-dataset)
"""

print(model_name_or_path)

from peft import PeftModel, PeftConfig

epochs = 3
peft_model_path = f"models/{model_name_or_path}-epoch{epochs}"

config = PeftConfig.from_pretrained(peft_model_path)
model = PeftModel.from_pretrained(base_model, peft_model_path)

"""### 使用微调后的 ChatGLM3-6B"""

def compare_chatglm_results(query):
    base_response, base_history = base_model.chat(tokenizer, query)

    inputs = tokenizer(query, return_tensors="pt").to(0)
    ft_out = model.generate(**inputs, max_new_tokens=512)
    ft_response = tokenizer.decode(ft_out[0], skip_special_tokens=True)

    print(f"问题：{query}\n\n原始输出：\n{base_response}\n\n\nChatGLM3-6B微调后：\n{ft_response}")
    return base_response, ft_response

base_response, ft_response = compare_chatglm_results(query="解释下乾卦是什么？")

base_response, ft_response = compare_chatglm_results(query="地水师卦是什么？")

base_response, ft_response = compare_chatglm_results(query="天水讼卦")

"""#### 加载 QLoRA Adapter(Epoch=3, automade-dataset)"""

from peft import PeftModel, PeftConfig

epochs = 3
peft_model_path = f"models/{model_name_or_path}-epoch{epochs}"

config = PeftConfig.from_pretrained(peft_model_path)
model = PeftModel.from_pretrained(base_model, peft_model_path)

def compare_chatglm_results(query):
    base_response, base_history = base_model.chat(tokenizer, query)

    inputs = tokenizer(query, return_tensors="pt").to(0)
    ft_out = model.generate(**inputs, max_new_tokens=512)
    ft_response = tokenizer.decode(ft_out[0], skip_special_tokens=True)

    print(f"问题：{query}\n\n原始输出：\n{base_response}\n\n\nChatGLM3-6B微调后：\n{ft_response}")
    return base_response, ft_response

base_response, ft_response = compare_chatglm_results(query="解释下乾卦是什么？")

base_response, ft_response = compare_chatglm_results(query="地水师卦是什么？")

base_response, ft_response = compare_chatglm_results(query="周易中的讼卦是什么")



"""#### 加载 QLoRA Adapter(Epoch=3, automade-dataset(fixed))"""

from peft import PeftModel, PeftConfig

epochs = 3
timestamp = "20240118_164514"
peft_model_path = f"models/{model_name_or_path}-epoch{epochs}-{timestamp}"

config = PeftConfig.from_pretrained(peft_model_path)
model = PeftModel.from_pretrained(base_model, peft_model_path)

def compare_chatglm_results(query):
    base_response, base_history = base_model.chat(tokenizer, query)

    inputs = tokenizer(query, return_tensors="pt").to(0)
    ft_out = model.generate(**inputs, max_new_tokens=512)
    ft_response = tokenizer.decode(ft_out[0], skip_special_tokens=True)

    print(f"问题：{query}\n\n原始输出：\n{base_response}\n\n\nChatGLM3-6B(Epoch=3, automade-dataset(fixed))微调后：\n{ft_response}")
    return base_response, ft_response

base_response, ft_response = compare_chatglm_results(query="解释下乾卦是什么？")

base_response, ft_response = compare_chatglm_results(query="地水师卦是什么？")

base_response, ft_response = compare_chatglm_results(query="周易中的讼卦是什么")

