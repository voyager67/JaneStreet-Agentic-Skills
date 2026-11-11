---
name: tick-data-engineering
description: Build or audit reliable tick, quote, trade, and order-book data pipelines for electronic trading research. Use for feed ingestion, normalization, timestamp alignment, sequence recovery, schema design, and historical data quality.
---
# Tick Data Engineering

Treat market data as event streams with venue-specific semantics, not as an ordinary table of prices. Preserve raw evidence so normalized datasets can be reproduced and challenged.

## Workflow

1. **Inventory the sources.** Record venue/provider, protocol and version, instrument coverage, session coverage, message granularity (trades, L1, L2, MBO), entitlements, timestamp fields, delivery guarantees, and known corrections.
2. **Keep raw immutable.** Archive raw messages or vendor files with checksums, acquisition time, source metadata, and version. Normalization must be a derived layer, never the only surviving representation.
3. **Define a canonical event schema.** Include venue, instrument identifier, event type, exchange timestamp, local receive timestamp, sequence/channel, price ticks, size lots, order/trade ID if available, side, and source/version metadata. Use explicit units and nullable fields.
4. **Normalize safely.** Parse fixed-point price/quantity correctly, handle symbol mapping and instrument lifecycle, convert timezones once with provenance, and model sessions/auctions/halts explicitly. Never infer missing events from OHLCV bars.
5. **Detect feed defects.** Check sequence gaps, duplicates, out-of-order records, invalid types, stale updates, zero/negative sizes, crossed books, implausible prices, and session discontinuities. Quarantine suspect intervals; do not patch them silently.
6. **Synchronize clocks.** Preserve source time and local time. Quantify precision, timezone, clock source, synchronization error, and timestamping point. Never compare unlike clocks without documenting the uncertainty.
7. **Build reproducible partitions.** Partition by venue/date/instrument or a workload-appropriate key. Keep deterministic sort order and schema versions. Ensure reruns over the same raw input generate identical outputs.
8. **Test at event boundaries.** Include session open/close, daylight-saving transitions, halts, auctions, instrument rolls, sequence resets, corrections, and partial files.
9. **Publish data quality metrics.** Report coverage, gap rate, duplicate rate, stale rate, parse failures, recovery intervals, and last trusted sequence per channel.

## Guardrails

- Do not forward-fill missing book updates across an unknown sequence gap.
- Do not use local receive time as exchange event time or vice versa.
- Do not combine data from multiple vendors without mapping differences in trade conditions, corrections, and timestamp semantics.
- Do not drop outliers without preserving a quarantine log and reason.
- Avoid floating-point prices as primary keys; store integer ticks or fixed-point values.

## Deliverable

Provide source inventory, schema contract, transformation steps, defect policy, recovery semantics, test cases, quality report, and replayable provenance from normalized row to raw source.

## Further reading

- Nasdaq TotalView-ITCH 5.0: https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf
- Nasdaq OUCH: https://nasdaqtrader.com/content/technicalsupport/specifications/TradingProducts/OUCH5.0.pdf
- Linux kernel network timestamping: https://docs.kernel.org/networking/timestamping.html
