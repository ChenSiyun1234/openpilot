#!/usr/bin/env python3
import numpy as np

from openpilot.common.pid import PIDController
from openpilot.system.hardware import HARDWARE

# raise fan setpoint on tici/tizi to reduce noise
# after raising LMH threshold in AGNOS 18.1 to prevent CPU throttling
OFFSET = 0 if HARDWARE.get_device_type() == "mici" else 5


class FanController:
  def __init__(self, rate: int) -> None:
    self.last_power_save = True
    self.controller = PIDController(k_p=0, k_i=4e-3, rate=rate)

  def update(self, cur_temp: float, power_save: bool) -> int:
    self.controller.pos_limit = 100 if not power_save else 30
    self.controller.neg_limit = 30 if not power_save else 0

    if power_save != self.last_power_save:
      self.controller.reset()
    self.last_power_save = power_save

    return int(self.controller.update(
                 error=(cur_temp - (75 + OFFSET)),  # temperature setpoint in C
                 feedforward=np.interp(cur_temp, [60.0 + OFFSET, 100.0 + OFFSET], [0, 100])
              ))
