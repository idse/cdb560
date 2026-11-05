import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Our first python script
    Marimo scripts have two types of cells: code and markdown. This is a markdown cell.
    Different heading levels are created in a markdown cell with different numbers of leading hashtages.
    Try to edit this cell (double click) and you will see.
    """)
    return


@app.cell
def _():
    # import the modules we'll need, this is best done at the top of the script
    # module are reusable collection of functions

    # marimo gives the notebook functionality so we can see the output (plots, etc) embedded in our code
    import marimo as mo 

    # matplotlib gives standard plotting functionality in python
    import matplotlib.pyplot as plt

    # lets us make our own colormap (used to show pERK in red)
    from matplotlib.colors import LinearSegmentedColormap

    # tifffile reads microscopy tif files, unlike other readers it can handle imagej hyperstacks and OME metadata
    import tifffile

    return LinearSegmentedColormap, mo, plt, tifffile


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # pERK after stimulation: a first look at the data

    In this notebook you will look at microscope images, see that an image is a grid
    of numbers, and measure how the signal of **pERK** (phosphorylated ERK, a readout
    of MAPK signaling) changes over time after cells are stimulated.

    The cells were fixed at different times after stimulation and stained for two things:

    - **Channel 0**: the nuclei (a DNA stain). This shows where the cells are.
    - **Channel 1**: pERK, the signal we want to measure.

    One sample was treated with a **MEK inhibitor (MEKi)**, which blocks the pathway
    upstream of ERK. If the pERK staining is specific, this sample should show very
    little signal.

    Run the cells from top to bottom. Read the text above each cell first.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Load one image

    First we tell Python where the data is and which files we want: the nuclear
    image and the pERK image of the sample at **0 min** (before stimulation).

    In the code below, a line like `data_folder = "data/pERK"` creates a **variable**:
    a name (left of the `=`) that stores a value (right of the `=`), so we can use the
    name later instead of retyping the value. Text in quotes, like a folder name or
    filename, is called a **string**. Adding two strings with `+` glues them together.

    The filename itself tells us which sample it is: `A2` is the well, `p0006` the
    position, and `w0000` / `w0001` the channel.
    """)
    return


@app.cell
def _():
    # the folder that holds all the images, relative to the folder of this project
    data_folder = "/Users/idse/Library/CloudStorage/Dropbox/work/0_teaching/CDB560_qbio/data/200808_pERK time series 2/MIP"

    # folder + "/" + filename gives the full path of each file
    nuclear_file = data_folder + "/A2_200819_ppERK_timeseries_E6T_MIP_p0006_w0000.tif"
    perk_file = data_folder + "/A2_200819_ppERK_timeseries_E6T_MIP_p0006_w0001.tif"
    return data_folder, nuclear_file, perk_file


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So far we only have the *names* of the files. Now we read them from disk.

    `tifffile.imread(...)` is a **function** from the `tifffile` module: you give it
    something in the parentheses (here a filename) and it gives something back
    (here the image). It returns the image as an **array**, which is a grid of
    numbers, like a table in a spreadsheet where every cell holds one number.
    We store each array in a variable so we can work with it below.
    """)
    return


@app.cell
def _(nuclear_file, perk_file, tifffile):
    # read each file and keep the resulting array under a descriptive name
    nuclear_image = tifffile.imread(nuclear_file)
    perk_image = tifffile.imread(perk_file)
    return nuclear_image, perk_image


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we show both channels side by side: the nuclei in grayscale and pERK in red.
    The color is only a way of displaying the numbers; the data is the same.
    """)
    return


@app.cell
def _(LinearSegmentedColormap, nuclear_image, perk_image, plt):
    # a colormap that goes from black (lowest value) to red (highest value)
    black_to_red = LinearSegmentedColormap.from_list("black_to_red", ["black", "red"])

    fig_side, (ax_nuclear, ax_perk) = plt.subplots(1, 2, figsize=(11, 5.5))

    ax_nuclear.imshow(nuclear_image, cmap="gray")
    ax_nuclear.set_title("Nuclei (channel 0)")
    ax_nuclear.set_xlabel("x (pixels)")
    ax_nuclear.set_ylabel("y (pixels)")

    ax_perk.imshow(perk_image, cmap=black_to_red)
    ax_perk.set_title("pERK (channel 1)")
    ax_perk.set_xlabel("x (pixels)")
    ax_perk.set_ylabel("y (pixels)")

    fig_side.tight_layout()
    fig_side
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Try this:** the pERK image looks dark. Why? Keep the question in mind;
    we come back to it in section 3.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. An image is a grid of numbers

    To the computer, the picture above is just the array we loaded: a table with one
    number per pixel. We can ask the array about itself by writing a dot and a property
    after its name, for example `perk_image.shape`. `print` shows the answer below the cell.

    - **shape**: the size of the table, as (rows, columns)
    - **dtype**: the kind of number stored (more on this below)
    - **min / max**: the smallest and largest number in the table
    """)
    return


@app.cell
def _(perk_image):
    print("shape (rows, columns):", perk_image.shape)
    print("dtype:", perk_image.dtype)
    print("smallest value:", perk_image.min())
    print("largest value:", perk_image.max())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `uint16` means *unsigned 16-bit integer*: whole numbers from 0 to 65535.
    A higher number means more light reached the camera at that pixel.

    Here is the value of a single pixel. Python counts from 0, and we give the
    **row first, then the column**.
    """)
    return


@app.cell
def _(perk_image):
    row = 500
    column = 300
    print("pERK value at that pixel:", perk_image[row, column])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now a small square of 20 × 20 pixels. In the plot, every square is one pixel.
    Below it, the top left corner of the same square is printed as numbers.
    """)
    return


@app.cell
def _(perk_image, plt):
    crop = perk_image[500:520, 300:320]

    fig_zoom, ax_zoom = plt.subplots(figsize=(5, 5))
    ax_zoom.imshow(crop, cmap="gray", interpolation="nearest")
    ax_zoom.set_title("20 x 20 pixel crop")
    ax_zoom.set_xlabel("x (pixels)")
    ax_zoom.set_ylabel("y (pixels)")
    fig_zoom.tight_layout()
    fig_zoom
    return (crop,)


@app.cell
def _(crop):
    # the first 6 rows and 6 columns of the crop
    print(crop[:6, :6])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Try this:** change `row` and `column` above to look at another pixel, or change
    the numbers in `perk_image[500:520, 300:320]` to zoom in somewhere else.
    Or ask Claude: *"Write code that finds the row and column of the brightest pixel
    in the pERK image."*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Contrast

    To display an image, the numbers are turned into gray levels. By default the
    smallest value is shown black and the largest white. If a few pixels are very
    bright, everything else looks dark. That is why the pERK image looked dim.

    The **histogram** shows how many pixels there are at each intensity. The y-axis
    is logarithmic, because there are far more dim pixels than bright ones.
    """)
    return


@app.cell
def _(perk_image, plt):
    fig_hist, ax_hist = plt.subplots(figsize=(8, 4))
    ax_hist.hist(perk_image.ravel(), bins=200, color="gray")
    ax_hist.set_yscale("log")
    ax_hist.set_xlabel("pixel intensity (camera counts)")
    ax_hist.set_ylabel("number of pixels")
    ax_hist.set_title("pERK intensity histogram")
    fig_hist.tight_layout()
    fig_hist
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The slider sets the **display limits**: pixels at or below the left handle are
    drawn black, pixels at or above the right handle are drawn white.
    Move the handles and watch the image. This changes only how the image is shown,
    not the data.
    """)
    return


@app.cell
def _(mo, perk_image):
    contrast_slider = mo.ui.range_slider(
        start=0,
        stop=int(perk_image.max()),
        step=50,
        value=[int(perk_image.min()), int(perk_image.max())],
        label="display limits",
        show_value=True,
        full_width=True,
    )
    contrast_slider
    return (contrast_slider,)


@app.cell
def _(contrast_slider, perk_image, plt):
    lower_limit, upper_limit = contrast_slider.value

    fig_contrast, ax_contrast = plt.subplots(figsize=(6.5, 6))
    contrast_view = ax_contrast.imshow(
        perk_image, cmap="gray", vmin=lower_limit, vmax=upper_limit
    )
    ax_contrast.set_title("pERK with chosen display limits")
    ax_contrast.set_xlabel("x (pixels)")
    ax_contrast.set_ylabel("y (pixels)")
    fig_contrast.colorbar(contrast_view, ax=ax_contrast, label="intensity (camera counts)")
    fig_contrast.tight_layout()
    fig_contrast
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Try this:** find limits that make the cells easy to see. Then move the left
    handle very far to the right. What disappears? Is the image with the best
    contrast the "true" image?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Browse the time series

    There is one image for each of 8 samples. Their filenames differ only in the
    first part (well and position), so we list that part for each sample.
    The end of the filename (`_w0000.tif` or `_w0001.tif`) selects the channel.
    """)
    return


@app.cell
def _():
    file_start = {
        "MEKi": "A1_200819_ppERK_timeseries_E6T_MIP_p0000",
        "0 min": "A2_200819_ppERK_timeseries_E6T_MIP_p0006",
        "5 min": "A3_200819_ppERK_timeseries_E6T_MIP_p0009",
        "10 min": "A4_200819_ppERK_timeseries_E6T_MIP_p0012",
        "30 min": "A5_200819_ppERK_timeseries_E6T_MIP_p0016",
        "60 min": "A6_200819_ppERK_timeseries_E6T_MIP_p0020",
        "120 min": "A7_200819_ppERK_timeseries_E6T_MIP_p0024",
        "240 min": "A8_200819_ppERK_timeseries_E6T_MIP_p0028",
    }
    return (file_start,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Choose a sample from the dropdown. Both pERK images are shown with the **same
    display limits**, so brightness can be compared between samples. If each image
    were stretched to its own range, a weak sample would look as bright as a strong one.
    """)
    return


@app.cell
def _(file_start, mo):
    condition_dropdown = mo.ui.dropdown(
        options=list(file_start.keys()),
        value="0 min",
        label="sample",
    )
    condition_dropdown
    return (condition_dropdown,)


@app.cell
def _(condition_dropdown, data_folder, file_start, plt, tifffile):
    condition = condition_dropdown.value
    start = data_folder + "/" + file_start[condition]

    browse_nuclear = tifffile.imread(start + "_w0000.tif")
    browse_perk = tifffile.imread(start + "_w0001.tif")

    fig_browse, (ax_n, ax_p) = plt.subplots(1, 2, figsize=(11, 5.5))

    ax_n.imshow(browse_nuclear, cmap="gray", vmin=400, vmax=8000)
    ax_n.set_title("Nuclei: " + condition)
    ax_n.set_xlabel("x (pixels)")
    ax_n.set_ylabel("y (pixels)")

    ax_p.imshow(browse_perk, cmap="gray", vmin=400, vmax=5000)
    ax_p.set_title("pERK: " + condition)
    ax_p.set_xlabel("x (pixels)")
    ax_p.set_ylabel("y (pixels)")

    fig_browse.tight_layout()
    fig_browse
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Try this:** go through the samples in order. When is the pERK signal strongest?
    Where in the cell do you see it? Then ask Claude to *"change the display limits
    of the pERK image so the dim samples are easier to see"*, and look at what
    happens to the bright ones.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. pERK over time

    Now we measure one number per image: the **mean pERK intensity**, the average
    of all pixel values. We load the pERK image of each time point, take its mean,
    and collect the results in a list.
    """)
    return


@app.cell
def _(data_folder, file_start, tifffile):
    time_points = [0, 5, 10, 30, 60, 120, 240]  # minutes after stimulation

    mean_perk = []
    for minutes in time_points:
        start_of_name = data_folder + "/" + file_start[f"{minutes} min"]
        image = tifffile.imread(start_of_name + "_w0001.tif")
        mean_perk.append(image.mean())
        print(f"{minutes:>4} min: mean pERK = {image.mean():.0f}")
    return mean_perk, time_points


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The MEKi sample has no time point, so we measure it separately and later draw it
    as a horizontal line: the "inhibited" baseline.
    """)
    return


@app.cell
def _(data_folder, file_start, tifffile):
    meki_image = tifffile.imread(data_folder + "/" + file_start["MEKi"] + "_w0001.tif")
    mean_perk_meki = meki_image.mean()
    print(f"MEKi: mean pERK = {mean_perk_meki:.0f}")
    return (mean_perk_meki,)


@app.cell
def _(mean_perk, mean_perk_meki, plt, time_points):
    fig_time, ax_time = plt.subplots(figsize=(8, 5))
    ax_time.plot(time_points, mean_perk, "o-", color="tab:red", markersize=8,
                 label="stimulated")
    ax_time.axhline(mean_perk_meki, color="gray", linestyle="--", label="MEKi")
    ax_time.set_xlabel("time after stimulation (min)")
    ax_time.set_ylabel("mean pERK intensity (camera counts)")
    ax_time.set_title("pERK response to stimulation")
    ax_time.legend()
    fig_time.tight_layout()
    fig_time
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Try this:** describe the curve in words. How fast does it rise, when is the
    peak, does it return to baseline? Then ask Claude to *"plot the time axis on a log
    scale"* or *"rescale the curve so that MEKi is 0 and the peak is 1"*.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Discussion: is this a fair measurement?

    We averaged every pixel in the image. That was quick, but think about what the
    number contains.

    1. **Background.** Even where there are no cells, the camera reports a value
       (see the lowest values in the histogram). How does this offset change the
       shape of the curve? The ratio between samples?
    2. **Cell density.** If one image has twice as many cells as another, the mean
       goes up even if each cell has the same amount of pERK. How could you check
       this with the nuclear channel?
    3. **Nuclear vs. cytoplasmic signal.** Is pERK in the nucleus, the cytoplasm, or
       both? Can the whole-image mean tell you? Could the location of pERK change
       over time?
    4. **Single cells.** Do all cells respond alike, or do a few respond strongly
       while most do not? What does a mean hide?
    5. **Replicates.** We looked at one image per sample. How sure are you about the
       differences between time points?

    All of these point to the same solution: find each cell (or nucleus) in the image
    and measure per cell. That is **segmentation**, the topic of next week.
    """)
    return


if __name__ == "__main__":
    app.run()
