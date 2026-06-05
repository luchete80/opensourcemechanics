# opensourcemechanics
Site

## Metrics

The homepage metrics block mixes automatic and manual values.

- Automatic metrics are refreshed from `publications.html` and `benchmarks.html`.
- Manual metrics are defined in `scripts/update_metrics.py`.

To recalculate and write the current values into `index.html`, run:

```bash
python3 scripts/update_metrics.py --write
```
