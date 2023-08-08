import torch
import torch.nn as nn

import config
from music_genre_classification.models.embedding_model import TorchEmbeddingModel


class TorchEmbeddingCosineModel(TorchEmbeddingModel):
    def match_embeddings(self, embeddings: torch.Tensor) -> torch.Tensor:
        embeddings = embeddings / torch.linalg.norm(embeddings, dim=1)[:, None]
        similarities = 1.0 - (embeddings @ self.reference_embeddings.T)
        return similarities

    def update_references(self, embeddings: torch.Tensor, labels: torch.Tensor):
        unique_labels = torch.unique(labels)
        normalized_embeddings = (
            embeddings / torch.linalg.norm(embeddings, dim=1)[:, None]
        )
        for unique_label in unique_labels:
            class_embeddings = normalized_embeddings[labels == unique_label]
            mean_embedding = torch.mean(class_embeddings[:-1], dim=0, keepdims=True)
            self.reference_embeddings = torch.cat(
                [
                    self.reference_embeddings,
                    mean_embedding.to(config.device),
                ]
            )
