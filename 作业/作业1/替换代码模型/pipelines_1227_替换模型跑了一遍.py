# -*- coding: utf-8 -*-
"""pipelines@1227-替换模型跑了一遍.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XZzC9EdS6rxPgN4zXhyJUzVaAxEsQEku

# HF Transformers 核心模块学习：Pipelines

**Pipelines**（管道）是使用模型进行推理的一种简单易上手的方式。

这些管道是抽象了 Transformers 库中大部分复杂代码的对象，提供了一个专门用于多种任务的简单API，包括**命名实体识别、掩码语言建模、情感分析、特征提取和问答**等。


| Modality                    | Task                         | Description                                                | Pipeline API                                  |
| --------------------------- | ---------------------------- | ---------------------------------------------------------- | --------------------------------------------- |
| Audio                       | Audio classification         | 为音频文件分配一个标签                                     | pipeline(task=“audio-classification”)         |
|                             | Automatic speech recognition | 将音频文件中的语音提取为文本                               | pipeline(task=“automatic-speech-recognition”) |
| Computer vision             | Image classification         | 为图像分配一个标签                                         | pipeline(task=“image-classification”)         |
|                             | Object detection             | 预测图像中目标对象的边界框和类别                           | pipeline(task=“object-detection”)             |
|                             | Image segmentation           | 为图像中每个独立的像素分配标签（支持语义、全景和实例分割） | pipeline(task=“image-segmentation”)           |
| Natural language processing | Text classification          | 为给定的文本序列分配一个标签                               | pipeline(task=“sentiment-analysis”)           |
|                             | Token classification         | 为序列里的每个 token 分配一个标签（人, 组织, 地址等等）    | pipeline(task=“ner”)                          |
|                             | Question answering           | 通过给定的上下文和问题, 在文本中提取答案                   | pipeline(task=“question-answering”)           |
|                             | Summarization                | 为文本序列或文档生成总结                                   | pipeline(task=“summarization”)                |
|                             | Translation                  | 将文本从一种语言翻译为另一种语言                           | pipeline(task=“translation”)                  |
| Multimodal                  | Document question answering  | 根据给定的文档和问题回答一个关于该文档的问题。             | pipeline(task=“document-question-answering”)  |
|                             | Visual Question Answering    | 给定一个图像和一个问题，正确地回答有关图像的问题           | pipeline(task=“vqa”)                          |



Pipelines 已支持的完整任务列表：https://huggingface.co/docs/transformers/task_summary

## Pipeline API

**Pipeline API** 是对所有其他可用管道的包装。它可以像任何其他管道一样实例化，并且降低AI推理的学习和使用成本。

![](data/image/pipeline_func.png)

### 使用 Pipeline API 实现 Text Classification 任务


**Text classification**(文本分类)与任何模态中的分类任务一样，文本分类将一个文本序列（可以是句子级别、段落或者整篇文章）标记为预定义的类别集合之一。文本分类有许多实际应用，其中包括：

- 情感分析：根据某种极性（如积极或消极）对文本进行标记，以在政治、金融和市场等领域支持决策制定。
- 内容分类：根据某个主题对文本进行标记，以帮助组织和过滤新闻和社交媒体信息流中的信息（天气、体育、金融等）。


下面以 `Text classification` 中的情感分析任务为例，展示如何使用 Pipeline API。

模型主页：https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english
"""

from transformers import pipeline

# 仅指定任务时，使用默认模型（不推荐）
pipe = pipeline(task="text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
pipe("今儿上海可真冷啊")

pipe("今儿上海可真暖和啊")

pipe("you happy")

pipe("you sadly and happy")

pipe("you happy and  sadly sadly")

pipe2 = pipeline(task="text-classification", model="papluca/xlm-roberta-base-language-detection")
pipe2("今儿上海可真冷啊")

pipe2("今儿上海可真暖和啊")

pipe2("你好")

pipe2("你坏")

"""### 测试更多示例"""

pipe("我觉得这家店蒜泥白肉的味道一般")

pipe2("我觉得这家店蒜泥白肉的味道一般")

# 默认使用的模型 distilbert-base-uncased-finetuned-sst-2-english
# 并未针对中文做太多训练，中文的文本分类任务表现未必满意
pipe("你学东西真的好快，理论课一讲就明白了")

pipe2("你学东西真的好快，理论课一讲就明白了")

# 替换为英文后，文本分类任务的表现立刻改善
pipe("You learn things really quickly. You understand the theory class as soon as it is taught.")

pipe2("You learn things really quickly. You understand the theory class as soon as it is taught.")

pipe("Today Shanghai is really cold.")

pipe2("Today Shanghai is really cold.")

"""### 批处理调用模型推理"""

text_list = [
    "Today Shanghai is really cold.",
    "I think the taste of the garlic mashed pork in this store is average.",
    "You learn things really quickly. You understand the theory class as soon as it is taught."
]

pipe(text_list)

text_list = [
    "Today Shanghai is really cold.",
    "I think the taste of the garlic mashed pork in this store is average.",
    "You learn things really quickly. You understand the theory class as soon as it is taught."
]

pipe(text_list)

pipe2(text_list)

"""## 使用 Pipeline API 调用更多预定义任务

## Natural Language Processing(NLP)

**NLP**(自然语言处理)任务是最常见的任务类型之一，因为文本是我们进行交流的一种自然方式。要将文本转换为模型可识别的格式，需要对其进行分词。这意味着将一系列文本划分为单独的单词或子词（标记），然后将这些标记转换为数字。结果就是，您可以将一系列文本表示为一系列数字，并且一旦您拥有了一系列数字，它就可以输入到模型中来解决各种NLP任务！

上面演示的 文本分类任务，以及接下来的标记、问答等任务都属于 NLP 范畴。

### Token Classification

在任何NLP任务中，文本都经过预处理，将文本序列分成单个单词或子词。这些被称为tokens。

**Token Classification**（Token分类）将每个token分配一个来自预定义类别集的标签。

两种常见的 Token 分类是：

- 命名实体识别（NER）：根据实体类别（如组织、人员、位置或日期）对token进行标记。NER在生物医学设置中特别受欢迎，可以标记基因、蛋白质和药物名称。
- 词性标注（POS）：根据其词性（如名词、动词或形容词）对标记进行标记。POS对于帮助翻译系统了解两个相同的单词如何在语法上不同很有用（作为名词的银行与作为动词的银行）。

模型主页：https://huggingface.co/dbmdz/bert-large-cased-finetuned-conll03-english
"""

from transformers import pipeline

classifier = pipeline(task="ner")

from transformers import pipeline

classifier = pipeline(task="ner")

preds = classifier("Hugging Face is a French company based in New York City.")
preds = [
    {
        "entity": pred["entity"],
        "score": round(pred["score"], 4),
        "index": pred["index"],
        "word": pred["word"],
        "start": pred["start"],
        "end": pred["end"],
    }
    for pred in preds
]
print(*preds, sep="\n")

from transformers import pipeline

classifier = pipeline(task="ner", model="KoichiYasuoka/chinese-bert-wwm-ext-upos")

preds = classifier("Hugging Face is a French company based in New York City.")
preds = [
    {
        "entity": pred["entity"],
        "score": round(pred["score"], 4),
        "index": pred["index"],
        "word": pred["word"],
        "start": pred["start"],
        "end": pred["end"],
    }
    for pred in preds
]
print(*preds, sep="\n")

"""#### 合并实体"""

classifier = pipeline(task="ner", grouped_entities=True)
classifier("Hugging Face is a French company based in New York City.")

classifier = pipeline(task="ner", model="KoichiYasuoka/chinese-bert-wwm-ext-upos", grouped_entities=True)
classifier("Hugging Face is a French company based in New York City.")

"""### Question Answering

**Question Answering**(问答)是另一个token-level的任务，返回一个问题的答案，有时带有上下文（开放领域），有时不带上下文（封闭领域）。每当我们向虚拟助手提出问题时，例如询问一家餐厅是否营业，就会发生这种情况。它还可以提供客户或技术支持，并帮助搜索引擎检索您要求的相关信息。

有两种常见的问答类型：

- 提取式：给定一个问题和一些上下文，模型必须从上下文中提取出一段文字作为答案
- 生成式：给定一个问题和一些上下文，答案是根据上下文生成的；这种方法由`Text2TextGenerationPipeline`处理，而不是下面展示的`QuestionAnsweringPipeline`

模型主页：https://huggingface.co/distilbert-base-cased-distilled-squad
"""

from transformers import pipeline

classifier = pipeline(task="ner", grouped_entities=True)
classifier("Hugging Face is a French company based in New York City.")

# 2
classifier = pipeline(task="ner", model="FlagAlpha/Llama2-Chinese-13b-Chat", grouped_entities=True)
classifier("Hugging Face is a French company based in New York City.")

# 3
classifier = pipeline(task="ner", model="FlagAlpha/Llama2-Chinese-7b-Chat", grouped_entities=True)
classifier("Hugging Face is a French company based in New York City.")

from transformers import pipeline

question_answerer = pipeline(task="question-answering")

preds = question_answerer(
    question="What is the name of the repository?",
    context="The name of the repository is huggingface/transformers",
)
print(
    f"score: {round(preds['score'], 4)}, start: {preds['start']}, end: {preds['end']}, answer: {preds['answer']}"
)

preds = question_answerer(
    question="What is the capital of China?",
    context="On 1 October 1949, CCP Chairman Mao Zedong formally proclaimed the People's Republic of China in Tiananmen Square, Beijing.",
)
print(
    f"score: {round(preds['score'], 4)}, start: {preds['start']}, end: {preds['end']}, answer: {preds['answer']}"
)





"""### Summarization

**Summarization**(文本摘要）从较长的文本中创建一个较短的版本，同时尽可能保留原始文档的大部分含义。摘要是一个序列到序列的任务；它输出比输入更短的文本序列。有许多长篇文档可以进行摘要，以帮助读者快速了解主要要点。法案、法律和财务文件、专利和科学论文等文档可以摘要，以节省读者的时间并作为阅读辅助工具。

与问答类似，摘要有两种类型：

- 提取式：从原始文本中识别和提取最重要的句子
- 生成式：从原始文本中生成目标摘要（可能包括输入文件中没有的新单词）；`SummarizationPipeline`使用生成式方法

模型主页：https://huggingface.co/t5-base
"""

from transformers import pipeline

summarizer = pipeline(task="summarization",
                      model="t5-base",
                      min_length=8,
                      max_length=32,
)

summarizer(
    """
    In this work, we presented the Transformer, the first sequence transduction model based entirely on attention,
    replacing the recurrent layers most commonly used in encoder-decoder architectures with multi-headed self-attention.
    For translation tasks, the Transformer can be trained significantly faster than architectures based on recurrent or convolutional layers.
    On both WMT 2014 English-to-German and WMT 2014 English-to-French translation tasks, we achieve a new state of the art.
    In the former task our best model outperforms even all previously reported ensembles.
    """
)

summarizer(
    '''
    Large language models (LLM) are very large deep learning models that are pre-trained on vast amounts of data.
    The underlying transformer is a set of neural networks that consist of an encoder and a decoder with self-attention capabilities.
    The encoder and decoder extract meanings from a sequence of text and understand the relationships between words and phrases in it.
    Transformer LLMs are capable of unsupervised training, although a more precise explanation is that transformers perform self-learning.
    It is through this process that transformers learn to understand basic grammar, languages, and knowledge.
    Unlike earlier recurrent neural networks (RNN) that sequentially process inputs, transformers process entire sequences in parallel.
    This allows the data scientists to use GPUs for training transformer-based LLMs, significantly reducing the training time.
    '''
)

"""## Audio 音频处理任务

音频和语音处理任务与其他模态略有不同，主要是因为音频作为输入是一个连续的信号。与文本不同，原始音频波形不能像句子可以被划分为单词那样被整齐地分割成离散的块。为了解决这个问题，通常在固定的时间间隔内对原始音频信号进行采样。如果在每个时间间隔内采样更多样本，采样率就会更高，音频更接近原始音频源。

以前的方法是预处理音频以从中提取有用的特征。现在更常见的做法是直接将原始音频波形输入到特征编码器中，以提取音频表示。这样可以简化预处理步骤，并允许模型学习最重要的特征。

### Audio classification

**Audio classification**(音频分类)是一项将音频数据从预定义的类别集合中进行标记的任务。这是一个广泛的类别，具有许多具体的应用，其中一些包括：

- 声学场景分类：使用场景标签（“办公室”、“海滩”、“体育场”）对音频进行标记。
- 声学事件检测：使用声音事件标签（“汽车喇叭声”、“鲸鱼叫声”、“玻璃破碎声”）对音频进行标记。
- 标记：对包含多种声音的音频进行标记（鸟鸣、会议中的说话人识别）。
- 音乐分类：使用流派标签（“金属”、“嘻哈”、“乡村”）对音乐进行标记。

模型主页：https://huggingface.co/superb/hubert-base-superb-er

数据集主页：https://huggingface.co/datasets/superb#er

```
情感识别（ER）为每个话语预测一个情感类别。我们采用了最广泛使用的ER数据集IEMOCAP，并遵循传统的评估协议：我们删除不平衡的情感类别，只保留最后四个具有相似数量数据点的类别，并在标准分割的五折交叉验证上进行评估。评估指标是准确率（ACC）。
```

#### 前置依赖包安装

建议在命令行安装必要的音频数据处理包: ffmpeg

```shell
$apt update & apt upgrade
$apt install -y ffmpeg
$pip install ffmpeg ffmpeg-python
```
"""

!apt update & apt upgrade
!apt install -y ffmpeg
!pip install ffmpeg ffmpeg-python

from transformers import pipeline

classifier = pipeline(task="audio-classification", model="superb/hubert-base-superb-er")
preds = classifier("https://huggingface.co/datasets/Narsil/asr_dummy/resolve/main/mlk.flac")
preds = [{"score": round(pred["score"], 4), "label": pred["label"]} for pred in preds]
preds

# 使用本地的音频文件做测试
preds = classifier("data/audio/mlk.flac")
preds = [{"score": round(pred["score"], 4), "label": pred["label"]} for pred in preds]
preds



"""### Automatic speech recognition（ASR）

**Automatic speech recognition**（自动语音识别）将语音转录为文本。这是最常见的音频任务之一，部分原因是因为语音是人类交流的自然形式。如今，ASR系统嵌入在智能技术产品中，如扬声器、电话和汽车。我们可以要求虚拟助手播放音乐、设置提醒和告诉我们天气。

但是，Transformer架构帮助解决的一个关键挑战是低资源语言。通过在大量语音数据上进行预训练，仅在一个低资源语言的一小时标记语音数据上进行微调，仍然可以产生与以前在100倍更多标记数据上训练的ASR系统相比高质量的结果。

模型主页：https://huggingface.co/openai/whisper-small

下面展示使用 `OpenAI Whisper Small` 模型实现 ASR 的 Pipeline API 示例：
"""

from transformers import pipeline

# 使用 `model` 参数指定模型
transcriber = pipeline(task="automatic-speech-recognition", model="openai/whisper-small")

text = transcriber("data/audio/mlk.flac")
text



"""## Computer Vision 计算机视觉

**Computer Vision**（计算机视觉）任务中最早成功之一是使用卷积神经网络（CNN）识别邮政编码数字图像。图像由像素组成，每个像素都有一个数值。这使得将图像表示为像素值矩阵变得容易。每个像素值组合描述了图像的颜色。

计算机视觉任务可以通过以下两种通用方式解决：

- 使用卷积来学习图像的层次特征，从低级特征到高级抽象特征。
- 将图像分成块，并使用Transformer逐步学习每个图像块如何相互关联以形成图像。与CNN偏好的自底向上方法不同，这种方法有点像从一个模糊的图像开始，然后逐渐将其聚焦清晰。

### Image Classificaiton

**Image Classificaiton**(图像分类)将整个图像从预定义的类别集合中进行标记。像大多数分类任务一样，图像分类有许多实际用例，其中一些包括：

- 医疗保健：标记医学图像以检测疾病或监测患者健康状况
- 环境：标记卫星图像以监测森林砍伐、提供野外管理信息或检测野火
- 农业：标记农作物图像以监测植物健康或用于土地使用监测的卫星图像
- 生态学：标记动物或植物物种的图像以监测野生动物种群或跟踪濒危物种

模型主页：https://huggingface.co/google/vit-base-patch16-224
"""

from transformers import pipeline

classifier = pipeline(task="image-classification")

preds = classifier(
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg"
)
preds = [{"score": round(pred["score"], 4), "label": pred["label"]} for pred in preds]
print(*preds, sep="\n")

# 使用本地图片（狼猫）
preds = classifier(
    "data/image/pipeline-cat-chonk.jpeg"
)
preds = [{"score": round(pred["score"], 4), "label": pred["label"]} for pred in preds]
print(*preds, sep="\n")

# 使用本地图片（熊猫）
preds = classifier(
    "data/image/panda.jpg"
)
preds = [{"score": round(pred["score"], 4), "label": pred["label"]} for pred in preds]
print(*preds, sep="\n")



"""### Object Detection

与图像分类不同，目标检测在图像中识别多个对象以及这些对象在图像中的位置（由边界框定义）。目标检测的一些示例应用包括：

- 自动驾驶车辆：检测日常交通对象，如其他车辆、行人和红绿灯
- 遥感：灾害监测、城市规划和天气预报
- 缺陷检测：检测建筑物中的裂缝或结构损坏，以及制造业产品缺陷

模型主页：https://huggingface.co/facebook/detr-resnet-50

#### 前置依赖包安装
"""

!pip install timm

pip install timm

# 执行完上述代码如果报错需要重启jupyter notebook 核心或重启colab会话

from transformers import pipeline

detector = pipeline(task="object-detection")

preds = detector(
    "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg"
)
preds = [{"score": round(pred["score"], 4), "label": pred["label"], "box": pred["box"]} for pred in preds]
preds

preds = detector(
    "data/image/cat_dog.jpg"
)
preds = [{"score": round(pred["score"], 4), "label": pred["label"], "box": pred["box"]} for pred in preds]
preds





"""### Homework：替换以上示例中的模型，对比不同模型在相同任务上的性能表现

在 Hugging Face Models 中找到适合你的模型：https://huggingface.co/models
"""



"""# 备份"""

from google.colab import drive
drive.mount('/content/drive')

!pwd

# Commented out IPython magic to ensure Python compatibility.
# %cp -r data drive/MyDrive/AI/FineTune/homwork

!ls -l drive/MyDrive/AI/FineTune/homwork
!ls -l drive/MyDrive/AI/FineTune/homwork/data
!ls -l drive/MyDrive/AI/FineTune/homwork/data/audio
!ls -l drive/MyDrive/AI/FineTune/homwork/data/image