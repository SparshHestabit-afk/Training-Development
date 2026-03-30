                                                Hestabit Training Development
                                                        Week 8 - Day 2
 #QLoRA Fine-Tuning Report

---

# 1. Overview

Large Language Models (LLMs) have transformed the capabilities of modern Natural Language Processing systems. These models are capable of understanding complex language patterns, reasoning about textual inputs, and generating coherent responses across a wide range of tasks.

However, adapting such models to domain-specific tasks traditionally requires **full fine-tuning**, which is computationally expensive and often impractical on limited hardware environments.

This project explores an alternative approach: **Parameter-Efficient Fine-Tuning (PEFT)**. Instead of updating every parameter in the model, PEFT techniques modify only a small portion of the model’s architecture while keeping the original weights frozen.

In this implementation, the model was fine-tuned using **QLoRA (Quantized Low-Rank Adaptation)**, which combines low-rank adaptation with quantized model loading. This technique significantly reduces memory requirements while maintaining effective training capability.

The entire pipeline — from dataset generation to model training — was implemented and executed in a cloud notebook environment using GPU acceleration.

---

# 2. Objectives

The primary objectives of this exercise were:

* To understand the architecture and working principles of modern language models.
* To implement **parameter-efficient fine-tuning techniques**.
* To prepare an instruction-style dataset suitable for model training.
* To train a language model using **LoRA adapters with quantized weights**.
* To evaluate the effectiveness of the fine-tuning workflow in a constrained environment.

This project also provided practical exposure to model training pipelines commonly used in modern machine learning workflows.

---

# 3. Model Selection

The base model selected for this project was:

**TinyLlama-1.1B-Chat-v1.0**

This model was chosen for several reasons:

* It provides strong instruction-following capabilities.
* The model size (~1.1 billion parameters) is manageable within limited GPU environments.
* It supports LoRA-based fine-tuning without requiring extensive computational resources.
* It integrates smoothly with the Hugging Face ecosystem and PEFT framework.

Using a moderately sized model allowed the focus of the project to remain on the **fine-tuning methodology rather than hardware limitations**.

---

# 4. Fine-Tuning Methodology

## 4.1 Parameter Efficient Fine-Tuning (PEFT)

Parameter Efficient Fine-Tuning focuses on updating only a **small fraction of the model parameters** instead of retraining the entire network.

Advantages include:

* reduced GPU memory usage
* faster training cycles
* improved modularity of trained models
* easier distribution of model updates

The **PEFT library** was used to implement LoRA adapters within the transformer architecture.

---

## 4.2 LoRA (Low-Rank Adaptation)

LoRA introduces trainable matrices inside the attention layers of the transformer model.

Rather than modifying the original weight matrices, LoRA learns a **low-rank representation of parameter updates**. These updates are combined with the frozen base model during inference.

Benefits of LoRA include:

* drastically reduced number of trainable parameters
* faster training times
* minimal impact on model inference performance

In this implementation, only the LoRA adapter parameters were trained while the original model weights remained frozen.

---

## 4.3 QLoRA (Quantized LoRA)

QLoRA enhances the LoRA approach by introducing **4-bit model quantization**.

Through the use of the BitsAndBytes library, the base model weights were loaded using **NF4 quantization**, reducing memory consumption while preserving training quality.

Key advantages of QLoRA include:

* substantial reduction in GPU memory usage
* ability to train models on consumer-level GPUs
* efficient training without modifying base model weights

This technique makes it possible to perform fine-tuning experiments even in limited computational environments.

---

# 5. Dataset Preparation

A custom instruction-based dataset was generated for this project. The dataset was designed to include multiple types of learning tasks so the model could learn different reasoning patterns.

The dataset consists of three main categories.

---

## 5.1 Question Answering (QA)

This category trains the model to respond to conceptual questions with clear explanations.

Example prompts include:

* What is Docker?
* Explain Kubernetes.
* What is Git used for?

These examples help the model learn general explanatory responses.

---

## 5.2 Reasoning Tasks

Reasoning samples were created to train the model to process structured logical problems.

Example:

```text
If a server processes 120 requests per minute, how many requests are processed in 10 minutes?
```

Expected reasoning output:

```text
Requests per minute = 120
Time = 10 minutes
Total requests = 1200
```

These samples encourage the model to generate step-by-step reasoning.

---

## 5.3 Information Extraction

This category focuses on converting unstructured sentences into structured data.

Example input:

```text
Emma joined Hestabit as a Human Resource Manager in 2019.
```

Expected output:

```json
{
"name": "Emma",
"company": "Hestabit",
"role": "Human Resource Manager",
"year": 2019
}
```

This task improves the model’s ability to interpret and structure information.

---

# 6. Dataset Statistics

The dataset was generated and processed through a custom pipeline.

| Dataset Type           | Samples |
| ---------------------- | ------- |
| Question Answering     | 2700    |
| Reasoning              | 2700    |
| Information Extraction | 2700    |

After dataset cleaning and validation, the data was split into training and validation sets.

| Split      | Samples |
| ---------- | ------- |
| Training   | 2740    |
| Validation | 685     |

The dataset was stored in JSONL format and structured to match instruction-based training requirements.

---

# 7. Training Configuration

The model was trained using the following configuration parameters:

| Parameter     | Value       |
| ------------- | ----------- |
| LoRA Rank (r) | 16          |
| Learning Rate | 2e-4        |
| Batch Size    | 4           |
| Epochs        | 3           |
| Quantization  | 4-bit (NF4) |
| Precision     | FP16        |

Only approximately **1% of the model parameters** were updated during training.

This demonstrates the effectiveness of parameter-efficient training methods.

---

# 8. Training Environment

The training process was executed using the following environment:

| Component | Configuration                         |
| --------- | ------------------------------------- |
| Platform  | Google Colab                          |
| GPU       | NVIDIA T4                             |
| Libraries | Transformers, PEFT, BitsAndBytes, TRL |
| Language  | Python                                |

QLoRA enabled the model to be trained successfully within the memory limits of the available GPU.

---

# 9. Training Observations

Throughout the training process, the **training loss decreased gradually across epochs**, indicating that the LoRA adapter parameters were successfully learning patterns from the dataset.

Key observations include:

* stable training behavior
* consistent loss reduction
* efficient memory usage through quantization
* minimal computational overhead

These observations confirm that the fine-tuning pipeline was implemented correctly.

---

# 10. Model Output Artifacts

After training, the LoRA adapter weights were saved separately from the base model.

Saved artifacts include:

```
/adapters/adapter_model.bin
/adapters/adapter_config.json
```

These files store the trained adapter parameters and can be combined with the base TinyLlama model to reproduce the fine-tuned behavior.

This modular design significantly reduces storage requirements when sharing trained models.

---

# 11. Project Repository Structure

The project follows a modular structure designed for clarity and reproducibility.

```
project/
│
├── data/
│   ├── train.jsonl
│   └── val.jsonl
│
├── scripts/
│   ├── generate_datasets.py
│   ├── combine_datasets.py
│   ├── split_dataset.py
│   └── data_cleaner.py
│
├── adapters/
│   ├── adapter_model.bin
│   └── adapter_config.json
│
├── notebooks/
│   └── lora_train.ipynb
│
└── TRAINING-REPORT.md
```

This structure separates datasets, scripts, model outputs, and documentation for better maintainability.

---

# 12. Practical Insights

This project provided valuable hands-on experience with modern LLM training workflows.

Key takeaways include:

* Efficient training techniques allow large models to be adapted with minimal resources.
* Quantization significantly reduces memory requirements without sacrificing training quality.
* Dataset design plays a crucial role in the effectiveness of instruction tuning.

Understanding these techniques is essential for deploying language models in real-world applications where computational resources may be limited.

---
