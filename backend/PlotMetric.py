import matplotlib.pyplot as plt
import seaborn as sns

def PlotMetric(calculation, x="content", y="RAF", fill_var=None, point=True, box=True, base_theme="whitegrid", **kwargs):
    #set base theme for plot
    sns.set_theme(style=base_theme)

    #intialize the plot
    #intializes the plot with a boxplot if box is true without outliers
    #hue is set by fillvar if its provided to color diff groups
    plt.figure(figsize=(8,6))
    ax= sns.boxplot(data=calculation, x=x, y=y, hue=fill_var, dodge=False, showfliers= False) if box else None

    if point:
        sns.stripplot(data=calculation, x=x, y=y, hue=fill_var, dodge=True, jitter=0.2, color="black", alpha=0.7, ax=ax) #adds jittered points to the plot
        plt.xticks(rotation=45, ha='right') #rotate x-axis labels
        for func in kwargs.get('additional_funcs', []):  #addtional styling or plot elem with kwargs
            func(ax)

        plt.tight_layout()
        plt.show()


