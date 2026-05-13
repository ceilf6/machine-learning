# 2026-05-09 微信课程群记录总结

## 1. 神经网络学习

推荐观看 3Blue1Brown 神经网络系列视频：

**YouTube：**
- https://www.youtube.com/watch?v=aircAruvnKk
- https://www.youtube.com/watch?v=IHZwWFHWa-w
- https://www.youtube.com/watch?v=Ilg3gGewQ5U
- https://www.youtube.com/watch?v=tIeHLnjs5U8

**Bilibili：**
- https://www.bilibili.com/video/BV1bx411M7Zx/
- https://www.bilibili.com/video/BV1Ux411j7ri/
- https://www.bilibili.com/video/BV16x411V7Qg

**播放列表：**
- https://space.bilibili.com/88461692/lists/1528929

## 2. 逻辑回归作业

- Notebook：[Task 3 - Logistic Regression - Embedding-based Classifier](https://gitee.com/lundechen/machine_learning_2026_spring/blob/master/session-400/Task%203%20-%20Logistic%20Regression%20-%20Embedding-based%20Classifier.ipynb)
- 编码指导：[Linear Regression and Logistic Regression with PyTorch](https://gitee.com/lundechen/machine_learning_2026_spring/blob/master/session-3/code-linear-regression-and-logistic-regression-with-pytorch.md)
- 可在 [Google Colab](https://colab.research.google.com/) 或本地 VS Code Jupyter Notebook 中完成

## 3. GloVe 词向量探索

- 任务说明：[Exploring tiny_glove Word Vectors.md](https://gitee.com/lundechen/machine_learning_2026_spring/blob/master/session-400/Exploring%20tiny_glove%20Word%20Vectors.md)
- Notebook：[Exploring tiny_glove Word Vectors.ipynb](https://gitee.com/lundechen/machine_learning_2026_spring/blob/master/session-400/Exploring%20tiny_glove%20Word%20Vectors.ipynb)
- 讨论：[Task 3 - Discussion.md](https://gitee.com/lundechen/machine_learning_2026_spring/blob/master/session-400/Task%203%20-%20Discussion.md)
- 注意：需将 json 文件放入 `datasets` 文件夹

## 4. HuggingFace 情感分析

使用 `distilbert-base-uncased-finetuned-sst-2-english` 模型进行情感分析，前 50 条评论准确率仅约 **88%**，与 Bag of Words + Logistic Regression 持平。

**要求：** 寻找准确率高于 **95%** 的其他模型，将模型名称和准确率发送到微信群。

## 5. CI/CD 实践

- 任务：设置 GitHub Actions CI/CD 和 Release 功能
- 参考示例：https://github.com/reveurmichael/session2-practice-ci-cd
- 完成后将仓库 URL 发送到微信群

## 6. 课程仓库同步

建议 clone 课程仓库，并在每次上课前同步更新：

```bash
git clone https://gitee.com/lundechen/machine_learning_2026_spring.git

# 每次同步
git stash
git pull
```
