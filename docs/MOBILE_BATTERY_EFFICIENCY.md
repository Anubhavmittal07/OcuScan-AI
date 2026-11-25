# Battery Preservation & Thermal Management on Mobile Screening Devices

During full-day community screening camps with limited charging infrastructure:

1. **Camera Stream Throttling**: Freeze live WebRTC viewfinder frames when no face or eye is detected within 3 seconds.
2. **Torch / Flash Management**: Pulse the device LED flash exclusively during the 100ms capture window rather than running continuous flashlight mode.
3. **Core Affinity**: Bound PyTorch inference execution to efficiency cores on hybrid ARM processors to prevent thermal throttling.
