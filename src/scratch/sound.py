import numpy as np
import wave

def clamp(a, lo, hi):
    return np.minimum(np.maximum(a, lo), hi)

def save_wav_stereo(filename, left, right, sample_rate=44100):
    # left/right are float32ish in [-1, 1]
    left_i  = np.int16(clamp(left,  -1, 1) * 32767)
    right_i = np.int16(clamp(right, -1, 1) * 32767)

    interleaved = np.empty(left_i.size + right_i.size, dtype=np.int16)
    interleaved[0::2] = left_i
    interleaved[1::2] = right_i

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)         # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(interleaved.tobytes())

def sonify_pendulum(t, x, y, sample_rate=44100,
                    base_freq=220.0, pitch_sensitivity=1.5,
                    amp_base=0.05, amp_gain=0.4,
                    pan_strength=0.9):
    """
    t, x, y: arrays from simulation (uniform dt preferred).
    Returns stereo audio arrays (left, right).
    """

    # Ensure uniform sampling for clean audio
    dt = np.mean(np.diff(t))
    # Resample to audio rate if needed
    duration = t[-1] - t[0]
    n = int(duration * sample_rate)
    ta = np.linspace(t[0], t[-1], n, endpoint=False)

    xa = np.interp(ta, t, x)
    ya = np.interp(ta, t, y)

    # Velocity magnitude for amplitude
    vxa = np.gradient(xa, 1 / sample_rate)
    vya = np.gradient(ya, 1 / sample_rate)
    speed = np.sqrt(vxa**2 + vya**2)

    # Pitch: exponential mapping so it feels musical
    # x is likely in meters; you may want to normalise
    x_norm = xa / (np.max(np.abs(xa)) + 1e-9)
    freq = base_freq * 2 ** (pitch_sensitivity * x_norm)

    # Amplitude follows speed (normalised)
    speed_norm = speed / (np.max(speed) + 1e-9)
    amp = clamp(amp_base + amp_gain * speed_norm, 0, 1)

    # Build phase and oscillator
    phase = 2 * np.pi * np.cumsum(freq) / sample_rate
    mono = amp * np.sin(phase)

    # Stereo pan from x
    pan = clamp(0.5 + 0.5 * pan_strength * x_norm, 0, 1)
    left = mono * np.sqrt(1 - pan)
    right = mono * np.sqrt(pan)

    return left, right

# --- Example usage (replace with your arrays) ---
# left, right = sonify_pendulum(t, x, y)
# save_wav_stereo("pendulum.wav", left, right)
