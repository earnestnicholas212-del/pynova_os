# Examples

## batch_simulation.json
A sample configuration file for headless batch simulation.

Run it via:
```bash
python cli.py sim --config examples/batch_simulation.json
```

Or load it programmatically:
```python
from utils.config_loader import ConfigLoader
cfg = ConfigLoader.load("examples/batch_simulation.json")
```
