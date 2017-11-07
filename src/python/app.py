# built-in imports
import timeit

# 3rd-party imports
import numpy as np
from scipy.io.wavfile import read as wavread
from scipy.io.wavfile import write

# local imports
from world import main


if __name__ == '__main__':   
    name = 'test-mwm'
    fs, x_int16 = wavread('{}.wav'.format(name))
    x = x_int16 / (2 ** 15 - 1)
    vocoder = main.World()
    dat = vocoder.encode(fs, x, f0_method='harvest')
    if 0:
        # global pitch scaling
        dat = vocoder.scale_pitch(dat, 2)  # be careful when scaling the pitch down too much
    if 0:
        # global duration scaling
        dat = vocoder.scale_duration(dat, 2)
    if 0:
        dat = vocoder.warp_spectrum(dat, 1.2)
    if 1:  # downsampling example
        dat['spectrogram'][257:, :] = 1e-12
    if 1:  # cepstral smoothing
        dat = vocoder.to_cepstrum(dat)
        cep = dat['cepstrum']
        D, N = cep.shape
        # liftering
        L = 30
        cep = cep[:L,:]
        #cep = cep[:40,:]
        #cep = np.r_[cep, np.zeros((((dat['spectrogram'].shape[0] - 1) * 2 - cep.shape[0]), cep.shape[1]))]
        # process cep here
        pass
        # reconstruct now
        cep2 = np.zeros((D, N))
        cep2[:L, :] = cep
        dat['cepstrum'] = cep2
        dat = vocoder.from_cepstrum(dat)
    if 0:  # LPC smoothing
        pass  # TODO
        # Levinson Durbin on spectrum
    # synthesis
    dat = vocoder.decode(dat)
    import simpleaudio as sa
    snd = sa.play_buffer((dat['out'] * 2 ** 15).astype(np.int16), 1, 2, fs)
    snd.wait_done()
    if 1:
        # visualize
        vocoder.draw(x, dat)
