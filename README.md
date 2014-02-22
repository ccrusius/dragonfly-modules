Speech recognition macros, using dragonfly. Used with Dragon
NaturallySpeaking 12, in Windows 7 64 bits.

This repository can be cloned directly into `C:\NatLink\NatLink\MacroSystem`
and NatLink will pick the macros up.

# Window Manipulation

| Command                           | Description                                       |
|-----------------------------------|---------------------------------------------------|
| `move window to monitor <number>` | Move window to given monitor, keeping size.       |
| `snap window to <place>`          | Resize and move window to given place (see below) |

* `<places>`: One of `top (left | half | right)`, `bottom (left | half | right)`, `left half`, or `right half`.

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

| Command                           | Description                                                  |
|-----------------------------------|--------------------------------------------------------------|
| `score <dictation>`               | Inserts `dictation_formatted_like_this`                      |
| `(upper|lower) camel <dictation>` | Inserts `[Dd]ictationFormattedLikeThis`                      |
| `constant <dictation>`            | Inserts `DICTATION_FORMATTED_LIKE_THIS`                      |
| `lisp <dictation>`                | Inserts `dictation-formatted-like-this`                      |

