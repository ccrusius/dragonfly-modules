Speech recognition macros, using dragonfly. Used with Dragon
NaturallySpeaking (DNL) 12 and SpeechStart+, in Windows 7 64 bits.

This repository can be cloned directly into `C:\NatLink\NatLink\MacroSystem`
and NatLink will pick the macros up.

# Window Manipulation

| Command                           | Description                                       |
|-----------------------------------|---------------------------------------------------|
| `move window to monitor <number>` | Move window to given monitor, keeping size        |
| `snap window to <place>`          | Resize and move window to given place (see below) |
| `maximize window`                 | Maximize current window                           |
| `minimize window`                 | Minimize (iconify) current window                 |
| `restore window`                  | Restore current window to non-maximized size      |
| `focus <window name>`             | Bring named window to the foreground              |

* `<places>`: One of `top (left | half | right)`, `bottom (left | half | right)`, `left half`, `right half`.

Although some of the above commands are pre-defined in DNL, they do not work
with some applications (such as Emacs). Some of those commands are also
present in SpeechStart+, but they do not take into account the real size of
the display when the Dragon Bar is visible.

# Emacs

## Symbols

| Command        | Symbol |
|----------------|--------|
| `at`           | `@`    |
| `close arc`    | `)`    |
| `close curly`  | `}`    |
| `close square` | `]`    |
| `colon`        | `:`    |
| `comma`        | `,`    |
| `dot`          | `.`    |
| `hash`         | `#`    |
| `open arc`     | `(`    |
| `open curly`   | `{`    |
| `open square`  | `[`    |
| `percent`      | `%`    |
| `slash`        | `/`    |

## Grouping Symbols

| Command                           | Description                                       |
|-----------------------------------|---------------------------------------------------|
| `angle`                           | Inserts `<>` and moves the cursor in between them |
| `arc`                             | Inserts `()` and moves the cursor in between them |
| `curly`                           | Inserts `{}` and moves the cursor in between them |
| `double`                          | Inserts `""` and moves the cursor in between them |
| `single`                          | Inserts `''` and moves the cursor in between them |
| `square`                          | Inserts `[]` and moves the cursor in between them |

## Identifiers

| Command                    | Description                                 |
|----------------------------|---------------------------------------------|
| `constant <dictation>`     | Inserts `DICTATION_FORMATTED_LIKE_THIS`     |
| `lisp <dictation>`         | Inserts `dictation-formatted-like-this`     |
| `lower camel <dictation>`  | Inserts `dictationFormattedLikeThis`        |
| `score <dictation>`        | Inserts `dictation_formatted_like_this`     |
| `upper camel <dictation>`  | Inserts `DictationFormattedLikeThis`        |
| `lower spaced <dictation>` | Inserts `dictation formatted like this`     |
