---
id: index
title: vocabulary
sidebar_label: Overview
slug: /vocabulary
---

<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->

# vocabulary

**Version**: v26.0727
**Namespace**: `https://behaverse.org/schemas/vocabulary`

Cross-cutting controlled terminology for behaverse data: general terms, demographics, and the suffix conventions used in variable names. Terms that one schema owns (e.g. trial table fields) live in that schema; this resource holds the terms no single schema owns.


This controlled vocabulary defines **42 terms** across **7 concept schemes**. Terms a single schema owns live in that schema; this resource holds the cross-cutting terms no single schema owns.


## General


General vocabulary

| Term | Type | Definition |
|:-----|:-----|:-----------|
| **accuracy** | `float` | Refers to a measure of performance. In many behavioral tasks, it reflects the percentage (0-100%) or fraction (0-1) of correct responses. Always use *accuracy* to refer to a performance measure that is a real number (float) and bounded to the [0-1] range. |
| **correct** | `boolean` | A boolean which indicates whether a response in a given trial was correct or not. When no response was given when it should (i.e., timeout), *correct* evaluates to `FALSE` rather than `N/A`. This is to avoid the case where subjects would be given a high performance score when in fact they avoided all difficult trials and responded correctly only to easy trials. |
| **response_time** | `float` | The meaning of response time or reaction time (and its unit) is not consistent across studies. In BDM, `response_time` is the duration in seconds between a) the moment the subjects fully completed their response on a given trial, and b) the moment that the earliest possible correct response could have been completed by a hypothetical agent with perfect knowledge of the task and ability to instantaneously execute the response. |
| **timed_out** | `boolean` | Indicates whether the subject failed to respond within the allocated time period. |

## Demographics


Demographics vocabulary

| Term | Type | Definition |
|:-----|:-----|:-----------|
| **age** | `float` | Age is typically expressed in years. However, we don't recommend rounding "age" to get integer values, as rounding implies losing data. It is better to leave variables as real numbers (floats when they are floats) and let the data analysts decide whether or not rounding this variable is necessary for their specific use case. |
| **gender/sex** | `enum` | Gender and sex are not exactly the same. Sex refers to a biological sex while gender is a more complex construct. A person may have a male biological sex but identify as a women for example. Depending on the question asked, the variable should therefore be either `sex` or `gender`.  For example, *"What sex were you assigned at birth, such as on an original birth certificate?"* is a question about biological sex and should be coded as `sex`. The possible values for `sex` are: |

## Generic Suffixes


Variables may describe a feature or property of an entity, using the format &lt;entity>_&lt;feature>. All names below are not to be used alone but rather as suffixes (e.g., "block_type", "stimulus_description").

| Term | Type | Definition |
|:-----|:-----|:-----------|
| **length** | `float` | Refers to the length in centimeters of a physical object. When possible use a more specific word (e.g., height, width, distance). |
| **height** | `float` | Refers to the height of a physical object in centimeters. |
| **width** | `float` | Refers to the width of a physical object in centimeters. |
| **weight** | `float` | Refers to the weight of a physical object in kilogram. |
| ***_count** | `integer` | Refers to the cardinality of that entity. A variable named `page_count` indicates the number of pages. Or, if an observation/row has `car_count = 5` this means that this particular observation involves a total count of 5 cars; this 5 is unrelated to other rows in the table. |
| **type** | `enum` | Type is always an enum with known values. The meaning of the particular enum value needs to be explained in a codebook. |
| **description** | `string` | Description is always a text (string) for human consumption. While it is not strictly necessary, a textual description can greatly facilitate the understanding and processing of the data by humans. |

## Aggregation Suffixes


Use the following terms as suffixes to refer to particular operations in variable names. For example the mean of a variable "age" would be called "age_mean" (and not for example age_avg or age_m). We typically use the same name as the aggregation function name in Python or R. More specialized terms require explicit descriptions.

| Term | Type | Definition |
|:-----|:-----|:-----------|
| **mean** | `float` | The average of a numeric variable. |
| **median** | `float` | The median of the variable. |
| **mode** |  | The mode of a variable. |
| **min** |  | The minimum value of a variable. |
| **max** |  | The maximum value of a variable. |
| **sd** |  | The standard deviation of a variable. |
| **var** |  | The variance of a variable. |
| **iqr** |  | The interquartile range of a variable. |
| **sum** | `float` | The sum of all values of a variable (e.g., `item_price_sum = sum(item_price)`). |
| **quantile*** | `float` | Quantile is similar to percentile, as both refer to the value of a parameter Q that splits the data such that a given fraction of the data is smaller than Q. Quantile expresses that fraction as a number between 0 and 1 while percentiles express it as a percentage (between 0 and 100). |
| **rank** | `integer` | Rank of a value in a set (ascending or first to last). |

## Transformation Suffixes


Use the following terms to refer to particular operations in variable names. In general, use the function name that was used to do the transformation. For example the log of a variable `age` would be called `age_log` (and not for example `log_age` or `age_in_log`). We typically use the same name as the transformation function name in Python or R.

| Term | Type | Definition |
|:-----|:-----|:-----------|
| **log** | `float` | Natural log. |
| **log2** | `float` | Log of base 2. |
| **log10** | `float` | Log of base 10. |
| **sqrt** |  | Square root. |
| **pow2** |  | Power of 2. |
| **floor** | `integer` | Flooring of a number (e.g., 3.6 becomes 3). |
| **ceil** | `integer` | Ceiling of a number (e.g., 3.6 becomes 4). |
| **round** | `integer` | Rounding of a number to the closest integer (e.g., 3.6 becomes 4). |

## Referencing Suffixes


Several variables are used to filter, identify or locate particular rows in a table or across multiple tables. Below is a list of the ones that are usually used in behavioral data and how they can be used.

| Term | Type | Definition |
|:-----|:-----|:-----------|
| ***_id** | `string | integer` | If a column or variable name is suffixed with `_id` (e.g., `participant_id`, `task_id`), it is expected that there exists a supplementary table which has the same name ("participant", "task"), with a primary key named `id` such that a value of in the first (`particiapant_id = 215`) refers to an entry in the second (a row in the participant table where `id = 215`). It is expected that the values in a variable postfixed `_id` are unique within a "local scope" of the source table; however, it is not expected that they are unique globally—for such purposes one should use the `_uuid`. |
| ***_name** | `string` | Sometimes "name" is used in a way that is similar to a unique id (e.g., `study_name` or `task_name`). The difference between "id" and "name" is that "name" is expected to be a readable text (e.g., `n-back` versus `f346-r23v`). As with "id", it is expected that it refers to other tables and that it is unique within a certain context (contrary to, for example, "label"). |
| ***_uuid** | `string` | [Universally Unique Identifier (UUID)](https://en.wikipedia.org/wiki/Universally_unique_identifier) is a random 32-digit label that can be generated on the fly and will most likely be unique in computer systems. UUID can be used to assign a record a unique identifier without having to ensure that that number is not yet used by some other records or tables. |
| ***_hash** | `string` | It is sometimes useful to create a reproducible keys based on some data. A [hash](https://en.wikipedia.org/wiki/Hash_function) is not strictly necessary as it can be recreated using different data but it can be convenient for data processing. |
| ***_index** | `integer` | Indices should be favored over labels and ids when a variable is used for referencing and when order is important (often, but not always, the chronological order). For example, a variable  named `stimulus_position_index` implies its value points to an entry in a list of possible stimulus positions. |
| ***_repetition** | `integer` | Repetition counts the number of times the same "thing" occurred, e.g., a participant completes the same test twice, the same stimulus appears multiple times. |
| ***_label** | `string` | A text attached to a variable and identifies it. It is expected to be human readable, but not always unique. |

## Time


Clock and timing terms for raw data acquisition. Recording engines timestamp samples on a monotonic clock; a single per-session anchor datetime bridges that clock to wall-clock time.

| Term | Type | Definition |
|:-----|:-----|:-----------|
| **engine_seconds** | `float` | A monotonic clock measuring seconds since the recording engine started. It never decreases, is unaffected by wall-clock adjustments (NTP, timezone, DST), and is sub-millisecond capable. All acquisition and timeseries sample times (`t`) within a session are expressed on this clock. |
| **anchor_datetime** | `datetime` | The RFC 9557 datetime (with timezone offset) corresponding to `engine_seconds` = 0 — the single bridge from the monotonic clock to wall-clock time, recorded once per runtime instance (one execution of an activity; a restart begins a new engine clock and therefore a new anchor). Wall-clock datetimes are derived as `anchor_datetime` + `t`. |
| **t** | `float` | The per-sample time field of an acquisition or timeseries record, in seconds on the declared monotonic clock (see `engine_seconds`). Event streams may carry it as the optional `bdm:t` context extension alongside the wall-clock `timestamp`. |
