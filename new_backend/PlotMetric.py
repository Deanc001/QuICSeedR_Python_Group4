import matplotlib.pyplot as plt
import seaborn as sns


def plot_metric(calculation, x="content", y="RAF", fill_var=None,
                point=True, box=True, base_theme="whitegrid",
                boxplot=None, scatter=None, xlab=None, ylab=None):

    sns.set_style(base_theme)
    fig, ax = plt.subplots(figsize=(12, 6))

    if boxplot is None:
        boxplot = {}
    if scatter is None:
        scatter = {}

    if box:
        sns.boxplot(data=calculation, x=x, y=y, hue=x, ax=ax, legend=False,
                    palette=boxplot.get('palette', 'gray'),
                    showcaps=False, boxprops=dict(alpha=0.7), whiskerprops=dict(color="gray"),
                    **{k: v for k, v in boxplot.items() if k != 'palette'})

    scatter_palette = scatter.pop('palette', None)
    sns.stripplot(data=calculation, x=x, y=y, hue=x, ax=ax, legend=False,
                  jitter=False, dodge=False, palette=scatter_palette, **scatter)

    ax.set_xlabel(xlab if xlab else x.capitalize())
    ax.set_ylabel(ylab if ylab else y.capitalize())
    ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()
