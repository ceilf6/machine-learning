- 3b1b videos:

Either on YouTube:
- https://www.youtube.com/watch?v=aircAruvnKk
- https://www.youtube.com/watch?v=IHZwWFHWa-w
- https://www.youtube.com/watch?v=Ilg3gGewQ5U
- https://www.youtube.com/watch?v=tIeHLnjs5U8

Or, on Bilibili:
- https://www.bilibili.com/video/BV1bx411M7Zx/
- https://www.bilibili.com/video/BV1Ux411j7ri/
- https://www.bilibili.com/video/BV16x411V7Qg (Two videos on this one url)

Or, in a playlist:
- https://space.bilibili.com/88461692/lists/1528929

- You are invited to watch those videos to understand Neural networks

- https://gitee.com/lundechen/machine_learning_2026_spring/blob/master/session-400/Task%203%20-%20Logistic%20Regression%20-%20Embedding-based%20Classifier.ipynb

- Follow the instructions here:

https://gitee.com/lundechen/machine_learning_2026_spring/blob/master/session-3/code-linear-regression-and-logistic-regression-with-pytorch.md

and do the coding on a jupyter notebook or google colab.

- https://colab.research.google.com/

or

local jupyter notebook with vscode

- https://gitee.com/lundechen/machine_learning_2026_spring/blob/master/session-400/Task%203%20-%20Discussion.md

- https://gitee.com/lundechen/machine_learning_2026_spring/blob/master/session-400/Exploring%20tiny_glove%20Word%20Vectors.md

- https://gitee.com/lundechen/machine_learning_2026_spring/blob/master/session-400/Exploring%20tiny_glove%20Word%20Vectors.ipynb

- put this json file in the folder "datasets"

- Of course, 

the much better way of doing things it to 
git clone the repo:

git clone https://gitee.com/lundechen/machine_learning_2026_spring.git

and each time for sync with the prof's repo:
git stash
git pull

- https://gitee.com/lundechen/machine_learning_2026_spring/blob/master/session-2/practice-2-ci-cd-github-actions-release.md

- As we can see for the huggingface sentiment analysis task,

with 

classifier = pipeline(
    task="sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    tokenizer="distilbert-base-uncased-finetuned-sst-2-english",
    framework="pt"
)

the model is not strong enough (88% of accuracy for the first 50 reviews, just in per with Bag Of Word + Logistic Regression). the model is kind of small.

So, i would like you guys to check out other models.

SEND YOUR FINDINGS HERE IN THE WECHAT GROUP, the model and the accuracy.

- Ideally, we should be able to find a good model with, let's say, higher than 95% of accuracy.

- After finishing the CI/CD task 

(Setting Up CI/CD with GitHub Actions and Release Functionality
Final delivery should look like: https://github.com/reveurmichael/session2-practice-ci-cd)

SEND THE URL here in the wecht group.