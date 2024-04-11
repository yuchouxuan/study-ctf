from fastai.vision.all import *
from fastai.tabular.all import *
import fastai
import torch ,torch.nn, pandas as pd
from fastai.collab import *
import numpy as np
import matplotlib.pyplot as plt
a = np.array([6,5,4,3,2,1,0])
b = np.array([1.5,3.1,7.2,1.66,0.7,1.5,0.3])

x = np.linspace(-5,5,10000)
y = np.array([np.sum(i**a*b) for i in x])

df = pd.DataFrame({'x':x.tolist(),'y':y.tolist()})
dls = TabularDataLoaders.from_df(df,y_names=['y'],cont_names=['x'])
class net(nn.Module):
  def __init__(self,n):
    super(net, self).__init__()
    self.a = torch.FloatTensor([i for i in range(0,n+1)])
    self.l = nn.Linear(n+1,1,bias=False)
  def forward(self,y,x):
    # print(x)
    x = x**self.a
    return self.l(x)

mod = net(6)
leaner = fastai.learner.Learner(dls,mod,loss_func= nn.MSELoss(),cbs=fastai.callback.all.ShowGraphCallback())
leaner.fit(20,10)
leaner.fit_one_cycle(10)

leaner.fit(50)
print(np.round(leaner.model.l.weight.detach().numpy() ,2))
print(np.round(b[::-1],3))
print(np.round(leaner.model.l.weight.detach().numpy()-b[::-1],3))
print(np.round((leaner.model.l.weight.detach().numpy()-b[::-1])/b[::-1],3))
