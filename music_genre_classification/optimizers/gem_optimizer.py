from typing import Iterable

from torch import Tensor
from torch.optim import AdamW

from music_genre_classification.optimizers.torch_base_optimizer import (
    TorchBaseOptimizer,
)
from torch.utils.data import DataLoader
import torch.nn as nn

from typing import Dict
import numpy as np
import quadprog
import torch
from torch import Tensor
from torch.utils.data import DataLoader
import config
from music_genre_classification.criterias.criteria import Criteria


class GemOptimizer(TorchBaseOptimizer):
    """
    Gradient Episodic Memory
    GEM projects the gradient on the current minibatch by using an external
    episodic memory of patterns from previous experiences. The gradient on
    the current minibatch is projected so that the dot product with all the
    reference gradients of previous tasks remains positive.
    This plugin does not use task identities.
    """

    def __init__(
        self,
        patterns_per_experience: int,
        memory_strength: float,
        optimizer: str = "adamw",
        lr: float = 1e-3,
        betas: tuple[float, float] = (0.9, 0.999),
        weight_decay: float = 1e-2,
    ):
        """
        :param patterns_per_experience: number of patterns per experience in the
            memory.
        :param memory_strength: offset to add to the projection direction
            in order to favour backward transfer (gamma in original paper).
        """

        super().__init__()

        self.patterns_per_experience = int(patterns_per_experience)
        self.memory_strength = memory_strength
        self.lr = lr
        self.betas = betas
        self.weight_decay = weight_decay

        self.memory_x: Dict[int, Tensor] = dict()
        self.memory_y: Dict[int, Tensor] = dict()
        self.memory_tid: Dict[int, Tensor] = dict()

        self.G: Tensor = torch.empty(0)

        if optimizer == "adamw":
            from torch.optim import AdamW

            self.optimizer = AdamW
        elif optimizer == "sgd":
            from torch.optim import SGD

            self.optimizer = SGD
        else:
            raise ValueError(f"Unknown optimizer {optimizer}")

    def configure(self, parameters: Iterable[Tensor] | Iterable[dict], **kwargs):
        self.optimizer = AdamW(
            parameters,
            lr=self.lr,
            betas=self.betas,
            weight_decay=self.weight_decay,
        )

    def before_training_iteration(
        self, model: nn.Module, criteria: Criteria, task_id: int, **kwargs
    ):
        """
        Compute gradient constraints on previous memory samples from all
        experiences.
        """

        if task_id > 0:
            G = []
            for task_id in range(task_id):
                model.train()
                self.optimizer.zero_grad()
                xref = self.memory_x[task_id].to(config.device)
                yref = self.memory_y[task_id].to(config.device)
                out = model(xref)
                loss = criteria(out, yref)
                loss.backward()

                G.append(
                    torch.cat(
                        [
                            p.grad.flatten()
                            if p.grad is not None
                            else torch.zeros(p.numel(), device=config.device)
                            for p in model.parameters()
                        ],
                        dim=0,
                    )
                )

            self.G = torch.stack(G)  # (experiences, parameters)

    @torch.no_grad()
    def after_backward(self, model: nn.Module, task_id: int, **kwargs):
        """
        Project gradient based on reference gradients and
        """

        if task_id > 0:
            g = torch.cat(
                [
                    p.grad.flatten()
                    if p.grad is not None
                    else torch.zeros(p.numel(), device=config.device)
                    for p in model.parameters()
                ],
                dim=0,
            )

            to_project = (torch.mv(self.G, g) < 0).any()
        else:
            to_project = False

        if to_project:
            v_star = self.solve_quadprog(g).to(config.device)

            num_pars = 0  # reshape v_star into the parameter matrices
            for p in model.parameters():
                curr_pars = p.numel()
                if p.grad is not None:
                    p.grad.copy_(v_star[num_pars : num_pars + curr_pars].view(p.size()))
                num_pars += curr_pars

            assert num_pars == v_star.numel(), "Error in projecting gradient"

        self.optimizer.step()

    def after_training_task(self, dataloader: DataLoader, task_id: int, **kwargs):
        """
        Save a copy of the model after each experience
        """

        self.update_memory(dataloader, task_id)

    @torch.no_grad()
    def update_memory(self, dataloader: DataLoader, task_id: int):
        """
        Update replay memory with patterns from current experience.
        """
        tot = 0
        for mbatch in dataloader:
            x, y, tid = mbatch[0], mbatch[1], mbatch[-1]
            if tot + x.size(0) <= self.patterns_per_experience:
                if task_id not in self.memory_x:
                    self.memory_x[task_id] = x.clone()
                    self.memory_y[task_id] = y.clone()
                    self.memory_tid[task_id] = tid.clone()
                else:
                    self.memory_x[task_id] = torch.cat(
                        (self.memory_x[task_id], x), dim=0
                    )
                    self.memory_y[task_id] = torch.cat(
                        (self.memory_y[task_id], y), dim=0
                    )
                    self.memory_tid[task_id] = torch.cat(
                        (self.memory_tid[task_id], tid), dim=0
                    )

            else:
                diff = self.patterns_per_experience - tot
                if task_id not in self.memory_x:
                    self.memory_x[task_id] = x[:diff].clone()
                    self.memory_y[task_id] = y[:diff].clone()
                    self.memory_tid[task_id] = tid[:diff].clone()
                else:
                    self.memory_x[task_id] = torch.cat(
                        (self.memory_x[task_id], x[:diff]), dim=0
                    )
                    self.memory_y[task_id] = torch.cat(
                        (self.memory_y[task_id], y[:diff]), dim=0
                    )
                    self.memory_tid[task_id] = torch.cat(
                        (self.memory_tid[task_id], tid[:diff]), dim=0
                    )
                break
            tot += x.size(0)

    def solve_quadprog(self, g):
        """
        Solve quadratic programming with current gradient g and
        gradients matrix on previous tasks G.
        Taken from original code:
        https://github.com/facebookresearch/GradientEpisodicMemory/blob/master/model/gem.py
        """

        memories_np = self.G.cpu().double().numpy()
        gradient_np = g.cpu().contiguous().view(-1).double().numpy()
        task_id = memories_np.shape[0]
        P = np.dot(memories_np, memories_np.transpose())
        P = 0.5 * (P + P.transpose()) + np.eye(task_id) * 1e-3
        q = np.dot(memories_np, gradient_np) * -1
        G = np.eye(task_id)
        h = np.zeros(task_id) + self.memory_strength
        v = quadprog.solve_qp(P, q, G, h)[0]
        v_star = np.dot(v, memories_np) + gradient_np

        return torch.from_numpy(v_star).float()