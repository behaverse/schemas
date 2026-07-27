---
id: index
title: event
sidebar_label: Overview
slug: /event
---

<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->

# event

**Version**: v26.0721
**Namespace**: `https://behaverse.org/schemas/event`

Raw experimental events for cognitive tests, questionnaires, and games. An xAPI-style envelope (actor / verb / object) carrying a single canonical `bdm:` vocabulary, so one set of analytics tooling can process every domain. Continuous signals (mouse, keyboard, EEG) are referenced via attachments, not inlined.


A Behaverse **event** is an [xAPI](http://adlnet.gov/projects/xapi/) *Statement* — an `actor` / `verb` / `object` envelope — carrying the Behaverse **`bdm:` controlled vocabulary**. The envelope is the standard container (defined by xAPI); the vocabulary below is **what Behaverse defines**. See [About](about.md) for the xAPI background.


## Controlled vocabulary — defined by Behaverse

All terms live in the `bdm:` namespace; the canonical id of `initialized` is `bdm:initialized`.

- **[Verbs](verbs.md)** — 25 actions an actor can perform.
- **[Object types](object-types.md)** — 15 kinds of thing an event is about.
- **[Actor types](actor-types.md)** — 5 kinds of actor.


## Event envelope (xAPI — external)

These are the standard **xAPI Statement** fields; Behaverse uses them as-is. They are the *container*, not what this schema defines — see [About](about.md).

| Field | Type | Requirement | Description |
|:------|:-----|:------------|:------------|
| [actor](envelope/actor.md) | object | required | Who or what performed/experienced the event — `&#123;objectType, id, name?&#125;`, where objectType is one of the actor types below. (Renamed from `agent`; an Agent is one type of actor — BDM deviation D5.) |
| [verb](envelope/verb.md) | string | required | The action that occurred, drawn from the canonical verb vocabulary below. |
| [object](envelope/object.md) | object | required | What the action was performed on — `&#123;objectType, id, name?&#125;`, where objectType is one of the object types below. |
| [timestamp](envelope/timestamp.md) | datetime (RFC 9557) | required | When the event occurred, as an ISO 8601 / RFC 9557 datetime with timezone offset. |
| [result](envelope/result.md) | object | optional | The outcome of the event (e.g. accuracy, response_time, score). Domain-specific payload lives under `result.extensions` keyed by `bdm:*` extension keys. |
| [context](envelope/context.md) | object | optional | Contextual information (study, studyflow, and the session→activity→runtime→block→trial scoping hierarchy) under `context.extensions`, keyed by `bdm:*` extension keys. |
| [version](envelope/version.md) | string | optional | The associated BDM/schema version (e.g. `v26.0608`). Typically populated by the LRS. |
| [stored](envelope/stored.md) | datetime (RFC 9557) | optional | When the event was stored in the LRS. Populated by the LRS. |
| [updated](envelope/updated.md) | datetime (RFC 9557) | optional | When the event was last updated in the LRS. Populated by the LRS. |
| [authority](envelope/authority.md) | object | optional | The authority that generated the event (e.g. the client app/developer). Populated by the LRS. |
| [attachments](envelope/attachments.md) | array | optional | References to additional files/data associated with the event (stimulus blobs, recording files, timeseries), each with its own metadata. Payloads are not inlined. |