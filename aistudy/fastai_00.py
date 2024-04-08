from fastai.vision.all import *
from fastai.tabular.all import *
import fastai
import torch ,torch.nn, pandas as pd
from fastai.collab import *
import numpy as np
import matplotlib.pyplot as plt
# import keras.callbacks as kcb
print(torch.version.cuda)

b = np.array([6.414,-1.3,2.75,-3.14,4.31,-5.77,6.28])
a = np.array([x for x in range(len(b))])

x = np.linspace(-10,10,571)
y = np.array([np.sum(i**a*b) for i in x])

df = pd.DataFrame({'x':x.tolist(),'y':y.tolist()})
dls = TabularDataLoaders.from_df(df,y_names=['y'],cont_names=['x'])
dls.cuda()
class net(nn.Module):
  def __init__(self,n,a):
    super(net, self).__init__()
    self.a = torch.FloatTensor(a)
    self.a =self.a.cuda()
    self.l = nn.Linear(n+1,1,bias=False)
  def forward(self,y,x):
    # print('>-< '*50,self.a.device)
    x = x**self.a
    return self.l(x)

mod = net(len(a)-1,a)
mod.cuda()
leaner = fastai.learner.Learner(dls,mod,loss_func= nn.BCELoss,cbs=fastai.callback.all.ShowGraphCallback())
leaner.cuda()

leaner.fit(10,2)
leaner.fit_one_cycle(10)

leaner.fit(2000)

print(*list(map(lambda x:'%0.3f'%x,b)) ,sep='\t')

x = np.linspace(-200,200,200)
y = np.array([np.sum(i**a*b) for i in x])

leaner.cpu()
b=leaner.model.l.weight.detach().numpy()[0]
print(*list(map(lambda x:'%0.3f'%x,b)) ,sep='\t')
y2 = np.array([np.sum(i**a*b) for i in x])

plt.plot(x,y-y2,'r')
# plt.plot(x,y2,'b')
plt.show()

