# probe_extraction

Self-contained module for training biased and unbiased linear probes on model activations.

For each task, two probes are produced:
- **biased**: trained on the ambiguous split (only correlated samples, e.g. male professors + female nurses). Can exploit a spurious shortcut.
- **unbiased**: trained on the balanced split (all four combinations of label × spurious feature). Must learn the true signal.

## Usage

```bash
python probe_extraction/train_probes.py --config probe_extraction/configs/bib_nurse_professor_gemma2_2b.yaml
```

### CLI overrides

```
--layer INT         Override the layer from the config
--device STR        Override the device (e.g. cuda:1, cpu)
--output-dir PATH   Override the output directory
--overwrite         Re-train even if output files already exist
```

### Example: different layer

```bash
python probe_extraction/train_probes.py \
    --config probe_extraction/configs/bib_nurse_professor_gemma2_2b.yaml \
    --layer 18 \
    --output-dir ./my_probes
```

## Output files

Files are written to `output_dir` with names:

```
{task_name}_layer{layer}_{dtype}.pt           # biased probe
{task_name}_layer{layer}_{dtype}_unbiased.pt  # unbiased probe
```

Each `.pt` file is a `state_dict` checkpoint (not a pickled `nn.Module`):

```python
{
    "state_dict":     OrderedDict,  # probe weights
    "activation_dim": int,          # e.g. 2304
    "dtype":          str,          # e.g. "bfloat16"
}
```

Load with:

```python
from probe_extraction.train_probes import load_probe
probe = load_probe("bib_nurse_professor_layer22_bfloat16.pt", device="cuda:0")
```

Or manually:

```python
import torch as t
from probe_extraction.probe_model import Probe

ckpt = t.load("bib_nurse_professor_layer22_bfloat16.pt", weights_only=True)
probe = Probe(ckpt["activation_dim"], dtype=getattr(t, ckpt["dtype"])).to("cuda:0")
probe.load_state_dict(ckpt["state_dict"])
```

Note: the existing files in `experiments/` (`probe_layer_22_bfloat16.pt`) use the
older `torch.save(module, path)` format and require `weights_only=False` to load.

## YAML config reference

| Key            | Description |
|----------------|-------------|
| `task_name`    | Prefix for output `.pt` filenames |
| `model_name`   | HuggingFace model ID passed to `nnsight.LanguageModel` |
| `layers_path`  | Dotted attr path to the layer list (see below) |
| `layer`        | Integer layer index |
| `dtype`        | `bfloat16`, `float16`, or `float32` |
| `device`       | e.g. `cuda:0` |
| `batch_size`   | Batch size for data loading and activation collection |
| `seed`         | Random seed for data shuffling and probe weight init |
| `lr`           | Learning rate for AdamW (default: 0.01) |
| `epochs`       | Training epochs (default: 1) |
| `output_dir`   | Where to write `.pt` files (default: current directory) |
| `model_kwargs` | Extra kwargs forwarded to `LanguageModel` |
| `adapter`      | Dataset adapter config (see below) |

### `layers_path` by architecture

| Architecture | `layers_path` |
|---|---|
| Gemma, Llama, Mistral | `model.model.layers` |
| Pythia, GPT-NeoX | `model.gpt_neox.layers` |
| GPT-2 | `model.transformer.h` |

## Dataset adapters

### `bias_in_bios` adapter

For the [LabHC/bias_in_bios](https://huggingface.co/datasets/LabHC/bias_in_bios) dataset.
Uses the `hard_text` field (gender markers partially removed) and `gender` as the spurious feature.

```yaml
adapter:
  type:                 bias_in_bios
  neg_profession:       professor       # label = 0
  pos_profession:       nurse           # label = 1
  activation_dim_value: 2304
  hf_dataset_name:      LabHC/bias_in_bios  # optional, this is the default
```

Available professions (from `dataset.features["profession"].names`):
`accountant`, `architect`, `attorney`, `chiropractor`, `comedian`, `composer`,
`dentist`, `dietitian`, `dj`, `filmmaker`, `interior_designer`, `journalist`,
`model`, `nurse`, `painter`, `paralegal`, `pastor`, `personal_trainer`,
`photographer`, `physician`, `poet`, `professor`, `psychologist`, `rapper`,
`software_engineer`, `surgeon`, `teacher`, `yoga_teacher`

The biased split takes the group where `neg_profession` is male and `pos_profession`
is female. Choose profession pairs where this correlation exists in the data
(e.g. professor/nurse, surgeon/teacher).

### `generic_hf` adapter

For any HuggingFace dataset with a text column, a binary primary label column,
and a binary spurious label column.

```yaml
adapter:
  type:                    generic_hf
  dataset_name:            LabHC/bias_in_bios
  text_column:             hard_text
  primary_label_column:    profession
  spurious_label_column:   gender
  neg_primary_value:       21        # professor
  pos_primary_value:       13        # nurse
  neg_spurious_value:      0         # male
  pos_spurious_value:      1         # female
  activation_dim_value:    2304
  train_split:             train     # default
  test_split:              test      # default
```

Both label columns must have values that match `neg_*_value` / `pos_*_value`
exactly. Defaults assume integer 0/1 labels.

## Adding a new adapter

1. Create `probe_extraction/adapters/my_adapter.py` implementing `DatasetAdapter`
2. Import it in `probe_extraction/adapters/__init__.py`
3. Add a branch to `build_adapter()` in `train_probes.py`
4. Write a YAML config with `adapter.type: my_adapter`
