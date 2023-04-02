from fire import Fire

from evaluators import Evaluator
from trainers import Trainer
from utils import parse_experiment


def train(experiment_name: str, trainer: Trainer):
    trainer.train(experiment_name)


def evaluate(experiment_name: str, evaluator: Evaluator):
    evaluator.evaluate(experiment_name)


@parse_experiment
def execute_experiment(
    experiment_name: str,
    **experiment,
):
    train(experiment_name, **experiment["train"])
    evaluate(experiment_name, **experiment["evaluate"])


if __name__ == "__main__":
    Fire(execute_experiment)