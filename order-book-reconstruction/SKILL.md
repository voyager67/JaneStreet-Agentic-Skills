---
name: order-book-reconstruction
description: Design, implement, or audit an exchange limit-order-book parser and state reconstructor from ITCH-like market-data messages or normalized MBO/L2 feeds. Use for order lifecycle, sequencing, snapshots, recovery, and book invariants; not for generic data cleaning.
---
# Order-Book Reconstruction

Act as an exchange-feed and market-data engineer. Reconstruct the exchange-visible book according to the venue's published protocol and matching rules. Never assume that two venues encode the same order lifecycle.

## Workflow

1. **Read the authoritative protocol.** Identify message types, field widths, byte order, message framing, sequence-number scope, order-ID scope, price/quantity scale, symbol mapping, session reset rules, and correction/bust semantics. Record the spec version and effective date.
2. **Choose the state model.** For MBO, maintain order-ID state and derive price levels; for MBP/L2, maintain aggregate levels and accept that individual queue rank unavailable. Represent bid/ask sides with explicit price ordering and integer ticks.
3. **Specify transitions before coding.** Map each message to a state transition: add, partial execution, full execution, cancel, replace, delete, trade-only event, cross/auction event, or session control. Define behavior for unknown IDs and duplicate messages.
4. **Handle sequence and recovery.** Detect gaps, duplicates, out-of-order delivery, retransmissions, and channel resets. Stop publishing a trusted book after a gap until protocol-correct recovery (snapshot/replay or channel recovery) completes. Do not silently skip unknown state-changing messages.
5. **Make updates atomic.** Apply each event as one state transition; preserve event order. Treat replace semantics according to protocol (some replacements lose priority; some do not). Do not assume cancel-plus-add unless the spec says so.
6. **Validate invariants.** Check nonnegative quantities, no zero-sized resting orders, one active order ID at a time where required, aggregate depth matching order-level sums, tick alignment, monotonic sequence within the applicable channel, and no crossed book outside documented market states.
7. **Cross-check against reference outputs.** Use Known protocol examples, independent decoders, venue-provided snapshots, and carefully selected event sequences. Build tests for every message type and transitions around boundary values.
8. **Expose observability.** Emit sequence-gap counters, parse errors, unknown-ID events, recovery state, message throughput, book age, and last trusted sequence.

## Data structures and correctness notes

- Store prices as integer ticks or fixed-point integers; avoid binary floating-point equality for price keys.
- Preserve exchange event timestamp and local receive timestamp separately. Do not overwrite one with the other.
- Keep symbol/market-session metadata versioned; corporate actions and instrument changes can invalidate historical assumptions.
- Distinguish order messages from trade messages: a trade print does not necessarily tell you how much displayed depth remains unless the feed semantics establish it.
- For L2 snapshots, model depth truncation and aggregated quantity explicitly.

## Guardrails

- Do not reverse-engineer a proprietary feed from examples when an authoritative spec is available.
- Do not resume a reconstructed book after a sequence gap without a verified recovery point.
- Do not call an L2 aggregate book an exact FIFO queue.
- Never convert protocol quantities/prices with undocumented scaling factors.

## Deliverable

Provide a protocol map, event/state transition table, data model, recovery design, invariant checklist, test matrix, and a reproducible replay comparison. Identify every message type or recovery case not yet handled.

## Further reading

- Nasdaq TotalView-ITCH 5.0: https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf
- Nasdaq oUCH overview and order-entry specs: https://nasdaqtrader.com/Trader.aspx?id=OUCH.- NYSE Pillar platform/specifications: https://www.nyse.com/trade/pillar
