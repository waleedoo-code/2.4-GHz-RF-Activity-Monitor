from machine import Pin, SPI
import nrf24l01
import time

# ── setup ───────────────────────────────────
spi = SPI(0, baudrate=2000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19), miso=Pin(16))

ce  = Pin(20, Pin.OUT)
csn = Pin(17, Pin.OUT)

ce.value(0)
csn.value(1)

nrf = nrf24l01.NRF24L01(spi, csn, ce, payload_size=4)

# ── override library defaults ────────────────
# 2Mbps speed — wider bandwidth, more sensitive
nrf.reg_write(0x06, 0x0E)

# CONFIG: PWR_UP=1, PRIM_RX=1, CRC disabled
# 0x03 = 0000 0011
nrf.reg_write(0x00, 0x03)

# disable auto-retransmit — not needed for scanning
nrf.reg_write(0x04, 0x00)

# enable all RX pipes so chip listens broadly
nrf.reg_write(0x02, 0x3F)

time.sleep_ms(5)

print("Config:", hex(nrf.reg_read(0x00)))
print("RF setup:", hex(nrf.reg_read(0x06)))
print()

# ── RPD scan function ────────────────────────
def rpd_scan(channel, samples=100):
    # set channel
    nrf.reg_write(0x05, channel)
    time.sleep_us(10)

    count = 0

    for _ in range(samples):
        # make sure CE is low before starting
        ce.value(0)

        # flush RX — clears any old data and resets RPD latch
        nrf.flush_rx()

        # clear status flags
        nrf.reg_write(0x07, 0x70)

        # CE high — start listening
        ce.value(1)

        # wait 40µs minimum — this is critical
        # RPD only latches after this minimum time
        time.sleep_us(200)

        # read RPD register — register 0x09
        # bit 0 = 1 means signal above -64dBm was detected
        rpd = nrf.reg_read(0x09) & 0x01

        # CE low — stop listening
        ce.value(0)

        count += rpd

    return count


# ── test on known WiFi frequencies first ────
print("Testing known WiFi channels...")
print("Keep your phone/router nearby")
print()

wifi_channels = [
    (1,  2412),
    (6,  2437),
    (11, 2462),
]

for wifi_ch, freq_mhz in wifi_channels:
    nrf_channel = freq_mhz - 2400
    result = rpd_scan(nrf_channel, samples=200)
    bar = "#" * result
    print("WiFi ch{} ({}MHz / NRF ch{:3d}): [{:<100}] {}/200".format(
        wifi_ch, freq_mhz, nrf_channel, bar, result))

print()
print("Now scanning all 126 channels...")
print()

# ── full scan ────────────────────────────────
results = []

for ch in range(126):
    count = rpd_scan(ch, samples=100)
    results.append(count)

# print results
print("=" * 50)
peak_ch = results.index(max(results))
peak_freq = 2400 + peak_ch

for ch in range(126):
    if results[ch] > 0:
        freq = 2400 + ch
        bar = "#" * results[ch]
        print("Ch{:3d} {}MHz |{:<30}| {}".format(
            ch, freq, bar, results[ch]))

print()
print("Peak: Ch{} ({}MHz) = {}/100".format(
    peak_ch, peak_freq, results[peak_ch]))
