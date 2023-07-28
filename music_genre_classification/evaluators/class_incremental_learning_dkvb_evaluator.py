from loguru import logger

import config
from music_genre_classification.evaluators.class_incremental_learning_evaluator import (
    ClassIncrementalLearningEvaluator,
)
from music_genre_classification.metrics import MetricsFactory


class ClassIncrementalLearningDKVBEvaluator(ClassIncrementalLearningEvaluator):
    def configure_task(self, cross_val_id: int, task_id: int, task: list[str]):
        self.model.update_bottleneck(task_id, task)

        # Updating metrics
        for metric_config in self.metrics_config:
            metric_config["args"].update({"num_classes": self.model.num_classes})
        self.metrics = MetricsFactory.build(self.metrics_config)

        self.model_saver.configure(
            self.model,
            experiment_name=self.experiment_name,
            cross_val_id=cross_val_id,
            task_id=task_id,
            task=task,
        )
        self.model_saver.load_model()
        self.model.to(config.device)
        self.data_transform.to(config.device)
        self.experiment_tracker.configure_task(
            cross_val_id=cross_val_id,
            train_task_number=task_id,
            train_task_name=task,
        )