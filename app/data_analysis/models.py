from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import datasets, linear_model
import time
import csv
from difflib import SequenceMatcher
from sklearn import metrics
from sklearn.preprocessing import normalize
from user_agents import parse

from sklearn.linear_model import LinearRegression, Ridge, ElasticNet
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from Levenshtein import distance as levenshtein_distance

columns = ['_id', 'host', 'dnt', 'user-agent', 'accept', 'accept-encoding',
           'accept-language', 'ad', 'canvas', 'cookies', 'font-flash', 'language-flash',
           'platform-flash', 'languages-js', 'platform', 'plugins', 'screen_width', 'screen_height',
           'screen_depth', 'storage_local', 'storage_session', 'timezone', 'userAgent-js',
           'webGLVendor', 'webGLRenderer', 'timestamp']

chosen_columns = ['webGLVendor', 'plugins', 'user-agent', 'webGLRenderer', 'screen_width', 'screen_height']
other_columns = set(columns) - set(chosen_columns)

chosen_columns_indexes = [columns.index(i) for i in chosen_columns]
other_indexes = [columns.index(i) for i in other_columns]

header_args = ['User-Agent', 'Accept-Language', 'Accept', 'Accept-Encoding', 'Dnt', 'Remote-Addr']
js_args = ['fonts', 'domBlockers', 'fontPreferences', 'audio', 'screenFrame', 'osCpu', 'languages', 'colorDepth',
               'deviceMemory', 'screenResolution', 'hardwareConcurrency', 'timezone', 'sessionStorage', 'localStorage',
               'indexedDB', 'openDatabase', 'cpuClass', 'platform', 'touchSupport', 'vendor',
               'vendorFlavors', 'cookiesEnabled', 'colorGamut', 'invertedColors', 'forcedColors', 'monochrome',
               'contrast', 'reducedMotion', 'hdr', 'math', 'webGL_vendor', 'webGL_renderer']
stable_params = ['osCpu', 'hardwareConcurrency', 'touchSupport', 'screenResolution', 'domBlockers',
                     'audio', 'languages', 'indexedDB', 'openDatabase', 'cpuClass', 'vendor',
                     'vendorFlavors', 'invertedColors', 'forcedColors',
                     'reducedMotion', 'hdr', 'fonts', 'timezone', 'webGL_vendor', 'webGL_renderer']

variable_params = ['User-Agent', 'plugins']
new_columns = ['browser_family', 'browser_version', 'os_family', 'os_version', 'plugins', 'webGLVendor', 'webGLRenderer', 'screen_width', 'screen_height']


def is_similar(row_1, row_2, model):
    other_1 = row_1[other_indexes]
    other_2 = row_2[other_indexes]
    if np.sum(other_1 != other_2) > 0:
        return False
    row_1 = to_chosen_row(row_1)
    row_2 = to_chosen_row(row_2)
    vec = to_vector(row_1, row_2)
    return model.predict(vec)


def to_test_row(row):
    return row[0], np.array(row)[other_indexes], to_chosen_row(row)


def to_chosen_row(row):
    # print(row, chosen_columns_indexes, flush=True)
    user_agent_index = chosen_columns_indexes[2]
    user_agent = parse(row[user_agent_index])
    ua_features = np.array([user_agent.browser.family, user_agent.browser.version_string, user_agent.os.family,
                     user_agent.os.version_string])
    # print(user_agent.browser.family, user_agent.browser.version_string, user_agent.os.family, user_agent.os.version_string)
    # return np.append(ua_features, np.array(row)[chosen_columns_indexes[1:]])
    result = np.array(row)[chosen_columns_indexes]
    result[2] = user_agent.browser.family + "#" + user_agent.browser.version_string
    return result


def str_dist(str_1, str_2):
    return levenshtein_distance(str_1, str_2)

def to_vector(row_1, row_2):
    # selected_row_1 = row_1[chosen_columns_indexes]
    # selected_row_2 = row_2[chosen_columns_indexes]
    # print(selected_row_1)

    # return row_1 == row_2
    return np.array([str_dist(row_1[i], row_2[i]) for i in range(row_1.shape[0] - 2)]
                    + [row_1[-2] != row_2[-2], row_1[-1] != row_2[-1]]).astype(float)


def to_dataset(rows):
    print(rows[0])
    n = len(rows)
    dataset = []
    y = []
    window = 6
    dataset_true = []
    y_true = []
    dataset_false = []
    y_false = []
    cnt = 0
    for i in range(n):
        for j in range(i, min(n, i + window)):
            id_i = rows[i][0]
            id_j = rows[j][0]
            vector = to_vector(rows[i], rows[j])
            # print(vector, flush=True)
            dataset.append(vector)
            y.append(int(id_i == id_j))
            if id_i == id_j:
                dataset_true.append(vector)
                y_true.append(int(id_i == id_j))
            else:
                dataset_false.append(vector)
                y_false.append(int(id_i == id_j))
            if np.sum(vector) == len(chosen_columns_indexes) and i != j:
                cnt += 1
    # print("collected sizes:", len(dataset_true), len(dataset_false), "with cnt", cnt)

    # print("dataset row sample", dataset[1])
    data = np.array(dataset_true + dataset_false[:len(dataset_true)])
    return normalize(data, axis=0, norm='max'), np.array(y_true + y_false[:len(y_true)])


def to_test_dataset(rows):
    n = len(rows)
    dataset = []
    y = []
    window = 6
    dataset_true = []
    dataset_true_simple = []
    y_true = []
    dataset_false = []
    dataset_false_simple = []
    y_false = []
    cnt = 0
    for i in range(n):
        for j in range(i, min(n, i + window)):
            (id_1, basic_1, smart_1) = rows[i]
            (id_2, basic_2, smart_2) = rows[j]
            equal = np.sum(basic_1 != basic_2)
            vector = to_vector(smart_1, smart_2)
            dataset.append(vector)
            y.append(int(id_1 == id_2))
            if id_1 == id_2:
                # print(basic_1 != basic_2)
                dataset_true.append(vector)
                dataset_true_simple.append(equal)
                y_true.append(int(id_1 == id_2))
            else:
                dataset_false.append(vector)
                dataset_false_simple.append(equal)
                y_false.append(int(id_1 == id_2))
            if np.sum(vector) == len(chosen_columns_indexes) and i != j:
                cnt += 1
    print("collected sizes:", len(dataset_true), len(dataset_false), "with cnt", cnt)

    # print("dataset row sample", dataset[1])
    data = np.array(dataset_true + dataset_false[:len(dataset_true)])
    simple_data = np.array(dataset_true_simple + dataset_false_simple[:len(dataset_true)])
    return normalize(data, axis=0, norm='max'), simple_data, np.array(y_true + y_false[:len(y_true)])


def restult(y_true, y_pred, str):
    print("result for", str)
    print(sum(np.array(y_true == y_pred)))
    mae = metrics.mean_absolute_error(y_true, y_pred)
    mse = metrics.mean_squared_error(y_true, y_pred)
    acc = metrics.accuracy_score(y_true, y_pred)
    print(acc, mse, mae)


def linear(dataset, y, test_ds, test_y):
    print(dataset, flush=True)
    # model = Ridge()
    model = LinearRegression()
    from sklearn.linear_model import Lasso
    # model = Lasso(alpha=0.01)
    # model = ElasticNet()

    print("calculating for dataset of", y.shape, "samples with sum", np.sum(y), flush=True)
    print("dataset row sample", dataset[1])
    model.fit(dataset, y)
    print(model.coef_)
    print("linear coefs:", model.coef_)
    for (name, w) in zip(chosen_columns, model.coef_):
        print(name, ":", w)
    predicted_y = model.predict(test_ds)
    predicted_y = np.array([round(i) for i in predicted_y])
    # print(np.sum(dataset == test_ds))
    restult(test_y, predicted_y, "linear")


def all_linear(dataset, y, test_ds, test_simple, test_y):
    model = LinearRegression()
    model.fit(dataset, y)
    print("fit done", flush=True)
    print("linear coefs:", model.coef_)
    for (name, w) in zip(chosen_columns, model.coef_):
        print(name, ":", w)
    predicted_y = []
    test_predicted_y = model.predict(test_ds)
    for i in range(test_ds.shape[0]):
        # print(test_simple[i], test_predicted_y[i], flush=True)
        predicted_y.append(test_simple[i] == 0 * test_predicted_y[i])
    restult(test_y, predicted_y, "all_linear")



def test_model(dataset, y, test_ds, test_y, model):
    model.fit(dataset, y)
    predicted_y = model.predict(test_ds)
    predicted_y = np.array([round(i) for i in predicted_y])
    restult(test_y, predicted_y, model.__class__.__name__)


if __name__ == '__main__':
    print(set(js_args) - set(variable_params))
    print()
    print(other_columns)
    file = open("fp-data.csv")
    csvreader = csv.reader(file)
    header = next(csvreader)
    print(header)
    rows = []
    skip = 100
    n = 300
    m = 1000
    take = 5000
    print(chosen_columns)
    user_agents = []
    times = []
    for row in csvreader:
        # print(row)
        times.append(row[-1])
        if skip > 0:
            skip -= 1
            continue
        rows.append(to_chosen_row(row))
        user_agents.append(rows[-1][0])
        # if len(rows) > 2*n:
        #     break
        if len(rows) > n + m:
            break
    times = sorted(times)
    print(datetime.fromtimestamp(float(times[0]) / 1000))
    print("min time", times[0], "max time", times[-1], "diff", int(float(times[-2]) - float(times[0])) / 1000)
    # print("sample rows done", flush=True)
    # test_rows = []
    # for row in csvreader:
    #     print(row[1])
    #
    #     test_rows.append(to_test_row(row))
    #     if len(test_rows) > 2*m:
    #         break

    print("different user agents", len(set(user_agents)))
    file.close()
    print("done", flush=True)

    # rows = np.array(rows[:(2*n)])
    print("done", flush=True)

    np.random.shuffle(rows)
    # np.random.shuffle(test_rows)
    # rows = [to_chosen_row(row) for row in rows]
    print("done rows", flush=True)

    sample = rows[:n]
    test = rows[n: n + m]
    # test = test_rows[:m]
    print("done", flush=True)

    dataset, y = to_dataset(sample)
    print("test ds")
    # test_ds, test_simple, test_y = to_test_dataset(test)
    test_ds, test_y = to_dataset(test)
    print("done", flush=True)
    # all_linear(dataset, y, test_ds, test_simple, test_y)
    linear(dataset, y, test_ds, test_y)
    # for m in [KNeighborsClassifier(), DecisionTreeClassifier(), GaussianNB()]:
    #     test_model(dataset, y, test_ds, test_y, m)

