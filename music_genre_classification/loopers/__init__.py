from music_genre_classification.loopers.dkvb_music_genre_classification_looper import (
    DkvbMusicGenreClassificationLooper,
)
from music_genre_classification.loopers.ewc_music_genre_classification_looper import (
    EwcMusicGenreClassificationLooper,
)
from music_genre_classification.loopers.gem_music_genre_classification_looper import (
    GemMusicGenreClassificationLooper,
)
from music_genre_classification.loopers.l2p_music_genre_classification_looper import (
    L2PMusicGenreClassificationLooper,
)
from music_genre_classification.loopers.looper import Looper
from music_genre_classification.loopers.looper_factory import LooperFactory
from music_genre_classification.loopers.music_genre_classification_looper import (
    MusicGenreClassificationLooper,
)
from music_genre_classification.loopers.icarl_music_genre_classification_looper import (
    iCaRLMusicGenreClassificationLooper,
)

__all__ = [
    "Looper",
    "LooperFactory",
    "MusicGenreClassificationLooper",
    "DkvbMusicGenreClassificationLooper",
    "GemMusicGenreClassificationLooper",
    "EwcMusicGenreClassificationLooper",
    "L2PMusicGenreClassificationLooper",
    "iCaRLMusicGenreClassificationLooper",
]
