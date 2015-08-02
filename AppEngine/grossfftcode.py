>>> N = len(d)
>>> len(N)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: object of type 'int' has no len()
>>> n
10000
>>> T = 100000
>>> a = np.abs(fft.rfft(data, n = data.size))
>>> a
array([  1.71977695e+04,   1.23154587e+01,   2.28699382e+00, ...,
         9.60867973e-01,   1.37960018e+00,   1.67578125e+00])
>>> a = a[1:]
>>> a
array([ 12.31545869,   2.28699382,   3.8579666 , ...,   0.96086797,
         1.37960018,   1.67578125])
>>> freqs = fft.rfftfreq(data.size, d=1./T)[1:]
>>> freqs
array([  1.00000000e+01,   2.00000000e+01,   3.00000000e+01, ...,
         4.99800000e+04,   4.99900000e+04,   5.00000000e+04])
>>> max_freq = freqs[np.argmax(a)
... ]
>>> max_freq = freqs[np.argmax(a)]
>>> max_freq
4000.0