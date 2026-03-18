# Neural Network — MNIST Digit Classifier

A neural network built from scratch in pure Python (no ML frameworks) to classify handwritten digits from the MNIST dataset.

## How it works

- **Architecture:** 785 → 40 → 25 → 10 → 10 neurons (sigmoid activation)
- **Training:** Gradient descent with backpropagation, learning rate 0.1, 10 epochs over 60,000 samples
- Pixel values normalized to [0, 1]; labels one-hot encoded
- Saves accuracy checkpoints every 5,000 samples to `accuracies_every_5k.txt`
- Saves final weights to `mnist_weights.txt`

`mnist_keras.ipynb` compares this implementation against a Keras baseline.

## How to run

1. Place `mnist_train.csv` in `NN/mnist_data/` (standard MNIST CSV format)
2. Run the training script:
   ```bash
   python MNIST.py
   ```
3. Watch accuracy printed during training; final test accuracy printed at the end.
