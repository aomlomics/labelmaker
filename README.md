<img src="https://images-na.ssl-images-amazon.com/images/I/61UOa%2BgxXuL._SL1024_.jpg" height=150> <img src="example.png" height=150> <img src="https://assets.fishersci.com/TFS-Assets/CCG/product-images/F144079~p.eps-650.jpg" height=150>

# Labelmaker

Make printable QR code labels for samples using basic information about a project. The sample names iterate from 1 to N, where N is the number of samples; the replicate numbers iterate from 1 to M, where M is the number of replicates per sample. We are planning for a future release where the sample names can be provided in a spreadsheet.

## Installation

If you don't have Conda installed on your machine, install [Miniconda](https://conda.io/miniconda.html) for your operating system (Python 3.7+ version).

Create a conda environment called `labels` where you will install the package [`qrcode`](https://pypi.org/project/qrcode/).

```
conda create -n labels pandas click python=3
source activate labels
pip install qrcode[pil]
```

Clone the Labelmaker repository to your computer:

```
git clone https://github.com/cuttlefishh/labelmaker
cd labelmaker
```

## Execution

Just run the command `generate_labels.py` with the required parameters:

```
./generate_labels.py \
  --project MyProject \
  --contact MySurname \
  --date 20180929 \
  --num_samples 5 \
  --num_replicates 2 \
  --label_width 1.05 \
  --label_height 0.5
```

To learn more about each parameter, run `./generate_labels.py --help`.
