- python3.6
- not use Anaconda (but I think it is useful to use Anaconda)

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

