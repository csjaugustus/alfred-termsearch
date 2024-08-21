# TermSearch

<p align="center">
  <img src="icon.png" alt="Bookmarker Logo" width="100" height="100" style="box-shadow: 10px 10px 20px 5px rgba(0,0,0,0.8);">
</p>

If you are a translator yourself, you probably know how much of a hassle it is when you cannot easily access your termbases. Especially if you are working on MacOS, there is currently no good alternative to Trados (which is often too laggy and therefore annoying to work with). With all the AI chatbots now, *glossary management* is now the only missing piece of a puzzle. You don't need bulky software!

**TermSearch** is an extremely lightweight Alfred workflow that allows you to easily manage and look up translations from termbases. Supports both English and Chinese searching, and fuzzy matching is enabled for English matching. Supports "Reverse Search" where you can look up a target text and the corresponding source text will be returned. Also supports pinyin matching for Chinese searches.

![img](preview.gif)

# Table of Contents

- [Features](#features)
- [Installation](#Setup)
- [Usage](#usage)
- [Known Issues](#known-issues)

# Features
- **Two-Way Searching**: You can search either the source text or the target text.
- **Fuzzy Matching**: Searching is made easy with fuzzy matching, which allows for partial matches and occasional typos.
- **Pinyin Support**: You will be able to search for Chinese words using their *pinyin*. Note however that *pinyin* searches do not support fuzzy matching.
- **Easy Access**: The search/add/delete functions can be triggered anywhere via Alfred, so you don't need to open any additional software.
- **Loading/Offloading Termbases**: Since each termbase is a separate file, you can choose to offload termbases that are currently not used, to declutter your search results.
- **Conversion (`.xlsx` → `.csv` → `.json`)**: While the termbase will ultimately be stored as `.json`, you will be able to load `.xlsx` or `.csv` files. But they have to be in the right format. More info in the workflow comments.

# Setup

## Installation
1. Download Alfred [here](https://www.alfredapp.com). Requires PowerPack.
2. Download Python [here](https://www.python.org/downloads/).
3. Get the latest version of the workflow via [Releases](https://github.com/csjaugustus/alfred-termsearch/releases).

## Configuration
1. Once you install the workflow, you will need to run a setup to install the required dependencies (`thefuzz` and `pinyin`). You simply need to type this command in Alfred:

```
`termsearch_setup
```

2. In the workflow configuration, set a directory to determine where your termbase files will be placed. Then you will need to create an empty `.json` file (with an empty `{}` in it) in order for you to be able to add new entries.

# Usage
- **Term Search** (`ts`) : Looks up a term.

- **Add Entry** (`tsa`): Add TT to an existing ST entry, or add an entirely new ST entry.

- **Delete Entry** (`tsd`): Delete a TT from an existing ST entry, or delete an entire ST entry.

- **Load/Offload Termbase** (`tsl`): Load or offload a termbase. Entries within offloaded  will be excluded from the search scope.

- **Load CSV File** (`loadcsv`): Converts a `.csv` file into `.json` format, which will be saved under the specified termbase directory.

- **Convert Excel file to CSV** (`xtc`): Converts a given `.xlsx` file into `.csv` format. The subsequent script will help to eliminate empty cells, but it is recommended that the user check it manually (resulting file will pop up).





# Known Issues
- The exact priority for returning matches is not fully decided yet. In some cases it is hard to decide which is a better match (as sometimes we match pinyin, sometimes we don't, etc. and there is no simple way to come up with a scoring system that works across different search methods). However, a scoring system has been implemented and results should generally be sorted as expected, except in rare cases.
- Pinyin conversion is inaccurate for certain words. This is a tokenization problem that cannot be completely resolved. You may explicitly specify known incorrect transcriptions in the `replace_d.json` in the workflow directory.
- `loadcsv` and `xtc` are not thoroughly tested. Likely to behave unexpectedly.
