# Failure modes or inputs and outputs on a function (2026-11-14)

Question (#63): how should a function describe what can go wrong, so the requirements
step finds input refusal and data kept across a restart, the two misses of the
requirements test (#60)? Web searches in the main session; the standards themselves
(AIAG-VDA, IEEE 1633) were not read. VERIFIED-secondary means a summary or secondary
source was seen; INFERRED means reasoning.

## Findings

- **FMEA separates the mode from its cause and effect.** A failure mode is "a simple
  description of the failure without stating the cause behind it or the effect after
  it"; causes and effects are listed per mode. VERIFIED-secondary
  (https://arxiv.org/pdf/2101.05444).
- **Software failure modes are manifestations,** such as "the value of data out of
  limits" and "garbled data" (IEEE 610.12, cited by NASA's software handbook).
  VERIFIED-secondary (https://swehb.nasa.gov/x/kABiC).
- **Function failure modes have a stock taxonomy:** no, partial, degraded,
  intermittent, unintended, exceeding and delayed function (AIAG-VDA 2019).
  VERIFIED-secondary (Cambridge 2024 paper on extending it for AI components). No
  software-specific taxonomy was found.
- **A functional FMEA assumes inputs within specification and one failure at a time**
  (GSFC FMEA procedure). VERIFIED-secondary
  (https://rsdo.gsfc.nasa.gov/documents/rapid-iii-documents/mar-reference/gsfc-fap-322-208-fmea-draft.pdf).
  So it is silent on the very case datum missed, input outside its range. INFERRED.
- **NASA describes a function by its inputs, outputs and failure modes** (SEH
  4.3.1.2.2). VERIFIED, earlier (`2026-10-18-functions.md`, item 4). Datum's function
  file held only a name and a definition.

## Conclusion (INFERRED)

The issue's list (bad input, an interrupted run, the part closed) names causes, and the
data-loss miss was a mode ("the result is not there next time"); a failure-mode field
would bring FMEA's mode-cause split back, which datum dropped for STPA and STRIDE. Both
misses were not harms but gaps in what each function is: the range of what it accepts,
and who uses its result and when. Listing each function's inputs and outputs gives the
requirements step something to walk: each input's range and the response outside it,
and for each output whether its user can run after the part is closed. Agreed as a
design note the same day.
