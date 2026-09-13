# RIS Management

Scripts to easily configure a Reconfigurable Intelligent Surface (RIS) over a serial connection.

## Requirements

- Python 3
- [`pyserial`](https://pypi.org/project/pyserial/) (`pip install pyserial`)
- A RIS connected via USB/serial (tested on `/dev/ttyACM0`, 115200 baud)

## Usage

Run the script with root privileges (required for serial port access):

```bash
sudo python3 ./test_serial_choice.py
```

If you need to identify the correct serial port, run:

```bash
sudo dmesg | grep tty
```

The script will prompt you for a `RIS_ID` and then for a configuration type:

| Option | Description |
|---|---|
| `1` | Configure a single element (row, column, phase shift) |
| `2` | Configure all elements with the same phase shift |
| `3` | Apply a full, custom configuration string |
| `4` | Reset the configuration |

## Communication protocol

Commands are sent as ASCII strings over serial, terminated with `\r\n`. The general format is:

```
AT<RIS_ID><COMMAND><PARAMETERS>
```

| Command | Meaning | Format |
|---|---|---|
| `S` | Set a single element | `AT<RIS_ID>S<ROW><COLUMN><PHASE_SHIFT>` — `ROW`/`COLUMN` are zero-padded to 2 digits, `PHASE_SHIFT` ranges from 1 to 8 |
| `F` | Set the full RIS | `AT<RIS_ID>F<256 x PHASE_SHIFT>` — one phase shift value (1-8) per element, 256 elements in total |
| `R` | Reset the RIS | `AT<RIS_ID>R` |

**Example:** to set element at row `03`, column `07` to phase shift `2` on RIS `1`:

```
AT1S03072
```

After sending a command, the script waits for and prints the reply received from the RIS.
