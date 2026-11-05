# Lecture 1: pERK time series

## Data
pERK immunostaining time series. 2 channels per position, maximum intensity
projections, 1024×1024, uint16.
- Channel 0 (`w0000`) = nuclear stain, channel 1 (`w0001`) = pERK.
- Filenames: `A{well}_200819_ppERK_timeseries_E6T_MIP_p{pos:04d}_w{channel:04d}.tif`

| Well | Position | Condition |
|---|---|---|
| A1 | p0000 | MEKi (inhibitor control) |
| A2 | p0006 | 0 min |
| A3 | p0009 | 5 min |
| A4 | p0012 | 10 min |
| A5 | p0016 | 30 min |
| A6 | p0020 | 60 min |
| A7 | p0024 | 120 min |
| A8 | p0028 | 240 min |

MEKi blocks ERK activation, so it should show the lowest pERK signal.

## Scope
This is the first lecture: no segmentation yet. Whole-image measurements only.
