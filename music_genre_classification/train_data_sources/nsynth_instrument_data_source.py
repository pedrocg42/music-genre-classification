# Found filtered dataset from https://github.com/coreyker/dnn-mgr/tree/master/gtzan
import os
from glob import glob

import numpy as np
from torch.utils.data import ConcatDataset, DataLoader, Dataset

import config
from music_genre_classification.train_data_sources.mert_genre_classification_dataset import (
    MertGenreClassificationDataset,
)
from music_genre_classification.train_data_sources.train_data_source import (
    TrainDataSource,
)

np.random.seed(config.seed)


INSTRUMENTS = [
    "bass",
    "brass",
    "flute",
    "guitar",
    "keyboard",
    "mallet",
    "organ",
    "reed",
    "string",
    "synth_lead",
    "vocal",
]


class NSynthInstrumentTechDataSource(TrainDataSource):
    def __init__(
        self,
        split: str,
        num_cross_val_splits: int = 5,
        instruments: list[str] = INSTRUMENTS,
        is_eval: bool = False,
        chunk_length: float = 5.0,
        **kwargs,
    ):
        self.name = "NSynthInstrument"
        self.dataset_path = os.path.join(config.dataset_path, "NSynth")
        self.instruments = instruments
        self.instrument_to_index = {
            instrument: i for i, instrument in enumerate(self.instruments)
        }
        self.index_to_instrument = {
            i: instrument for i, instrument in enumerate(self.instruments)
        }

        # Split parameters
        self.split = split
        self.num_cross_val_splits = num_cross_val_splits
        self.is_eval = is_eval

        # Audio parameters
        self.sample_rate = 44100
        self.song_length = 6  # Average time per clip, useful for training
        self.chunk_length = chunk_length

        self._get_songs()

    def _get_songs(self):
        # Read annotations
        self.songs = np.array(
            glob(os.path.join(self.dataset_path, "*", "audio", "*.wav"))
        )

        song_labels = []
        for song in self.songs:
            splitted_name = os.path.basename(song).split("_")
            match len(splitted_name):
                case 3:
                    label = splitted_name[0]
                case 4:
                    label = "_".join(splitted_name[:2])
                case _:
                    raise NotImplementedError()
            song_labels.append(label)
        self.labels = np.array(
            [self.instrument_to_index[label] for label in song_labels]
        )

        # Shuffling
        idx = np.arange(len(self.songs))
        np.random.shuffle(idx)
        self.songs = self.songs[idx]
        self.labels = self.labels[idx]

        # Split
        self.cross_val_split()

    def cross_val_split(self, cross_val_id: int = 0):
        # Split
        self.songs_splits = {
            "train": [],
            "val": [],
            "test": [],
        }
        self.labels_splits = {
            "train": [],
            "val": [],
            "test": [],
        }
        for index in self.index_to_instrument.keys():
            songs_instrument = self.songs[self.labels == index]
            labels_instrument = self.labels[self.labels == index]
            split_size = len(songs_instrument) // self.num_cross_val_splits
            songs_splits = [
                songs_instrument[int(i * split_size) : int((i + 1) * split_size)]
                for i in range(self.num_cross_val_splits)
            ]
            labels_splits = [
                labels_instrument[int(i * split_size) : int((i + 1) * split_size)]
                for i in range(self.num_cross_val_splits)
            ]

            # Get train, val and test splits
            test_set_songs = songs_splits.pop(cross_val_id)
            val_set_songs = songs_splits.pop(-1)
            train_set_songs = np.concatenate(songs_splits)
            self.songs_splits["train"].append(train_set_songs)
            self.songs_splits["val"].append(val_set_songs)
            self.songs_splits["test"].append(test_set_songs)

            test_set_labels = labels_splits.pop(cross_val_id)
            val_set_labels = labels_splits.pop(-1)
            train_set_labels = np.concatenate(labels_splits)
            self.labels_splits["train"].append(train_set_labels)
            self.labels_splits["val"].append(val_set_labels)
            self.labels_splits["test"].append(test_set_labels)

        self.songs_splits["train"] = np.concatenate(self.songs_splits["train"])
        self.songs_splits["val"] = np.concatenate(self.songs_splits["val"])
        self.songs_splits["test"] = np.concatenate(self.songs_splits["test"])
        self.labels_splits["train"] = np.concatenate(self.labels_splits["train"])
        self.labels_splits["val"] = np.concatenate(self.labels_splits["val"])
        self.labels_splits["test"] = np.concatenate(self.labels_splits["test"])

    def get_dataset(
        self,
        task: str | list[str] = None,
        cross_val_id: int = 0,
        memory_dataset: Dataset = None,
        is_eval: bool | None = None,
    ) -> Dataset:
        self.cross_val_split(cross_val_id=cross_val_id)

        songs = self.songs_splits[self.split]
        labels = self.labels_splits[self.split]

        if task is not None and task != "all":
            if isinstance(task, str):
                songs = songs[labels == self.instrument_to_index[task]]
                labels = labels[labels == self.instrument_to_index[task]]
            elif isinstance(task, list):
                task = [self.instrument_to_index[instrument] for instrument in task]
                songs = songs[np.isin(labels, task)]
                labels = labels[np.isin(labels, task)]

        dataset = MertGenreClassificationDataset(
            songs=songs,
            labels=labels,
            is_eval=self.is_eval if is_eval is None else is_eval,
            song_length=self.song_length,
            audio_length=self.chunk_length,
            input_sample_rate=self.sample_rate,
        )

        if memory_dataset is not None:
            dataset = ConcatDataset([dataset, memory_dataset])

        return dataset

    def get_dataloader(
        self,
        task: str = None,
        cross_val_id: int = 0,
        batch_size: int = 32,
        num_workers: int = 0,
        **kwargs,
    ) -> DataLoader:
        dataset = self.get_dataset(task=task, cross_val_id=cross_val_id, **kwargs)

        data_loader = DataLoader(
            dataset=dataset,
            batch_size=batch_size,
            shuffle=True if (self.split == "train") else False,
            drop_last=False,
            num_workers=num_workers,
            pin_memory=True,
        )
        return data_loader