# S Language Encoder
If you took Computability Theory course in the university, you'll probably either appreciate these scripts or you'll throw your computer out of the window seeing them (please ensure that no pedestrian will be neither physically nor mentally harmed from your actions)

## S Language to Gödel Number encoder
Encodes each line by calculating <a, <b, c>></br>
<x, y> = $2^x(2y + 1) - 1$

If no label is starting the line:</br>
&ensp;&ensp;a = 0</br>
Else:</br>
|label|A|B|C|D|E|A2|B2|C2|D2|E2|A3|B3|C3|D3|E3|...
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
|a =|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|...

|b = 0|b = 1|b = 2|b > 2
|-|-|-|-
|V <- V|V <- V + 1|V <- V - 1|IF V != 0 GOTO L

Note: L is the label who's id is b - 2

|var|Y|X|Z|X1|Z1|X2|Z2|X3|Z3|X4|Z4|X5|Z5|X6|Z6|...
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
|c =|0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|...

Then after there is a list of line codes [l1, l2, l3, l4, ...],</br>
the [gödel number](https://en.wikipedia.org/wiki/G%C3%B6del_numbering) will be calculated based on it.

The code of the program will be: gödel_number - 1

## Gödel Number to S Language decoder
Samething like the [section above](#s-language-to-gödel-number-encoder) but reversed.
