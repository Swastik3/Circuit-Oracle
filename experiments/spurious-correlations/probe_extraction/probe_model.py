import torch as t
import torch.nn as nn


class Probe(nn.Module):
    """Linear probe: maps activation_dim -> scalar logit."""

    def __init__(self, activation_dim: int, dtype: t.dtype = t.bfloat16):
        super().__init__()
        self.net = nn.Linear(activation_dim, 1, bias=True, dtype=dtype)

    def forward(self, x: t.Tensor) -> t.Tensor:
        return self.net(x).squeeze(-1)
