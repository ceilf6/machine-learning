- 1. in our code-my_nn.py, how is the forword pass done?

2. in our code-my_nn.py, how is the BP done?

code source: 

https://gitee.com/lundechen/machine_learning_2026_spring/blob/master/session-4/code-my_nn.py


- maybe things like: 

```
def train(network, X, y):
    """Train the network on a batch of examples"""
    # Forward pass
    activations = ____YOUR_CODE_HERE__1_____(network, X)
    logits = activations____YOUR_CODE_HERE__2_____

    # Compute loss and initial gradient
    loss, grad_logits = softmax_crossentropy_with_logits(logits, y)

    # Backward pass (backpropagation)
    grad_output = grad_logits
    for i in range(len(network))[____YOUR_CODE_HERE__3_____]:  # Reversed order
        layer = network[i]
        grad_output = layer.backward(____YOUR_CODE_HERE__4_____)

    return loss
```