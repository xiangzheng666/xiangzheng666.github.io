from math import sqrt
import torch
import torch.nn as nn


class Self_attention(nn.Module):
    # input : batch_size * seq_len * input_dim
    # q : batch_size * input_dim * dim_k
    # k : batch_size * input_dim * dim_k
    # v : batch_size * input_dim * dim_v
    def __init__(self, input_dim, dim_k, dim_v):
        super(Self_attention, self).__init__()
        # self_attention中Q与K维度一致
        self.q = nn.Linear(input_dim, dim_k)
        self.k = nn.Linear(input_dim, dim_k)
        self.v = nn.Linear(input_dim, dim_v)
        self._norm_fact = 1 / sqrt(dim_k)

    def forward(self, x):
        # 此处将input的矩阵x进行线性变换得到Q,K,V
        x=torch.tensor(x,dtype=torch.float32)
        Q = self.q(x)  # Q: batch_size * seq_len * dim_k
        K = self.k(x)  # K: batch_size * seq_len * dim_k
        V = self.v(x)  # V: batch_size * seq_len * dim_v

        # 计算 
        atten = nn.Softmax(dim=-1)(
            torch.bmm(Q, K.permute(0, 2, 1))) * self._norm_fact  # Q * K.T() # batch_size * seq_len * seq_len
        output = torch.bmm(atten, V)  # Q * K.T() * V # batch_size * seq_len * dim_v
        return output


