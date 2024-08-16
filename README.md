# TermSearch

<p align="center">
  <img src="icon.png" style="box-shadow: 10px 10px 5px grey;">
</p>


An Alfred workflow that allows you to easily manage and look up translations from termbases. Supports both English and Chinese searching, and fuzzy matching is enabled for English matching. Supports "Reverse Search" where you can look up a target text and the corresponding source text will be returned. Also supports pinyin matching for Chinese searches.

![img](preview.gif)

## Dependencies

- Python
- Install [thefuzz](https://github.com/seatgeek/thefuzz) via pip. This is required for fuzzy matching.
- Install `pinyin` via pip. This is requiring for pinyin matching.

Ensure that you install it with the specific Python that Alfred uses. Read [How to Install Python Dependencies](#how-to-install-python-dependencies) for more detailed info on how that can be done.

## Core Features
- **Term Search** (`ts`) : Looks up a term from all .json files in your temrbase directory. English is matched fuzzily using the fuzziness value specified in the configuration. Chinese is matched more naively to simply see if at least one character matches. Pinyin is also supported for Chinese searches (same naive matching).

- **Add Entry** (`tsa`): Add TT to an existing ST entry, or add an entirely new ST entry to a specified termbase.

- **Delete Entry** (`tsd`): Delete a TT from an existing ST entry, or delete an entire ST entry.

- **Load CSV File** (`loadcsv`): Converts a CSV file into JSON format, which will be saved under the specified termbase directory.

- **Convert Excel file to CSV** (`xtc`): Converts a given XLSX file into CSV format. The subsequent script will help to eliminate empty cells, but it is recommended that the user check it manually (resulting file will pop up).

## How to Install Python Dependencies

To ensure that dependencies are installed for the same Python that is used for the scripts in this workflow, you can open the workflow's directory and open any of the `.py` files. Then input this line at the very beginning:

```python
import sys

print(sys.executable)
```

Then turn on the debugger console in your Alfred workflow window. It should print the path of the Python executable.

For example if the path you get is `/opt/homebrew/opt/python@3.12/bin/python3.12`, you will need to install your packages like so:

```python
 /opt/homebrew/opt/python@3.12/bin/python3.12 -m pip install package_name --break-system-packages
```

(`--break-system-packages` is only required if the path is a homebrew one. Not including this will throw an error message.)

It is recommended to bind this to a snippet or snippet trigger for easier installation in the future.

## Known Issues
- The exact priority for returning matches is not fully decided yet. In some cases it is hard to decide which is a better match (as sometimes we match pinyin, sometimes we don't, etc. and there is no simple way to come up with a scoring system that works across different search methods). However, a scoring system has been implemented and results should generally be sorted as expected, except in rare cases.
- Pinyin conversion is inaccurate for certain words. This is a tokenization problem that cannot be completely resolved. You may explicitly specify known incorrect transcriptions in the `replace_d.json` in the workflow directory.
- `loadcsv` and `xtc` are not thoroughly tested. Likely to behave unexpectedly.
