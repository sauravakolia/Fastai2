{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "minibatch.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyNaEUcx5TsAUeqQlR9m9PXv",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "accelerator": "GPU"
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/sauravakolia/Fastai2/blob/master/minibatch.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "tdZ-Twp5Zr56",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "%load_ext autoreload\n",
        "%autoreload 2\n",
        "%matplotlib inline"
      ],
      "execution_count": 1,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "smwRd6IsZ-x5",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "import torch.nn.functional as F"
      ],
      "execution_count": 2,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "MDHkTb4EaHUD",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "import operator\n",
        "\n",
        "def test(a,b,cmp,cname=None):\n",
        "    if cname is None: cname=cmp.__name__\n",
        "    assert cmp(a,b),f\"{cname}:\\n{a}\\n{b}\"\n",
        "\n",
        "def test_eq(a,b): test(a,b,operator.eq,'==')\n"
      ],
      "execution_count": 3,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "GlNdYr4Lopof",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "#export\n",
        "def near(a,b): return torch.allclose(a, b, rtol=1e-3, atol=1e-5)\n",
        "def test_near(a,b): test(a,b,near)"
      ],
      "execution_count": 4,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "cSG6XW38aI7o",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "#export\n",
        "from pathlib import Path\n",
        "from IPython.core.debugger import set_trace\n",
        "from fastai import datasets\n",
        "import pickle, gzip, math, torch, matplotlib as mpl\n",
        "import matplotlib.pyplot as plt\n",
        "from torch import tensor\n",
        "\n",
        "MNIST_URL='http://deeplearning.net/data/mnist/mnist.pkl'"
      ],
      "execution_count": 5,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "A8517SkpaKOT",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "#export\n",
        "def get_data():\n",
        "    path = datasets.download_data(MNIST_URL, ext='.gz')\n",
        "    with gzip.open(path, 'rb') as f:\n",
        "        ((x_train, y_train), (x_valid, y_valid), _) = pickle.load(f, encoding='latin-1')\n",
        "    return map(tensor, (x_train,y_train,x_valid,y_valid))\n",
        "\n",
        "def normalize(x, m, s): return (x-m)/s"
      ],
      "execution_count": 6,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "pjTQl3dpgvMj",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "mpl.rcParams['image.cmap'] = 'gray'"
      ],
      "execution_count": 7,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "om1Pmtr1aMXu",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "x_train,y_train,x_valid,y_valid = get_data()\n",
        "# train_mean,train_std = x_train.mean(),x_train.std()\n",
        "# x_train = normalize(x_train, train_mean, train_std)\n",
        "# x_valid = normalize(x_valid, train_mean, train_std)"
      ],
      "execution_count": 8,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "b-vkNf4GaOe-",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "\n",
        "n,m = x_train.shape\n",
        "c = y_train.max()+1\n",
        "nh = 50"
      ],
      "execution_count": 9,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "-RLItYcdazjk",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "from torch import nn"
      ],
      "execution_count": 10,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "qM6IF2EPaZbm",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "class Model(nn.Module):\n",
        "    def __init__(self, n_in, nh, n_out):\n",
        "        super().__init__()\n",
        "        self.layers = [nn.Linear(n_in,nh), nn.ReLU(), nn.Linear(nh,n_out)]\n",
        "        \n",
        "    def __call__(self, x):\n",
        "        for l in self.layers: x = l(x)\n",
        "        return x"
      ],
      "execution_count": 11,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "v5MIVEkpaxfC",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "model = Model(m, nh, 10)"
      ],
      "execution_count": 12,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "RFWIS0hKbADu",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "pred=model(x_train)"
      ],
      "execution_count": 13,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "zzb1bO9FbdMq",
        "colab_type": "text"
      },
      "source": [
        "### Cross entropy loss"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Zcn6l_5VbZCf",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def log_softmax(x): return (x.exp()/(x.exp().sum(-1,keepdims=True))).log()"
      ],
      "execution_count": 14,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Dz6zE1-jj6Dg",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "sm_pred=log_softmax(pred)"
      ],
      "execution_count": 15,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "qy9-xk1fkDC-",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "5211a31d-be86-4f92-ed08-ee38b39a49fc"
      },
      "source": [
        "y_train[:3]"
      ],
      "execution_count": 16,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor([5, 0, 4])"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 16
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "zZN6jorUl3Dw",
        "colab_type": "text"
      },
      "source": [
        "The cross entropy loss for some target $x$ and some prediction $p(x)$ is given by:\n",
        "\n",
        "$$ -\\sum x\\, \\log p(x) $$\n",
        "\n",
        "But since our $x$s are 1-hot encoded, this can be rewritten as $-\\log(p_{i})$ where i is the index of the desired target."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "J6uUlMo5kvUq",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "f12a7294-c789-4891-8a81-1ebc622f3c9b"
      },
      "source": [
        "sm_pred[[0,1,2], [5,0,4]]"
      ],
      "execution_count": 17,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor([-2.3125, -2.1745, -2.3845], grad_fn=<IndexBackward>)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 17
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "njxcBtxqlhEL",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def nll(input,target): return -input[range(target.shape[0]),target].mean()\n",
        "\n",
        "# def nll(input, target): return -input[range(target.shape[0]), target].mean()"
      ],
      "execution_count": 18,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "WgJvWNgKmORM",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "7c096f5c-805e-4b93-feb6-866bc1a11bf0"
      },
      "source": [
        "range(y_train.shape[0])\n",
        "y_train"
      ],
      "execution_count": 19,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor([5, 0, 4,  ..., 8, 4, 8])"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 19
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "RCDUTKx9mQ9v",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "loss = nll(sm_pred, y_train)"
      ],
      "execution_count": 20,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "nNEXDlaimkfX",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "d915367a-6ac5-49ce-f807-a9b4f3821763"
      },
      "source": [
        "loss"
      ],
      "execution_count": 21,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor(2.3052, grad_fn=<NegBackward>)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 21
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "JhhZx3hkoFow",
        "colab_type": "text"
      },
      "source": [
        "Note that the formula \n",
        "\n",
        "$$\\log \\left ( \\frac{a}{b} \\right ) = \\log(a) - \\log(b)$$ \n",
        "\n",
        "gives a simplification when we compute the log softmax, which was previously defined as `(x.exp()/(x.exp().sum(-1,keepdim=True))).log()`"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "243x-wsMn-NX",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def log_softmax(x):return x-(x.exp().sum(-1,keepdims=True).log())\n",
        "# def log_softmax(x): return x - x.exp().sum(-1,keepdim=True).log()"
      ],
      "execution_count": 22,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "1lxCYuAnoWrq",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "sm_pred=log_softmax(pred)"
      ],
      "execution_count": 23,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "svJpOWwnoct-",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "test_near(nll(log_softmax(pred), y_train), loss)"
      ],
      "execution_count": 24,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "P2iv80-lpeYA",
        "colab_type": "text"
      },
      "source": [
        "Then, there is a way to compute the log of the sum of exponentials in a more stable way, called the [LogSumExp trick](https://en.wikipedia.org/wiki/LogSumExp). The idea is to use the following formula:\n",
        "\n",
        "$$\\log \\left ( \\sum_{j=1}^{n} e^{x_{j}} \\right ) = \\log \\left ( e^{a} \\sum_{j=1}^{n} e^{x_{j}-a} \\right ) = a + \\log \\left ( \\sum_{j=1}^{n} e^{x_{j}-a} \\right )$$\n",
        "\n",
        "where a is the maximum of the $x_{j}$."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "9x7TC4s8ofZC",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def logsumexp(x):\n",
        "  m = x.max(-1)[0] \n",
        "  return m+(x-m[:,None]).exp().sum(-1).log()"
      ],
      "execution_count": 25,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Lpn0iOd4qSe9",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "test_near(logsumexp(pred), pred.logsumexp(-1))"
      ],
      "execution_count": 26,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "kYG4c-w1qfBR",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def log_softmax(x): return x-x.logsumexp(-1,keepdim=True)"
      ],
      "execution_count": 27,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "w9gcXe1jraRQ",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "test_near(nll(log_softmax(pred), y_train), loss)"
      ],
      "execution_count": 28,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "hs-JA9Y-rfOm",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "test_near(F.nll_loss(F.log_softmax(pred, -1), y_train), loss)"
      ],
      "execution_count": 29,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "kOQBaqlDsWDJ",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "test_near(F.cross_entropy(pred, y_train), loss)"
      ],
      "execution_count": 30,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "iXTZaQehg5ww",
        "colab_type": "text"
      },
      "source": [
        "# Basic training loop"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "4LzP-5S_IBp7",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "loss_func=F.cross_entropy"
      ],
      "execution_count": 31,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "cwi-8uUGhBav",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "# def accuracy(out,yb):return (torch.argmax(out,dim=1) ==yb).float().mean()\n",
        "\n",
        "def accuracy(out, yb): return (torch.argmax(out, dim=1)==yb).float().mean()"
      ],
      "execution_count": 32,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Iby4CxP6hZ7u",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "bs=64\n",
        "xb=x_train[0:bs]\n",
        "preds=model(xb)"
      ],
      "execution_count": 40,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "0Xp9zeJBhwHm",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 54
        },
        "outputId": "7b61f490-efc7-4d65-94d1-98d00f03607d"
      },
      "source": [
        "preds[0]"
      ],
      "execution_count": 41,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor([ 2.6797, -1.7254, -0.8668,  4.1648, -9.6635,  8.8489, -0.4412, -0.4908,\n",
              "        -1.9321, -0.7138], grad_fn=<SelectBackward>)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 41
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "cQXmM059hyiO",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "62f08be5-7de8-4135-fed0-08315ae9114f"
      },
      "source": [
        "yb=y_train[0:bs]\n",
        "accuracy(preds,yb)"
      ],
      "execution_count": 42,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor(0.9375)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 42
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "lo_Just_h_IL",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "db8757e5-b778-43c8-f583-576bdac7bb0c"
      },
      "source": [
        "loss_func(preds,yb)"
      ],
      "execution_count": 43,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor(0.1478, grad_fn=<NllLossBackward>)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 43
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "6TxTi81wia5a",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "lr=0.5\n",
        "epochs=1"
      ],
      "execution_count": 44,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "HpCTNopgiiJd",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "for epoch in range(epochs):\n",
        "  for i in range(n-1//bs):\n",
        "    start_i=i*bs\n",
        "    end_i=i*bs+bs\n",
        "    xb=x_train[start_i:end_i]\n",
        "    yb=y_train[start_i:end_i]\n",
        "    preds=model(xb)\n",
        "\n",
        "    loss=loss_func(preds,yb)\n",
        "\n",
        "    loss.backward()\n",
        "    with torch.no_grad():\n",
        "      for l in model.layers:\n",
        "        if hasattr(l,'weight'):\n",
        "          l.weight-=l.weight.grad *lr\n",
        "          l.bias-=lr*l.bias.grad\n",
        "          l.weight.grad.zero_()\n",
        "          l.bias.grad.zero_()  \n",
        "    "
      ],
      "execution_count": 38,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "7vK-CoQwiv_-",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "bd6a9ace-768d-4dfd-9a01-41c203a5a420"
      },
      "source": [
        "loss_func(model(xb), yb), accuracy(model(xb), yb)"
      ],
      "execution_count": 45,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(tensor(0.1478, grad_fn=<NllLossBackward>), tensor(0.9375))"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 45
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "vdC8VxMSWgBu",
        "colab_type": "text"
      },
      "source": [
        "## Using parameters and optim"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "N2zKUupmNHQ1",
        "colab_type": "text"
      },
      "source": [
        "### Parameters"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "sOswylO5oXnW",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "class Model(nn.Module):\n",
        "  def __init__(self,n_in,nh,n_out):\n",
        "    super().__init__()\n",
        "    self.l1=nn.Linear(n_in,nh)\n",
        "    self.l2=nn.Linear(nh,n_out)\n",
        "\n",
        "  # def __call__(self,x):\n",
        "  #   return self.l2(F.ReLU(self.l1(x)))\n",
        "\n",
        "  def __call__(self, x): return self.l2(F.relu(self.l1(x)))  \n"
      ],
      "execution_count": 46,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "it3CTFn-Kr9O",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "model=Model(m,nh,10)"
      ],
      "execution_count": 47,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "JHFx7Gk0OEaO",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 92
        },
        "outputId": "213dbf8e-e1c4-45ae-f967-f517a41938a3"
      },
      "source": [
        "model"
      ],
      "execution_count": 48,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "Model(\n",
              "  (l1): Linear(in_features=784, out_features=50, bias=True)\n",
              "  (l2): Linear(in_features=50, out_features=10, bias=True)\n",
              ")"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 48
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "HhOb04r4W6fx",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "dff461e0-4db8-4a89-b72e-b73cfd152e4b"
      },
      "source": [
        "model.l1"
      ],
      "execution_count": 49,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "Linear(in_features=784, out_features=50, bias=True)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 49
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "40_Ig2M9XARI",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def fit():\n",
        "  for epoch in range(epochs):\n",
        "    for i in range((n-1)//bs +1):\n",
        "      start_i=i*bs\n",
        "      end_i=start_i+bs\n",
        "      xb=x_train[start_i:end_i]\n",
        "      yb=y_train[start_i:end_i]\n",
        "      pred=model(xb)\n",
        "      loss=loss_func(pred,yb)\n",
        "\n",
        "      loss.backward()\n",
        "      with torch.no_grad():\n",
        "        for p in model.parameters():\n",
        "          p-=lr*p.grad\n",
        "          model.zero_grad()\n",
        "\n",
        "          # if hasattr(l,'weight'):\n",
        "          #   l.weight-=lr*l.weight.grad\n",
        "          #   l.bias-=lr*l.bias.grad\n",
        "\n",
        "          #   l.weight.grad.zero_()\n",
        "          #   l.bias.grad.zero_()\n"
      ],
      "execution_count": 50,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "_8IFOcNBPRsx",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "fit()"
      ],
      "execution_count": 51,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "fEmdvL3ARI9x",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "3a8003aa-55ff-4ac4-bda9-5bb5abc7d593"
      },
      "source": [
        "loss_func(model(xb), yb), accuracy(model(xb), yb)"
      ],
      "execution_count": 52,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(tensor(0.3357, grad_fn=<NllLossBackward>), tensor(0.9219))"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 52
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "4vvBXVxWUSwv",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "class DummyModule():\n",
        "  def __init__(self,n_in,nh,n_out):\n",
        "    self._modules={}\n",
        "    self.l1=nn.Linear(n_in,nh)\n",
        "    self.l2=nn.Linear(nh,n_out)\n",
        "\n",
        "  def __setattr__(self,k,v):\n",
        "    if not k.startswith(\"_\"):self._modules[k]=v\n",
        "    super().__setattr__(k,v)\n",
        "\n",
        "  def __repr__(self):return f'{self._modules}'\n",
        "\n",
        "  def parameters(self):\n",
        "    for l in self._modules.values():\n",
        "      for p in l.parameters(): yield p"
      ],
      "execution_count": 53,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "m9fxd5BbUeM4",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "mdl=DummyModule(m,nh,10)"
      ],
      "execution_count": 54,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "WVfEBGxJWZkw",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "35347c1e-d2c7-4f00-abbc-4b505a1d924c"
      },
      "source": [
        "mdl"
      ],
      "execution_count": 55,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "{'l1': Linear(in_features=784, out_features=50, bias=True), 'l2': Linear(in_features=50, out_features=10, bias=True)}"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 55
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "O3bb5kOVWq3W",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 92
        },
        "outputId": "08f10161-4a6f-4b7c-aa7a-8f92d9721e5d"
      },
      "source": [
        "[o.shape for o in mdl.parameters()]"
      ],
      "execution_count": 56,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "[torch.Size([50, 784]),\n",
              " torch.Size([50]),\n",
              " torch.Size([10, 50]),\n",
              " torch.Size([10])]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 56
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "BHEuN6Vyb0w9",
        "colab_type": "text"
      },
      "source": [
        "### Registering modules"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "YnOiFVSAb6Gy",
        "colab_type": "text"
      },
      "source": [
        "We can use the original `layers` approach, but we have to register the modules."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "0IQRoqD0WwOa",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "layers=[nn.Linear(m,nh),nn.ReLU(),nn.Linear(nh,10)]"
      ],
      "execution_count": 57,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "JaggtiCHcC5S",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        " class Model(nn.Module):\n",
        "  def __init__(self,layers):\n",
        "    super().__init__()\n",
        "    self.layers=layers\n",
        "    for i,l in enumerate(self.layers):self.add_module(f'layer_{i}',l)\n",
        "\n",
        "  def __call__(self,x):\n",
        "    for l in self.layers: l=l(x)  \n",
        "    return x\n"
      ],
      "execution_count": 58,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "XTVk2m2M0Fd8",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 111
        },
        "outputId": "0c5d1209-bd36-4b17-d137-435c80ab07c4"
      },
      "source": [
        "model = Model(layers)\n",
        "model"
      ],
      "execution_count": 59,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "Model(\n",
              "  (layer_0): Linear(in_features=784, out_features=50, bias=True)\n",
              "  (layer_1): ReLU()\n",
              "  (layer_2): Linear(in_features=50, out_features=10, bias=True)\n",
              ")"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 59
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "kUAePL5n05b3",
        "colab_type": "text"
      },
      "source": [
        "### nn.ModuleList"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "T9CkxYxk0J8Z",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "class SequentialModel(nn.Module):\n",
        "  def __init__(self,layers):\n",
        "    super().__init__()\n",
        "    self.layers=nn.ModuleList(layers)\n",
        "\n",
        "  def __call__(self,x):\n",
        "    for l in self.layers:  x=l(x)\n",
        "    return x  \n"
      ],
      "execution_count": 60,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "JktDkqCw2Teo",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "model=SequentialModel(layers)"
      ],
      "execution_count": 61,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "pU9AJCf42ecW",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 148
        },
        "outputId": "f18fcb67-cf0f-45f6-b3e4-a6be4a0a2917"
      },
      "source": [
        "model"
      ],
      "execution_count": 62,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "SequentialModel(\n",
              "  (layers): ModuleList(\n",
              "    (0): Linear(in_features=784, out_features=50, bias=True)\n",
              "    (1): ReLU()\n",
              "    (2): Linear(in_features=50, out_features=10, bias=True)\n",
              "  )\n",
              ")"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 62
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "EMb8wHfq2feJ",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "9fd3145a-582f-4cfe-e821-67630f2ccc02"
      },
      "source": [
        "fit()\n",
        "loss_func(model(xb), yb), accuracy(model(xb), yb)"
      ],
      "execution_count": 63,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(tensor(0.3375, grad_fn=<NllLossBackward>), tensor(0.9375))"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 63
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "0ZGAAyly3JFq",
        "colab_type": "text"
      },
      "source": [
        "### nn.Sequential"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "PkAKSVnB3Cx5",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "model=nn.Sequential(nn.Linear(m,nh),nn.ReLU(),nn.Linear(nh,10))"
      ],
      "execution_count": 64,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "z3ytXQQu3aJs",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "70ad5315-4443-4918-d00f-9e6fdbe8958c"
      },
      "source": [
        "fit()\n",
        "loss_func(model(xb), yb), accuracy(model(xb), yb)"
      ],
      "execution_count": 65,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(tensor(0.3279, grad_fn=<NllLossBackward>), tensor(0.9375))"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 65
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "dTMnZVvL3bpf",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "nn.Sequential??"
      ],
      "execution_count": 66,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Wfwwo_753hTF",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 111
        },
        "outputId": "57d8ae9d-86c4-4828-c5b6-bd28e1354cab"
      },
      "source": [
        "model"
      ],
      "execution_count": 67,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "Sequential(\n",
              "  (0): Linear(in_features=784, out_features=50, bias=True)\n",
              "  (1): ReLU()\n",
              "  (2): Linear(in_features=50, out_features=10, bias=True)\n",
              ")"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 67
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "TfVsMUFMD9TM",
        "colab_type": "text"
      },
      "source": [
        "### optim"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "eKrQGVwMEGeC",
        "colab_type": "text"
      },
      "source": [
        "Let's replace our previous manually coded optimization step:\n",
        "\n",
        "```python\n",
        "with torch.no_grad():\n",
        "    for p in model.parameters(): p -= p.grad * lr\n",
        "    model.zero_grad()\n",
        "```\n",
        "\n",
        "and instead use just:\n",
        "\n",
        "```python\n",
        "opt.step()\n",
        "opt.zero_grad()\n",
        "```"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "N33qpuXr3pBb",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "class optimizer():\n",
        "  def __init__(self,params,lr=0.5):\n",
        "    self.params,self.lr=list(params),lr\n",
        "\n",
        "  def one_step(self):  \n",
        "    with torch.no_grad():\n",
        "      for p in self.params:\n",
        "        p-=self.lr*p.grad\n",
        "\n",
        "  def zero_grad(self):\n",
        "    for p in self.params:\n",
        "      p.grad.data.zero_()        \n"
      ],
      "execution_count": 68,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "1uMUHVJxFlIy",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "model=nn.Sequential(nn.Linear(m,nh),nn.ReLU(),nn.Linear(nh,10))"
      ],
      "execution_count": 69,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "xbYZ2LSOFJOG",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "opt=optimizer(model.parameters())"
      ],
      "execution_count": 70,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "sqwDsgLUFwxZ",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "for epoch in range(epochs):\n",
        "  for i in range((n-1)//bs +1):\n",
        "    start_i=i*bs\n",
        "    end_i=start_i+bs\n",
        "    xb=x_train[start_i:end_i]\n",
        "    yb=y_train[start_i:end_i]\n",
        "    preds=model(xb)\n",
        "    loss=loss_func(preds,yb)\n",
        "\n",
        "    loss.backward()\n",
        "    opt.one_step()\n",
        "    opt.zero_grad()\n"
      ],
      "execution_count": 71,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "dRko5lsUHKRg",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "122a1003-c6ce-4cc6-bd46-4ca0892ba36b"
      },
      "source": [
        "loss,acc = loss_func(model(xb), yb), accuracy(model(xb), yb)\n",
        "loss,acc"
      ],
      "execution_count": 72,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(tensor(0.0678, grad_fn=<NllLossBackward>), tensor(1.))"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 72
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "mK08UbAnIBr5",
        "colab_type": "text"
      },
      "source": [
        "PyTorch already provides this exact functionality in `optim.SGD` (it also handles stuff like momentum, which we'll look at later - except we'll be doing it in a more flexible way!)"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "dgzAu3OKHuBl",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "from torch import optim"
      ],
      "execution_count": 73,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "6eYYlcCoIG8T",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def get_model():\n",
        "  model=nn.Sequential(nn.Linear(m,nh),nn.ReLU(),nn.Linear(nh,10))\n",
        "  return model,optim.SGD(model.parameters(),lr=lr)"
      ],
      "execution_count": 74,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "LUNbr6stIhTw",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "model,opt=get_model()"
      ],
      "execution_count": 75,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Eu42INKtIprN",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "c9da592b-98cc-42fa-a6e2-5fa2f0fcfb0b"
      },
      "source": [
        "loss_func(model(xb), yb)"
      ],
      "execution_count": 76,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "tensor(2.3709, grad_fn=<NllLossBackward>)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 76
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "RiL73MnKIzKB",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "for epoch in range(epochs):\n",
        "  for i in range((n-1)//bs +1):\n",
        "    start_i=i*bs\n",
        "    end_i=start_i+bs\n",
        "    xb=x_train[start_i:end_i]\n",
        "    yb=y_train[start_i:end_i]\n",
        "    preds=model(xb)\n",
        "    loss=loss_func(preds,yb)\n",
        "\n",
        "    loss.backward()\n",
        "    opt.step()\n",
        "    opt.zero_grad()\n"
      ],
      "execution_count": 77,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "0IwqqYrJI2Yt",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "ddf75ee2-2261-4986-e87a-304916b9f454"
      },
      "source": [
        "loss,acc = loss_func(model(xb), yb), accuracy(model(xb), yb)\n",
        "loss,acc"
      ],
      "execution_count": 78,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(tensor(0.3594, grad_fn=<NllLossBackward>), tensor(0.9375))"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 78
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "ooCBp4yu_1Ni",
        "colab_type": "text"
      },
      "source": [
        "## Dataset and DataLoader"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "6wobrbAm_6QU",
        "colab_type": "text"
      },
      "source": [
        "### Dataset"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "7D2PGaLUtZoV",
        "colab_type": "text"
      },
      "source": [
        "It's clunky to iterate through minibatches of x and y values separately:\n",
        "\n",
        "```python\n",
        "    xb = x_train[start_i:end_i]\n",
        "    yb = y_train[start_i:end_i]\n",
        "```\n",
        "\n",
        "Instead, let's do these two steps together, by introducing a `Dataset` class:\n",
        "\n",
        "```python\n",
        "    xb,yb = train_ds[i*bs : i*bs+bs]\n",
        "```"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "gJ7U-NlWI88_",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "class Dataset():\n",
        "  def __init__(self,x,y):\n",
        "    self.x=x\n",
        "    self.y=y\n",
        "\n",
        "  def __len__(self):\n",
        "    return len(self.x) \n",
        "\n",
        "  def __getitem__(self,i):\n",
        "    return self.x[i],self.y[i]"
      ],
      "execution_count": 79,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "NhPUlztBAdiN",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "train_ds,valid_ds=Dataset(x_train,y_train),Dataset(x_valid,y_valid)\n",
        "assert len(train_ds)==len(x_train)\n",
        "assert len(valid_ds)==len(x_valid)"
      ],
      "execution_count": 80,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "V7iI_30IA19f",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "model,opt=get_model()"
      ],
      "execution_count": 81,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "KWRYctimA_DM",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "for epoch in range(epochs):\n",
        "  for i in range((n-1)//bs +1):\n",
        "    start_i=i*bs\n",
        "    end_i=start_i+bs\n",
        "    xb,yb=train_ds[start_i:end_i]\n",
        "    \n",
        "    preds=model(xb)\n",
        "    loss=loss_func(preds,yb)\n",
        "\n",
        "    loss.backward()\n",
        "    opt.step()\n",
        "    opt.zero_grad()\n",
        "  "
      ],
      "execution_count": 82,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "mgs0-JqBBMqx",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "3b5b8f5a-2a91-4fa2-8f49-2223375cf2c6"
      },
      "source": [
        "loss,acc = loss_func(model(xb), yb), accuracy(model(xb), yb)\n",
        "assert acc>0.7\n",
        "loss,acc"
      ],
      "execution_count": 83,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(tensor(0.1457, grad_fn=<NllLossBackward>), tensor(0.9375))"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 83
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "tEIirDbTBWIq",
        "colab_type": "text"
      },
      "source": [
        "### DataLoader"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "TYiY_EPwBaFG",
        "colab_type": "text"
      },
      "source": [
        "Previously, our loop iterated over batches (xb, yb) like this:\n",
        "\n",
        "```python\n",
        "for i in range((n-1)//bs + 1):\n",
        "    xb,yb = train_ds[i*bs : i*bs+bs]\n",
        "    ...\n",
        "```\n",
        "\n",
        "Let's make our loop much cleaner, using a data loader:\n",
        "\n",
        "```python\n",
        "for xb,yb in train_dl:\n",
        "    ...\n",
        "```"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "eIdF0Z0SBSaj",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "class DataLoader():\n",
        "  def __init__(self,ds,bs):\n",
        "    self.ds=ds\n",
        "    self.bs=bs\n",
        "\n",
        "  def __iter__(self): \n",
        "    for i in range(0,len(self.ds),self.bs): yield self.ds[i:i+self.bs]"
      ],
      "execution_count": 84,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "SbwYgmbCCmSg",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "train_dl,valid_dl=DataLoader(train_ds,bs),DataLoader(valid_ds,bs)"
      ],
      "execution_count": 85,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "oJJ-VVb0D6zJ",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "xb,yb = next(iter(valid_dl))\n",
        "assert xb.shape==(bs,28*28)\n",
        "assert yb.shape==(bs,)"
      ],
      "execution_count": 86,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "eII2QEnsDKUK",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def fit():\n",
        "  for epoch in range(epochs):  \n",
        "    for xb,yb in train_dl: \n",
        "      preds=model(xb)\n",
        "      loss=loss_func(preds,yb)\n",
        "\n",
        "      loss.backward()\n",
        "      opt.step()\n",
        "      opt.zero_grad()\n",
        "  "
      ],
      "execution_count": 87,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "h5tI51HIEchF",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "fit()"
      ],
      "execution_count": 88,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "McbItKHyEnki",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "b151555b-df83-4bd2-c0e8-04a39bd42588"
      },
      "source": [
        "loss,acc = loss_func(model(xb), yb), accuracy(model(xb), yb)\n",
        "assert acc>0.7\n",
        "loss,acc"
      ],
      "execution_count": 89,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(tensor(0.0473, grad_fn=<NllLossBackward>), tensor(0.9844))"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 89
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "R_UXRyzpcBZA",
        "colab_type": "text"
      },
      "source": [
        "### Random sampling"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "onU6AgZucFyw",
        "colab_type": "text"
      },
      "source": [
        "We want our training set to be in a random order, and that order should differ each iteration. But the validation set shouldn't be randomized."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "1zpPCWhLEp8g",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "class Sampler():\n",
        "  def __init__(self,ds,bs,shuffle=False):\n",
        "    self.n=len(ds)\n",
        "    self.bs=bs\n",
        "    self.shuffle=shuffle\n",
        "  \n",
        "  def __iter__(self):\n",
        "    self.idxs=torch.randperm(self.n)if self.shuffle  else torch.arange(self.n)\n",
        "    for i in range(0,self.n,self.bs):yield self.idxs[i:i+self.bs]"
      ],
      "execution_count": 90,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "uqDlZhwteAZz",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "small_ds = Dataset(*train_ds[:10])"
      ],
      "execution_count": 91,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "ovfgN6-FeEcz",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "46da085b-9d6f-4822-8b71-7975308150ce"
      },
      "source": [
        "s = Sampler(small_ds,3,False)\n",
        "[o for o in s]"
      ],
      "execution_count": 92,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "[tensor([0, 1, 2]), tensor([3, 4, 5]), tensor([6, 7, 8]), tensor([9])]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 92
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "zbjKKdMOeGIh",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "4fc82239-aee6-4365-ad15-8868ac614a1d"
      },
      "source": [
        "s = Sampler(small_ds,3,True)\n",
        "[o for o in s]"
      ],
      "execution_count": 93,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "[tensor([9, 0, 1]), tensor([4, 5, 2]), tensor([3, 7, 8]), tensor([6])]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 93
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "gTli9qz_ePEJ",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def collate(b):\n",
        "    xs,ys = zip(*b)\n",
        "    return torch.stack(xs),torch.stack(ys)\n",
        "\n",
        "class DataLoader():\n",
        "  def __init__(self,ds,sampler,collate_fn=collate):\n",
        "    self.ds=ds\n",
        "    self.sampler=sampler\n",
        "    self.collate_fn=collate_fn\n",
        "\n",
        "  def __iter__(self):\n",
        "    for s in self.sampler: yield self.collate_fn([self.ds[i] for i in s])\n",
        "      "
      ],
      "execution_count": 94,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "AEWR9Y0XflBC",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "train_samp=Sampler(train_ds,bs,shuffle=True)\n",
        "valid_samp=Sampler(valid_ds,bs,shuffle=True)\n"
      ],
      "execution_count": 95,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "YsMU79IojwrE",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "train_dl = DataLoader(train_ds, sampler=train_samp, collate_fn=collate)\n",
        "valid_dl = DataLoader(valid_ds, sampler=valid_samp, collate_fn=collate)"
      ],
      "execution_count": 96,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "DZY_LeB2jX6l",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "fit()"
      ],
      "execution_count": 97,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "_a8J_n6rj77i",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "63ca8570-c0eb-4596-8dfa-39a31bd1beaf"
      },
      "source": [
        "loss,acc = loss_func(model(xb), yb), accuracy(model(xb), yb)\n",
        "assert acc>0.7\n",
        "loss,acc"
      ],
      "execution_count": 98,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(tensor(0.0824, grad_fn=<NllLossBackward>), tensor(0.9844))"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 98
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "2i_cq_p5lTYD",
        "colab_type": "text"
      },
      "source": [
        "### PyTorch DataLoader"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "DpT7p_4HlFyF",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "from torch.utils.data import DataLoader,RandomSampler,SequentialSampler"
      ],
      "execution_count": 99,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "t1RC-aFslrJV",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "train_dl=DataLoader(train_ds,bs,sampler=RandomSampler(train_ds),collate_fn=collate)\n",
        "valid_dl=DataLoader(valid_ds,bs,sampler=RandomSampler(valid_ds),collate_fn=collate)"
      ],
      "execution_count": 100,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "AEQjgQommC_3",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "8a55bc9a-9cf8-43c3-d6e7-b5a0c51b56c3"
      },
      "source": [
        "fit()\n",
        "loss,acc = loss_func(model(xb), yb), accuracy(model(xb), yb)\n",
        "assert acc>0.7\n",
        "loss,acc"
      ],
      "execution_count": 101,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(tensor(0.0183, grad_fn=<NllLossBackward>), tensor(1.))"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 101
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "iyTcrkYYmYvZ",
        "colab_type": "text"
      },
      "source": [
        "PyTorch's defaults work fine for most things however:"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "L6Xa2L7emGQW",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "train_dl = DataLoader(train_ds, bs, shuffle=True, drop_last=True)\n",
        "valid_dl = DataLoader(valid_ds, bs, shuffle=False)"
      ],
      "execution_count": 102,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "FM-nVAM5mcRj",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 36
        },
        "outputId": "c88719dd-3fbd-4258-8c1e-419689231a8b"
      },
      "source": [
        "fit()\n",
        "loss,acc = loss_func(model(xb), yb), accuracy(model(xb), yb)\n",
        "assert acc>0.7\n",
        "loss,acc"
      ],
      "execution_count": 103,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(tensor(0.0306, grad_fn=<NllLossBackward>), tensor(0.9844))"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 103
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "n7pxTIn8mpIV",
        "colab_type": "text"
      },
      "source": [
        "## Validation"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "7wmm_tfAmeF0",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "# def fit(epochs, model, loss_func, opt, train_dl, valid_dl):\n",
        "#    for epoch in range(epochs):\n",
        "#      model.train()  \n",
        "#      for xb,yb in train_dl: \n",
        "#       preds=model(xb)\n",
        "#       loss=loss_func(preds,yb)\n",
        "\n",
        "#       loss.backward()\n",
        "#       opt.step()\n",
        "#       opt.zero_grad()\n",
        "\n",
        "#      model.eval()\n",
        "\n",
        "#      with torch.no_grad():\n",
        "#        tot_loss,tot_acc = 0.,0.\n",
        "#        for epoch in range(epochs):\n",
        "#          for xb,yb in train_dl: \n",
        "#            preds=model(xb)\n",
        "#            tot_loss+=loss_func(preds,yb)\n",
        "#            tot_acc+=accuracy(preds,yb)\n",
        "\n",
        "#        nv=len(valid_dl)\n",
        "#        print(epoch, tot_loss/nv, tot_acc/nv)\n",
        "#     return tot_loss/nv, tot_acc/nv\n",
        "#     # for epoch in range(epochs):\n",
        "#     # return tot_loss/nv, tot_acc/nv\n"
      ],
      "execution_count": 104,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "GeXlcyuDpskJ",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def fit(epochs, model, loss_func, opt, train_dl, valid_dl):\n",
        "  for epoch in range(epochs):\n",
        "    model.train()  \n",
        "    for xb,yb in train_dl:\n",
        "      preds=model(xb)\n",
        "      loss=loss_func(preds,yb)\n",
        "\n",
        "      loss.backward()\n",
        "      opt.step()\n",
        "      opt.zero_grad()\n",
        "    model.eval()\n",
        "    with torch.no_grad():\n",
        "      tot_loss,tot_acc = 0.,0.\n",
        "      for xb,yb in valid_dl:\n",
        "        pred = model(xb)\n",
        "        tot_loss += loss_func(pred, yb)\n",
        "        tot_acc  += accuracy (pred,yb)\n",
        "    nv = len(valid_dl)\n",
        "    print(epoch, tot_loss/nv, tot_acc/nv)\n",
        "  return tot_loss/nv, tot_acc/nv"
      ],
      "execution_count": 119,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "2rnzTEs98Nfa",
        "colab_type": "text"
      },
      "source": [
        "`get_dls` returns dataloaders for the training and validation sets:"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "V7iI77PR8O7G",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def get_dls(train_ds,valid_ds,bs,**kwargs):\n",
        "  return (DataLoader(train_ds, batch_size=bs, shuffle=True, **kwargs),\n",
        "            DataLoader(valid_ds, batch_size=bs*2, **kwargs))\n"
      ],
      "execution_count": 120,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "eYsLMKjC8O5n",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 111
        },
        "outputId": "3eb16c46-7602-4054-ead1-13ca77de5ea4"
      },
      "source": [
        "train_dl,valid_dl=get_dls(train_ds,valid_ds,bs)\n",
        "model,opt=get_model()\n",
        "loss,acc=fit(5, model, loss_func, opt, train_dl, valid_dl)"
      ],
      "execution_count": 121,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "0 tensor(0.2166) tensor(0.9344)\n",
            "1 tensor(0.3381) tensor(0.9104)\n",
            "2 tensor(0.7509) tensor(0.8640)\n",
            "3 tensor(0.0995) tensor(0.9728)\n",
            "4 tensor(0.1056) tensor(0.9703)\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Qo0hVmsy8O2i",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "assert acc>0.9"
      ],
      "execution_count": 122,
      "outputs": []
    }
  ]
}