# csc.tools.attractor.Args

> 公式: https://cascadeur.com/python-api/_generate/csc.tools.attractor.Args.html

Arguments for configuring attractor operations.

## Methods

- `__init__(self: csc.tools.attractor.Args, scene: csc.domain.Scene, gravity: float, general_settings: csc.tools.attractor.AttractorGeneralSettings, only_key_frames: bool, mode: csc.tools.attractor.ArgsMode, for_interval: bool = False, hard: bool = False, frame_action_on_change: csc.domain.FrameActionOnChange = <FrameActionOnChange.DoNothing: 2>, interval_action_on_change: csc.domain.IntervalActionOnChange = <IntervalActionOnChange.Fixing: 0>) → None`
  - Initializes Args with scene, gravity, general settings, and operation modes.

## Properties

- `general_settings`
  - General settings for the attractor operation.
- `mode`
  - Mode controlling attractor behavior.
- `for_interval`
  - Whether the operation applies to an interval.
- `only_key_frames`
  - Whether to process only keyframes.
- `frame_action_on_change`
  - Action to perform on frame change.
- `interval_action_on_change`
  - Action to perform on interval change.
