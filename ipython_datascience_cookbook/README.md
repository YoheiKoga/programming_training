- reference: [cookbook-code/notebooks at master · ipython-books/cookbook-code](https://github.com/ipython-books/cookbook-code/tree/master/notebooks)
- I use python3.6
- I don't use Anaconda (but I think it's better to use Anaconda)

<br>

---
### 8.3 K-nearest neighbors classifier
--- 

- knc.predict needs to be passed a two-dimensional array
- I got bottom error

```
>>> knc.predict(one.ravel())
Reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample.

>>> knc.predict(one.reshape(1,-1))
array([1])
```

<br>

---
### 8.5 SVM
---

- I found the simplest example(below link), it helps to understand SVM
    - [Python Programming Tutorials](https://pythonprogramming.net/linear-svc-example-scikit-learn-svm-python/)