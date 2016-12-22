import pyaudio
import scipy.fftpack
import scipy.interpolate
import numpy
import pylab

#pyAudio settings
settings = {
    "format": pyaudio.paInt16,
    "channels": 2,
    "rate": 96000,
    "input": True,
    "frames_per_buffer": 1024
}
audio = pyaudio.PyAudio()
stream = audio.open(**settings)

#pyLab configurations
pylab.ion()
figura, (spectrum_log, spectrum, wave) = pylab.subplots(nrows=3, ncols=1)
pylab.subplots_adjust(hspace=0.5, left=0.1)

#Plot settings
spectrum_log.set_ylabel("a (dB)")
spectrum_log.set_xlabel("ƒ (Hz)")
spectrum_log.ticklabel_format(style="sci", scilimits=(0, 0), axis="x")
spectrum_log.grid(True)
curve1, = spectrum_log.plot([0, 8 * 10 ** 3], [0, 10 ** 2], "b-")

spectrum.yaxis.set_visible(False)
spectrum.set_xlabel("ƒ (Hz)")
spectrum.ticklabel_format(style="sci", scilimits=(0, 0), axis="x")
spectrum.grid(True)
curve2, = spectrum.plot([0, 8 * 10 ** 3], [0, 10 ** 5])

wave.xaxis.set_visible(False)
wave.yaxis.set_visible(False)
curve3, = wave.plot([0, 8 * 10 ** 3], [-2 * 10 ** 3, 2 * 10 ** 3], "g-")

#Main loop
while True:
    try:
        block = numpy.array(numpy.fromstring(stream.read(settings["frames_per_buffer"]), dtype="int16"))
    except IOError:
        continue

        # FFT of registred block
    fftx = scipy.fftpack.rfftfreq(settings["frames_per_buffer"],1 / settings["rate"])

    # Calculate log version

    ffty = abs(scipy.fftpack.fft(block)[0:len(fftx)])

    ffty_log = 10 * scipy.log10(ffty)

    # Data interpolation

    wave = scipy.interpolate.interp1d(fftx, block[0:len(fftx)])(fftx)

    # Update plot data

    curve1.set_xdata(fftx)
    curve2.set_xdata(fftx)
    curve3.set_xdata(fftx)

    curve1.set_ydata(ffty_log)
    curve2.set_ydata(ffty)
    curve3.set_ydata(wave)

    # Redraw
    pylab.draw()

