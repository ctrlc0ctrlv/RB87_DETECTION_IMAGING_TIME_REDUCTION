from collections.abc import Callable
import fnmatch
import json
import logging
import os
from pathlib import Path
from typing import List

import numpy as np
from PIL import Image
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageLoader:
    @staticmethod
    def convert_index_to_exposure_time(index: int) -> float:
        """
        Converts image indices to exposure time (ms)

        0-999: 2.0 ms
        1'000-1'999: 2.5 ms
        ...
        14'000 - 14'999: 9.0 ms

        Important note: each group of three images (first-second-third) has the same image index!
        """
        for i in range(15):
            if i * 1000 <= index < (i + 1) * 1000:
                return i * 0.5 + 2
        assert False, "Wrong image indexing!"

    def __init__(
        self,
        datapath: Path,
        exposure_time_ms: float = 30.0,
        index_to_exposure_time: Callable[[int], float] = convert_index_to_exposure_time,
        from_files=True,
        data=None,
        pattern: str = "*.png",
    ) -> None:
        self.datapath = Path(datapath)
        self.exposure_time_ms = exposure_time_ms
        self.index_to_exposure_time = index_to_exposure_time
        self.data = None
        self.first = None
        self.second = None
        self.third = None
        self.dir_files = None
        self.pattern = pattern
        self.trap_xy = None
        self.mask = None
        self.remasked_data = None
        self.remasked_data_first = None
        self.remasked_data_second = None
        self.remasked_data_third = None

        logging.basicConfig(level=logging.INFO)
        logger.info(
            "Initialized ImageLoader in path: %s", self.datapath.absolute().resolve()
        )

        if from_files:
            self.__get_all_pngs_from_folder()
        else:
            assert data is not None, "None passed to data when loading from files"
            self.data = data
        self.align_with_real_points()

    def __get_all_pngs_from_folder(self) -> None:
        if self.data is not None:
            return

        folder_path = self.datapath
        total_images = []
        first_images = []
        second_images = []
        third_images = []

        self.dir_files = sorted(
            [
                file
                for file in os.listdir(folder_path)
                if fnmatch.fnmatch(file, self.pattern)
                and np.isclose(
                    self.exposure_time_ms,
                    self.index_to_exposure_time(int(file.split(".")[1].split("_")[-1])),
                )
            ],
            key=lambda x: int(x.replace("us", "").split("_")[1]),
        )
        logger.info("self.dirfiles size = %s", len(self.dir_files))

        for filename in tqdm(self.dir_files, leave=False):
            path = folder_path / filename
            inp_image = np.asarray(Image.open(path, mode="r")).astype("uint8")
            if inp_image is None:
                logger.error("Could not open image %s", path)

            if "first" in filename:
                first_images.append(inp_image)
            elif "second" in filename:
                second_images.append(inp_image)
            elif "third" in filename:
                third_images.append(inp_image)
            total_images.append(inp_image)

        self.data = np.array(total_images)
        self.first = np.array(first_images)
        self.second = np.array(second_images)
        self.third = np.array(third_images)

    def align_with_real_points(self) -> None:
        trap_array_json_path = self.datapath / "trap_positions.json"
        with open(trap_array_json_path, "r") as f:
            data = json.load(f)
        self.trap_xy = {
            int(key): (float(pos["x"]), float(pos["y"])) for key, pos in data.items()
        }

    def update_mask(self, trap_inds: List[int], trap_radius: float = 4.0) -> None:
        if trap_inds is None:
            trap_inds = [54]  # central trap
        self.trap_inds = trap_inds
        self.trap_radius = trap_radius
        self.mask = self.get_traps_mask(
            trap_inds=self.trap_inds, trap_radius=self.trap_radius
        )
        self.remasked_data = np.ma.masked_array(
            self.data,
            np.repeat(~self.mask[np.newaxis, :, :], self.data.shape[0], axis=0),
        )
        self.remasked_data_first = np.ma.masked_array(
            self.first,
            np.repeat(~self.mask[np.newaxis, :, :], self.first.shape[0], axis=0),
        )
        self.remasked_data_second = np.ma.masked_array(
            self.second,
            np.repeat(~self.mask[np.newaxis, :, :], self.second.shape[0], axis=0),
        )
        self.remasked_data_third = np.ma.masked_array(
            self.third,
            np.repeat(~self.mask[np.newaxis, :, :], self.third.shape[0], axis=0),
        )

    def get_traps_mask(
        self, trap_inds: List[int] = [54], trap_radius: float = 4.0
    ) -> np.ndarray:
        mask = np.zeros_like(self.data[0], dtype=bool)
        if trap_inds is None:
            trap_inds = range(len(self.trap_xy))

        for tr_ind in trap_inds:
            left_x, left_y = np.round(
                np.array(self.trap_xy[tr_ind]) - trap_radius
            ).astype(int)
            right_x, right_y = np.round(
                np.array(self.trap_xy[tr_ind]) + trap_radius + 1
            ).astype(int)
            mask[left_y:right_y, left_x:right_x] = True
        return mask
