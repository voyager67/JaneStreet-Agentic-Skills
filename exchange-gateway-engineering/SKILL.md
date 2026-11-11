---
name: exchange-gateway-engineering
description: Design, audit, or troubleshoot exchange connectivity and order-entry state machines, including protocol parsing, sequence handling, acknowledgements, rejects, cancel/replace, throttles, disconnect recovery, and session controls. Use for FIX, OUCH-like, or binary gateway work.
---
# Exchange Gateway and Order-State Engineering

Treat an exchange gateway as a correctness-critical distributed state machine. A local send is not an exchange acknowledgement; a timeout is not proof that an order was rejected or cancelled.

## Workflow

1. **Use the exact venue specification.** Record protocol/version, session type, framing, field encoding, order types/TIF, price and quantity scales, sequence rules, heartbeat, throttle, cancel/replace semantics, and business-day changes.
2. **Model order states explicitly.** Define accepted, pending new, working, partially filled, pending cancel, pending replace, filled, cancelled, rejected, expired, and unknown/reconciliation-required states as applicable. Map every inbound/outbound message and legal transition.
3. **Separate request IDs from venue order IDs.** Persist client order ID, venue order ID, session sequence, original/replace chain, parent strategy ID, and idempotency key. Never reuse identifiers outside protocol rules.
4. **Handle asynchronous races.** Design for fill-during-cancel, partial-fill-during-replace, duplicate acknowledgements, late rejects, cancel reject, disconnect during send, and reconnect before reconciliation. Keep state monotone only where the protocol allows it.
5. **Implement sequencing and recovery.** Detect gaps and duplicates. Follow venue-defined retransmission, recovery, session reset, and open-order reconcilation. Do not resume order flow on an uncertain state.
6. **Enforce backpressure and throttles.** Bound outbound queues, prioritize risk-reducing cancels where policy allows, monitor rate limits, and define behavior when the exchange or network stalls.
7. **Test with a simulator or certification environment.** Use deterministic message transcripts, malformed messages, timeout injection, reconnects, sequence resets, partial fills, and recovery tests. Do not test on a live venue without explicit authorization.
8. **Audit every transition.** Persist raw inbound/outbound messages, timestamps, state transitions, decision source, and error path with sensitive credentials redacted.

## Guardrails

- Never infer order state solely from a local timeout.
- Never retry a non-idempotent order blindly after a disconnect.
- Do not ignore unknown messages or unexpected state transitions.
- Do not log secrets, session keys, private certificates, or account credentials.
- Do not place/cancel/replace live orders without explicit user authorization and the required operational approvals.

## Deliverable

Return protocol/version references, state diagram, transition table, recovery plan, throttle/backpressure design, fault-injection test matrix, audit fields, and unresolved edge cases.

## Further reading

- Nasdaq OUCH: https://nasdaqtrader.com/Trader.aspx?id=OUCH
- Nasdaq OUCH 5.0 specification: https://www.nasdaqtrader.com/content/technicalsupport/specifications/TradingProducts/OUCH5.0.pdf
- NYSE pillar specifications: https://www.nyse.com/trade/pillar
