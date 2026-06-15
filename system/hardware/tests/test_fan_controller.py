import pytest

from openpilot.system.hardware.fan_controller import FanController

ALL_CONTROLLERS = [FanController]

def patched_controller(mocker, controller_class):
  mocker.patch("os.system", new=mocker.Mock())
  return controller_class(2)

class TestFanController:
  def wind_up(self, controller, power_save=False):
    for _ in range(1000):
      controller.update(100, power_save)

  def wind_down(self, controller, power_save=True):
    for _ in range(1000):
      controller.update(10, power_save)

  @pytest.mark.parametrize("controller_class", ALL_CONTROLLERS)
  def test_hot_onroad(self, mocker, controller_class):
    controller = patched_controller(mocker, controller_class)
    self.wind_up(controller)
    assert controller.update(100, False) >= 70

  @pytest.mark.parametrize("controller_class", ALL_CONTROLLERS)
  def test_offroad_limits(self, mocker, controller_class):
    controller = patched_controller(mocker, controller_class)
    self.wind_up(controller)
    assert controller.update(100, True) <= 30

  @pytest.mark.parametrize("controller_class", ALL_CONTROLLERS)
  def test_no_fan_wear(self, mocker, controller_class):
    controller = patched_controller(mocker, controller_class)
    self.wind_down(controller)
    assert controller.update(10, True) == 0

  @pytest.mark.parametrize("controller_class", ALL_CONTROLLERS)
  def test_limited(self, mocker, controller_class):
    controller = patched_controller(mocker, controller_class)
    self.wind_up(controller, False)
    assert controller.update(100, False) == 100

  @pytest.mark.parametrize("controller_class", ALL_CONTROLLERS)
  def test_windup_speed(self, mocker, controller_class):
    controller = patched_controller(mocker, controller_class)
    self.wind_down(controller, False)
    for _ in range(10):
      controller.update(90, False)
    assert controller.update(90, False) >= 60
