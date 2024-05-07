import sys; args = sys.argv[1:]
import math; import random

#This code got me to a 100/100 on the AI Grader.

def setGlobals(lstArgs):
  global weights, trainingData, layerCts, epochs
  trainingData, layerCts = readInputs(lstArgs)
  weights, epochs = getWeights(layerCts), 300000

def readInputs(args): 
  global trainingData, layerCts
  inputFile = open(args[0]).read().splitlines()
  trainingData = []
  for line in inputFile:
    parsedLine = line.split("=>")
    trainingData.append([list(map(int, item.split())) for item in parsedLine])
  inputSize, outputSize = len(trainingData[0][0]),len(trainingData[0][1])
  layerCts = [inputSize+1, 2, outputSize, outputSize]
  return trainingData, layerCts

def getWeights(layerCts):
  weights = []
  for i in range(len(layerCts)-1):
    layerLength = layerCts[i]*layerCts[i+1] if i!=len(layerCts)-2 else layerCts[i]
    weightLayer = [random.random()-0.5 for j in range(layerLength)]
    weights.append(weightLayer)
  return weights

def dotProduct(v1,v2): return sum(hadamard(v1,v2))

def hadamard(v1,v2): return [i*j for i,j in zip(v1,v2)]

def f(x): return 1/(1+math.e**(-x))

def fDeriv(x): return f(x)*(1-f(x))

def feedforward(inputs):
  nodes = [inputs]
  currentInput = inputs
  for i in range(len(weights)):
    inputSize, layer, newInput = len(currentInput), weights[i], []
    for j in range(len(layer)//inputSize):
      product = dotProduct(currentInput,layer[j*inputSize:j*inputSize+inputSize]) if i!=len(weights)-1 else hadamard(currentInput,layer[j*inputSize:j*inputSize+inputSize])
      if type(product)!=list: newInput.append(f(product))
      else: newInput = product
    currentInput = newInput
    nodes.append(currentInput)
  return nodes

def error(nodes, outputs):
  return 0.5*sum((i-j)**2 for i,j in zip(outputs, nodes[-1]))

def backprop(nodes, weights, outputs):
  partialWRTy = [[0 for node in layer] for layer in nodes]
  negGradient = [[0 for weight in layer] for layer in weights]

  
  for layer in range(len(partialWRTy)-1, 0, -1):
    if layer == len(partialWRTy)-1:
      for i in range(len(nodes[layer])):
        partialWRTy[layer][i]=outputs[i]-nodes[layer][i]
        negGradient[layer-1][i] = partialWRTy[layer][i]*nodes[layer-1][i]
    elif layer == len(partialWRTy)-2:
      for i in range(len(nodes[layer])):
        partialWRTy[layer][i] = partialWRTy[layer+1][i]*weights[layer][i]*((nodes[layer][i])*(1-(nodes[layer][i])))
    else:
      for i in range(len(nodes[layer])):
        product = dotProduct(partialWRTy[layer+1],weights[layer][i::len(nodes[layer])])
        partialWRTy[layer][i]=product*((nodes[layer][i])*(1-(nodes[layer][i])))
  for layer in range(1,len(partialWRTy)-1):
    for i in range(len(negGradient[layer-1])):
      negGradient[layer-1][i] = partialWRTy[layer][i//len(nodes[layer-1])]*nodes[layer-1][i%len(nodes[layer-1])]
  return negGradient

def modifyWeights(negGradient, alpha):
  for layer in range(len(negGradient)):
    weights[layer] = [weights[layer][weight]+alpha*negGradient[layer][weight] for weight in range(len(negGradient[layer]))]

def main():
  setGlobals(args)
  global weights
  print("Layer cts:", " ".join(str(item) for item in layerCts))
  for epoch in range(epochs):
    errorSum = 0
    for line in trainingData:
      inputs, outputs = line[0]+[1], line[1]
      nodes = feedforward(inputs)
      summDiffs = 0
      for p,i in enumerate(outputs):
        for q, u in enumerate(nodes[-1]):
            if p == q:
                summDiffs+= (i-u) *(i-u)
      summDiffs = summDiffs/2
      errorSum +=summDiffs
      #errorSum+=error(nodes,outputs)
      negGradient = backprop(nodes,weights,outputs)
      
      modifyWeights(negGradient,0.1)
    if (epoch+1)%10000==1:
      if errorSum>0.1: weights = [[random.random()-0.5 for weight in layer] for layer in weights]
    if (epoch+1)%10000==0:
      print(f"Error: {errorSum}")
      for line in weights:
        print(" ".join(str(weight) for weight in line))

if __name__=="__main__": main()

