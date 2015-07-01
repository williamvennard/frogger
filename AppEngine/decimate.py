import numpy as np

def kaiser_atten(numtaps, width):
    a = 2.285 * (numtaps - 1) * np.pi * width + 7.95
    return a

def kaiser_beta(a):
    if a > 50:
        beta = 0.1102 * (a - 8.7)
    elif a > 21:
        beta = 0.5842 * (a - 21) ** 0.4 + 0.07886 * (a - 21)
    else:
        beta = 0.0
    return beta

def hamming(M, sym=True):
    if M < 1:
        return np.array([])
    if M == 1:
        return np.ones(1, 'd')
    odd = M % 2
    if not sym and not odd:
        M = M + 1
    n = np.arange(0, M)
    w = 0.54 - 0.46 * np.cos(2.0 * np.pi * n / (M - 1))
    if not sym and not odd:
        w = w[:-1]
    return w

def get_window(window, Nx, fftbins=True):
    string_types = basestring
    sym = not fftbins
    try:
        beta = float(window)
    except (TypeError, ValueError):
        args = ()
        if isinstance(window, tuple):
            winstr = window[0]
            if len(window) > 1:
                args = window[1:]
        elif isinstance(window, string_types):
            #if window in _needs_param:
            #    raise ValueError("The '" + window + "' window needs one or "
            #                     "more parameters -- pass a tuple.")
            #else:
            #    winstr = window
            winstr = window
        else:
            raise ValueError("%s as window type is not supported." %
                             str(type(window)))

        try:
            #winfunc = _win_equiv[winstr]
            winfunc = hamming
        except KeyError:
            raise ValueError("Unknown window type.")

        params = (Nx,) + args + (sym,)
    else:
        winfunc = kaiser
        params = (Nx, beta, sym)

    return winfunc(*params)

from numpy import sinc

def firwin(numtaps, cutoff, width=None, window='hamming', pass_zero=True,
           scale=True, nyq=1.0):
    # The major enhancements to this function added in November 2010 were
    # developed by Tom Krauss (see ticket #902).

    cutoff = np.atleast_1d(cutoff) / float(nyq)

    # Check for invalid input.
    if cutoff.ndim > 1:
        raise ValueError("The cutoff argument must be at most "
                         "one-dimensional.")
    if cutoff.size == 0:
        raise ValueError("At least one cutoff frequency must be given.")
    if cutoff.min() <= 0 or cutoff.max() >= 1:
        raise ValueError("Invalid cutoff frequency: frequencies must be "
                         "greater than 0 and less than nyq.")
    if np.any(np.diff(cutoff) <= 0):
        raise ValueError("Invalid cutoff frequencies: the frequencies "
                         "must be strictly increasing.")

    if width is not None:
        # A width was given.  Find the beta parameter of the Kaiser window
        # and set `window`.  This overrides the value of `window` passed in.
        atten = kaiser_atten(numtaps, float(width) / nyq)
        beta = kaiser_beta(atten)
        window = ('kaiser', beta)

    pass_nyquist = bool(cutoff.size & 1) ^ pass_zero
    if pass_nyquist and numtaps % 2 == 0:
        raise ValueError("A filter with an even number of coefficients must "
                         "have zero response at the Nyquist rate.")

    # Insert 0 and/or 1 at the ends of cutoff so that the length of cutoff
    # is even, and each pair in cutoff corresponds to passband.
    cutoff = np.hstack(([0.0] * pass_zero, cutoff, [1.0] * pass_nyquist))

    # `bands` is a 2D array; each row gives the left and right edges of
    # a passband.
    bands = cutoff.reshape(-1, 2)

    # Build up the coefficients.
    alpha = 0.5 * (numtaps - 1)
    m = np.arange(0, numtaps) - alpha
    h = 0
    for left, right in bands:
        h += right * sinc(right * m)
        h -= left * sinc(left * m)

    # Get and apply the window function.
    #from .signaltools import get_window
    win = get_window(window, numtaps, fftbins=False)
    h *= win

    # Now handle scaling if desired.
    if scale:
        # Get the first passband.
        left, right = bands[0]
        if left == 0:
            scale_frequency = 0.0
        elif right == 1:
            scale_frequency = 1.0
        else:
            scale_frequency = 0.5 * (left + right)
        c = np.cos(np.pi * m * scale_frequency)
        s = np.sum(h * c)
        h /= s

    return h

def lfilter(b, a, x, axis=-1, zi=None):
    a = np.atleast_1d(a)
    if len(a) == 1:
        # This path only supports types fdgFDGO to mirror _linear_filter below.
        # Any of b, a, x, or zi can set the dtype, but there is no default 
        # casting of other types; instead a NotImplementedError is raised.
        b = np.asarray(b)
        a = np.asarray(a)
        if b.ndim != 1 and a.ndim != 1:
            raise ValueError('object of too small depth for desired array')
        x = np.asarray(x)
        inputs = [b, a, x]
        if zi is not None:
            # _linear_filter does not broadcast zi, but does do expansion of singleton dims.
            zi = np.asarray(zi)
            if zi.ndim != x.ndim:
                raise ValueError('object of too small depth for desired array')
            expected_shape = list(x.shape)
            expected_shape[axis] = b.shape[0] - 1
            expected_shape = tuple(expected_shape)
            # check the trivial case where zi is the right shape first
            if zi.shape != expected_shape:
                strides = zi.ndim * [None]
                if axis < 0:
                    axis += zi.ndim
                for k in range(zi.ndim):
                    if k == axis and zi.shape[k] == expected_shape[k]:
                        strides[k] = zi.strides[k]
                    elif k != axis and zi.shape[k] == expected_shape[k]:
                        strides[k] = zi.strides[k]
                    elif k != axis and zi.shape[k] == 1:
                        strides[k] = 0
                    else:
                        raise ValueError('Unexpected shape for zi: expected '
                                         '%s, found %s.' %
                                         (expected_shape, zi.shape))
                zi = np.lib.stride_tricks.as_strided(zi, expected_shape, strides)
            inputs.append(zi)
        dtype = np.result_type(*inputs)

        if dtype.char not in 'fdgFDGO':
            raise NotImplementedError("input type '%s' not supported" % dtype)
        b = np.array(b, dtype=dtype, copy=False)
        a = np.array(a, dtype=dtype, copy=False)
        b /= a[0]
        x = np.array(x, dtype=dtype, copy=False)

        out_full = np.apply_along_axis(lambda y: np.convolve(b, y), axis, x)
        ind = out_full.ndim * [slice(None)]
        ind[axis] = slice(out_full.shape[axis] - len(b) + 1)
        out = out_full[ind]
        if zi is None:
            return out
        else:
            ind[axis] = slice(out_full.shape[axis] - len(b) + 1, None)
            zf = out_full[ind]
            ind[axis] = slice(zi.shape[axis])
            out[ind] += zi
            return out, zf
    else:
        if zi is None:
            return sigtools._linear_filter(b, a, x, axis)
        else:
            return sigtools._linear_filter(b, a, x, axis, zi)



def decimate(x, q, n=None, ftype='iir', axis=-1):
    if not isinstance(q, int):
        raise TypeError("q must be an integer")

    if n is None:
        if ftype == 'fir':
            n = 30
        else:
            n = 8

    if ftype == 'fir':
        b = firwin(n + 1, 1. / q, window='hamming')
        a = 1.
    #else:
    #    b, a = cheby1(n, 0.05, 0.8 / q)

    y = lfilter(b, a, x, axis=axis)

    sl = [slice(None)] * y.ndim
    sl[axis] = slice(None, None, q)
    return y[sl]
