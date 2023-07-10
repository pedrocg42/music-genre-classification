from typing import Iterable

from torch import Tensor
from torch.optim import SGD

from music_genre_classification.optimizers.torch_base_optimizer import (
    TorchBaseOptimizer,
)


class TorchSgdOptimizer(TorchBaseOptimizer):
    def __init__(
        self,
        lr: float = 0.01,
        momentum: float = 0.9,
        weight_decay: float = 2e-4,
    ):
        self.lr = lr
        self.momentum = momentum
        self.weight_decay = weight_decay
        self.optimizer = None

    def configure(self, parameters: Iterable[Tensor] | Iterable[dict]):
        self.optimizer = SGD(
            parameters,
            lr=self.lr,
            momentum=self.momentum,
            weight_decay=self.weight_decay,
        )

    def step(self):
        self.optimizer.step()
