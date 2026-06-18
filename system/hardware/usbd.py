#!/usr/bin/env python3
import os
import re
import glob

from cereal import messaging
from openpilot.common.realtime import Ratekeeper
from openpilot.common.swaglog import cloudlog

PUB_HZ = 10            # cereal publish rate

DEVICE = "/sys/bus/usb/devices/4-1"  # aux USB
PORT = "/sys/bus/usb/devices/usb4/4-0:1.0/usb4-port1"

# cereal LtssmState by ordinal (the kernel sampler emits these indices)
LTSSM = ["unknown", "u0", "u1", "u2", "u3", "ssDisabled", "rxDetect", "ssInactive",
         "poll", "recovery", "hotReset", "compliance", "loopback", "reset", "resume", "poweredOff"]


def read(attr: str, base: str = DEVICE) -> str | None:
  try:
    with open(os.path.join(base, attr)) as f:
      return f.read().strip()
  except OSError:
    return None


def read_int(path: str, default: int = 0) -> int:
  try:
    with open(path) as f:
      return int(f.read().strip())
  except (OSError, ValueError):
    return default


def over_current_count() -> int:
  return read_int(os.path.join(PORT, "over_current_count"))


def find_controller() -> str | None:
  """Resolve the dwc3 core (.dwc3) sysfs node exposing the SS link telemetry"""
  m = re.search(r"([0-9a-f]+\.dwc3)", os.path.realpath(DEVICE))
  if m:
    cand = f"/sys/bus/platform/devices/{m.group(1)}"
    if os.path.exists(os.path.join(cand, "ltssm_state")):
      return cand
  for c in glob.glob("/sys/bus/platform/devices/*.dwc3"):
    if os.path.exists(os.path.join(c, "ltssm_state")):
      return c
  return None


def ltssm_name(idx: int) -> str:
  return LTSSM[idx] if 0 <= idx < len(LTSSM) else "unknown"


def read_vbus_mv() -> int:
  for p in ("/sys/class/power_supply/usb/voltage_now", os.path.join(PORT, "../voltage_now")):
    uv = read_int(p, -1)
    if uv >= 0:
      return uv // 1000
  return 0


def main():
  pm = messaging.PubMaster(['usbState'])
  rk = Ratekeeper(PUB_HZ, print_delay_threshold=None)
  ctrl = find_controller()
  cloudlog.event("usbd_start", ctrl=ctrl, device=DEVICE)

  disconnect_count = 0
  was_connected = False

  while True:
    speed = read("speed")
    connected = speed is not None
    speed_mbps = int(speed) if (speed and speed.isdigit()) else 0

    # connect / disconnect (USB device presence, not LTSSM)
    if was_connected and not connected:
      disconnect_count += 1
      cloudlog.event("usb_disconnected", count=disconnect_count)
    elif connected and not was_connected:
      cloudlog.event("usb_connected", idVendor=read("idVendor"), idProduct=read("idProduct"), speed=speed)
    was_connected = connected

    msg = messaging.new_message('usbState', valid=True)
    s = msg.usbState
    s.connected = connected
    s.speedMbps = speed_mbps
    s.pmActive = read("power/runtime_status") == "active"
    s.disconnectCount = disconnect_count
    s.overCurrentCount = over_current_count()

    # LTSSM spine + transition counters: all edge detection runs in the kernel sampler
    if ctrl is not None:
      s.ltssmState = ltssm_name(read_int(os.path.join(ctrl, "ltssm_state")))
      s.lastNonU0State = ltssm_name(read_int(os.path.join(ctrl, "last_non_u0_state")))
      s.lastTransitionMonoTime = read_int(os.path.join(ctrl, "last_transition_ns"))
      hist = read("ltssm_history", ctrl)
      s.ltssmHistory = [int(x) for x in hist.split()] if hist else []
      s.recoveryCount = read_int(os.path.join(ctrl, "recovery_count"))
      s.rxDetectCount = read_int(os.path.join(ctrl, "rx_detect_count"))
      s.ssInactiveCount = read_int(os.path.join(ctrl, "ss_inactive_count"))
      s.poweredOffCount = read_int(os.path.join(ctrl, "powered_off_count"))
      s.linkErrorCount = read_int(os.path.join(ctrl, "link_error_count"))

    # sleep / power states
    s.runtimeSuspendedMs = read_int(os.path.join(DEVICE, "power/runtime_suspended_time"))
    s.lpmU1Enabled = read("power/usb3_hardware_lpm_u1") == "enabled"
    s.lpmU2Enabled = read("power/usb3_hardware_lpm_u2") == "enabled"

    # VBUS brownout discriminator
    s.vbusMv = read_vbus_mv()

    pm.send('usbState', msg)
    rk.keep_time()


if __name__ == "__main__":
  main()
