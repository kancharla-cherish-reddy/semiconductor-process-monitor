# Product Brief

## Working title

**Semiconductor Process Stability and Yield Analysis**

## One-sentence concept

A reproducible educational case study that audits anonymized semiconductor manufacturing measurements, investigates process stability using statistical process control, and explores how those measurements relate to pass/fail outcomes.

## Why build it

The project connects an Electronics and Communication Engineering background with semiconductor manufacturing and process-engineering preparation. It provides a concrete way to learn process variation, measurement data, SPC, Python analytics, and technical communication.

## Intended audience

- The learner, who is developing semiconductor-process and data-analysis skills.
- An academic or engineering reviewer who wants to inspect the methods, code, evidence, and limitations.

The app is an educational exploration tool; it is not intended for fab operators to make live production decisions.

## Problem framing

Manufacturing processes generate many measurements. Engineers need to understand whether measurements are usable, how they vary over time, and whether an observed change deserves investigation. The SECOM dataset provides a public, anonymized example for practicing parts of this workflow.

## Core questions

1. What is the shape and quality of the dataset?
2. Which features contain missing or constant values, and how should that affect analysis?
3. Are timestamps and observation order suitable for a time-ordered monitoring exercise?
4. What does a selected univariate I-MR chart indicate about stability under its assumptions?
5. Which observations or patterns trigger defined Western Electric rules?
6. How do measured features associate with pass/fail labels, and what conclusions remain unsupported?

## Product promise

The project will make its analysis reproducible and understandable. It will show data checks, choices, visual evidence, and limitations together.

## Non-goals

- Diagnosing a real Micron process or identifying a physical root cause.
- Claiming that anonymized feature IDs are named process parameters.
- Treating every chart alarm as a defect or automatically changing data to remove alarms.
- Claiming a production-ready manufacturing execution or monitoring system.
- Presenting a simulated DOE as if it were measured fab data.
