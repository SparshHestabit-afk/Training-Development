                                                Hestabit Training Development
                                                        Week 8 - Day 3

# Model Quantisation Report

---

## 1. Introduction

Large Language Models (LLMs) have demonstrated remarkable capabilities across a wide range of natural language tasks. However, these models often require significant computational resources and memory, making them difficult to deploy in constrained environments.

One practical solution to this challenge is **model quantisation**, a technique that reduces the numerical precision of model weights while preserving most of the model’s performance. By lowering precision, it becomes possible to significantly reduce model size and improve inference speed without retraining the model.

This report presents the process of quantising a fine-tuned language model into multiple formats and evaluating the trade-offs between **memory usage, execution speed, and output quality**.

---

## 2. Objective

The main goal of this exercise was to explore how different quantisation techniques affect model performance. Specifically, the model was converted into several lower-precision formats and tested under identical conditions.

The objectives included:

* Converting the trained model into multiple quantised formats
* Measuring differences in model size and execution speed
* Evaluating the impact of quantisation on output quality
* Understanding the trade-off between performance and accuracy

---

## 3. Base Model

The model used for this experiment was:

**TinyLlama-1.1B-Chat-v1.0**

This model was previously fine-tuned using **QLoRA (Quantized Low-Rank Adaptation)** during Day-2 of the project. The fine-tuned model was then merged with the base model to create a standalone version that could be further optimised through quantisation.

---

## 4. Understanding Model Quantisation

Quantisation reduces the precision of numerical values used to represent model parameters.

Typical precision formats include:

| Format | Description                                        |
| ------ | -------------------------------------------------- |
| FP16   | 16-bit floating point precision                    |
| INT8   | 8-bit integer representation                       |
| INT4   | 4-bit compressed representation                    |
| GGUF   | Quantised format optimized for llama.cpp inference |

Lower precision formats require **less memory and computation**, but they may introduce minor reductions in accuracy.

Quantisation methods can generally be divided into:

**Post-Training Quantisation**
Applied after model training without modifying the training process.

**Quantisation-Aware Training**
Incorporates quantisation effects during training itself.

In this experiment, **post-training quantisation** was used.

---

## 5. Quantisation Workflow

The following workflow was implemented during the experiment:

```
Fine-tuned model (FP16)
        ↓
Merge LoRA adapters
        ↓
Save full-precision model
        ↓
Convert to INT8
        ↓
Convert to INT4
        ↓
Convert to GGUF format
        ↓
Run inference tests and performance comparisons
```

This pipeline allowed the same base model to be evaluated across multiple deployment formats.

---

## 6. Generated Model Formats

Four versions of the model were created:

| Model Version | Location              |
| ------------- | --------------------- |
| FP16 Model    | /quantized/model-fp16 |
| INT8 Model    | /quantized/model-int8 |
| INT4 Model    | /quantized/model-int4 |
| GGUF Model    | /quantized/model.gguf |

These models represent progressively more aggressive levels of compression.

---

## 7. Performance Evaluation

To compare the models, the same prompt was executed across all formats.

### Test Prompt

```
### Instruction: Explain in simple terms

### Input: What are Docker containers?

### Output:
```

The goal was to measure:

* execution speed
* output quality
* relative model efficiency

---

## 8. Quantisation Comparison

| Format | Approx Model Size | Inference Speed | Output Quality   |
| ------ | ----------------- | --------------- | ---------------- |
| FP16   | Largest           | Slowest         | Highest quality  |
| INT8   | Medium            | Faster          | Nearly identical |
| INT4   | Small             | Fast            | Slight reduction |
| GGUF   | Smallest          | Fastest         | Good             |

---

## 9. Observed Results

### FP16 Model

The FP16 version produced the most accurate and detailed responses. Since the model weights retain full floating-point precision, no information loss occurs during inference.

However, this format consumes the most memory and requires more computational resources.

---

### INT8 Quantisation

The INT8 model significantly reduced memory usage while maintaining almost identical output quality compared to the FP16 model.

In most cases, the difference between FP16 and INT8 outputs was minimal.

This format represents a strong balance between performance and accuracy.

---

### INT4 Quantisation

The INT4 model achieved the largest compression among the transformer-based formats tested. While inference became faster and memory usage decreased further, minor changes in output wording and reasoning depth were occasionally observed.

Despite this, the model remained usable for most tasks.

---

### GGUF Format

The GGUF model is designed for efficient inference using the **llama.cpp runtime**.

This format demonstrated the best performance in terms of inference speed and deployment efficiency. GGUF models are particularly suitable for environments where lightweight inference is required, such as edge devices or local deployments.

---

## 10. Practical Observations

Several key insights emerged from this experiment:

* Quantisation drastically reduces model size and memory consumption.
* INT8 offers the best balance between efficiency and accuracy.
* INT4 and GGUF formats provide significant compression but may slightly affect response quality.
* Quantised models enable deployment on hardware with limited resources.

These observations highlight why quantisation plays an important role in real-world LLM deployment.

---

# 11. Conclusion

This experiment demonstrated the effectiveness of model quantisation in reducing the computational footprint of large language models.

By converting the fine-tuned model into multiple formats, it was possible to evaluate the trade-offs between **model size, speed, and output quality**.

The results show that while FP16 provides the highest accuracy, lower precision formats such as INT8 and INT4 allow models to operate efficiently with minimal performance degradation.

Quantisation techniques therefore play a critical role in enabling scalable and practical deployment of modern language models.

---
