# SLO Template

## Service
- Name: billing-api
- Owner: payments-platform

## SLIs
- Availability
- Latency p95
- Error rate

## Objectives
- Availability >= 99.9%
- p95 latency <= 300ms
- Error rate <= 1%

## Error Budget Policy
- Freeze non-critical deploys if budget burn exceeds threshold.
