from copy import deepcopy

from experiments.components_clmr import (
    oracle_trainer,
    oracle_evaluator,
    continual_learning_trainer,
    continual_learning_replay_trainer,
    continual_learning_ewc_trainer,
    continual_learning_gem_trainer,
    continual_learning_icarl_trainer,
    continual_learning_l2p_trainer,
    continual_learning_l2center_trainer,
    continual_learning_evaluator_l2center,
    continual_learning_evaluator_l2p,
    evaluator,
    mert_data_transform_vocalset,
)

###############################################################
###########                SCENARIOS                ###########
###############################################################

all_tasks = [
    ["vibrato", "straight"],
    ["belt", "breathy"],
    ["lip_trill", "spoken"],
    ["inhaled", "trill"],
    ["trillo", "vocal_fry"],
]

scenario1 = [
    ["vibrato", "straight"],
    ["belt", "breathy"],
    ["lip_trill", "spoken"],
    ["inhaled", "trill"],
    ["trillo", "vocal_fry"],
]

scenario2 = [
    ["belt", "trill"],
    ["vibrato", "inhaled"],
    ["breathy", "straight"],
    ["vocal_fry", "lip_trill"],
    ["spoken", "trillo"],
]

scenario3 = [
    ["spoken", "breathy"],
    ["straight", "inhaled"],
    ["lip_trill", "trillo"],
    ["vibrato", "vocal_fry"],
    ["trill", "belt"],
]

###############################################################
###########               COMPONENTS                ###########
###############################################################

num_classes = 10

# Data sources
train_vocalsettech_data_source = {
    "name": "VocalSetTechDataSource",
    "args": {
        "split": "train",
        "chunk_length": 3,
        "is_eval": False,
    },
}
val_vocalsettech_data_source = deepcopy(train_vocalsettech_data_source)
val_vocalsettech_data_source["args"]["split"] = "val"
val_vocalsettech_data_source["args"]["is_eval"] = True
test_vocalsettech_data_source = deepcopy(train_vocalsettech_data_source)
test_vocalsettech_data_source["args"]["split"] = "test"
test_vocalsettech_data_source["args"]["is_eval"] = True

# Metrics
classification_metrics_vocalsettech = [
    {
        "name": "Accuracy",
        "args": {
            "task": "multiclass",
            "average": "micro",
            "num_classes": num_classes,
        },
    },
    {
        "name": "F1 Score",
        "args": {
            "task": "multiclass",
            "average": "macro",
            "num_classes": num_classes,
        },
    },
    {
        "name": "Precision",
        "args": {
            "task": "multiclass",
            "average": "macro",
            "num_classes": num_classes,
        },
    },
    {
        "name": "Recall",
        "args": {
            "task": "multiclass",
            "average": "macro",
            "num_classes": num_classes,
        },
    },
]


###########                TRAINERS                 ###########

oracle_train_model_vocalsettech = {
    "name": "TorchMertClassificationModel",
    "args": {"num_classes": num_classes},
}

update_trainer_vocalsettech = dict(
    train_data_source=train_vocalsettech_data_source,
    val_data_source=val_vocalsettech_data_source,
    metrics_config=classification_metrics_vocalsettech,
    train_data_transform=mert_data_transform_vocalset,
    val_data_transform=mert_data_transform_vocalset,
)

# Oracle
oracle_trainer_vocalsettech = deepcopy(oracle_trainer)
oracle_trainer_vocalsettech["args"]["train_model"] = oracle_train_model_vocalsettech
oracle_trainer_vocalsettech["args"].update(update_trainer_vocalsettech)


## Finetuning
continual_learning_trainer_vocalsettech_scenario1 = deepcopy(continual_learning_trainer)
continual_learning_trainer_vocalsettech_scenario1["args"]["tasks"] = scenario1
continual_learning_trainer_vocalsettech_scenario1["args"].update(
    update_trainer_vocalsettech
)


continual_learning_trainer_vocalsettech_scenario2 = deepcopy(
    continual_learning_trainer_vocalsettech_scenario1
)
continual_learning_trainer_vocalsettech_scenario2["args"]["tasks"] = scenario2
continual_learning_trainer_vocalsettech_scenario3 = deepcopy(
    continual_learning_trainer_vocalsettech_scenario1
)
continual_learning_trainer_vocalsettech_scenario3["args"]["tasks"] = scenario3


## Replay
continual_learning_replay_trainer_vocalsettech_scenario1 = deepcopy(
    continual_learning_replay_trainer
)
continual_learning_replay_trainer_vocalsettech_scenario1["args"]["tasks"] = scenario1
continual_learning_replay_trainer_vocalsettech_scenario1["args"].update(
    update_trainer_vocalsettech
)

continual_learning_replay_trainer_vocalsettech_scenario2 = deepcopy(
    continual_learning_replay_trainer_vocalsettech_scenario1
)
continual_learning_replay_trainer_vocalsettech_scenario2["args"]["tasks"] = scenario2
continual_learning_replay_trainer_vocalsettech_scenario3 = deepcopy(
    continual_learning_replay_trainer_vocalsettech_scenario1
)
continual_learning_replay_trainer_vocalsettech_scenario3["args"]["tasks"] = scenario3


## iCaRL
continual_learning_icarl_trainer_vocalsettech_scenario1 = deepcopy(
    continual_learning_icarl_trainer
)
continual_learning_icarl_trainer_vocalsettech_scenario1["args"]["tasks"] = scenario1
continual_learning_icarl_trainer_vocalsettech_scenario1["args"].update(
    update_trainer_vocalsettech
)


continual_learning_icarl_trainer_vocalsettech_scenario2 = deepcopy(
    continual_learning_icarl_trainer_vocalsettech_scenario1
)
continual_learning_icarl_trainer_vocalsettech_scenario2["args"]["tasks"] = scenario2
continual_learning_icarl_trainer_vocalsettech_scenario3 = deepcopy(
    continual_learning_icarl_trainer_vocalsettech_scenario1
)
continual_learning_icarl_trainer_vocalsettech_scenario3["args"]["tasks"] = scenario3


## GEM
continual_learning_gem_trainer_vocalsettech_scenario1 = deepcopy(
    continual_learning_gem_trainer
)
continual_learning_gem_trainer_vocalsettech_scenario1["args"]["tasks"] = scenario1
continual_learning_gem_trainer_vocalsettech_scenario1["args"].update(
    update_trainer_vocalsettech
)


continual_learning_gem_trainer_vocalsettech_scenario2 = deepcopy(
    continual_learning_gem_trainer_vocalsettech_scenario1
)
continual_learning_gem_trainer_vocalsettech_scenario2["args"]["tasks"] = scenario2
continual_learning_gem_trainer_vocalsettech_scenario3 = deepcopy(
    continual_learning_gem_trainer_vocalsettech_scenario1
)
continual_learning_gem_trainer_vocalsettech_scenario3["args"]["tasks"] = scenario3


## EWC
continual_learning_ewc_trainer_vocalsettech_scenario1 = deepcopy(
    continual_learning_ewc_trainer
)
continual_learning_ewc_trainer_vocalsettech_scenario1["args"]["tasks"] = scenario1
continual_learning_ewc_trainer_vocalsettech_scenario1["args"].update(
    update_trainer_vocalsettech
)


continual_learning_ewc_trainer_vocalsettech_scenario2 = deepcopy(
    continual_learning_ewc_trainer_vocalsettech_scenario1
)
continual_learning_ewc_trainer_vocalsettech_scenario2["args"]["tasks"] = scenario2
continual_learning_ewc_trainer_vocalsettech_scenario3 = deepcopy(
    continual_learning_ewc_trainer_vocalsettech_scenario1
)
continual_learning_ewc_trainer_vocalsettech_scenario3["args"]["tasks"] = scenario3


## L2P
continual_learning_l2p_trainer_vocalsettech_scenario1 = deepcopy(
    continual_learning_l2p_trainer
)
continual_learning_l2p_trainer_vocalsettech_scenario1["args"]["tasks"] = scenario1
continual_learning_l2p_trainer_vocalsettech_scenario1["args"].update(
    update_trainer_vocalsettech
)


continual_learning_l2p_trainer_vocalsettech_scenario2 = deepcopy(
    continual_learning_l2p_trainer_vocalsettech_scenario1
)
continual_learning_l2p_trainer_vocalsettech_scenario2["args"]["tasks"] = scenario2
continual_learning_l2p_trainer_vocalsettech_scenario3 = deepcopy(
    continual_learning_l2p_trainer_vocalsettech_scenario1
)
continual_learning_l2p_trainer_vocalsettech_scenario3["args"]["tasks"] = scenario3


## L2Center
continual_learning_l2center_trainer_vocalsettech_scenario1 = deepcopy(
    continual_learning_l2center_trainer
)
continual_learning_l2center_trainer_vocalsettech_scenario1["args"]["tasks"] = scenario1
continual_learning_l2center_trainer_vocalsettech_scenario1["args"].update(
    update_trainer_vocalsettech
)


continual_learning_l2center_trainer_vocalsettech_scenario2 = deepcopy(
    continual_learning_l2center_trainer_vocalsettech_scenario1
)
continual_learning_l2center_trainer_vocalsettech_scenario2["args"]["tasks"] = scenario2
continual_learning_l2center_trainer_vocalsettech_scenario3 = deepcopy(
    continual_learning_l2center_trainer_vocalsettech_scenario1
)
continual_learning_l2center_trainer_vocalsettech_scenario3["args"]["tasks"] = scenario3


###########               EVALUATORS                ###########

update_evaluator_vocalsettech = dict(
    data_source=test_vocalsettech_data_source,
    metrics_config=classification_metrics_vocalsettech,
    data_transform=mert_data_transform_vocalset,
)

# Oracle
oracle_evaluator_vocalsettech = deepcopy(oracle_evaluator)
oracle_evaluator_vocalsettech["args"]["model"] = oracle_train_model_vocalsettech
oracle_evaluator_vocalsettech["args"].update(update_evaluator_vocalsettech)

oracle_evaluator_vocalsettech_scenario1 = deepcopy(oracle_evaluator_vocalsettech)
oracle_evaluator_vocalsettech_scenario1["args"]["tasks"] = scenario1
oracle_evaluator_vocalsettech_scenario2 = deepcopy(oracle_evaluator_vocalsettech)
oracle_evaluator_vocalsettech_scenario2["args"]["tasks"] = scenario2
oracle_evaluator_vocalsettech_scenario3 = deepcopy(oracle_evaluator_vocalsettech)
oracle_evaluator_vocalsettech_scenario3["args"]["tasks"] = scenario3

## Finetuning
continual_learning_evaluator_vocalsettech_scenario1 = deepcopy(evaluator)
continual_learning_evaluator_vocalsettech_scenario1["args"]["tasks"] = scenario1
continual_learning_evaluator_vocalsettech_scenario1["args"].update(
    update_evaluator_vocalsettech
)


continual_learning_evaluator_vocalsettech_scenario2 = deepcopy(
    continual_learning_evaluator_vocalsettech_scenario1
)
continual_learning_evaluator_vocalsettech_scenario2["args"]["tasks"] = scenario2
continual_learning_evaluator_vocalsettech_scenario3 = deepcopy(
    continual_learning_evaluator_vocalsettech_scenario1
)
continual_learning_evaluator_vocalsettech_scenario3["args"]["tasks"] = scenario3


## L2P
continual_learning_l2p_evaluator_vocalsettech_scenario1 = deepcopy(
    continual_learning_evaluator_l2p
)
continual_learning_l2p_evaluator_vocalsettech_scenario1["args"]["tasks"] = scenario1
continual_learning_l2p_evaluator_vocalsettech_scenario1["args"].update(
    update_evaluator_vocalsettech
)


continual_learning_l2p_evaluator_vocalsettech_scenario2 = deepcopy(
    continual_learning_l2p_evaluator_vocalsettech_scenario1
)
continual_learning_l2p_evaluator_vocalsettech_scenario2["args"]["tasks"] = scenario2
continual_learning_l2p_evaluator_vocalsettech_scenario3 = deepcopy(
    continual_learning_l2p_evaluator_vocalsettech_scenario1
)
continual_learning_l2p_evaluator_vocalsettech_scenario3["args"]["tasks"] = scenario3


## L2Center
continual_learning_l2center_evaluator_vocalsettech_scenario1 = deepcopy(
    continual_learning_evaluator_l2center
)
continual_learning_l2center_evaluator_vocalsettech_scenario1["args"][
    "tasks"
] = scenario1
continual_learning_l2center_evaluator_vocalsettech_scenario1["args"].update(
    update_evaluator_vocalsettech
)


continual_learning_l2center_evaluator_vocalsettech_scenario2 = deepcopy(
    continual_learning_l2center_evaluator_vocalsettech_scenario1
)
continual_learning_l2center_evaluator_vocalsettech_scenario2["args"][
    "tasks"
] = scenario2
continual_learning_l2center_evaluator_vocalsettech_scenario3 = deepcopy(
    continual_learning_l2center_evaluator_vocalsettech_scenario1
)
continual_learning_l2center_evaluator_vocalsettech_scenario3["args"][
    "tasks"
] = scenario3


###############################################################
###########               EXPERIMENTS               ###########
###############################################################

###########                BASELINES                ###########

clmrsamplecnnxl_base_oracle_vocalsettech_scenario1 = {
    "experiment_name": "clmrsamplecnnxl_base_oracle_vocalsettech_all",
    "experiment_type": "Baseline",
    "experiment_subtype": "Oracle",
    # data
    "train": {
        "trainer": oracle_trainer_vocalsettech,
    },
    "evaluate": {
        "evaluator": oracle_evaluator_vocalsettech_scenario1,
    },
}

clmrsamplecnnxl_base_oracle_vocalsettech_scenario2 = {
    "experiment_name": "clmrsamplecnnxl_base_oracle_vocalsettech_all",
    "experiment_type": "Baseline",
    "experiment_subtype": "Oracle",
    # data
    "train": {
        "trainer": oracle_trainer_vocalsettech,
    },
    "evaluate": {
        "evaluator": oracle_evaluator_vocalsettech_scenario2,
    },
}

clmrsamplecnnxl_base_oracle_vocalsettech_scenario3 = {
    "experiment_name": "clmrsamplecnnxl_base_oracle_vocalsettech_all",
    "experiment_type": "Baseline",
    "experiment_subtype": "Oracle",
    # data
    "train": {
        "trainer": oracle_trainer_vocalsettech,
    },
    "evaluate": {
        "evaluator": oracle_evaluator_vocalsettech_scenario3,
    },
}


###########            CONTINUAL LEARNING           ###########

# SCENARIO 1

clmrsamplecnnxl_finetuning_cl_vocalsettech_scenario1 = {
    "experiment_name": "clmrsamplecnnxl_finetuning_cl_vocalsettech_scenario1",
    "experiment_type": "CL",
    "experiment_subtype": "Finetuning",
    # data
    "train": {
        "trainer": continual_learning_trainer_vocalsettech_scenario1,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario1,
    },
}

clmrsamplecnnxl_replay_cl_vocalsettech_scenario1 = {
    "experiment_name": "clmrsamplecnnxl_replay_cl_vocalsettech_scenario1",
    "experiment_type": "CL",
    "experiment_subtype": "Replay",
    # data
    "train": {
        "trainer": continual_learning_replay_trainer_vocalsettech_scenario1,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario1,
    },
}

clmrsamplecnnxl_icarl_cl_vocalsettech_scenario1 = {
    "experiment_name": "clmrsamplecnnxl_icarl_cl_vocalsettech_scenario1",
    "experiment_type": "CL",
    "experiment_subtype": "iCaRL",
    # data
    "train": {
        "trainer": continual_learning_icarl_trainer_vocalsettech_scenario1,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario1,
    },
}

clmrsamplecnnxl_gem_cl_vocalsettech_scenario1 = {
    "experiment_name": "clmrsamplecnnxl_gem_cl_vocalsettech_scenario1",
    "experiment_type": "CL",
    "experiment_subtype": "GEM",
    # data
    "train": {
        "trainer": continual_learning_gem_trainer_vocalsettech_scenario1,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario1,
    },
}

clmrsamplecnnxl_ewc_cl_vocalsettech_scenario1 = {
    "experiment_name": "clmrsamplecnnxl_ewc_cl_vocalsettech_scenario1",
    "experiment_type": "CL",
    "experiment_subtype": "EWC",
    # data
    "train": {
        "trainer": continual_learning_ewc_trainer_vocalsettech_scenario1,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario1,
    },
}

clmrsamplecnnxl_l2p_cl_vocalsettech_scenario1 = {
    "experiment_name": "clmrsamplecnnxl_l2p_cl_vocalsettech_scenario1",
    "experiment_type": "CL",
    "experiment_subtype": "L2P",
    # data
    "train": {
        "trainer": continual_learning_l2p_trainer_vocalsettech_scenario1,
    },
    "evaluate": {
        "evaluator": continual_learning_l2p_evaluator_vocalsettech_scenario1,
    },
}

clmrsamplecnnxl_l2center_cl_vocalsettech_scenario1 = {
    "experiment_name": "clmrsamplecnnxl_l2center_cl_vocalsettech_scenario1",
    "experiment_type": "CL",
    "experiment_subtype": "L2Center",
    # data
    "train": {
        "trainer": continual_learning_l2center_trainer_vocalsettech_scenario1,
    },
    "evaluate": {
        "evaluator": continual_learning_l2center_evaluator_vocalsettech_scenario1,
    },
}


# SCENARIO 2

clmrsamplecnnxl_finetuning_cl_vocalsettech_scenario2 = {
    "experiment_name": "clmrsamplecnnxl_finetuning_cl_vocalsettech_scenario2",
    "experiment_type": "CL",
    "experiment_subtype": "Finetuning",
    # data
    "train": {
        "trainer": continual_learning_trainer_vocalsettech_scenario2,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario2,
    },
}

clmrsamplecnnxl_replay_cl_vocalsettech_scenario2 = {
    "experiment_name": "clmrsamplecnnxl_replay_cl_vocalsettech_scenario2",
    "experiment_type": "CL",
    "experiment_subtype": "Replay",
    # data
    "train": {
        "trainer": continual_learning_replay_trainer_vocalsettech_scenario2,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario2,
    },
}

clmrsamplecnnxl_icarl_cl_vocalsettech_scenario2 = {
    "experiment_name": "clmrsamplecnnxl_icarl_cl_vocalsettech_scenario2",
    "experiment_type": "CL",
    "experiment_subtype": "iCaRL",
    # data
    "train": {
        "trainer": continual_learning_icarl_trainer_vocalsettech_scenario2,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario2,
    },
}

clmrsamplecnnxl_gem_cl_vocalsettech_scenario2 = {
    "experiment_name": "clmrsamplecnnxl_gem_cl_vocalsettech_scenario2",
    "experiment_type": "CL",
    "experiment_subtype": "GEM",
    # data
    "train": {
        "trainer": continual_learning_gem_trainer_vocalsettech_scenario2,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario2,
    },
}

clmrsamplecnnxl_ewc_cl_vocalsettech_scenario2 = {
    "experiment_name": "clmrsamplecnnxl_ewc_cl_vocalsettech_scenario2",
    "experiment_type": "CL",
    "experiment_subtype": "EWC",
    # data
    "train": {
        "trainer": continual_learning_ewc_trainer_vocalsettech_scenario2,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario2,
    },
}

clmrsamplecnnxl_l2p_cl_vocalsettech_scenario2 = {
    "experiment_name": "clmrsamplecnnxl_l2p_cl_vocalsettech_scenario2",
    "experiment_type": "CL",
    "experiment_subtype": "L2P",
    # data
    "train": {
        "trainer": continual_learning_l2p_trainer_vocalsettech_scenario2,
    },
    "evaluate": {
        "evaluator": continual_learning_l2p_evaluator_vocalsettech_scenario2,
    },
}

clmrsamplecnnxl_l2center_cl_vocalsettech_scenario2 = {
    "experiment_name": "clmrsamplecnnxl_l2center_cl_vocalsettech_scenario2",
    "experiment_type": "CL",
    "experiment_subtype": "L2Center",
    # data
    "train": {
        "trainer": continual_learning_l2center_trainer_vocalsettech_scenario2,
    },
    "evaluate": {
        "evaluator": continual_learning_l2center_evaluator_vocalsettech_scenario2,
    },
}


# SCENARIO 3

clmrsamplecnnxl_finetuning_cl_vocalsettech_scenario3 = {
    "experiment_name": "clmrsamplecnnxl_finetuning_cl_vocalsettech_scenario3",
    "experiment_type": "CL",
    "experiment_subtype": "Finetuning",
    # data
    "train": {
        "trainer": continual_learning_trainer_vocalsettech_scenario3,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario3,
    },
}

clmrsamplecnnxl_replay_cl_vocalsettech_scenario3 = {
    "experiment_name": "clmrsamplecnnxl_replay_cl_vocalsettech_scenario3",
    "experiment_type": "CL",
    "experiment_subtype": "Replay",
    # data
    "train": {
        "trainer": continual_learning_replay_trainer_vocalsettech_scenario3,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario3,
    },
}

clmrsamplecnnxl_icarl_cl_vocalsettech_scenario3 = {
    "experiment_name": "clmrsamplecnnxl_icarl_cl_vocalsettech_scenario3",
    "experiment_type": "CL",
    "experiment_subtype": "iCaRL",
    # data
    "train": {
        "trainer": continual_learning_icarl_trainer_vocalsettech_scenario3,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario3,
    },
}

clmrsamplecnnxl_gem_cl_vocalsettech_scenario3 = {
    "experiment_name": "clmrsamplecnnxl_gem_cl_vocalsettech_scenario3",
    "experiment_type": "CL",
    "experiment_subtype": "GEM",
    # data
    "train": {
        "trainer": continual_learning_gem_trainer_vocalsettech_scenario3,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario3,
    },
}

clmrsamplecnnxl_ewc_cl_vocalsettech_scenario3 = {
    "experiment_name": "clmrsamplecnnxl_ewc_cl_vocalsettech_scenario3",
    "experiment_type": "CL",
    "experiment_subtype": "EWC",
    # data
    "train": {
        "trainer": continual_learning_ewc_trainer_vocalsettech_scenario3,
    },
    "evaluate": {
        "evaluator": continual_learning_evaluator_vocalsettech_scenario3,
    },
}

clmrsamplecnnxl_l2p_cl_vocalsettech_scenario3 = {
    "experiment_name": "clmrsamplecnnxl_l2p_cl_vocalsettech_scenario3",
    "experiment_type": "CL",
    "experiment_subtype": "L2P",
    # data
    "train": {
        "trainer": continual_learning_l2p_trainer_vocalsettech_scenario3,
    },
    "evaluate": {
        "evaluator": continual_learning_l2p_evaluator_vocalsettech_scenario3,
    },
}

clmrsamplecnnxl_l2center_cl_vocalsettech_scenario3 = {
    "experiment_name": "clmrsamplecnnxl_l2center_cl_vocalsettech_scenario3",
    "experiment_type": "CL",
    "experiment_subtype": "L2Center",
    # data
    "train": {
        "trainer": continual_learning_l2center_trainer_vocalsettech_scenario3,
    },
    "evaluate": {
        "evaluator": continual_learning_l2center_evaluator_vocalsettech_scenario3,
    },
}
