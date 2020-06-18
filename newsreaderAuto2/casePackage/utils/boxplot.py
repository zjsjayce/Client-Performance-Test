# -*- coding=utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def getOutliers(data_source):
    plt.style.use("ggplot")
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = ['SimHei']
    df = pd.DataFrame()

    df["default"] = data_source

    p = df.boxplot(return_type='dict')
    return list(p['fliers'][0].get_ydata())


if __name__ == "__main__":
    data = [1098.9, 1565.1, 1631.7, 1864.8, 1631.7, 1898.1, 1631.7, 1665.0, 1665.0, 1498.5]
    outliers = getOutliers(data)
    print outliers
